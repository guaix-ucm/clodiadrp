

import numpy
import astropy.io.fits as fits

from numina.core import Product, Requirement
from numina.core import DataFrameType
from numina.types.obsresult import ObservationResultType
from numina.core.recipes import BaseRecipe
from numina.core.query import Result

from clodiadrp.products import MasterFlat, MasterBias, SkyImage


class ImageRecipe(BaseRecipe):

    obresult = Requirement(ObservationResultType, "Observation Result")
    master_bias = Requirement(MasterBias, "Master Bias")
    master_flat = Requirement(MasterFlat, "Master Flat")
    final = Product(DataFrameType)

    def run(self, rinput):

        # Here the raw images are processed
        # and a final image myframe is created
        myframe = produce_image(rinput.obresult)

        result = self.create_result(final=myframe)
        return result


class ImageSkyRecipe(BaseRecipe):

    obresult = Requirement(ObservationResultType, "Observation Result")

    master_bias = Requirement(MasterBias, "Master Bias")
    master_flat = Requirement(MasterFlat, "Master Flat")

    # This field can be disabled via
    # query_options: sky_image: False
    # in drp.yaml
    sky_image = Requirement(SkyImage,
                            description="Previous Sky Image",
                            query_opts=Result('sky.sky_image', node='prev'),
                            default=None # This value is used only if the query is disabled
                            )
    final = Product(DataFrameType)

    def run(self, rinput):

        query_sky_image = self.query_options.get('sky_image', True)

        if query_sky_image:
            self.logger.debug('using sky, value=%s', rinput.sky_image)
        else:
            self.logger.debug('not using sky, value=%s', rinput.sky_image)

        # Here the raw images are processed
        # and a final image myframe is created
        myframe = produce_image(rinput.obresult)

        result = self.create_result(final=myframe)
        return result


class SkyRecipe(BaseRecipe):

    obresult = Requirement(ObservationResultType, "Observation Result")
    master_bias = Requirement(MasterBias, "Master Bias")
    master_flat = Requirement(MasterFlat, "Master Flat")

    sky_image = Product(SkyImage)

    def run(self, rinput):

        # Here the raw images are processed
        # and a final image myframe is created
        myframe = produce_image(rinput.obresult)

        result = self.create_result(sky_image=myframe)
        return result


def produce_image(obresult):
    """Create a image, without reduction"""
    fr0 = obresult.frames[0].open()
    data = numpy.ones_like(fr0[0].data)
    hdu = fits.PrimaryHDU(data, header=fr0[0].header)
    myframe = fits.HDUList([hdu])
    return myframe