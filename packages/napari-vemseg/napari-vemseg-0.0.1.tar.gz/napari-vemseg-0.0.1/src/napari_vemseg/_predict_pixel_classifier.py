from napari.layers import Image, Labels
from napari.qt import thread_worker
from qtpy.QtGui import QPixmap, QFont
from qtpy.QtWidgets import (QVBoxLayout,
                            QLabel,
                            QWidget,
                            QHBoxLayout,
                            QCheckBox,
                            QComboBox,
                            QFileDialog,
                            QPushButton,
                            QLineEdit,
                            QSpinBox
                            )
from .utils import set_border, abspath, make_widget


class VEMSEGClassifierPredict(QWidget):
    """
    This is the widget class for the VEMseg
    classifier predict tool. It initializes
    all the GUI components of the tool.
    """
    def __init__(self, napari_viewer):
        """
        This function initialises all the widgets
        that will be used for the VEMseg classifier
        predict tool.

        :param napari_viewer: The napari viewer.
        """
        super().__init__()

        # INITIALISE WIDGET
        self.viewer = napari_viewer
        self.setLayout(QVBoxLayout())

        # VEMSEG LOGO
        logo_path = abspath(__file__, 'resources/VEMSEG-WHITE-OG-RES.png')
        label = QLabel()
        pixmap = QPixmap(logo_path)
        pixmap = pixmap.scaledToWidth(250)
        label.setPixmap(pixmap)
        self.layout().addWidget(label)

        # PLUGIN TOOL NAME
        plugin_label_font = QFont()
        plugin_label_font.setPointSize(20)
        self.plugin_label = QLabel("Predict Pixel Classifier")
        self.plugin_label.setFont(plugin_label_font)
        self.layout().addWidget(self.plugin_label)

        # IMAGE INPUT
        w, self.image_select = make_widget(annotation=Image, label="Image")
        w.setToolTip('The selected image will be segmented.')
        self.layout().addWidget(w)
        napari_viewer.layers.selection.events.changed.connect(self._on_selection)

        # MASK INPUT
        self.mask_select = QComboBox()
        self.mask_flag = QCheckBox("Mask")
        self.mask_flag.toggled.connect(self._on_mask_selection)
        mask_widget = QWidget()
        mask_widget.setToolTip('The selected mask will be applied to the image. Only parts of the image where there'
                               'is a mask will be segmented')
        mask_widget.setLayout(QHBoxLayout())
        mask_widget.layout().addWidget(self.mask_flag)
        mask_widget.layout().addWidget(self.mask_select)
        set_border(mask_widget)
        self.layout().addWidget(mask_widget)

        # OPEN FILE DIALOGUE
        self._open_file_button = QPushButton("Open File")
        self._open_file_path = QLineEdit()
        open_file_widget = QWidget()
        open_file_widget.setLayout(QHBoxLayout())
        open_file_widget.layout().addWidget(self._open_file_button)
        open_file_widget.layout().addWidget(self._open_file_path)
        set_border(open_file_widget)
        self.layout().addWidget(open_file_widget)
        self._open_file_button.clicked.connect(self.open_file_dialogue)

        # PREDICT BUTTON
        self._run_button = QPushButton("Predict")
        self.layout().addWidget(self._run_button)
        self._run_button.clicked.connect(self.predict)

        # STOP BUTTON
        self._stop_button = QPushButton("Stop Prediction")
        self._stop_button.setVisible(False)
        self.layout().addWidget(self._stop_button)

    def predict(self):
        """
        This function applies the user selected pretrained model to
        input the input and then returns the result back to the
        napari viewer as a label.

        This function is called once the user clicks the
        predict button.

        :return:
            The prediction of the users model as a np.ndarray.
        """
        import vemseg as vem
        import warnings

        # INPUT VALIDATION
        if self.image_select.value is None:
            warnings.warn("WARNING: You have not inputted an image")
            return
        if self._open_file_path.text() == "":
            warnings.warn("WARNING: You have not selected a model")
            return

        # GETS MASK DATA IF USER HAS INPUTTED A MASK
        mask = None
        if self.mask_flag.isChecked():
            if self.mask_select.currentText() is None:
                warnings.warn("WARNING: You have not inputted a mask")
                return
            mask = self.viewer.layers[self.mask_select.currentText()].data

        self._run_button.setVisible(False)
        self._stop_button.setVisible(True)

        X = self.image_select.value.data

        pre_trained_model = vem.VEMClassifier()
        pre_trained_model.load_model(self._open_file_path.text())

        @thread_worker
        def predict_thread():
            return pre_trained_model.predict(X, mask=mask)

        def add_prediction(prediction):
            self.viewer.add_labels(prediction)

        def worker_end():
            """
            Upon segmentation completing the run button is set to visible
            and stop button is made invisible
            """
            self._run_button.setVisible(True)
            self._stop_button.setVisible(False)
            self._stop_button.clicked.disconnect()

        worker = predict_thread()
        self._stop_button.clicked.connect(worker.quit)
        worker.finished.connect(worker_end)
        worker.returned.connect(add_prediction)
        worker.start()

    def _on_selection(self, event=None):
        """
        Function simply updates the image and mask
        list to the available images and labels if
        a new image is added then list is updated.

        :param event: An instance of the user adding a new image or labels layer.
        :return: Updated image and mask layer list.
        """
        self.image_select.reset_choices(event)
        self._on_mask_selection()

    def _on_mask_selection(self, event=None):
        """
        If mask checkbox is selected then the
        mask list will be updated.

        :param event: An instance of the user adding a new image or labels layer.
        :return: Updated mask layers list.
        """
        if self.mask_flag.isChecked():
            self.mask_select.clear()

            for l in self.viewer.layers:
                if isinstance(l, Labels):
                    self.mask_select.addItem(l.name)
        else:
            self.mask_select.clear()

    def open_file_dialogue(self):
        """
        If the `Open File` button is clicked a FielDialog will open
        and the users selected model will update the _open_file_path
        var.

        :return: path to the model.
        """
        filename = QFileDialog.getOpenFileName(self, 'Open File', '/', '*.json')
        self._open_file_path.setText(filename[0])

