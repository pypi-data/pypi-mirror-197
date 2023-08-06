from dataclasses import dataclass


@dataclass
class MODEL_TYPE:
    SKLEARN = "sklearn"
    XGBOOST = "xboost"
    TENSORFLOW = "tensorflow"
    PYTORCH = "pytorch"
