
import numina.simulation.actions as seq


class ClodiaSequence(seq.Sequence):
    def __init__(self, mode):
        super().__init__('CLODIA', mode)


class ClodiaNullSequence(ClodiaSequence):
    def __init__(self):
        super().__init__('null')

    def run(self, control, exposure, repeat):
        # This is an empty generator
        return iter(())


class ClodiaBiasSequence(ClodiaSequence):
    def __init__(self):
        super().__init__('bias')

    def setup_instrument(self, instrument):
        instrument.shutter = 'STOP'

    def run(self, control, exposure, repeat):
        instrument = control.get(self.instrument)

        self.setup_instrument(instrument)

        for i in range(repeat):
            instrument.detector.expose()
            final = instrument.detector.readout()
            yield final


class ClodiaFlatSequence(ClodiaSequence):
    def __init__(self):
        super().__init__('flat')

    def setup_instrument(self, instrument):
        instrument.shutter = 'OPEN'

    def run(self, control, exposure, repeat):
        instrument = control.get(self.instrument)

        out = 10000

        for i in range(repeat):
            instrument.detector.expose(source=out, time=exposure)
            final = instrument.detector.readout()
            yield final


def clodia_sequences():
    seqs = {}
    # Keys must correspod to MEGARA ObsMode.key
    seqs['null'] = ClodiaNullSequence()
    seqs['bias'] = ClodiaBiasSequence()
    seqs['flat'] = ClodiaFlatSequence()
    return seqs
