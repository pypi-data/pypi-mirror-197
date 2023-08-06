/*
  rtree/state.h

  This structure is open, but we only access it via accessors,
  often trivial; these are implemented as (C99 standard) inline
  functions, so there's no performance penalty.

  Copyright (c) J.J. Green 2019
*/

#ifndef RTREE_STATE_H
#define RTREE_STATE_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

#include <rtree/types.h>
#include <rtree/rectf.h>

typedef uint32_t state_flags_t;

typedef struct
{
  size_t dims, factor;
  rtree_coord_t volume;
  struct {
    size_t page, branch, node;
  } size;
  struct {
    rectf_rsv_t *spherical_volume;
    rectf_rc_t *combine;
  } rectf;
  state_flags_t flags;
} state_t;

#define RTREE_DEFAULT 0

#define RTREE_SPLIT_QUADRATIC 0
#define RTREE_SPLIT_LINEAR 1
#define RTREE_SPLIT_GREENE 2

#define RTREE_NODE_PAGE(n) ((n) << 2)

state_t* state_new(size_t, state_flags_t);
state_t* state_clone(const state_t*);
void state_destroy(state_t*);
state_flags_t state_split(const state_t*);
state_flags_t state_node_page(const state_t*);
bool state_identical(const state_t*, const state_t*);

inline rtree_coord_t state_rsv(const state_t *state, const rtree_coord_t *rect)
{
  return state->rectf.spherical_volume(state->dims, rect) * state->volume;
}

inline void state_rc(const state_t *state,
                     const rtree_coord_t *rect0,
                     const rtree_coord_t *rect1,
                     rtree_coord_t *rect2)
{
  state->rectf.combine(state->dims, rect0, rect1, rect2);
}

inline size_t state_dims(const state_t *state)
{
  return state->dims;
}

inline size_t state_branch_size(const state_t *state)
{
  return state->size.branch;
}

inline size_t state_page_size(const state_t *state)
{
  return state->size.page;
}

inline size_t state_node_size(const state_t *state)
{
  return state->size.node;
}

inline size_t state_rect_size(const state_t *state)
{
  return state_dims(state) * 2 * sizeof(rtree_coord_t);
}

inline size_t state_branching_factor(const state_t *state)
{
  return state->factor;
}

inline double state_unit_sphere_volume(const state_t *state)
{
  return state->volume;
}

inline size_t state_bytes(const state_t *state)
{
  return (state ? sizeof(state_t) : 0);
}

#ifdef __cplusplus
}
#endif

#endif
