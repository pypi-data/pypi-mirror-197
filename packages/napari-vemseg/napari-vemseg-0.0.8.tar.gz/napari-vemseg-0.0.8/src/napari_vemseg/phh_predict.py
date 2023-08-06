import os
import sys
import warnings
from typing import Tuple
from urllib.parse import urlparse
import numpy as np
import torch
import torch.nn as nn
from napari.layers import Image
from napari.qt.threading import thread_worker
from qtpy.QtGui import QPixmap, QFont
from qtpy.QtWidgets import (QVBoxLayout,
                            QLabel,
                            QWidget,
                            QPushButton,
                            QProgressBar)
from tqdm import tqdm
from .models.Standard_UNet.Standard_UNet import UNet
from .utils import abspath, make_widget, imnorm


def load_model_to_device(fpath_or_url, device):
    """ Check whether to use a local version of the mitonet model
    or to download it from a given url

    Parameters
    ----------
    fpath_or_url : str
        String indicating whether the model is stored locally or will be downloaded
    device : str
        Device which the model will be loaded to
    Returns
    -------
        Loaded model
    """
    #
    if os.path.isfile(fpath_or_url):
        model = torch.jit.load(fpath_or_url, map_location=device)
    else:
        hub_dir = torch.hub.get_dir()

        # download file to hub_dir
        try:
            os.makedirs(hub_dir)
        except:
            pass

        # set the filename
        parts = urlparse(fpath_or_url)
        filename = os.path.basename(parts.path)
        cached_file = os.path.join(hub_dir, filename)

        if not os.path.exists(cached_file):
            sys.stderr.write('Downloading: "{}" to {}\n'.format(fpath_or_url, cached_file))
            hash_prefix = None
            torch.hub.download_url_to_file(fpath_or_url, cached_file, hash_prefix, progress=True)

        model = torch.jit.load(cached_file, map_location=device)

    return model


@thread_worker
def segment_stack(image_stack: np.ndarray,
                  model: nn.Module,
                  patch_shape: Tuple[int, int, int],
                  compute_device: torch.device,
                  normalize_func,
                  segmentation_mode: str = 'center',
                  overlap_divider: int = 4,
                  batch_size: int = 12) -> np.ndarray:
    """
    The idea here is to pad the entire stack on both sides, such that sliding a window
    across and not quite covering the volume (for example because the stack isn't neatly
    divisible in to patch sized chunks) will still cover the initial volume.

    There is overlap in the window positions, and some of the overlap is discarded from
    each side.
    """
    model.eval()

    overlap_xy = patch_shape[1] // overlap_divider
    overlap_z = patch_shape[0] // overlap_divider

    # padding guarantees that the whole volume is convolved over.
    padded_volume = np.pad(
        image_stack,
        (
            (overlap_z + patch_shape[0], overlap_z + patch_shape[0]),
            (overlap_xy + patch_shape[1], overlap_xy + patch_shape[1]),
            (overlap_xy + patch_shape[2], overlap_xy + patch_shape[2])
        ),
        'symmetric'
    )

    # This creates a list of corner coordinates for image patches to start from
    # it starts from the left/upmost edge of the padded image stack, and iterates
    # through in steps of (patch shape - overlap). It stops a full patch shape
    # before the end of the padded volume so that the model window always falls
    # inside the volume.
    grid_coordinates = [
        (z, y, x)
        for z in range(0, padded_volume.shape[0] - patch_shape[0], patch_shape[0] - (overlap_z * 2))
        for y in range(0, padded_volume.shape[1] - patch_shape[1], patch_shape[1] - (overlap_xy * 2))
        for x in range(0, padded_volume.shape[2] - patch_shape[2], patch_shape[2] - (overlap_xy * 2))
    ]
    result_volume = np.zeros_like(padded_volume, dtype=np.float16)

    for batch_start in tqdm(range(0, len(grid_coordinates), batch_size), desc='Segmenting stack'):
        # yield batch_start, grid_coordinates

        batch_corner_coords = grid_coordinates[batch_start:batch_start + batch_size]

        # NOTE: the final batch will be less than batch_size unless exactly divisible by len(grid_coordinates)
        true_batch_size = len(batch_corner_coords)

        # create a batch of image patches from coordinates
        image_patches = np.zeros((true_batch_size, patch_shape[0], patch_shape[1], patch_shape[2]))
        for i, corner_coord in enumerate(batch_corner_coords):
            image_patch = padded_volume[
                          corner_coord[0]:corner_coord[0] + patch_shape[0],
                          corner_coord[1]:corner_coord[1] + patch_shape[1],
                          corner_coord[2]:corner_coord[2] + patch_shape[2],
                          ]
            image_patches[i, :, :, :] = image_patch

        # normalize and then predict on batch
        image_patches = normalize_func(image_patches)
        image_patches = torch.from_numpy(image_patches.astype(np.float32)).to(compute_device)
        with torch.no_grad():
            predictions = model(image_patches).cpu().detach().numpy()

        # iterate through patches in batch and place them in the result image volume
        for i, corner_coord in enumerate(batch_corner_coords):
            if segmentation_mode == 'center':
                # crop out the patch overlap (remove the perimeter)
                cropped_image_patch = predictions[i,
                                      overlap_z:-overlap_z,
                                      overlap_xy:-overlap_xy,
                                      overlap_xy:-overlap_xy]
                # insert that crop into the right place in the result image
                result_volume[
                corner_coord[0] + overlap_z:corner_coord[0] + patch_shape[0] - overlap_z,
                corner_coord[1] + overlap_xy:corner_coord[1] + patch_shape[1] - overlap_xy,
                corner_coord[2] + overlap_xy:corner_coord[2] + patch_shape[2] - overlap_xy
                ] = cropped_image_patch
            elif segmentation_mode == 'any':
                image_patch = predictions[i, ...]
                segmented_at_patch = result_volume[
                                     corner_coord[0]:corner_coord[0] + patch_shape[0],
                                     corner_coord[1]:corner_coord[1] + patch_shape[1],
                                     corner_coord[2]:corner_coord[2] + patch_shape[2],
                                     ]
                # element wise maximum of current result volume and new predictions
                # i.e. if two windows disagree, use the one asserting the pixel should be segmented
                result_volume[
                corner_coord[0]:corner_coord[0] + patch_shape[0],
                corner_coord[1]:corner_coord[1] + patch_shape[1],
                corner_coord[2]:corner_coord[2] + patch_shape[2],
                ] = np.maximum(image_patch, segmented_at_patch)
            else:
                raise ValueError(f"Unrecognised segmentation mode: {segmentation_mode}")

        live_view = result_volume[
                    overlap_z + patch_shape[0]:-(overlap_z + patch_shape[0]),
                    overlap_xy + patch_shape[1]:-(overlap_xy + patch_shape[1]),
                    overlap_xy + patch_shape[2]:-(overlap_xy + patch_shape[2]),
                    ]

        print(((overlap_z + patch_shape[0]), -(overlap_z + patch_shape[0])),
              ((overlap_xy + patch_shape[1]), -(overlap_xy + patch_shape[1])),
              ((overlap_xy + patch_shape[2]), -(overlap_xy + patch_shape[2])))
        yield batch_start + batch_size, grid_coordinates, live_view, patch_shape, batch_corner_coords


class PHHPredictWidget(QWidget):
    def __init__(self, napari_viewer):
        super().__init__()

        # INITIALISE WIDGET
        self.viewer = napari_viewer
        self.setLayout(QVBoxLayout())

        # LOGO
        logo_path = abspath(__file__, 'resources/VEMSEG-WHITE-OG-RES.png')
        label = QLabel()
        pixmap = QPixmap(logo_path)
        pixmap = pixmap.scaledToWidth(250)
        label.setPixmap(pixmap)
        self.layout().addWidget(label)

        # TOOL NAME
        plugin_label_font = QFont()
        plugin_label_font.setPointSize(20)
        self.plugin_label = QLabel("PHH Prediction")
        self.plugin_label.setFont(plugin_label_font)
        self.layout().addWidget(self.plugin_label)

        # IMAGE AND LABEL INPUT
        w, self.image_select = make_widget(annotation=Image, label="Image")
        w.setToolTip('The selected image will be segmented.')
        self.layout().addWidget(w)
        napari_viewer.layers.selection.events.changed.connect(self._on_selection)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.layout().addWidget(self.progress_bar)

        # PREDICT BUTTON
        self._run_button = QPushButton("Predict")
        self.layout().addWidget(self._run_button)
        self._run_button.clicked.connect(self.run_prediction_pipeline)

        # PREDICT BUTTON
        self._stop_button = QPushButton("Stop Prediction")
        self._stop_button.setVisible(False)
        self.layout().addWidget(self._stop_button)
        # self._run_button.clicked.connect(self.run_prediction_pipeline)

    def _on_selection(self, event):
        """
        If a new layer is added the viewer the list widget is updated
        with the new

        :param event: An event where a layer is removed or added or updated.
        :return: Updated version of the image_select widget
        """
        self.image_select.reset_choices(event)

    def run_prediction_pipeline(self):
        """
        Upon the Predict button being called this function is called
        where the segmentation pipeline is ran. The function checks
        for the model if it has been previously installed or not.
        If the model has not been installed then it will be installed.
        Once the model is installed the segmentation will begin.

        :return: Segmentation of the inputted stack
        """
        if self.image_select.value is None:
            warnings.warn('No Image Selected')
            return

        self._run_button.setVisible(False)
        self._stop_button.setVisible(True)

        stack = np.asarray(self.image_select.value.data)

        self.progress_bar.setValue(0)

        fpath_or_url = 'https://zenodo.org/record/7650381/files/Standard_UNet.pt?download=1'

        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        hub_dir = torch.hub.get_dir()

        try:
            os.makedirs(hub_dir)
        except:
            pass

        os.path.exists(hub_dir)

        parts = urlparse(fpath_or_url)
        filename = os.path.basename(parts.path)
        cached_file = os.path.join(hub_dir, filename)

        if not os.path.exists(cached_file):
            sys.stderr.write('Downloading: "{}" to {}\n'.format(fpath_or_url, cached_file))
            hash_prefix = None
            torch.hub.download_url_to_file(fpath_or_url, cached_file, hash_prefix, progress=True)

        model = UNet(12)

        if torch.cuda.is_available():
            model.cuda()

        model.load_state_dict(torch.load(cached_file, device))

        def on_yield(value):
            """
            Upon the segmentation thread yielding this function takes
            the output which is the batch start value and grid coords
            which are used to calculate the progression of the
            segmentation. The segmentation at its current state is also
            returned to the viewer.

            :param value:
            :return:
            """
            batch_start = value[0]
            grid_coordinates = value[1]
            new_image = value[2]
            patch_shape = value[3]
            batch_corner_coords = value[4]

            print(patch_shape, batch_corner_coords[0])
            self.progress_bar.setValue(int(np.round(batch_start / len(grid_coordinates) * 100, 2)))

            corner = batch_corner_coords[0]
            patch = np.asarray([[corner[0], corner[1], corner[2]],
                                [corner[0], corner[1], corner[2] + patch_shape[2]],
                                [corner[0], corner[1] + patch_shape[1], corner[2] + patch_shape[2]],
                                [corner[0], corner[1] + patch_shape[1], corner[2]],
                                ]
                               )

            try:
                # if the layer exists, update the data
                self.viewer.layers['result'].data = new_image
            except KeyError:
                # otherwise add it to the viewer
                self.viewer.add_image(
                    new_image,
                    name='result',
                    blending='additive',
                    colormap='green',
                )
            try:
                self.viewer.layers['segmentation mask'].data = patch
            except KeyError:
                self.viewer.add_shapes(
                    patch,
                    shape_type='polygon',
                    name='segmentation mask',
                    opacity=0.5,
                    edge_color='red',
                    face_color='royalblue',
                    blending='additive'
                )

        def worker_end():
            """
            Upon segmentation completing the run button is set to visible
            and stop button is made invisible
            """
            print("Ending Segmentation")
            self._run_button.setVisible(True)
            self._stop_button.setVisible(False)
            self._stop_button.clicked.disconnect()

        worker = segment_stack(image_stack=stack,
                               model=model,
                               patch_shape=(12, 304, 304),
                               compute_device=device,
                               normalize_func=imnorm)
        self._stop_button.clicked.connect(worker.quit)
        worker.yielded.connect(on_yield)
        worker.finished.connect(worker_end)
        worker.start()
