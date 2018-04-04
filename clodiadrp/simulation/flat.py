
import astropy.io.fits as fits

from clodiadrp.simulation.detector import CLODIA_DETECTOR


def create_flat(source, time):
    detector = CLODIA_DETECTOR

    detector.expose(source, time)
    data = detector.readout()
    hdu = fits.PrimaryHDU(data)
    hdu.header['INSTRUME'] = 'CLODIA'
    hdu.header['DATE-OBS'] = '2018-01-15T03:40:12.5'
    return fits.HDUList([hdu])


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('names', nargs='+')

    args = parser.parse_args()

    for name in args.names:
        hdulist = create_flat(source=10000, time=1.0)
        hdulist.writeto(name, overwrite=True)


if __name__ == '__main__':

    main()