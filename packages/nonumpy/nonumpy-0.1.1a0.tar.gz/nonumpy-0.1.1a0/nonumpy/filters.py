from enum import IntEnum
from .libnonumpy import LibNonumpy


class FilterNameEnum(IntEnum):
    Butterworth = 1


class FilterTypeEnum(IntEnum):
    LowPass = 101,
    HighPass = 102,
    BandPass = 103,
    BandStop = 104


class Filter:
    _tokens = {
        FilterNameEnum.Butterworth: 'bw',
        FilterTypeEnum.LowPass: 'lp',
        FilterTypeEnum.HighPass: 'hp',
    }

    def __init__(self, lib: LibNonumpy,
                 name: FilterNameEnum,
                 type: FilterTypeEnum,
                 sample_rate_hz: float,
                 order: int,
                 cutoff_high_hz: float = None,
                 cutoff_low_hz: float = None):

        self._lib = lib
        self._name = name
        self._type = type
        self._order = order
        self._sample_rate_hz = sample_rate_hz
        self._cutoff_high_hz = cutoff_high_hz
        self._cutoff_low_hz = cutoff_low_hz

        self.init_func = None
        self.run_func = None

        self._init_impl()

    def _init_impl(self) -> bool:
        key = f'{Filter._tokens[self._name]}_{Filter._tokens[self._type]}_{self._order}'

        self._filter_state = self._lib.new(
            f'struct nonumpy_filter_{key}_state_t')

        self.init_func = getattr(self._lib, f'nonumpy_filter_{key}_init')
        self.run_func = getattr(self._lib, f'nonumpy_filter_{key}_run')

        if FilterTypeEnum.LowPass == self._type:
            self.init_func(self._filter_state,
                           self._sample_rate_hz, self._cutoff_low_hz)
        elif FilterTypeEnum.HighPass == self._type:
            self.init_func(self._filter_state,
                           self._sample_rate_hz, self._cutoff_low_hz)

        return True

    def run(self, value: float) -> float:
        return self.run_func(self._filter_state, value)
