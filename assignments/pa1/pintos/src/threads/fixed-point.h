#ifndef THREADS_FIXED_POINT_H
#define THREADS_FIXED_POINT_H

#include <stdint.h>

/* Signed 17.14 arithmetic.  Results must fit in fixed_t, and divisors
   must be nonzero.  Intermediate products use 64 bits. */
typedef int32_t fixed_t;

#define FP_SHIFT 14
#define FP_SCALE (1 << FP_SHIFT)

static inline fixed_t
fp_from_int (int n)
{
  return (fixed_t) ((int64_t) n * FP_SCALE);
}

/* Convert toward zero, including for negative values. */
static inline int
fp_to_int (fixed_t x)
{
  return x / FP_SCALE;
}

/* Round to nearest, with exact halves rounded away from zero. */
static inline int
fp_round (fixed_t x)
{
  int64_t value = x;
  value += value >= 0 ? FP_SCALE / 2 : -FP_SCALE / 2;
  return (int) (value / FP_SCALE);
}

static inline fixed_t
fp_add (fixed_t x, fixed_t y)
{
  return (fixed_t) ((int64_t) x + y);
}

static inline fixed_t
fp_sub (fixed_t x, fixed_t y)
{
  return (fixed_t) ((int64_t) x - y);
}

static inline fixed_t
fp_add_int (fixed_t x, int n)
{
  return (fixed_t) ((int64_t) x + (int64_t) n * FP_SCALE);
}

static inline fixed_t
fp_sub_int (fixed_t x, int n)
{
  return (fixed_t) ((int64_t) x - (int64_t) n * FP_SCALE);
}

static inline fixed_t
fp_mul (fixed_t x, fixed_t y)
{
  return (fixed_t) ((int64_t) x * y / FP_SCALE);
}

static inline fixed_t
fp_div (fixed_t x, fixed_t y)
{
  return (fixed_t) ((int64_t) x * FP_SCALE / y);
}

static inline fixed_t
fp_mul_int (fixed_t x, int n)
{
  return (fixed_t) ((int64_t) x * n);
}

static inline fixed_t
fp_div_int (fixed_t x, int n)
{
  return (fixed_t) ((int64_t) x / n);
}

/* Return 100 times X, rounded to nearest without overflowing while
   scaling the stored value. */
static inline int
fp_round_100 (fixed_t x)
{
  int64_t value = (int64_t) x * 100;
  value += value >= 0 ? FP_SCALE / 2 : -FP_SCALE / 2;
  return (int) (value / FP_SCALE);
}

#endif /* threads/fixed-point.h */
