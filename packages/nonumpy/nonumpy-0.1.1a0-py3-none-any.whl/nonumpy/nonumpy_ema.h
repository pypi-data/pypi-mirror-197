#pragma once

#include "nonumpy_config.h"

struct nonumpy_ema_state_t {
  NONUMPY_FLOAT_T alpha;
  NONUMPY_FLOAT_T value;
  int first;
};

int nonumpy_ema_init(struct nonumpy_ema_state_t *state);
NONUMPY_FLOAT_T nonumpy_ema_run(struct nonumpy_ema_state_t *state,
                                NONUMPY_FLOAT_T input);