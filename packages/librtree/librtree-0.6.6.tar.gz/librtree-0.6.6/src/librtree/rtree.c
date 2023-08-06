#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "rtree.h"
#include "rtree/error.h"

#include "csv.h"
#include "json.h"
#include "bsrt.h"

#include <errno.h>
#include <stdlib.h>

rtree_t* rtree_alloc(void)
{
  rtree_t *rtree;

  if ((rtree = malloc(sizeof(rtree_t))) == NULL)
    errno = ENOMEM;
  else
    {
      rtree->state = NULL;
      rtree->root = NULL;
    }

  return rtree;
}

int rtree_init(rtree_t *rtree, size_t dims, state_flags_t flags)
{
  state_t *state;

  if ((state = state_new(dims, flags)) != NULL)
    {
      node_t *root;

      if ((root = node_new(state)) != NULL)
        {
          rtree->state = state;
          rtree->root = root;

          return 0;
        }

      state_destroy(state);
    }

  return 1;
}

rtree_t* rtree_new(size_t dims, state_flags_t flags)
{
  rtree_t *rtree;

  if ((rtree = rtree_alloc()) != NULL)
    {
      if ((rtree_init(rtree, dims, flags)) == 0)
        return rtree;

      free(rtree);
    }

  return NULL;
}

rtree_t* rtree_clone(const rtree_t *src)
{
  node_t *dest_root;

  if ((dest_root = node_clone(src->state, src->root)) != NULL)
    {
      state_t *dest_state;
      if ((dest_state = state_clone(src->state)) != NULL)
        {
          rtree_t *dest;

          if ((dest = rtree_alloc()) == NULL)
            errno = ENOMEM;
          else
            {
              dest->root = dest_root;
              dest->state = dest_state;
              return dest;
            }
          state_destroy(dest_state);
        }
      node_destroy(src->state, dest_root);
    }
  return NULL;
}

void rtree_destroy(rtree_t *rtree)
{
  if (rtree != NULL)
    {
      node_destroy(rtree->state, rtree->root);
      state_destroy(rtree->state);
    }
  free(rtree);
}

rtree_height_t rtree_height(const rtree_t *rtree)
{
  return node_height(rtree->state, rtree->root);
}

rtree_t* rtree_csv_read(FILE *stream, size_t dim, state_flags_t flags)
{
  return csv_rtree_read(stream, dim, flags);
}

int rtree_json_write(const rtree_t *rtree, FILE *stream)
{
  return json_rtree_write(rtree, stream);
}

rtree_t* rtree_json_read(FILE *stream)
{
  return json_rtree_read(stream);
}

int rtree_bsrt_write(const rtree_t *rtree, FILE *stream)
{
  return bsrt_rtree_write(rtree, stream);
}

rtree_t* rtree_bsrt_read(FILE *stream)
{
  return bsrt_rtree_read(stream);
}

int rtree_add_rect(rtree_t *rtree, rtree_id_t id, rtree_coord_t *rect)
{
  node_t *node = node_add_rect(rtree->state, id, rect, rtree->root, 0);

  if (node == NULL)
    return RTREE_ERR_ADDRECT;

  if (node != rtree->root)
    rtree->root = node;

  return RTREE_OK;
}

int rtree_update(rtree_t *rtree, rtree_update_t *f, void *context)
{
  return node_update(rtree->state, rtree->root, f, context);
}

bool rtree_identical(const rtree_t *a, const rtree_t *b)
{
  if (a && b)
    {
      return
        state_identical(a->state, b->state) &&
        node_identical(a->state, a->root, b->root);
    }

  return ! (a || b);
}

int rtree_search(const rtree_t *rtree, const rtree_coord_t *rect,
                 rtree_search_t *f, void *arg)
{
  return search(rtree->state, rect, rtree->root, f, arg);
}

int rtree_postscript(const rtree_t *rtree,
                     const rtree_postscript_t *options,
                     FILE *stream)
{
  return postscript_write(rtree->state, rtree->root, options, stream);
}

const char* rtree_strerror(int err)
{
  return strerror_rtree(err);
}

size_t rtree_bytes(const rtree_t *rtree)
{
  if (rtree == NULL)
    return 0;
  else
    return
      sizeof(rtree_t) +
      state_bytes(rtree->state) +
      node_bytes(rtree->state, rtree->root);
}

bool rtree_empty(const rtree_t *rtree)
{
  return
    (rtree == NULL) ||
    (! node_nonempty(rtree->state, rtree->root));
}
