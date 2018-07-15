

from numina.core import Result, Requirement
from numina.types.obsresult import ObservationResultType
from numina.core.recipes import BaseRecipe

from clodiadrp.products import MasterBias


class BiasRecipe(BaseRecipe):

    obresult = Requirement(ObservationResultType, "Observation Result")
    master_bias = Result(MasterBias)

    def run(self, rinput):

        # Here the raw images are processed
        # and a final image myframe is created
        myframe = rinput.obresult.frames[0].open()
        #

        result = self.create_result(master_bias=myframe)
        return result