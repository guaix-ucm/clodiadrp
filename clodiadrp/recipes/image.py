

from numina.core import Product, Requirement
from numina.core import DataFrameType
from numina.types.obsresult import ObservationResultType
from numina.core.recipes import BaseRecipe

from clodiadrp.products import MasterFlat, MasterBias


class Image(BaseRecipe):

    obresult = Requirement(ObservationResultType, "Observation Result")
    master_bias = Requirement(MasterBias, "Master Bias")
    master_flat = Requirement(MasterFlat, "Master Flat")
    final = Product(DataFrameType)

    def run(self, rinput):

        # Here the raw images are processed
        # and a final image myframe is created
        myframe = None

        result = self.create_result(final=myframe)
        return result