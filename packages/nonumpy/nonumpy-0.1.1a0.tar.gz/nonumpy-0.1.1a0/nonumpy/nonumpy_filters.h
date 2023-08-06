#pragma once

#include "nonumpy_config.h"

// #ifndef NONUMPY_FLOAT_T
// #define NONUMPY_FLOAT_T float
// #endif

#define ACCUMULATOR_T NONUMPY_FLOAT_T

#ifndef M_PI
#define M_PI 3.141592653589793238462643383279502884197163993751
#endif

#define NONUMPY_FILTER_NAME_BW_LOW_PASS bw_lp
#define NONUMPY_FILTER_NAME_BW_HIGH_PASS bw_hp
#define NONUMPY_FILTER_NAME_BW_BAND_PASS bw_bp
#define NONUMPY_FILTER_NAME_BW_BAND_STOP bw_bs

#define NONUMPY_FILTER_STATE_TAG(NAME, ORDER)                                  \
  struct nonumpy_filter_##NAME##_##ORDER##_state_t

#define NONUMPY_FILTER_BW_SINGLE_STATE_DECLARE(NAME, ORDER)                    \
  NONUMPY_FILTER_STATE_TAG(NAME, ORDER) {                                      \
    ACCUMULATOR_T A[(ORDER / 2)];                                              \
    ACCUMULATOR_T d1[(ORDER / 2)];                                             \
    ACCUMULATOR_T d2[(ORDER / 2)];                                             \
    ACCUMULATOR_T w0[(ORDER / 2)];                                             \
    ACCUMULATOR_T w1[(ORDER / 2)];                                             \
    ACCUMULATOR_T w2[(ORDER / 2)];                                             \
  };

#define NONUMPY_FILTER_INIT_NAME(NAME, ORDER)                                  \
  nonumpy_filter_##NAME##_##ORDER##_init

#define NONUMPY_FILTER_RUN_NAME(NAME, ORDER)                                   \
  nonumpy_filter_##NAME##_##ORDER##_run

#define NONUMPY_FILTER_SINGLE_INIT_SIG(NAME, ORDER)                            \
  int NONUMPY_FILTER_INIT_NAME(NAME, ORDER)(                                   \
      NONUMPY_FILTER_STATE_TAG(NAME, ORDER) * state,                           \
      ACCUMULATOR_T sample_rate_hz, ACCUMULATOR_T cutoff_hz)

#define NONUMPY_FILTER_RUN_SIG(NAME, ORDER)                                    \
  ACCUMULATOR_T NONUMPY_FILTER_RUN_NAME(NAME, ORDER)(                          \
      NONUMPY_FILTER_STATE_TAG(NAME, ORDER) * state, ACCUMULATOR_T value)

#define NONUMPY_FILTER_SINGLE_INIT_DECLARE(NAME, ORDER)                        \
  NONUMPY_FILTER_SINGLE_INIT_SIG(NAME, ORDER);

#define NONUMPY_FILTER_SINGLE_INIT_DEFINE(NAME, ORDER, CODE)                   \
  NONUMPY_FILTER_SINGLE_INIT_SIG(NAME, ORDER) { CODE }

#define NONUMPY_FILTER_RUN_DECLARE(NAME, ORDER)                                \
  NONUMPY_FILTER_RUN_SIG(NAME, ORDER);

#define NONUMPY_FILTER_RUN_DEFINE(NAME, ORDER, CODE)                           \
  NONUMPY_FILTER_RUN_SIG(NAME, ORDER) {                                        \
    do {                                                                       \
      CODE                                                                     \
    } while (0);                                                               \
  }

#define NONUMPY_FILTER_BW_SINGLE(NAME, ORDER)                                  \
  NONUMPY_FILTER_BW_SINGLE_STATE_DECLARE(NAME, ORDER)                          \
  NONUMPY_FILTER_SINGLE_INIT_DECLARE(NAME, ORDER)                              \
  NONUMPY_FILTER_RUN_DECLARE(NAME, ORDER)

#define X_ORDERS                                                               \
  X(2)                                                                         \
  X(4)                                                                         \
  X(6)                                                                         \
  X(8)                                                                         \
  X(10)

#define X(ORDER)                                                               \
  NONUMPY_FILTER_BW_SINGLE(NONUMPY_FILTER_NAME_BW_LOW_PASS, ORDER)             \
  NONUMPY_FILTER_BW_SINGLE(NONUMPY_FILTER_NAME_BW_HIGH_PASS, ORDER)

X_ORDERS

#undef X
