#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "rtree/rect.h"
#include "rtree/error.h"

#ifdef HAVE_TGMATH_H
#include <tgmath.h>
#else
#include <math.h>
#endif

#ifdef HAVE_FEATURES_H
#include <features.h>
#endif

#include <string.h>
#include <errno.h>

int rect_init(const state_t *state, rtree_coord_t *rect)
{
  if (rect == NULL)
    return RTREE_ERR_INVAL;

#ifdef __STDC_IEC_559__

  memset(rect, 0, state_rect_size(state));

#else

  const size_t dims = state_dims(state);

  for (size_t i = 0 ; i < 2 * dims ; i++)
    rect[i] = 0;

#endif

  return RTREE_OK;
}

bool rect_intersect(const state_t *state,
                    const rtree_coord_t *a, const rtree_coord_t *b)
{
  const size_t dims = state_dims(state);

  for (size_t dim = 0 ; dim < dims ; dim++)
    {
      const size_t
        low = dim,
        high = dim + dims;

      if ((a[high] < b[low]) || (a[low] > b[high]))
        return false;
    }

  return true;
}

rtree_coord_t rect_volume(const state_t *state, const rtree_coord_t *rect)
{
  const size_t dims = state_dims(state);
  rtree_coord_t v = rect[dims] - rect[0];

  for (size_t i = 1 ; i < dims ; i++)
    v *= (rect[dims + i] - rect[i]);

  return v;
}

rtree_coord_t rect_spherical_volume(const state_t *state,
                                    const rtree_coord_t *rect)
{
  return state_rsv(state, rect);
}

void rect_copy(const state_t *state, const rtree_coord_t *src,
               rtree_coord_t *dest)
{
  memcpy(dest, src, state_rect_size(state));
}


void rect_combine(const state_t *state,
                  const rtree_coord_t *restrict rect0,
                  const rtree_coord_t *restrict rect1,
                  rtree_coord_t *restrict rect2)
{
  state_rc(state, rect0, rect1, rect2);
}

void rect_merge(const state_t *state,
                const rtree_coord_t *rect0,
                rtree_coord_t *rect1)
{
  state_rc(state, rect0, rect1, rect1);
}

bool rect_identical(const state_t *state,
                    const rtree_coord_t *rect0,
                    const rtree_coord_t *rect1)
{
  for (size_t i = 0 ; i < 2 * state_dims(state) ; i++)
    if (rect0[i] != rect1[i]) return false;
  return true;
}

/*
  Allocates n rectangles (as rtree_coord_t*) and assigns them to the
  elements of the array rects, which should already be allocated (so
  one would pass 'array' declared as rtree_coord_t *array[2], for
  example).
*/

int rects_alloc(const state_t *state, size_t n, rtree_coord_t **rects)
{
  const size_t
    dims = state_dims(state),
    rect_size = state_rect_size(state);
  rtree_coord_t *floats;

  if ((floats = calloc(n, rect_size)) == NULL)
    return RTREE_ERR_NOMEM;

  *rects = floats;

  for (size_t i = 1 ; i < n ; i++)
    rects[i] = floats + 2 * i * dims;

  return RTREE_OK;
}

void rects_free(size_t n, rtree_coord_t **rects)
{
  free(*rects);

  for (size_t i = 0 ; i < n ; i++)
    rects[i] = NULL;
}
