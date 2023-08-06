#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "rtree/node.h"
#include "rtree/branches.h"
#include "rtree/rect.h"
#include "rtree/error.h"

#include "split.h"

#include <stdbool.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>
#include <errno.h>

#ifdef HAVE_TGMATH_H
#include <tgmath.h>
#else
#include <math.h>
#endif

/*
  how many branches can we fit at the end of a node of the specified
  size, typically this will be a fraction of a page size.  This does
  not take a state_t* as argument since it is used to initialise it.
*/

size_t node_num_branch(size_t node_size, size_t branch_size)
{
  return (node_size - offsetof(node_t, branches)) / branch_size;
}

static branch_t* node_get_branch(const state_t *state,
                                 const node_t *node, size_t i)
{
  return branches_get(state, (void*)node->branches, i);
}

int node_init(const state_t *state, node_t *node)
{
  node->count = 0;
  node->level = 0;

  const size_t n = state_branching_factor(state);

  for (size_t i = 0 ; i < n ; i++)
    {
      int err = branch_init(state, node_get_branch(state, node, i));
      if (err != RTREE_OK)
        return err;
    }

  return RTREE_OK;
}

node_t* node_new(const state_t *state)
{
  node_t *node;

  if ((node = malloc(state_node_size(state))) == NULL)
    errno = ENOMEM;
  else
    {
      if (node_init(state, node) == 0)
        return node;

      free(node);
    }

  return NULL;
}

/*
  Rather than iterate over the branches, we here recurse: this is so
  that we can do all of the work that we need to do but leave the
  allocation in node_clone() until last, and only then call ourself.
  In case of failure we back out with node_destroy() return error and
  our recursive parents do the same, so cleaning up after ourselves.
*/

static int node_clone_children(const state_t *state,
                               const node_t *src, node_t *dest,
                               size_t i)
{
  if (i >= node_count(src)) return RTREE_OK;

  const branch_t *src_branch;
  if ((src_branch = node_get_branch(state, src, i)) == NULL)
    return RTREE_ERR_GETBRANCH;

  branch_t *dest_branch;
  if ((dest_branch = node_get_branch(state, dest, i)) == NULL)
    return RTREE_ERR_GETBRANCH;

  const node_t *src_child;
  if ((src_child = branch_get_child(src_branch)) == NULL)
    return RTREE_ERR_GETCHILD;

  node_t *dest_child;
  if ((dest_child = node_clone(state, src_child)) == NULL)
    return RTREE_ERR_NODECLONE;

  int err = node_clone_children(state, src, dest, i + 1);
  if (err != RTREE_OK)
    {
      node_destroy(state, dest_child);
      return err;
    }

  branch_set_child(dest_branch, dest_child);

  return RTREE_OK;
}

/*
  To clone a leaf node (and its branches), we just need to copy,
  but for internal nodes we need to replace the branches' pointers
  to node by the pointer to its clone; so recursion.
*/

node_t* node_clone(const state_t *state, const node_t *src)
{
  const size_t node_size = state_node_size(state);
  node_t *dest;

  if ((dest = malloc(node_size)) == NULL)
    {
      errno = ENOMEM;
      return NULL;
    }

  memcpy(dest, src, node_size);
  if (node_level(src) > 0)
    {
      if (node_clone_children(state, src, dest, 0) != 0)
        {
          free(dest);
          return NULL;
        }
    }

  return dest;
}

/*
  For the destroy, we go a bit overboard checking that everything
  is non-NULL, this since we expect it to be used backing out on
  failure, and that failure might be a bad alloc.
*/

void node_destroy(const state_t *state, node_t *node)
{
  if (node != NULL)
    {
      if (node_level(node) > 0)
        {
          for (size_t i = 0 ; i < node_count(node) ; i++)
            {
              branch_t *branch;
              if ((branch = node_get_branch(state, node, i)) != NULL)
                {
                  node_t *child;
                  if ((child = branch_get_child_mutable(branch)) != NULL)
                    node_destroy(state, child);
                }
            }
        }
      free(node);
    }
}

/*
  Apply the function f to each branch of the specified node, even if
  that branch is empty (i.e., has no child).  The function f should
  return zero to indicate success, if a non-zero value is returned
  then the iteration is aborted and that value returned.
*/

int node_branch_each(const state_t *state, const node_t *node,
                     nbe_cb_t *f, void *arg)
{
  for (size_t i = 0 ; i < node_count(node) ; i++)
    {
      int err;
      if ((err = f(state, node_get_branch(state, node, i), arg)) != 0)
        return err;
    }
  return RTREE_OK;
}

/*
  a bit like node_branch each, but applied to all nodes at the specified
  level; a breadth-first iterate if you will
*/

int node_branch_each_level(const state_t *state, const node_t *node,
                           node_level_t level, nbe_cb_t *f, void *arg)
{
  const node_level_t this_level = node_level(node);

  if (this_level > level)
    {
      for (size_t i = 0 ; i < node_count(node) ; i++)
        {
          branch_t *branch = node_get_branch(state, node, i);
          const node_t *child = branch_get_child(branch);
          int err = node_branch_each_level(state, child, level, f, arg);
          if (err != 0) return err;
        }
    }
  else if (this_level == level)
    {
      for (size_t i = 0 ; i < node_count(node) ; i++)
        {
          branch_t *branch = node_get_branch(state, node, i);
          int err = f(state, branch, arg);
          if (err != 0) return err;
        }
    }
  return RTREE_OK;
}

size_t node_bytes(const state_t *state, const node_t *node)
{
  if (node == NULL)
    return 0;

  if (node_level(node) == 0)
    return state_node_size(state);

  size_t bytes = state_node_size(state);

  for (size_t i = 0 ; i < node_count(node) ; i++)
    {
      branch_t *branch = node_get_branch(state, node, i);
      const node_t *child = branch_get_child(branch);
      bytes += node_bytes(state, child);
    }

  return bytes;
}

/*
  remove branch i from node, to maintain contiguousness, we copy the
  final branch to i (we don't need to do that if it is the final branch
  of course, indeed, since we use memcpy we shouldn't do that). Note
  that this handles the case when there is only one branch.
*/

int node_detach_branch(const state_t *state, node_t *node, size_t i)
{
  branch_t *branch;

  if ((i >= node_count(node)) ||
      ((branch = node_get_branch(state, node, i)) == NULL))
    return RTREE_ERR_GETBRANCH;

  if (i + 1 != node_count(node))
    {
      branch_t *branch_end = node_get_branch(state, node, node_count(node) - 1);

      if (branch_end == NULL)
        return RTREE_ERR_GETBRANCH;

      if (branch_copy(state, branch_end, branch) == NULL)
        return RTREE_ERR_NOMEM;
    }

  node_count_decrement(node);

  return RTREE_OK;
}

static node_t* node_split(const state_t *state, node_t *node, branch_t *branch)
{
  return split_node(state, node, branch);
}

/*
  add branch to node, which may split the node: if so the new node
  argumemnt is returned, so comparing the node argument and return
  value is the way to detect that splitting has occured.
*/

node_t* node_add_branch(const state_t *state, node_t *node, branch_t *branch)
{
  if (node_count(node) < state_branching_factor(state))
    {
      branch_t *b;

      if ((b = node_get_branch(state, node, node_count(node))) == NULL)
        return NULL;

      branch_copy(state, branch, b);
      node_count_increment(node);

      return node;
    }

  return node_split(state, node, branch);
}

/*
  Pick a branch.  Pick the one that will need the smallest increase
  in volume to accomodate the new (hyper-)rectangle.  This will result
  in the least total volume for the covering rectangles in the current
  node.  In case of a tie, pick the one which was smaller before, to
  get the best resolution when searching.
*/

static int node_pick_branch(const state_t *state,
                            node_t *node, const rtree_coord_t *rect,
                            size_t *index)
{
  const size_t
    dims = state_dims(state);
  size_t
    index_min = SIZE_MAX;
  rtree_coord_t
    dvol_min = INFINITY,
    vol_min = INFINITY;

  for (size_t i = 0 ; i < node_count(node) ; i++)
    {
      branch_t *branch;

      if ((branch = node_get_branch(state, node, i)) == NULL)
        return RTREE_ERR_GETBRANCH;

      const rtree_coord_t *rect1 = branch_get_rect(branch);
      rtree_coord_t rect2[2 * dims];
      rect_combine(state, rect, rect1, rect2);

      rtree_coord_t
        vol1 = rect_spherical_volume(state, rect1),
        vol2 = rect_spherical_volume(state, rect2),
        dvol = vol2 - vol1;

      if ((dvol < dvol_min) || ((dvol == dvol_min) && (vol1 < vol_min)))
        {
          index_min = i;
          vol_min = vol1;
          dvol_min = dvol;
        }
    }

  /*
    This can only happen if no branches are assigned in the above
    block, on the first call of it, dvol_min == DBL_MAX, so either
    the first case is called, or dvol == DBL_MAX, but dvol is equal
    to vol2 - vol1, and vol1, vol2 are non-negative, so vol2 must
    be DBL_MAX and vol1 zero, in particular vol1 < vol_min (DBL_MAX),
    so the second condition is met.
  */

  if (index_min == SIZE_MAX)
    return RTREE_ERR_PICKBRANCH;

  *index = index_min;

  return RTREE_OK;
}

int node_envelope(const state_t *state, const node_t *node,
                  rtree_coord_t *rect)
{
  size_t n = node_count(node);

  if (n > 0)
    {
      const branch_t *branch;

      if ((branch = node_get_branch(state, node, 0)) == NULL)
        return RTREE_ERR_GETBRANCH;
      rect_copy(state, branch_get_rect(branch), rect);

      for (size_t i = 1 ; i < n ; i++)
        {
          if ((branch = node_get_branch(state, node, i)) == NULL)
            return RTREE_ERR_GETBRANCH;
          rect_merge(state, branch_get_rect(branch), rect);
        }
    }

  return RTREE_OK;
}

static node_t* node_add_rect2(const state_t *state,
                              rtree_id_t id, const rtree_coord_t *rect, node_t *node,
                              node_level_t level)
{
  const size_t rect_size = state_rect_size(state);

  if (node_level(node) > level)
    {
      /* internal node */

      size_t i;

      if (node_pick_branch(state, node, rect, &i) != 0)
        return NULL;

      branch_t *picked;

      if ((picked = node_get_branch(state, node, i)) == NULL)
        return NULL;

      node_t
        *child = branch_get_child_mutable(picked),
        *node2 = node_add_rect2(state, id, rect, child, level);

      if (node2 == child)
        {
          /* child not split */

          rtree_coord_t rect_comb[rect_size];
          rect_combine(state, rect, branch_get_rect(picked), rect_comb);
          branch_set_rect(state, picked, rect_comb);

          return node;
        }
      else
        {
          /* child split */

          rtree_coord_t rect_comb[rect_size];
          if (node_envelope(state, child, rect_comb) != 0)
            return NULL;
          branch_set_rect(state, picked, rect_comb);

          char branch_bytes[state_branch_size(state)];
          branch_t *branch = (branch_t*)branch_bytes;
          branch_init(state, branch);

          branch_set_child(branch, node2);

          if (node_envelope(state, node2, rect_comb) != 0)
            return NULL;
          branch_set_rect(state, branch, rect_comb);

          node_t *new_node = node_add_branch(state, node, branch);

          return new_node;
        }
    }
  else if (node_level(node) == level)
    {
      /* leaf node */

      char branch_bytes[state_branch_size(state)];
      branch_t *branch = (branch_t*)branch_bytes;
      branch_init(state, branch);

      branch_set_id(branch, id);
      branch_set_rect(state, branch, rect);

      node_t *new_node = node_add_branch(state, node, branch);

      return new_node;
    }

  return NULL;
}

/*
  Insert the rect (array) into the node root, the root may be split
  and the sibling is returned from the function on success.  On failure
  NULL is returned and the root is not modified (so can be reallocated)
*/

node_t* node_add_rect(const state_t *state,
                      rtree_id_t id, rtree_coord_t *rect, node_t *root,
                      node_level_t level)
{
  const size_t dims = state_dims(state);

  /*
    dims is never zero as that would not make sense at the application
    level, and that is enforced in state_new(), but scan-build does
    not look that deep and thinks that it might be so errors on a length
    zero VLA below; this assert fixes that, removing it leads to spurious
    CI failures.
  */

  assert(dims > 0);

  for (size_t i = 0 ; i < dims ; i++)
    {
      if (rect[i] > rect[dims + i])
        {
          errno = EINVAL;
          return NULL;
        }
    }

  node_t *sibling;

  if ((sibling = node_add_rect2(state, id, rect, root, level)) == NULL)
    return NULL;

  if (sibling == root)
    return root;

  node_t *new_root;

  if ((new_root = node_new(state)) != NULL)
    {
      node_set_level(new_root, node_level(root) + 1);

      char branch_bytes[state_branch_size(state)];
      branch_t *branch = (branch_t*)branch_bytes;
      branch_init(state, branch);

      rtree_coord_t envelope[2 * dims];

      if (node_envelope(state, root, envelope) == 0)
        {
          branch_set_child(branch, root);
          branch_set_rect(state, branch, envelope);

          /*
            node_add_branch() may return a node different to the input
            node if the node splits -- that shouldn't happen, since we
            have just created this node, so if it does then we error
            out (making a half-hearted effort to clean up).
          */

          node_t *n = node_add_branch(state, new_root, branch);

          if (n != new_root)
            node_destroy(state, n);
          else
            {
              if (node_envelope(state, sibling, envelope) == 0)
                {
                  branch_set_child(branch, sibling);
                  branch_set_rect(state, branch, envelope);
                  node_add_branch(state, new_root, branch);

                  return new_root;
                }
            }
        }

      node_destroy(state, new_root);
    }

  node_destroy(state, sibling);

  return NULL;
}

int node_update(const state_t *state, const node_t *node,
                rtree_update_t *f, void *context)
{
  node_level_t level = node_level(node);

  if (level > 0)
    {
      const size_t dims = state_dims(state);

      for (size_t i = 0 ; i < node_count(node) ; i++)
        {
          branch_t *branch = node_get_branch(state, node, i);
          if (branch == NULL) return RTREE_ERR_GETBRANCH;

          const node_t *child = branch_get_child(branch);
          if (child == NULL) return RTREE_ERR_GETCHILD;

          /*
            Note, in the case that node_update returns RTREE_ERR_USER,
            we could calculate and assign the envelope, and then the
            search index should be correct. but it seems unlikely that
            this would ever be useful, since you're then be indexing a
            half-updated set of rectangles.  So we leave that until the
            need arises.
          */

          int err;

          err = node_update(state, child, f, context);
          if (err != RTREE_OK) return err;

          rtree_coord_t envelope[2 * dims];
          err = node_envelope(state, child, envelope);
          if (err != RTREE_OK) return err;

          branch_set_rect(state, branch, envelope);
        }
    }
  else
    {
      for (size_t i = 0 ; i < node_count(node) ; i++)
        {
          branch_t *branch = node_get_branch(state, node, i);
          if (branch == NULL) return RTREE_ERR_GETBRANCH;

          rtree_coord_t *rect = branch_get_rect_mutable(branch);
          rtree_id_t id = branch_get_id(branch);

          if (f(id, rect, context) != 0) return RTREE_ERR_USER;
        }
    }

  return RTREE_OK;
}

/*
  Height is the maximal number of branches from the root to a leaf,
  or zero if the tree is empty.  If there have been no branch
  deletions, then this is the same as the level of the root plus one,
  but if there have been deletions then this is not the case.  This
  function iterates over all internal nodes to calculate the height,
  this could probably be done more efficiently by holding some state
  on branch deletions, but we don't expect this to be called that
  often (and it's still pretty quick).
*/

node_level_t node_height(const state_t *state, const node_t *node)
{
  node_count_t count;

  if ((count = node_count(node)) == 0)
    return 0;

  if (node_level(node) == 0)
    return 1;

  node_level_t child_max_height = 0;

  for (size_t i = 0 ; i < count ; i++)
    {
      const branch_t *branch = node_get_branch(state, node, i);
      const node_t *child = branch_get_child(branch);
      node_level_t child_height = node_height(state, child);

      if (child_height > child_max_height)
        child_max_height = child_height;
    }

  if (child_max_height == 0)
    return 0;
  else
    return child_max_height + 1;
}

/*
  it is assumed that the state is identical for a and b, i.e., that
  state_identical() is true (so we don't need to pass the state for
  both nodes).
*/

bool node_identical(const state_t *state, const node_t *a, const node_t *b)
{
  if (a && b)
    {
      if ((node_level(a) != node_level(b)) || (node_count(a) != node_count(b)))
        return false;

      node_level_t level = node_level(a);
      node_count_t count = node_count(a);

      for (size_t i = 0 ; i < count ; i++)
        {
          const branch_t
            *branch_a = node_get_branch(state, a, i),
            *branch_b = node_get_branch(state, b, i);
          const rtree_coord_t
            *rect_a = branch_get_rect(branch_a),
            *rect_b = branch_get_rect(branch_b);

          if (! rect_identical(state, rect_a, rect_b))
            return false;

          if (level > 0)
            {
              const node_t
                *child_a = branch_get_child(branch_a),
                *child_b = branch_get_child(branch_b);

              if (! node_identical(state, child_a, child_b))
                return false;
            }
          else
            {
              rtree_id_t
                id_a = branch_get_id(branch_a),
                id_b = branch_get_id(branch_b);

              if (id_a != id_b)
                return false;
            }
        }
      return true;
    }

  return ! (a || b);
}

/*
  find whether the node or its descendants have a leaf,  so we're
  looking for a level-zero node with a non-zero count, of course
  we short circuit as soon as we find one.
*/

bool node_nonempty(const state_t *state, const node_t *node)
{
  node_count_t count;

  if ((count = node_count(node)) == 0)
    return false;

  if (node_level(node) == 0)
    return true;

  for (size_t i = 0 ; i < count ; i++)
    {
      const branch_t *branch = node_get_branch(state, node, i);
      const node_t *child = branch_get_child(branch);

      if (node_nonempty(state, child))
        return true;
    }

  return false;
}

extern node_count_t node_count(const node_t*);
extern void node_count_increment(node_t*);
extern void node_count_decrement(node_t*);
extern node_level_t node_level(const node_t*);
extern void node_set_level(node_t*, node_level_t);
extern void* node_get_branches(node_t*);
