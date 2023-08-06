from .filters import FilterNameEnum, FilterTypeEnum
from .filters import Filter
from .ema import EMA


class Factory:
    def __init__(self, verbose: bool = False, debug: bool = False, path=None):
        # self._verbose = verbose
        # self._debug = debug
        # self._gen_folder = path
        self._lib = Factory._build_lib(verbose=verbose, debug=debug, path=path)

    # @classmethod
    # def CreateFilterLowPassButterworth(cls, sample_rate_hz: float, order: int, cutoff_hz: float):
    #     return Filter(
    #         name=FilterNameEnum.Butterworth,
    #         type=FilterTypeEnum.LowPass,
    #         order=order,
    #         sample_rate_hz=sample_rate_hz,
    #         cutoff_low_hz=cutoff_hz)

    # @classmethod
    # def CreateFilterHighPassButterworth(cls, sample_rate_hz: float, order: int, cutoff_hz: float):
    #     return Filter(
    #         name=FilterNameEnum.Butterworth,
    #         type=FilterTypeEnum.HighPass,
    #         order=order,
    #         sample_rate_hz=sample_rate_hz,
    #         cutoff_low_hz=cutoff_hz)

    # @classmethod
    # def CreateEMA(cls, alpha: float):
    #     return EMA(alpha=alpha)

    def create_FilterLowPassButterworth(self, sample_rate_hz: float, order: int, cutoff_hz: float):
        return Filter(self._lib,
                      name=FilterNameEnum.Butterworth,
                      type=FilterTypeEnum.LowPass,
                      order=order,
                      sample_rate_hz=sample_rate_hz,
                      cutoff_low_hz=cutoff_hz)

    def create_FilterHighPassButterworth(self, sample_rate_hz: float, order: int, cutoff_hz: float):
        return Filter(self._lib,
                      name=FilterNameEnum.Butterworth,
                      type=FilterTypeEnum.HighPass,
                      order=order,
                      sample_rate_hz=sample_rate_hz,
                      cutoff_low_hz=cutoff_hz)

    def create_EMA(self, alpha: float):
        return EMA(self._lib, alpha=alpha)

    @staticmethod
    def _build_lib(verbose: bool, debug: bool, path: str):
        from crelm import Tube

        if verbose:
            print(f'building libnumpy, DEBUG={debug}, gen folder={path}')

        paste = Tube('nonumpy') \
            .verbose(verbose) \
            .set_source_folder_from(__file__) \
            .add_header_files(['nonumpy_ema.h', 'nonumpy_filters.h']) \
            .add_source_files(['nonumpy_ema.c', 'nonumpy_filters.c']) \
            .add_macro('NONUMPY_FLOAT_32') \
            .add_macro_if(debug, 'DEBUG') \
            .squeeze()

        return paste
