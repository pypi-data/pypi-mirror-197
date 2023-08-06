#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "rtree/rectf.h"

#ifdef HAVE_TGMATH_H
#include <tgmath.h>
#else
#include <math.h>
#endif

#ifdef HAVE_XMMINTRIN_H
#include <xmmintrin.h>
#endif

#ifdef HAVE_IMMINTRIN_H
#include <immintrin.h>
#endif

/*
  rect_spherical_volume has some simplifications for small dimensions
  (one need not call pow(), for example), and it gets called a lot so
  worth selecting which to use just the once.
*/

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wunused-parameter"

rtree_coord_t rectf_rsv1(size_t dims, const rtree_coord_t *rect)
{
  return 0.5 * fabs(rect[1] - rect[0]);
}

rtree_coord_t rectf_rsv2(size_t dims, const rtree_coord_t *rect)
{
  rtree_coord_t
    hx1 = rect[2] - rect[0],
    hx2 = rect[3] - rect[1],
    r2 = hx1 * hx1 + hx2 * hx2;

  return 0.25 * r2;
}

#pragma GCC diagnostic pop

rtree_coord_t rectf_rsvd(size_t dims, const rtree_coord_t *rect)
{
  rtree_coord_t
    hx = rect[dims] - rect[0],
    r2 = hx * hx;

  for (size_t i = 1 ; i < dims ; i++)
    {
      hx = rect[i + dims] - rect[i];
      r2 += hx * hx;
    }

  return pow(0.25 * r2, 0.5 * dims);
}

rectf_rsv_t* rectf_spherical_volume(size_t dims)
{
  switch (dims)
    {
    case 1:
      return rectf_rsv1;
    case 2:
      return rectf_rsv2;
    default:
      return rectf_rsvd;
    }
}

/*
  rect_combine is performance-critical, and we use the same trick
  for cases where the entire rectangle fits in a wide register:
  the 128-bit register (SSE2) in the dim-2 float case, the 256
  register (AVX) in the dim-3, -4 float and dim-2 double case. for
  the first, We XOR with the "sign-mask" { 0, 0, -0, -0 } to sign
  change the last two values, then find the min, then XOR again.
  The result is the min of the bottom two values, the max of the
  top two.

  The dim-4 float and dim-2 double cases are similar, the dim-3
  float  version is the trickiest since we need to load 6 floats
  into an 8-float register, so we need a mask (which is an AVX
  facility).
*/

void rectf_rcd(size_t dims,
               const rtree_coord_t *rect0,
               const rtree_coord_t *rect1,
               rtree_coord_t *rect2)
{
  for (size_t i = 0 ; i < dims ; i++)
    {
      const size_t j = i + dims;
      const rtree_coord_t
        x0 = rect0[i], x1 = rect1[i],
        y0 = rect0[j], y1 = rect1[j];

      rect2[i] = fmin(x0, x1);
      rect2[j] = fmax(y0, y1);
    }
}

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wunused-parameter"

#if SIZEOF_RTREE_COORD_T == 4

#ifdef HAVE_SSE2

void rectf_rc2(size_t dims,
               const rtree_coord_t *rect0,
               const rtree_coord_t *rect1,
               rtree_coord_t *rect2)
{
  const __m128
    sm = { 0.0f, 0.0f, -0.0f, -0.0f },
    sr0 = _mm_loadu_ps(rect0),
    sr1 = _mm_loadu_ps(rect1),
    srmin = _mm_min_ps(_mm_xor_ps(sm, sr0), _mm_xor_ps(sm, sr1)),
    res = _mm_xor_ps(sm, srmin);

  _mm_storeu_ps(rect2, res);
}


#endif

#ifdef HAVE_AVX

void rectf_rc3(size_t dims,
               const rtree_coord_t *rect0,
               const rtree_coord_t *rect1,
               rtree_coord_t *rect2)
{
  const __m256i
    mask = _mm256_setr_epi32(-1, -1, -1, -1, -1, -1, 0, 0);
  const __m256
    sm = { 0.0f, 0.0f, 0.0f, -0.0f, -0.0f, -0.0f, 0.0f, 0.0f },
    sr0 = _mm256_maskload_ps(rect0, mask),
    sr1 = _mm256_maskload_ps(rect1, mask),
    srmin = _mm256_min_ps(_mm256_xor_ps(sm, sr0), _mm256_xor_ps(sm, sr1)),
    res = _mm256_xor_ps(sm, srmin);

  _mm256_maskstore_ps(rect2, mask, res);
}

void rectf_rc4(size_t dims,
               const rtree_coord_t *rect0,
               const rtree_coord_t *rect1,
               rtree_coord_t *rect2)
{
  const __m256
    sm = { 0.0f, 0.0f, 0.0f, 0.0f, -0.0f, -0.0f, -0.0f, -0.0f },
    sr0 = _mm256_loadu_ps(rect0),
    sr1 = _mm256_loadu_ps(rect1),
    srmin = _mm256_min_ps(_mm256_xor_ps(sm, sr0), _mm256_xor_ps(sm, sr1)),
    res = _mm256_xor_ps(sm, srmin);

  _mm256_storeu_ps(rect2, res);
}

#endif

#elif SIZEOF_RTREE_COORD_T == 8

#ifdef HAVE_AVX

void rectf_rc2(size_t dims,
               const rtree_coord_t *rect0,
               const rtree_coord_t *rect1,
               rtree_coord_t *rect2)
{
  const __m256d
    sm = { 0.0, 0.0, -0.0, -0.0 },
    sr0 = _mm256_loadu_pd(rect0),
    sr1 = _mm256_loadu_pd(rect1),
    srmin = _mm256_min_pd(_mm256_xor_pd(sm, sr0), _mm256_xor_pd(sm, sr1)),
    res = _mm256_xor_pd(sm, srmin);

  _mm256_storeu_pd(rect2, res);
}

#endif

#else
#error "strange size for rtree_coord_t"
#endif

#pragma GCC diagnostic pop

rectf_rc_t* rectf_combine(size_t dims)
{
  switch (dims)
    {

#if SIZEOF_RTREE_COORD_T == 4
# ifdef HAVE_SSE2
    case 2: return rectf_rc2;
# endif
# ifdef HAVE_AVX
    case 3: return rectf_rc3;
    case 4: return rectf_rc4;
# endif
#elif SIZEOF_RTREE_COORD_T == 8
# ifdef HAVE_AVX
    case 2: return rectf_rc2;
# endif
#else
# error "strange size for rtree_coord_t"
#endif

    default: return rectf_rcd;
    }
}
