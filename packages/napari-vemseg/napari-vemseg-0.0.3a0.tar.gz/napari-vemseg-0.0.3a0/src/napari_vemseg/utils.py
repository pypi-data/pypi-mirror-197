import numpy as np
from skimage import exposure
from skimage.filters import rank
from skimage.morphology import disk
from magicgui.widgets import create_widget
from pathlib import Path
from qtpy.QtWidgets import (QVBoxLayout,
                            QLabel,
                            QCheckBox,
                            QWidget,
                            QGridLayout,
                            QHBoxLayout)


def patch_wise_norm(train_batch: np.ndarray) -> np.ndarray:
    """
    Patch wise normalization approach Harry settled on. Works well in practice.
    Also reasonably performant is centering and scaling the stacks based on
    standard 0-255 image intensity range.
    """
    mean = np.mean(train_batch, axis=(1, 2, 3), keepdims=True)
    std = np.std(train_batch, axis=(1, 2, 3), keepdims=True)
    return (train_batch - mean) / (std + 0.0001)


def imnorm(train_batch: np.ndarray) -> np.ndarray:
    """ center and scale stacks between -1:1 """
    return (train_batch - 127) / 128


def hist(train_batch: np.ndarray) -> np.ndarray:
    out = np.zeros_like(train_batch)
    for p in range(train_batch.shape[0]):
        out[p, ...] = exposure.equalize_hist(train_batch[p, ...])
    return out


def hist_local(train_batch: np.ndarray) -> np.ndarray:
    out = np.zeros_like(train_batch)
    for p in range(train_batch.shape[0]):
        for z in range(train_batch.shape[-3]):
            zslice = train_batch[p, ..., z, :, :].astype(np.uint8)
            zslice = rank.equalize(zslice, selem=disk(30)).astype(out.dtype)
            out[p, ..., z, :, :] = zslice
    return out


def pscale(train_batch: np.ndarray) -> np.ndarray:
    out = np.zeros_like(train_batch)
    for p in range(train_batch.shape[0]):
        p2, p98 = np.percentile(train_batch, (2, 98))
        out[p, ...] = exposure.rescale_intensity(train_batch[p, ...], in_range=(p2, p98))
    return out


def histb(train_batch: np.ndarray) -> np.ndarray:
    return np.array(2. * (exposure.equalize_hist(train_batch) - 0.5), dtype=np.float32)


def pscaleb(train_batch: np.ndarray) -> np.ndarray:
    p2, p98 = np.percentile(train_batch, (2, 98))
    return 2. * (exposure.rescale_intensity(train_batch, in_range=(p2, p98)) - 0.5)


def make_widget(annotation, label):
    w = QWidget()
    w.setLayout(QHBoxLayout())
    w.layout().addWidget(QLabel(label))

    magic_w = create_widget(annotation=annotation, label=label)
    w.layout().addWidget(magic_w.native)

    set_border(w)

    return w, magic_w


def bnorm(train_batch: np.ndarray) -> np.ndarray:
    """ boolean input images """
    return (train_batch > 127).astype(np.float32)


def bnormc(train_batch: np.ndarray) -> np.ndarray:
    """ centered bnorm """
    return ((train_batch > 127) * 2. - 1.).astype(np.float32)


def abspath(root, relpath):
    root = Path(root)
    if root.is_dir():
        path = root / relpath
    else:
        path = root.parent / relpath
    return str(path.absolute())


def set_border(widget: QWidget, spacing=2, margin=0):
    if hasattr(widget.layout(), "setContentsMargins"):
        widget.layout().setContentsMargins(margin, margin, margin, margin)
    if hasattr(widget.layout(), "setSpacing"):
        widget.layout().setSpacing(spacing)


class FeatureSelector(QWidget):
    def __init__(self, parent, feature_definition: str):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.feature_definition = " " + feature_definition.lower() + " "

        self.available_features = ["gaussian_blur", "difference_of_gaussian", "laplace_box_of_gaussian_blur",
                                   "sobel_of_gaussian_blur"]
        self.available_features_short_names = ["Gauss", "DoG", "LoG", "SoG"]
        self.available_features_tool_tips = ["Gaussian filter", "Difference of Gaussian", "Laplacian of Gaussian",
                                             "Sobel of Gaussian\nalso known as Gradient Magnitude of Gaussian"]

        self.radii = [0.3, 0.5, 1, 2, 3, 4, 5, 10, 15, 25]

        # Headline
        table = QWidget()
        table.setLayout(QGridLayout())
        label_sigma = QLabel("sigma")
        sigma_help = "Increase sigma in case a pixels classification depends on the intensity of other more proximal pixels."
        label_sigma.setToolTip(sigma_help)
        table.layout().addWidget(label_sigma, 0, 0)
        set_border(table)

        for i, r in enumerate(self.radii):
            label_sigma = QLabel(str(r))
            label_sigma.setToolTip(sigma_help)
            table.layout().addWidget(label_sigma, 0, i + 1)

        # Feature lines
        row = 1
        for f, f_short, f_tooltip in zip(self.available_features, self.available_features_short_names,
                                         self.available_features_tool_tips):
            label = QLabel(f_short)
            label.setToolTip(f_tooltip)
            table.layout().addWidget(label, row, 0)
            for i, r in enumerate(self.radii):
                table.layout().addWidget(
                    self._make_checkbox("", f + "=" + str(r), (f + "=" + str(r)) in self.feature_definition), row,
                    i + 1)
            row = row + 1

        self.layout().addWidget(table)

        self.layout().addWidget(
            self._make_checkbox("Consider original image as well", "original", " original " in self.feature_definition))
        set_border(self)

    def _make_checkbox(self, title, feature, checked):
        checkbox = QCheckBox(title)
        checkbox.setChecked(checked)

        def check_the_box(*args, **kwargs):
            if checkbox.isChecked():
                self._add_feature(feature)
            else:
                self._remove_feature(feature)

        checkbox.stateChanged.connect(check_the_box)
        return checkbox

    def _remove_feature(self, feature):
        self.feature_definition = " " + (self.feature_definition.replace(" " + feature + " ", " ")).strip() + " "

    def _add_feature(self, feature):
        self.feature_definition = self.feature_definition + " " + feature + " "

    def getFeatures(self):
        return self.feature_definition.replace("  ", " ").strip(" ")
