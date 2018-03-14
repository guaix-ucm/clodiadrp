
import astropy.io.fits as fits

from clodiadrp.simulation.detector import CLODIA_DETECTOR


def create_bias():
    detector = CLODIA_DETECTOR

    detector.expose(source=0.0, time=0.0)
    data = detector.readout()
    hdu = fits.PrimaryHDU(data)
    hdu.header['INSTRUME'] = 'CLODIA'
    return fits.HDUList([hdu])


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('names', nargs='+')

    args = parser.parse_args()

    for name in args.names:
        hdulist = create_bias()
        hdulist.writeto(name, overwrite=True)


if __name__ == '__main__':

    main()