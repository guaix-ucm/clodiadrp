

from numina.simulation.device import HWDevice
import clodiadrp.simulation.sequences as seqs

class ClodiaInstrument(HWDevice):
    """Simple MEGARA detector."""

    def __init__(self, shutter, detector):

        super(ClodiaInstrument, self).__init__('CLODIA')
        self.dev_shutter = shutter
        self.detector = detector

        self.detector.set_parent(self)
        self.dev_shutter.set_parent(self)
        self.sequences = seqs.clodia_sequences()

    @property
    def shutter(self):
        return self.dev_shutter.label

    @shutter.setter
    def shutter(self, value):
        self.dev_shutter.label = value
