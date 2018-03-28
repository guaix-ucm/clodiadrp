
import uuid
from datetime import datetime
import logging

import astropy.io.fits as fits
from numina.simulation.factory import extract
from numina.simulation.shutter import Shutter
from numina.simulation.factory import PersistentRunCounter

from clodiadrp.simulation.instrument import ClodiaInstrument
from clodiadrp.simulation.detector import CLODIA_DETECTOR
from clodiadrp.simulation.sequences import clodia_sequences

_logger = logging.getLogger(__name__)


class ClodiaImageFactory(object):
    CARDS_P = [
        ('OBSERVAT', 'UCM', 'Name of observatory'),
        ('TELESCOP', 'PATRIX', 'Telescope id.'),
        ('INSTRUME', 'CLODIA', 'Name of the Instrument'),
        ('ORIGIN', 'SIMULATOR', 'FITS file originator'),
        ('INSCONF', 'v1')
    ]

    def create(self, data, name, control):
        pheader = fits.Header(self.CARDS_P)
        # pheader['FILENAME'] = name
        instrument = control.get(name)
        pheader['OBSMODE'] = control.mode
        pheader['UUID'] = str(uuid.uuid4())

        meta = instrument.config_info()
        extract(pheader, meta, ['CLODIA.Detector', 'exposed'], 'EXPTIME')
        extract(pheader, meta, ['CLODIA.Detector', 'exposed'], 'EXPOSED')
        extract(pheader, meta, ['CLODIA.Detector', 'DATE-OBS'], 'DATE-OBS')
        extract(pheader, meta, ['CLODIA', 'insmode'], 'insmode', default='unknown')
        hdu1 = fits.PrimaryHDU(data, header=pheader)
        hdul = fits.HDUList([hdu1])
        return hdul


def create_instrument():

    detector = CLODIA_DETECTOR
    shutter = Shutter()

    instrument = ClodiaInstrument(shutter, detector)
    return instrument


class ControlSystem(object):
    """Top level"""
    def __init__(self, factory):
        self.imagecount = PersistentRunCounter('r00%04d.fits')
        self._elements = {}
        self.mode = 'null'
        self.factory = factory
        self.ob_data = dict(count=0, repeat=0, name=None, obsid=1)
        self.targets = None

    def register(self, name, element):
        self._elements[name] = element

    def get(self, name):
        return self._elements[name]

    def set_mode(self, mode):
        self.mode = mode

    def run(self, instrument, exposure, repeat=1):

        if repeat < 1:
            return

        ins = self.get(instrument)

        _logger.info('mode is %s', self.mode)
        try:
            thiss = ins.sequences[self.mode]
        except KeyError:
            _logger.error('No sequence for mode %s', self.mode)
            raise

        iterf = thiss.run(self, exposure, repeat)

        self.ob_data['repeat'] = repeat
        self.ob_data['name'] = None
        for count, final in enumerate(iterf, 1):
            _logger.info('image %d of %d', count, repeat)
            self.ob_data['name'] = self.imagecount.runstring()
            self.ob_data['count'] = count
            fitsfile = self.factory.create(final, instrument, self)
            _logger.info('save image %s', self.ob_data['name'])
            fitsfile.writeto(self.ob_data['name'], overwrite=True)

    def config_info(self):
        return {'ob_data': self.ob_data}


def main():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-e', '--exposure', type=float, default=0.0,
                        help="Exposure time per image (in seconds) [0,36000]")
    parser.add_argument('-n', '--nimages', metavar="INT", type=int, default=1,
                        help="Number of images to generate")

    parser.add_argument('omode', choices=clodia_sequences().keys(),
                        help="Observing mode of the intrument")

    args = parser.parse_args()

    instrument = create_instrument()

    factory = ClodiaImageFactory()

    control = ControlSystem(factory)
    control.register('CLODIA', instrument)

    control.set_mode(args.omode)

    control.run('CLODIA', args.exposure, repeat=args.nimages)
    control.imagecount.store()

main()