#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <float.h>
#include <errno.h>

#ifdef HAVE_TGMATH_H
#include <tgmath.h>
#else
#include <math.h>
#endif

#include "rtree/error.h"
#include "rtree/branches.h"

#include "split.h"
#include "bindex.h"

typedef struct
{
  bindex_t *choice, *taken;
  size_t total, minfill, count[2];
  rtree_coord_t area[2], *cover[2];
} partition_t;

typedef struct
{
  size_t n;
  void *branches;
  rtree_coord_t *rect;
  partition_t partition;
} split_t;

/*
  Assign branch i to a partition group, updating the covering
  rectangles, areas, counts
*/

static int split_classify(size_t i, size_t group,
                          const state_t *state, split_t *split)
{
  partition_t *part = &(split->partition);
  branch_t *branch = branches_get(state, split->branches, i);
  const rtree_coord_t *rect = branch_get_rect(branch);

  int err;

  if (((err = bindex_set(part->choice, i, group)) != RTREE_OK) ||
      ((err = bindex_set(part->taken, i, 1)) != RTREE_OK))
    return err;

  if (part->count[group] == 0)
    rect_copy(state, rect, part->cover[group]);
  else
    rect_merge(state, rect, part->cover[group]);

  part->area[group] = rect_spherical_volume(state, part->cover[group]);
  part->count[group]++;

  return RTREE_OK;
}

/*
  Picks two rectangles to be the first (seed) elements of the
  partition groups.  We try to get two which are most-separated
  along any dimension, or overlap least.  In degenerate case we
  may not find such a pair, but this is not fatal.
*/

static int split_seed_linear(const state_t *state, split_t *split)
{
  const size_t
    dims = state_dims(state),
    nbuf = state_branching_factor(state);
  size_t
    greatest_lower[dims],
    least_upper[dims];
  rtree_coord_t width[dims];

  for (size_t dim = 0 ; dim < dims ; dim++)
    {
      greatest_lower[dim] = least_upper[dim] = 0;

      for (size_t i = 1 ; i < nbuf ; i++)
        {
          branch_t
            *b0 = branches_get(state, split->branches, greatest_lower[dim]),
            *b1 = branches_get(state, split->branches, i),
            *b2 = branches_get(state, split->branches, least_upper[dim]);
          const rtree_coord_t
            *r0 = branch_get_rect(b0),
            *r1 = branch_get_rect(b1),
            *r2 = branch_get_rect(b2);

          if (r1[dim] > r0[dim])
            greatest_lower[dim] = i;

          if (r1[dim + dims] < r2[dim + dims])
            least_upper[dim] = i;
        }

      width[dim] = split->rect[dim + dims] - split->rect[dim];
    }

  rtree_coord_t sep_max = -1.0;
  size_t seed0 = 0, seed1 = 0;

  for (size_t dim = 0 ; dim < dims ; dim++)
    {
      branch_t
        *bl = branches_get(state, split->branches, least_upper[dim]),
        *bh = branches_get(state, split->branches, greatest_lower[dim]);
      const rtree_coord_t
        *rl = branch_get_rect(bl),
        *rh = branch_get_rect(bh),
        w = (width[dim] ? width[dim] : 1.0),
        sep = (rh[dim] - rl[dim + dims]) / w;

      if (sep > sep_max)
        {
          seed0 = least_upper[dim];
          seed1 = greatest_lower[dim];
          sep_max = sep;
        }
    }

  if (seed0 != seed1)
    {
      int err;

      if (((err = split_classify(seed0, 0, state, split)) != RTREE_OK) ||
          ((err = split_classify(seed1, 1, state, split)) != RTREE_OK))
        return err;
    }

  return RTREE_OK;
}

/*
  Picks two rectangles to be the first (seed) elements of the
  partition groups.  They are the two that waste the most area
  if convered by a single rectangle.

  Note that this is as implemented in the Guttman-Green version
  quadratic splitting, but is quadratic only in the page-size,
  so I'm not sure if it is rather a "better seeding method"
  developed during the work on quadratic splitting and then not
  back-ported to the linear case.
*/

static int split_seed_quadratic(const state_t *state, split_t *split)
{
  size_t
    dims = state_dims(state),
    total = split->partition.total;
  rtree_coord_t area[total];

  for (size_t i = 0 ; i < total ; i++)
    {
      branch_t *branch = branches_get(state, split->branches, i);
      const rtree_coord_t *rect = branch_get_rect(branch);
      area[i] = rect_spherical_volume(state, rect);
    }

  rtree_coord_t worst = -INFINITY;
  size_t seed0 = 0, seed1 = 0;
  int err;

  for (size_t i = 0 ; i < total - 1 ; i++)
    {
      branch_t *bi = branches_get(state, split->branches, i);
      const rtree_coord_t *ri = branch_get_rect(bi);

      for (size_t j = i + 1 ; j < total ; j++)
        {
          branch_t *bj = branches_get(state, split->branches, j);
          const rtree_coord_t *rj = branch_get_rect(bj);
          rtree_coord_t rect[2 * dims];

          rect_combine(state, ri, rj, rect);

          rtree_coord_t waste =
            rect_spherical_volume(state, rect) - area[i] - area[j];

          if (waste > worst)
            {
              worst = waste;
              seed0 = i;
              seed1 = j;
            }
        }
    }

  if (((err = split_classify(seed0, 1, state, split)) != RTREE_OK) ||
      ((err = split_classify(seed1, 0, state, split)) != RTREE_OK))
    return err;

  return RTREE_OK;
}

/*
  Assign unseeded branches to partition groups, using a cascade of
  conditions (on tie, drop to the next one).
*/

static int split_linear(const state_t *state, split_t *split)
{
  int err;

  if ((err = split_seed_linear(state, split)) != RTREE_OK)
    return err;

  const size_t n = split->n;
  partition_t *part = &(split->partition);
  rtree_coord_t *cover[2], area[2], increase[2];

  if ((err = rects_alloc(state, 2, cover)) != RTREE_OK)
    return err;

  for (size_t i = bindex_first_unset(part->taken) ;
       i <= n ;
       i = bindex_next_unset(part->taken, i + 1))
    {
      if (part->count[0] >= part->total - part->minfill)
        {
          if ((err = split_classify(i, 1, state, split)) != RTREE_OK)
            return err;
          continue;
        }
      else if (part->count[1] >= part->total - part->minfill)
        {
          if ((err = split_classify(i, 0, state, split)) != RTREE_OK)
            return err;
          continue;
        }

      branch_t *branch = branches_get(state, split->branches, i);
      const rtree_coord_t *rect = branch_get_rect(branch);

      for (size_t group = 0 ; group < 2 ; group++)
        {
          if (part->count[group] == 0)
            rect_copy(state, rect, cover[group]);
          else
            rect_combine(state, rect, part->cover[group], cover[group]);

          area[group] = rect_spherical_volume(state, cover[group]);
          increase[group] = area[group] - part->area[group];
        }

      if (increase[0] < increase[1])
        {
          if ((err = split_classify(i, 0, state, split)) != RTREE_OK)
            return err;
        }
      else if (increase[0] > increase[1])
        {
          if ((err = split_classify(i, 1, state, split)) != RTREE_OK)
            return err;
        }
      else if (part->area[0] < part->area[1])
        {
          if ((err = split_classify(i, 0, state, split)) != RTREE_OK)
            return err;
        }
      else if (part->area[0] > part->area[1])
        {
          if ((err = split_classify(i, 1, state, split)) != RTREE_OK)
            return err;
        }
      else if (part->count[0] < part->count[1])
        {
          if ((err = split_classify(i, 0, state, split)) != RTREE_OK)
            return err;
        }
      else
        {
          if ((err = split_classify(i, 1, state, split)) != RTREE_OK)
            return err;
        }
    }

  rects_free(2, cover);

  return RTREE_OK;
}

/*
  Assign non-seeded branches according to the greatest difference in
  area expansion - the rectangle most strongly attracted to one group
  and repelled from the other.

  If one group gets too full (more would force other group to violate
  minimum-fill requirement) then other group gets the rest.  These last
  are the ones that can go in either group most easily.
*/

static int split_quadratic(const state_t *state, split_t *split)
{
  int err;

  if ((err = split_seed_quadratic(state, split)) != RTREE_OK)
    return err;

  partition_t *part = &(split->partition);
  const size_t
    dims = state_dims(state),
    total = part->total,
    minfill = part->minfill,
    *count = part->count;
  rtree_coord_t
    **cover = part->cover,
    *area = part->area;

  while ( (count[0] + count[1] < total) &&
          (count[0] + minfill < total) &&
          (count[1] + minfill < total) )
    {
      rtree_coord_t dg_max = -1;
      size_t group = 0, chosen = 0;

      for (size_t i = bindex_first_unset(part->taken) ;
           i < total ;
           i = bindex_next_unset(part->taken, i + 1))
        {
          branch_t *branch = branches_get(state, split->branches, i);
          const rtree_coord_t *rect = branch_get_rect(branch);
          rtree_coord_t r0[2 * dims], r1[2 * dims];

          rect_combine(state, rect, cover[0], r0);
          rect_combine(state, rect, cover[1], r1);

          const rtree_coord_t
            g0 = rect_spherical_volume(state, r0) - area[0],
            g1 = rect_spherical_volume(state, r1) - area[1];
          rtree_coord_t dg = g1 - g0;

          size_t putative;
          if (dg >= 0)
            putative = 0;
          else
            {
              putative = 1;
              dg *= -1;
            }

          if (dg > dg_max)
            {
              dg_max = dg;
              group = putative;
              chosen = i;
            }
        }

      if ((err = split_classify(chosen, group, state, split)) != RTREE_OK)
        return err;
    }

  if (count[0] + count[1] < total)
    {
      const size_t group = (count[0] + minfill < total) ? 0 : 1;

      for (size_t i = bindex_first_unset(part->taken) ;
           i < total ;
           i = bindex_next_unset(part->taken, i + 1))
        {
          if ((err = split_classify(i, group, state, split)) != RTREE_OK)
            return err;
        }
    }

  return RTREE_OK;
}

/*
  The splitting method described by D. Green in "An Implementation and
  Performance Analysis of Spatial Data Access Methods", 1989
*/

/*
  for the sort pair, id will be much smaller that UINT16_MAX, but we
  choose it to be the same size as rtree_coord_t for alignment
*/

typedef struct
{
#if SIZEOF_RTREE_COORD_T == 2
  uint16_t id;
#elif SIZEOF_RTREE_COORD_T == 4
  uint32_t id;
#elif SIZEOF_RTREE_COORD_T == 8
  uint64_t id;
#else
#error rtree_id_t size not handled
#endif
  rtree_coord_t min;
} pair_t;

static int pair_compare(const void *va, const void *vb)
{
  const pair_t *a = va, *b = vb;
  rtree_coord_t ma = a->min, mb = b->min;

  if (ma > mb)
    return 1;
  else if (ma < mb)
    return -1;
  else
    return 0;
}

static int split_greene(const state_t *state, split_t *split)
{
  int err;

  /* dimension on which to split */

  const size_t dims = state_dims(state);
  size_t axis = dims;

  /* quadratic seeds */

  {
    if ((err = split_seed_quadratic(state, split)) != RTREE_OK)
      return err;

    branch_t
      *b0 = branches_get(state, split->branches, 0),
      *b1 = branches_get(state, split->branches, 1);
    const rtree_coord_t
      *r0 = branch_get_rect(b0),
      *r1 = branch_get_rect(b1);

    rtree_coord_t sep_best = -INFINITY;

    for (size_t dim = 0 ; dim < dims ; dim++)
      {
        rtree_coord_t
          s0 = r0[dim] - r1[dim + dims],
          s1 = r1[dim] - r0[dim + dims],
          s2 = fmax(s0, s1),
          n0 = fmin(r0[dim], r1[dim]),
          n1 = fmax(r0[dim + dims], r1[dim + dims]),
          n2 = n1 - n0,
          sep = s2 / n2;

        if (sep > sep_best)
          {
            sep_best = sep;
            axis = dim;
          }
      }
  }

  if (axis == dims)
    return RTREE_ERR_SPLIT;

  /* order by lower boumd in this dimension */

  partition_t *part = &(split->partition);
  const size_t total = part->total;
  pair_t pairs[total];

  for (size_t i = 0 ; i < total ; i++)
    {
      branch_t *b = branches_get(state, split->branches, i);
      const rtree_coord_t *r = branch_get_rect(b);
      pairs[i].id = i;
      pairs[i].min = r[axis];
    }

  qsort(pairs, total, sizeof(pair_t), pair_compare);

  /* lower part to group 0 */

  size_t half = (total + 1) >> 1;

  for (size_t i = 0 ; i < half ; i++)
    if ((err = split_classify(pairs[i].id, 0, state, split)) != RTREE_OK)
      return err;

  if (total & 1)
    {
      /* tiebreak in the odd case */

      const branch_t *b = branches_get(state, split->branches, pairs[0].id);
      rtree_coord_t r0[2 * dims], r1[2 * dims];

      rect_copy(state, branch_get_rect(b), r0);

      for (size_t i = 1 ; i < half ; i++)
        {
          b = branches_get(state, split->branches, pairs[i].id);
          rect_merge(state, branch_get_rect(b), r0);
        }

      b = branches_get(state, split->branches, pairs[half + 1].id);
      rect_copy(state, branch_get_rect(b), r1);

      for (size_t i = half + 2 ; i < total ; i++)
        {
          b = branches_get(state, split->branches, pairs[i].id);
          rect_merge(state, branch_get_rect(b), r1);
        }

      rtree_coord_t
        v0 = rect_volume(state, r0),
        v1 = rect_volume(state, r1);

      b = branches_get(state, split->branches, pairs[half].id);
      const rtree_coord_t *rh = branch_get_rect(b);

      rect_merge(state, rh, r0);
      rect_merge(state, rh, r1);

      rtree_coord_t
        v0p = rect_volume(state, r0),
        v1p = rect_volume(state, r1);

      size_t group = (v0p - v0 < v1p - v1) ? 0 : 1;

      if ((err = split_classify(pairs[half].id, group, state, split)) != RTREE_OK)
        return err;

      for (size_t i = half + 1 ; i < total ; i++)
        if ((err = split_classify(pairs[i].id, 1, state, split)) != RTREE_OK)
          return err;
    }
  else
    {
      /* total is even, no tiebreaker needed */

      for (size_t i = half ; i < total ; i++)
        if ((err = split_classify(pairs[i].id, 1, state, split)) != RTREE_OK)
          return err;
    }

  return RTREE_OK;
}


static int split_assign(const state_t *state, split_t *split)
{
  switch (state_split(state))
    {
    case RTREE_SPLIT_LINEAR:
      return split_linear(state, split);
    case RTREE_SPLIT_QUADRATIC:
      return split_quadratic(state, split);
    case RTREE_SPLIT_GREENE:
      return split_greene(state, split);
    default:
      return RTREE_ERR_NOSUCHSPLIT;
    }
}

/*
  This actually performs the split, the input node is reset, a new
  node is created, and the branches in the split struct are distributed
  between these nodes.  So the input node is half-emptied and the new
  node is half-filled.
*/

static node_t* split_load(const state_t *state, node_t *node, split_t *split)
{
  const node_level_t level = node_level(node);

  if (node_init(state, node) != RTREE_OK)
    return NULL;

  node_t *new_node;

  if ((new_node = node_new(state)) == NULL)
    return NULL;

  node_set_level(node, level);
  node_set_level(new_node, level);

  const partition_t *part = &(split->partition);
  const size_t n = split->n;

  for (size_t i = 0 ; i <= n ; i++)
    {
      branch_t *branch = branches_get(state, split->branches, i);
      size_t group = bindex_get(part->choice, i);
      node_t *result;

      switch (group)
        {
        case 0:
          result = node_add_branch(state, node, branch);
          if (result != node)
            goto cleanup_load;
          break;
        case 1:
          result = node_add_branch(state, new_node, branch);
          if (result != new_node)
            goto cleanup_load;
          break;
        default:
          goto cleanup_load;
        }
    }

  return new_node;

 cleanup_load:

  node_destroy(state, new_node);

  return NULL;
}

static node_t* split_part(const state_t *state, node_t *node, split_t *split)
{
  partition_t *part = &(split->partition);
  const size_t n = split->n;
  node_t *new_node = NULL;

  part->count[0] = part->count[1] = 0;
  part->total = n + 1;
  part->minfill = n / 2;

  if (rects_alloc(state, 2, part->cover) == RTREE_OK)
    {
      if ((part->choice = bindex_new(n + 1)) != NULL)
        {
          if ((part->taken = bindex_new(n + 1)) != NULL)
            {
              if (split_assign(state, split) == RTREE_OK)
                {
                  new_node = split_load(state, node, split);
                }
              bindex_destroy(part->taken);
            }
          bindex_destroy(part->choice);
        }
      rects_free(2, part->cover);
    }

  return new_node;
}

/* Get the covering rectangle */

static node_t* split_cover(const state_t *state, node_t *node, split_t *split)
{
  node_t *new_node = NULL;
  rtree_coord_t split_rect[2 * state_dims(state)];

  split->rect = split_rect;

  branch_t *b = branches_get(state, split->branches, 0);
  const rtree_coord_t *r;

  if ((r = branch_get_rect(b)) != NULL)
    {
      rect_copy(state, r, split->rect);

      int err = 0;

      for (size_t i = 0 ; i <= split->n  ; i++)
        {
          b = branches_get(state, split->branches, 1);
          if ((r = branch_get_rect(b)) == NULL)
            err++;
          rect_merge(state, r, split->rect);
        }

      if (err == 0)
        new_node = split_part(state, node, split);
    }

  split->rect = NULL;

  return new_node;
}

node_t* split_node(const state_t *state, node_t *node, branch_t *branch)
{
  void *branches;
  node_t *new_node = NULL;

  if ((branches = node_get_branches(node)) != NULL)
    {
      split_t split;
      const size_t
        n = split.n = state_branching_factor(state),
        branch_size = state_branch_size(state);
      char split_branches[(n + 1) * branch_size];

      split.branches = split_branches;

      for (size_t i = 0 ; i < n ; i++)
        {
          branch_t *b = branches_get(state, branches, i);
          branches_set(state, split.branches, i, b);
        }

      branches_set(state, split.branches, n, branch);

      if (branch_init(state, branch) == RTREE_OK)
        new_node = split_cover(state, node, &split);

      split.branches = NULL;
    }

  return new_node;
}
