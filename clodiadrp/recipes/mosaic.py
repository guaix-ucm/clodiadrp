

from numina.core import Product, Requirement
from numina.core import DataFrameType
from numina.types.obsresult import ObservationResultType
from numina.core.recipes import BaseRecipe
from numina.core.query import ResultOf


class Mosaic(BaseRecipe):

    obresult = Requirement(
        ObservationResultType,
        description="Observation Result"
    )

    accum_in = Requirement(
        DataFrameType,
        description='Accumulated result',
        optional=True,
        destination='accum',
        query_opts=ResultOf('mosaic.accum', node='prev-rel')
    )

    mosaic = Product(DataFrameType)

    accum = Product(DataFrameType, optional=True)

    def run(self, rinput):

        # Here the raw images are processed
        # and a final image myframe is created
        partial_result = self.run_single(rinput)
        new_result = self.aggregate_result(partial_result, rinput)
        return new_result

    def run_single(self, rinput):

        # Here the raw images are processed
        # and a final image myframe is created
        myframe = process_mosaic(rinput.obresult, self.logger)
        result = self.create_result(mosaic=myframe)
        return result

    def aggregate_result(self, partial_result, rinput):
        accum = rinput.accum
        frame = partial_result.mosaic
        newaccum = self.aggregate_frames(accum, frame)
        partial_result.accum = newaccum
        return partial_result

    def aggregate_frames(self, accum, frame):
        return process_accum(frame, accum, self.logger)


def process_accum(result, accum, logger):
    import astropy.io.fits as fits

    if accum is None:
        logger.debug('accum is None, first loop')
        naccum = 0
        accum_data = 0
    else:
        accum_f = accum.open()
        naccum = accum_f[0].header['NUMACCUM']
        accum_data = accum_f[0].data

    logger.debug('accum is not None, naccum=%d', naccum)
    nxaccum = naccum + 1
    result_f = result.open()
    data_result = (result_f[0].data + naccum * accum_data) / nxaccum
    hdu = fits.PrimaryHDU(data_result, header=result_f[0].header)
    hdu.header['NUMACCUM'] = nxaccum
    newaccum = fits.HDUList([hdu])
    return newaccum


def process_mosaic(obresult, logger):
    import astropy.io.fits as fits

    if obresult.results:
        dat = []

        for r in obresult.results.values():
            logger.debug('Result is: %s', r)
            dat.append(r.open()[0].data)
        sum_data = sum(dat)

        # first element
        fr0 = next(iter(obresult.results.values()))
        fr0_o = fr0.open()
        header = fr0_o[0].header
    else:
        import numpy
        sum_data = numpy.zeros((4,4))
        header = None

    hdu = fits.PrimaryHDU(sum_data, header=header)
    myframe = fits.HDUList([hdu])

    return myframe