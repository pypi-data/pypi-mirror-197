#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "rtree/search.h"

#include "rtree/branch.h"
#include "rtree/error.h"
#include "rtree/rect.h"

typedef struct
{
  rtree_search_t *callback;
  void *context;
  const rtree_coord_t *rect;
} search_context_t;

static int internal(const state_t *state,
                    const branch_t *branch, void *arg)
{
  int err = RTREE_OK;
  search_context_t *search_context = arg;
  if (rect_intersect(state, branch_get_rect(branch), search_context->rect))
    err = search(state, search_context->rect, branch_get_child(branch),
                 search_context->callback, search_context->context);
  return err;
}

static int leaf(const state_t *state,
                const branch_t *branch, void *arg)
{
  int err = RTREE_OK;
  search_context_t *search_context = arg;
  if (rect_intersect(state, branch_get_rect(branch), search_context->rect))
    err = search_context->callback(branch_get_id(branch),
                                   search_context->context);
  return err;
}

int search(const state_t *state,
           const rtree_coord_t *rect, const node_t *node,
           rtree_search_t *callback, void *context)
{
  search_context_t search_context = {
    .callback = callback,
    .context = context,
    .rect = rect
  };
  node_level_t level = node_level(node);

  return node_branch_each(state, node,
                          level > 0 ? internal : leaf,
                          &search_context);
}
