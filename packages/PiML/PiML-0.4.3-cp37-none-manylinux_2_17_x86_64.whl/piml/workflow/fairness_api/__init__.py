from .fairness_api import FairnessAPI
from .fairness_compare_api import FairnessCompareAPI
from .fairness_solas_api import FairnessAPI_solas

__all__ = ["FairnessAPI", "FairnessCompareAPI", 'FairnessAPI_solas']

def get_all_supported_models():
    return sorted(__all__)
