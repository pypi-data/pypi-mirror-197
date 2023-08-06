#pragma once

#ifdef NONUMPY_FLOAT_32
#define NONUMPY_FLOAT_T float
#endif

#ifdef NONUMPY_FLOAT_64
#define NONUMPY_FLOAT_T double
#endif

#ifndef NONUMPY_FLOAT_T
#define NONUMPY_FLOAT_T float
#endif
