#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "rtree/branch.h"

#include <stddef.h>
#include <stdalign.h>
#include <string.h>

/*
  The size of branch_t with n rect elements, with padding taken into
  account: kindly provided by Eric Postpischil in the stackoverflow
  question https://stackoverflow.com/questions/59435697/

  Atypically this takes the total number of rect elements (so 2 * dims)
  rather than the state, this is because it is used in state_new().
*/

size_t branch_sizeof(size_t n)
{
  const size_t s = offsetof(branch_t, rect) + n * sizeof(rtree_coord_t);
  return ((s - 1) / alignof(branch_t) + 1) * alignof(branch_t);
}

int branch_init(const state_t *state, branch_t *branch)
{
  branch->child = NULL;
  return rect_init(state, branch->rect);
}

branch_t* branch_copy(const state_t *state,
                      const branch_t *src, branch_t *dest)
{
  const size_t branch_size = state_branch_size(state);
  if ((dest = memcpy(dest, src, branch_size)) == NULL)
    return NULL;
  rect_copy(state, src->rect, dest->rect);
  return dest;
}

/* inline accessors */

extern void branch_set_child(branch_t*, node_t*);
extern const node_t* branch_get_child(const branch_t*);
extern node_t* branch_get_child_mutable(branch_t*);
extern void branch_set_id(branch_t*, rtree_id_t);
extern rtree_id_t branch_get_id(const branch_t*);
extern void branch_set_rect(const state_t*, branch_t*, const rtree_coord_t*);
extern const rtree_coord_t* branch_get_rect(const branch_t*);
extern rtree_coord_t* branch_get_rect_mutable(branch_t*);
