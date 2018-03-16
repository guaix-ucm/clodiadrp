
import uuid
from datetime import datetime

import astropy.io.fits as fits
from numina.simulation.factory import extract
from numina.simulation.shutter import Shutter

from clodiadrp.simulation.instrument import ClodiaInstrument
from clodiadrp.simulation.detector import CLODIA_DETECTOR


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
        pheader['OBSMODE'] = "mode"
        pheader['UUID'] = str(uuid.uuid4())
        # Date of simulation
        pheader['DATE'] = datetime.utcnow().isoformat()
        # Date of simulated observation, not set yet
        pheader['DATE-OBS'] = datetime.utcnow().isoformat()

        meta = instrument.config_info()
        extract(pheader, meta, ['CLODIA.Detector', 'exposed'], 'EXPTIME')
        extract(pheader, meta, ['CLODIA.Detector', 'exposed'], 'EXPOSED')
        extract(pheader, meta, ['CLODIA', 'insmode'], 'insmode', default='unknown')
        hdu1 = fits.PrimaryHDU(data, header=pheader)
        hdul = fits.HDUList([hdu1])
        return hdul


def create_instrument():

    detector = CLODIA_DETECTOR
    shutter = Shutter()

    instrument = ClodiaInstrument(shutter, detector)
    return instrument


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('names', nargs='+')

    args = parser.parse_args()

    instrument = create_instrument()
    print(instrument.config_info())
    factory = ClodiaImageFactory()
    control = {'CLODIA': instrument}

    # source = 10000
    # time = 1.0
    for name in args.names:
        instrument.detector.expose(source=10000, time=1.0)
        final = instrument.detector.readout()
        result = factory.create(final, 'CLODIA', control)
        result.writeto(name, overwrite=True)

main()