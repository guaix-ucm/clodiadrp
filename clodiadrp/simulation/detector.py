
import numpy

from numina.simulation.detector import DetectorBase


class ReadParams(object):
    """Readout parameters of each channel."""
    def __init__(self, gain=1.0, ron=2.0, bias=1000.0):
        self.gain = gain
        self.ron = ron
        self.bias = bias


class ClodiaDetector(DetectorBase):
    """Simple MEGARA detector."""

    def __init__(self, name, shape,
                 qe=1.0, qe_wl=None, dark=0.0,
                 readpars=None):

        super(ClodiaDetector, self).__init__(name, shape, qe, qe_wl, dark)

        self.readpars = readpars if not None else ReadParams()

    def base_readout(self, elec_f):
        # Output image
        final = numpy.zeros(self.dshape)
        self.readout_in_buffer(elec_f, final)
        return final

    def readout_in_buffer(self, elec, final):
        final[:] = elec
        final[:] = final[:] / self.readpars.gain
        # We could use different RON and BIAS in each section
        final[:] = self.readpars.bias + numpy.random.normal(final[:], self.readpars.ron)
        return final

    def init_config_info(self):
        info = super(ClodiaDetector, self).init_config_info()
        info['exposed'] = self._time_last
        return info


DETECTOR_SHAPE = (4, 4)

DETECTOR_READ_PARAMS = ReadParams(ron=3.0, bias=2000)

CLODIA_DETECTOR = ClodiaDetector(name='Detector',
                                 shape=DETECTOR_SHAPE,
                                 readpars=DETECTOR_READ_PARAMS
                                 )
