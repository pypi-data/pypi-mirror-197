#include "nonumpy_config.h"

#include "nonumpy_ema.h"

int nonumpy_ema_init(struct nonumpy_ema_state_t *state) {
  state->value = 0;
  state->first = 1;

  return 0;
}

NONUMPY_FLOAT_T nonumpy_ema_run(struct nonumpy_ema_state_t *state,
                                NONUMPY_FLOAT_T input) {
  if (state->first) {
    state->value = input;
    state->first = 0;
  }

  state->value = input * state->alpha + state->value * (1 - state->alpha);

  return state->value;
}
