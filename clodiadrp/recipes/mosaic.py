

from numina.core import Product, Requirement
from numina.core import DataFrameType
from numina.types.obsresult import ObservationResultType
from numina.core.recipes import BaseRecipe
from numina.core.query import Result


class Mosaic(BaseRecipe):

    obresult = Requirement(
        ObservationResultType,
        description="Observation Result",
        query_opts=Result('final', node='children', ignore_fail=True)
    )

    accum_in = Requirement(
        DataFrameType,
        description='Accumulated result',
        optional=True,
        destination='accum',
        query_opts=Result('mosaic.accum', node='prev-rel')
    )

    mosaic = Product(DataFrameType)

    accum = Product(DataFrameType, optional=True)

    def run(self, rinput):

        # Here the raw images are processed
        # and a final image myframe is created
        myframe = process_mosaic(rinput.obresult, self.logger)

        newaccum = process_accum(myframe, rinput.accum, self.logger)

        result = self.create_result(mosaic=myframe, accum=newaccum)
        return result


def process_accum(result, accum, logger):
    import astropy.io.fits as fits

    if accum is None:
        logger.debug('accum is None, first loop')
        data_result = result[0].data[:]
        data_result[:] = 1
        hdu = fits.PrimaryHDU(data_result, header=result[0].header)
        newaccum = fits.HDUList([hdu])
        return newaccum
    else:
        logger.debug('accum is not None, posterior loop')
        data_result = result[0].data[:]
        data_result += 1
        hdu = fits.PrimaryHDU(data_result, header=result[0].header)
        newaccum = fits.HDUList([hdu])
        return newaccum


def process_mosaic(obresult, logger):
    import astropy.io.fits as fits

    if obresult.results:
        dat = []
        fr0 = obresult.results[0].open()
        header = fr0[0].header
        for r in obresult.results:
            logger.debug('Result is: %s', r)
            dat.append(r.open()[0].data)

        sum_data = sum(dat)
    else:
        import numpy
        sum_data = numpy.zeros((4,4))
        header = None

    hdu = fits.PrimaryHDU(sum_data, header=header)
    myframe = fits.HDUList([hdu])

    return myframe