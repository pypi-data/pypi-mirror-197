import time
from apoc import PredefinedFeatureSet
from napari.layers import Image, Labels
from napari.qt.threading import thread_worker
from qtpy.QtGui import QPixmap, QFont
from qtpy.QtWidgets import (QVBoxLayout,
                            QLabel,
                            QPushButton,
                            QWidget,
                            QSpinBox,
                            QHBoxLayout,
                            QCheckBox,
                            QLineEdit,
                            QDoubleSpinBox,
                            QComboBox)
from superqt import QCollapsible
from .utils import FeatureSelector, set_border, abspath, make_widget


class VEMSEGClassifier(QWidget):
    """
    This is the widget class for the train VEMseg
    classifier tool. It initializes all the GUI components
    of the tool and calls the train function upon clicking
    the train button.
    """

    def __init__(self, napari_viewer):
        """
        This function initialises all the widgets
        that will be used for the train VEMseg
        classifier tool.

        :param napari_viewer: The napari viewer
        """
        super().__init__()
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
        self.plugin_label = QLabel("Pixel Classifier")
        self.plugin_label.setFont(plugin_label_font)
        self.layout().addWidget(self.plugin_label)

        # IMAGE AND LABEL INPUT
        w, self.image_select = make_widget(annotation=Image, label="Image")
        w.setToolTip('The selected image will be segmented.')
        self.layout().addWidget(w)
        w, self.labels_select = make_widget(annotation=Labels, label="Labels")
        w.setToolTip('The selected labels will be used to train a VEM Classifier to segment your selected image.')
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

        # FEATURE SELECTOR DROPDOWN - FEATURES AND SIGMA
        self._feature_collapse = QCollapsible('Feature Selection', self)
        self.feature_selector = FeatureSelector(self, PredefinedFeatureSet.v070.value)
        self._feature_collapse.addWidget(self.feature_selector)
        self._feature_collapse.setDuration(0)
        set_border(self._feature_collapse)
        self.layout().addWidget(self._feature_collapse)

        # DEPTH AND ENSEMBLE INPUT
        self.max_depth = QSpinBox()
        self.max_depth.setMinimum(2)
        self.max_depth.setMaximum(9)
        self.max_depth.setValue(6)
        self.n_estimators = QSpinBox()
        self.n_estimators.setMinimum(1)
        self.n_estimators.setMaximum(999)
        self.n_estimators.setValue(200)
        self.n_estimators.setSingleStep(100)
        depth_ensembles_widget = QWidget()
        depth_ensembles_widget.setLayout(QHBoxLayout())
        depth_ensembles_widget.layout().addWidget(QLabel("Max Depth, Num. Estimators"))
        depth_ensembles_widget.layout().addWidget(self.max_depth)
        depth_ensembles_widget.layout().addWidget(self.n_estimators)
        set_border(depth_ensembles_widget)

        # LEARNING RATE INPUT
        self.learning_rate = QDoubleSpinBox()
        self.learning_rate.setMinimum(0.0)
        self.learning_rate.setMaximum(1.0)
        self.learning_rate.setSingleStep(0.1)
        self.learning_rate.setValue(0.4)
        self.layout().addWidget(self.learning_rate)
        learning_rate_widget = QWidget()
        learning_rate_widget.setLayout(QHBoxLayout())
        learning_rate_widget.layout().addWidget(QLabel("Learning Rate"))
        learning_rate_widget.layout().addWidget(self.learning_rate)
        set_border(learning_rate_widget)

        # SAVE MODEL INPUT
        self.save_model = QCheckBox("Save Model")
        self.save_model.setChecked(False)
        self.model_name = QLineEdit("model.json")
        save_model_name_widget = QWidget()
        save_model_name_widget.setLayout(QHBoxLayout())
        save_model_name_widget.layout().addWidget(self.save_model)
        save_model_name_widget.layout().addWidget(self.model_name)
        set_border(save_model_name_widget)

        # CLASSIFIER DROPDOWN
        self._classifier_collapse = QCollapsible('Classifier Parameters', self)
        self._classifier_collapse.addWidget(depth_ensembles_widget)
        self._classifier_collapse.addWidget(learning_rate_widget)
        self._classifier_collapse.addWidget(save_model_name_widget)
        self._classifier_collapse.setDuration(0)
        set_border(self._classifier_collapse)
        self.layout().addWidget(self._classifier_collapse)

        # RUN BUTTON
        self._run_button = QPushButton("Train")
        self.layout().addWidget(self._run_button)
        self._run_button.clicked.connect(self.predict_clicked)

        # STOP BUTTON
        self._stop_button = QPushButton("Stop Prediction")
        self._stop_button.setVisible(False)
        self.layout().addWidget(self._stop_button)

    def predict_clicked(self):
        """
        This function trains a VEMseg Classifier using the
        user specified parameters and input image and labels.

        Upon clicking the `Train` button this function will be called.

        :return: This function trains a VEMseg Classifier
        and applies it the users inputted image. Optionally,
        saves the model to a user defined path and name.
        """
        import warnings
        import vemseg as vem

        # IMAGE AND LABEL ERROR CHECKING
        if self.image_select.value is None:
            warnings.warn("WARNING: You have not inputted an image")
            return
        elif self.labels_select.value is None:
            warnings.warn("WARNING: You have not inputted labels")
            return

        # OPTIONALLY CREATES MASK TO APPLY TO DATA
        mask = None
        if self.mask_flag.isChecked():
            if self.mask_select.currentText() is None:
                warnings.warn("WARNING: You have not inputted a mask")
                return
            mask = self.viewer.layers[self.mask_select.currentText()].data

        self._run_button.setVisible(False)
        self._stop_button.setVisible(True)

        # CREATE X AND y TRAINING DATA
        x = self.image_select.value.data
        y = self.labels_select.value.data

        # INIT USER DEFINED VEMClassifier
        clf = vem.VEMClassifier(
            features=self.feature_selector.getFeatures(),
            tree_method='hist',
            max_depth=self.max_depth.value(),
            n_estimators=self.n_estimators.value(),
            learning_rate=self.learning_rate.value()
        )

        @thread_worker
        def train_predict_thread():
            # TRAIN AND THEN RETURN PREDICTION TO VIEWER
            st = time.time()
            print("Preprocessing")
            X = vem.pre_process(X=x, mask=mask)

            print("Training")
            clf.fit(X, y)

            # OPTIONALLY SAVE MODEL
            if self.save_model.isChecked():
                print("Saving Model")
                clf.save_model(self.model_name.text())

            print("Predicting")
            return clf.predict(X), st

        def add_data(return_value):
            self.viewer.add_labels(return_value[0])
            print("End time: ", time.time() - return_value[1])

        def worker_end():
            """
            Upon segmentation completing the run button is set to visible
            and stop button is made invisible
            """
            self._run_button.setVisible(True)
            self._stop_button.setVisible(False)
            self._stop_button.clicked.disconnect()

        worker = train_predict_thread()
        self._stop_button.clicked.connect(worker.quit)
        worker.finished.connect(worker_end)
        worker.returned.connect(add_data)
        worker.start()

    def _on_selection(self, event=None):
        """
        Function simply updates the image, labels and mask
        list to the available images and labels if
        a new image is added then list is updated.

        :param event: An instance of the user adding a new image or labels layer.
        :return: Updated image and mask layer list.
        """
        self.labels_select.reset_choices(event)
        self.image_select.reset_choices(event)
        self._on_mask_selection()

    def _on_mask_selection(self):
        """
        If mask checkbox is selected then the
        mask list will be updated.

        :return: Updated mask layers list.
        """
        if self.mask_flag.isChecked():
            self.mask_select.clear()

            for l in self.viewer.layers:
                if isinstance(l, Labels):
                    self.mask_select.addItem(l.name)
        else:
            self.mask_select.clear()
