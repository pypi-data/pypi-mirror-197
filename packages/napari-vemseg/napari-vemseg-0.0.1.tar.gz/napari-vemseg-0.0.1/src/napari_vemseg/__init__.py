__version__ = "0.0.1"

from ._vem_pixel_classifier import VEMSEGClassifier
from ._predict_pixel_classifier import VEMSEGClassifierPredict

__all__ = (
    "VEMSEGClassifier",
    "VEMSEGClassifierPredict"
)
