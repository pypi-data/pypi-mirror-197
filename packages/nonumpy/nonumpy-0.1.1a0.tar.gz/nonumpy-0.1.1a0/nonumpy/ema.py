from .libnonumpy import LibNonumpy


class EMA:
    def __init__(self, lib: LibNonumpy, alpha: float, value: float = 0):
        self._lib = lib

        self._state = self._lib.new('struct nonumpy_ema_state_t')
        self._state.alpha = alpha
        self._state.value = value

        self._init_func = getattr(self._lib, f'nonumpy_ema_init')
        self._run_func = getattr(self._lib, f'nonumpy_ema_run')

        self._init_func(self._state)

    def run(self, value: float) -> float:
        return self._run_func(self._state, value)
