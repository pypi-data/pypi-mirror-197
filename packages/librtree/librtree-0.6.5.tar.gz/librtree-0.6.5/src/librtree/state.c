#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "rtree/state.h"
#include "rtree/branch.h"
#include "rtree/node.h"

#include "page.h"
#include "constants.h"
#include "spvol.h"

#include <errno.h>
#include <string.h>

#ifdef HAVE_TGMATH_H
#include <tgmath.h>
#else
#include <math.h>
#endif

#ifdef HAVE_UNISTD_H
#include <unistd.h>
#endif


#define SPLIT_MASK ((1 << 2) - 1)
#define SPLIT_SHIFT 0

static state_flags_t flags_split(state_flags_t flags)
{
  return (flags << SPLIT_SHIFT) & SPLIT_MASK;
}

state_flags_t state_split(const state_t *state)
{
  return flags_split(state->flags);
}

#define NODE_PAGE_MASK ((1 << 8) - 1)
#define NODE_PAGE_SHIFT 2

static state_flags_t flags_node_page(state_flags_t flags)
{
  return (flags >> NODE_PAGE_SHIFT) & NODE_PAGE_MASK;
}

state_flags_t state_node_page(const state_t *state)
{
  return flags_node_page(state->flags);
}

/*
  For dim 2 with floats and 4K page-size we find that a node-page
  of 8 gives reasonable performance; here we guess a formula which
  scales the way you would expect and choose the parameter 64 so that
  it gives  8 in the dim 2 float case.  No doubt one could do better
  with a case-by-case optimisation, but there are a lot of cases to
  consider, look at that later ...
*/

static size_t node_page_default(size_t dims, size_t npg, size_t psz)
{
  if (npg != 0) return npg;
  size_t guess = psz / (dims * SIZEOF_RTREE_COORD_T * 64);
  return guess ? guess : 1;
}

state_t* state_new(size_t dims, state_flags_t flags)
{
  if (dims == 0)
    {
      errno = EDOM;
      return NULL;
    }

  size_t psz;

  if (page_size(&psz) != 0)
    return NULL;

  const size_t
    npg = node_page_default(dims, flags_node_page(flags), psz),
    nsz = psz / npg,
    bsz = branch_sizeof(2 * dims),
    factor = node_num_branch(nsz, bsz);

  if (factor < 2)
    {
      errno = EINVAL;
      return NULL;
    }

  double volume;

  if (spvol(dims, &volume) != 0)
    {
      errno = EDOM;
      return NULL;
    }

  state_t *state = malloc(sizeof(state_t));

  if (state == NULL)
    {
      errno = ENOMEM;
      return NULL;
    }

  state->dims = dims;
  state->factor = factor;
  state->size.page = psz;
  state->size.branch = bsz;
  state->size.node = nsz;
  state->volume = volume;
  state->flags = flags;
  state->rectf.spherical_volume = rectf_spherical_volume(dims);
  state->rectf.combine = rectf_combine(dims);

  return state;
}

state_t* state_clone(const state_t *src)
{
  state_t *dest;

  if ((dest = malloc(sizeof(state_t))) != NULL)
    {
      memcpy(dest, src, sizeof(state_t));
      return dest;
    }

  errno = ENOMEM;
  return NULL;
}

void state_destroy(state_t *state)
{
  free(state);
}

bool state_identical(const state_t *a, const state_t *b)
{
  if (a && b)
    {
      return
        (state_dims(a) == state_dims(b)) &&
        (state_page_size(a) == state_page_size(b)) &&
        (state_node_size(a) == state_node_size(b)) &&
        (state_rect_size(a) == state_rect_size(b)) &&
        (state_branching_factor(a) == state_branching_factor(b));
    }

  return ! (a || b);
}

extern size_t state_dims(const state_t*);
extern size_t state_page_size(const state_t*);
extern size_t state_node_size(const state_t*);
extern size_t state_rect_size(const state_t*);
extern size_t state_branch_size(const state_t*);
extern size_t state_branching_factor(const state_t*);
extern double state_unit_sphere_volume(const state_t*);
extern size_t state_bytes(const state_t*);
extern rtree_coord_t state_rsv(const state_t*, const rtree_coord_t*);
extern void state_rc(const state_t*,
                     const rtree_coord_t*,
                     const rtree_coord_t*,
                     rtree_coord_t*);
