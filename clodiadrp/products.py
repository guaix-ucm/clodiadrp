

from numina.types.frame import DataFrameType
from numina.types.product import DataProductTag


class MasterBias(DataFrameType, DataProductTag):
    "Master Bias calibration image of CLODIA"
    pass


class MasterFlat(DataFrameType, DataProductTag):
    "Master Flat calibration image of CLODIA"
    pass