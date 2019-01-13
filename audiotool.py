from dataclasses import dataclass, field

from pprint import pprint


@dataclass
class Session:
    # The root (a.k.a. one octave = 12 notes) for the re-pitching equation
    REPITCH_ROOT: float = field(init=False, default=12., repr=False)
    # How much to round the results
    ROUND: int = field(init=False, default=5, repr=False)

    tempo: float = 128.0
    sampling_rate: float = 48000.

    def __init__(self, repitch_root=None, rounding=None):
        self.REPITCH_ROOT = repitch_root or self.REPITCH_ROOT
        self.ROUND = rounding or self.ROUND

    def _repitch(self, rate, steps):
        return round(rate * (2 ** (steps / self.REPITCH_ROOT)), self.ROUND)

    def repitch_tempo(self, steps):
        return self._repitch(self.tempo, steps)

    def repitch_sampling_rate(self, steps):
        return self._repitch(self.sampling_rate, steps)

    def _time_ms(self, tempo, length):
        return round(length * (60000. / tempo), self.ROUND)

    def measure_full_ms(self):
        return self._time_ms(self.tempo, 1.)

    def measure_half_ms(self):
        return self._time_ms(self.tempo, 0.5)

    def measure_fourth_ms(self):
        return self._time_ms(self.tempo, 0.25)

    def measure_ms(self, length):
        return self._time_ms(self.tempo, length)

    def _time_hz(self, tempo, length):
        return round(1000. / (self._time_ms(tempo, length)), self.ROUND)

    def measure_full_hz(self):
        return self._time_hz(self.tempo, 1.)

    def measure_half_hz(self):
        return self._time_hz(self.tempo, 0.5)

    def measure_fourth_hz(self):
        return self._time_hz(self.tempo, 0.25)

    def measure_hz(self, length):
        return self._time_hz(self.tempo, length)

    def _time_samples(self, tempo, length):
        return round(self._time_ms(tempo, length) * self.sampling_rate / 1000., self.ROUND)

    def measure_full_samples(self):
        return self._time_samples(self.tempo, 1.)

    def measure_half_samples(self):
        return self._time_samples(self.tempo, 0.5)

    def measure_fourth_samples(self):
        return self._time_samples(self.tempo, 0.25)

    def measure_samples(self, length):
        return self._time_samples(self.tempo, length)

    def times(self, length):
        return {
            'length': length,
            'ms': self.measure_ms(length),
            'hz': self.measure_hz(length),
            'samples': self.measure_samples(length)
        }

    def measures(self, times):
        return [self.times(time) for time in times]

    def measures_halves(self, n):
        return self.measures([1. / (2 ** x) for x in range(n)])


a = Session()

pprint(a.measures_halves(10))
