

from numina.core import Product, Requirement
from numina.core import DataFrameType
from numina.types.obsresult import ObservationResultType
from numina.core.recipes import BaseRecipe


class Bias(BaseRecipe):

    obresult = Requirement(ObservationResultType, "Observation Result")
    master_bias = Product(DataFrameType)

    def run(self, rinput):

        # Here the raw images are processed
        # and a final image myframe is created
        myframe = None
        #

        result = self.create_result(master_bias=myframe)  (5)
        return result