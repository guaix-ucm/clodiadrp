
import numpy
import astropy.io.fits as fits
from numina.core import Result, Requirement, Parameter
from numina.types.obsresult import ObservationResultType
from numina.core.recipes import BaseRecipe
from numina.core.validator import range_validator
from clodiadrp.products import MasterBias, MasterFlat


class Flat(BaseRecipe):

    obresult = Requirement(ObservationResultType, "Observation Result")
    master_bias = Requirement(MasterBias, "Master Bias")
    polynomial_degree = Parameter(5, 'Polynomial degree of arc calibration',
                                  as_list=True, nelem='+',
                                  validator=range_validator(minval=1)
                                  )

    @master_bias.validator
    def custom_validator(self, value):
        print('func', self, value)
        return True

    master_flat = Result(MasterFlat)

    def run(self, rinput):

        # Here the raw images are processed
        # and a final image myframe is created
        obresult = rinput.obresult
        fr0 = obresult.frames[0].open()
        data = numpy.ones_like(fr0[0].data)
        hdu = fits.PrimaryHDU(data, header=fr0[0].header)
        myframe = fits.HDUList([hdu])
        #
        result = self.create_result(master_flat=myframe)
        return result
