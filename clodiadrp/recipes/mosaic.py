

from numina.core import Product, Requirement
from numina.core import DataFrameType
from numina.types.obsresult import ObservationResultType
from numina.core.recipes import BaseRecipe
from numina.core.query import Result


class Mosaic(BaseRecipe):
    obresult = Requirement(
        ObservationResultType,
        description="Observation Result",
        query_opts=Result('final', node='children')
    )

    mosaic = Product(DataFrameType)

    def run(self, rinput):

        # Here the raw images are processed
        # and a final image myframe is created
        myframe = process_mosaic(rinput.obresult, self.logger)

        result = self.create_result(mosaic=myframe)
        return result


def process_mosaic(obresult, logger):
    import astropy.io.fits as fits

    dat = []
    fr0 = obresult.results[0].open()
    for r in obresult.results:
        logger.debug('Result is: %s', r)
        dat.append(r.open()[0].data)

    sum_data = sum(dat)

    hdu = fits.PrimaryHDU(sum_data, header=fr0[0].header)
    myframe = fits.HDUList([hdu])

    return myframe