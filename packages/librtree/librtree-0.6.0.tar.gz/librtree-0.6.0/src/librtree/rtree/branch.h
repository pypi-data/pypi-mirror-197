/*
  rtree/branch.h
  Copyright (c) J.J. Green 2019
*/

#ifndef RTREE_BRANCH_H
#define RTREE_BRANCH_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdlib.h>

typedef struct branch_t branch_t;

#include <rtree/types.h>
#include <rtree/state.h>
#include <rtree/node.h>
#include <rtree/rect.h>

/*
  The union is either a pointer to the child-node in the tree, or
  if we are at level zero, the id payload.  The latter may as well
  be the size of a pointer.

  The rect is big enough to hold 2 * dims floats, understood to be
  [x0, y0, ..., x1, y1, ...] corresponding to the (hyper-)rectangle
  x0 < x < x1, y0 < y < y1, ..., this must be at the end of the
  struct (since variable).

  For the sake of SSE, we would like the rect member to be 16-byte
  aligned, and this could be done with

    rtree_coord_t alignas(16) rect[];

  but this would force the size of branch_t to be a multiple of 16,
  so for the dimension 2 case with rtree_coord_t a float increases
  branch size from 24 to 32 bytes, essentially increasing the size
  of the tree by 20%.  So we don't do that, and use non-aligned
  variants for SSE load/save (apparently on recent CPUs the penalty
  is pretty small).
*/

struct branch_t
{
  union {
    node_t *child;
    rtree_id_t id;
  };
  rtree_coord_t rect[];
};

size_t branch_sizeof(size_t);
int branch_init(const state_t*, branch_t*);
branch_t* branch_copy(const state_t*, const branch_t*, branch_t*);

/* inline accessors */

inline void branch_set_child(branch_t *branch, node_t *child)
{
  branch->child = child;
}

inline const node_t* branch_get_child(const branch_t *branch)
{
  return branch->child;
}

inline node_t* branch_get_child_mutable(branch_t *branch)
{
  return branch->child;
}

inline void branch_set_id(branch_t *branch, rtree_id_t id)
{
  branch->id = id;
}

inline rtree_id_t branch_get_id(const branch_t *branch)
{
  return branch->id;
}

inline void branch_set_rect(const state_t *state, branch_t *branch,
                            const rtree_coord_t *rect)
{
  rect_copy(state, rect, branch->rect);
}

inline const rtree_coord_t* branch_get_rect(const branch_t *branch)
{
  return branch->rect;
}

inline rtree_coord_t* branch_get_rect_mutable(branch_t *branch)
{
  return branch->rect;
}

#ifdef __cplusplus
}
#endif

#endif
