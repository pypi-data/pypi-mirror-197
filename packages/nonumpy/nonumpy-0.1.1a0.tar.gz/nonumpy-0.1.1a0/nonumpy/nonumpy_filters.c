#include "nonumpy_filters.h"
#include "nonumpy.h"

#include <math.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FLOAT_T_IS_DOUBLE 0 //(sizeof(double) == sizeof(ACCUMULATOR_T))

#if FLOAT_T_IS_DOUBLE
#define COS cos
#define SIN sin
#define TAN tan
#define COSH cosh
#define SINH sinh
#define SQRT sqrt
#define LOG log
#else
#define COS cosf
#define SIN sinf
#define TAN tanf
#define COSH coshf
#define SINH sinhf
#define SQRT sqrtf
#define LOG logf
#endif

#define NONUMPY_FILTER_BW_LP_INIT_DEFINE(ORDER)                                \
  NONUMPY_FILTER_SINGLE_INIT_SIG(NONUMPY_FILTER_NAME_BW_LOW_PASS, ORDER) {     \
    ACCUMULATOR_T a = TAN((ACCUMULATOR_T)(M_PI * cutoff_hz / sample_rate_hz)); \
    ACCUMULATOR_T a2 = a * a;                                                  \
    ACCUMULATOR_T r;                                                           \
    int i;                                                                     \
    for (i = 0; i < (ORDER / 2); ++i) {                                        \
      r = SIN((ACCUMULATOR_T)(M_PI * (2.0 * i + 1.0) / (4.0 * (ORDER / 2))));  \
      sample_rate_hz = (ACCUMULATOR_T)(a2 + 2.0 * a * r + 1.0);                \
      state->A[i] = a2 / sample_rate_hz;                                       \
      state->d1[i] = (ACCUMULATOR_T)(2.0 * (1 - a2) / sample_rate_hz);         \
      state->d2[i] =                                                           \
          (ACCUMULATOR_T)(-(a2 - 2.0 * a * r + 1.0) / sample_rate_hz);         \
    }                                                                          \
    return 0;                                                                  \
  }

#define NONUMPY_FILTER_BW_HP_INIT_DEFINE(ORDER)                                \
  NONUMPY_FILTER_SINGLE_INIT_SIG(NONUMPY_FILTER_NAME_BW_HIGH_PASS, ORDER) {    \
    ACCUMULATOR_T a = TAN((ACCUMULATOR_T)(M_PI * cutoff_hz / sample_rate_hz)); \
    ACCUMULATOR_T a2 = a * a;                                                  \
    ACCUMULATOR_T r;                                                           \
    int i;                                                                     \
    for (i = 0; i < (ORDER / 2); ++i) {                                        \
      r = SIN((ACCUMULATOR_T)(M_PI * (2.0 * i + 1.0) / (4.0 * (ORDER / 2))));  \
      sample_rate_hz = (ACCUMULATOR_T)(a2 + 2.0 * a * r + 1.0);                \
      state->A[i] = (ACCUMULATOR_T)(1.0 / sample_rate_hz);                     \
      state->d1[i] = (ACCUMULATOR_T)(2.0 * (1 - a2) / sample_rate_hz);         \
      state->d2[i] =                                                           \
          (ACCUMULATOR_T)(-(a2 - 2.0 * a * r + 1.0) / sample_rate_hz);         \
    }                                                                          \
    return 0;                                                                  \
  }

NONUMPY_FILTER_BW_LP_INIT_DEFINE(2)
NONUMPY_FILTER_BW_LP_INIT_DEFINE(4)
NONUMPY_FILTER_BW_LP_INIT_DEFINE(6)
NONUMPY_FILTER_BW_LP_INIT_DEFINE(8)
NONUMPY_FILTER_BW_LP_INIT_DEFINE(10)

NONUMPY_FILTER_BW_HP_INIT_DEFINE(2)
NONUMPY_FILTER_BW_HP_INIT_DEFINE(4)
NONUMPY_FILTER_BW_HP_INIT_DEFINE(6)
NONUMPY_FILTER_BW_HP_INIT_DEFINE(8)
NONUMPY_FILTER_BW_HP_INIT_DEFINE(10)

#define NONUMPY_FILTER_BW_LP_RUN_DEFINE(ORDER)                                 \
  NONUMPY_FILTER_RUN_SIG(NONUMPY_FILTER_NAME_BW_LOW_PASS, ORDER) {             \
    int i;                                                                     \
    for (i = 0; i < (ORDER / 2); ++i) {                                        \
      state->w0[i] =                                                           \
          state->d1[i] * state->w1[i] + state->d2[i] * state->w2[i] + value;   \
      value =                                                                  \
          state->A[i] * (state->w0[i] + 2.0f * state->w1[i] + state->w2[i]);   \
      state->w2[i] = state->w1[i];                                             \
      state->w1[i] = state->w0[i];                                             \
    }                                                                          \
    return value;                                                              \
  }

#define NONUMPY_FILTER_BW_HP_RUN_DEFINE(ORDER)                                 \
  NONUMPY_FILTER_RUN_SIG(NONUMPY_FILTER_NAME_BW_HIGH_PASS, ORDER) {            \
    int i;                                                                     \
    for (i = 0; i < (ORDER / 2); ++i) {                                        \
      state->w0[i] =                                                           \
          state->d1[i] * state->w1[i] + state->d2[i] * state->w2[i] + value;   \
      value =                                                                  \
          state->A[i] * (state->w0[i] - 2.0f * state->w1[i] + state->w2[i]);   \
      state->w2[i] = state->w1[i];                                             \
      state->w1[i] = state->w0[i];                                             \
    }                                                                          \
    return value;                                                              \
  }

NONUMPY_FILTER_BW_LP_RUN_DEFINE(2)
NONUMPY_FILTER_BW_LP_RUN_DEFINE(4)
NONUMPY_FILTER_BW_LP_RUN_DEFINE(6)
NONUMPY_FILTER_BW_LP_RUN_DEFINE(8)
NONUMPY_FILTER_BW_LP_RUN_DEFINE(10)

NONUMPY_FILTER_BW_HP_RUN_DEFINE(2)
NONUMPY_FILTER_BW_HP_RUN_DEFINE(4)
NONUMPY_FILTER_BW_HP_RUN_DEFINE(6)
NONUMPY_FILTER_BW_HP_RUN_DEFINE(8)
NONUMPY_FILTER_BW_HP_RUN_DEFINE(10)
