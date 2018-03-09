

from numina.core import Product, Requirement
from numina.types.obsresult import ObservationResultType
from numina.core.recipes import BaseRecipe

from clodiadrp.products import MasterBias


class Bias(BaseRecipe):

    obresult = Requirement(ObservationResultType, "Observation Result")
    master_bias = Product(MasterBias)

    def run(self, rinput):

        # Here the raw images are processed
        # and a final image myframe is created
        myframe = None
        #

        result = self.create_result(master_bias=myframe)  (5)
        return result