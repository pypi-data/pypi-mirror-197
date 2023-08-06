#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "json.h"
#include "bounds.h"

#include "rtree/error.h"
#include "rtree/branches.h"

#include <errno.h>

#ifdef WITH_JSON

#include <jansson.h>

/*
  This module exports json_rtree_read(), json_rtree_write() but
  we make a change in our usual naming conventions in having all
  static functions prefixed "jr/w_" (for JSON reed/write) since
  the Jansson library uses the "json_" prefix, so to avoid a clash
  with that namespace
*/

static json_t* jw_leaf(const state_t *state, const branch_t *branch)
{
  json_t *jb = json_object(), *jr = json_array();
  const rtree_coord_t *rect = branch_get_rect((branch_t*)branch);
  const size_t dims = state_dims(state);
  const unsigned long id = branch_get_id(branch);

  for (size_t i = 0 ; i < 2 * dims ; i++)
    json_array_append_new(jr, json_real(rect[i]));

  json_object_set_new(jb, "rect", jr);
  json_object_set_new(jb, "id", json_integer(id));

  return jb;
}

static int jw_leaf_f(const state_t *state, const branch_t *branch, void *arg)
{
  json_t *ja = (json_t*)arg, *jb;

  if ((jb = jw_leaf(state, branch)) != NULL)
    {
      json_array_append_new(ja, jb);
      return 0;
    }

  return 1;
}

static json_t* jw_node(const state_t*, const node_t*);

static int jw_branch_f(const state_t *state, const branch_t *branch, void *arg)
{
  const size_t dims = state_dims(state);

  json_t *jr;
  if ((jr = json_array()) != NULL)
    {
      const rtree_coord_t *rect;
      if ((rect = branch_get_rect((branch_t*)branch)) != NULL)
        {
          for (size_t i = 0 ; i < 2 * dims ; i++)
            json_array_append_new(jr, json_real(rect[i]));

          const node_t *child;
          if ((child = branch_get_child(branch)) != NULL)
            {
              json_t *jb;
              if ((jb = json_object()) != NULL)
                {
                  json_t *jn;
                  if ((jn = jw_node(state, child)) != NULL)
                    {
                      json_object_set_new(jb, "rect", jr);
                      json_object_set_new(jb, "node", jn);
                      json_array_append_new((json_t*)arg, jb);

                      return 0;
                    }
                  json_decref(jb);
                }
            }
        }
      json_decref(jr);
    }

  return 1;
}

static json_t* jw_branch(const state_t *state, const node_t *node)
{
  json_t *json;
  nbe_cb_t *json_f;

  if (node_level(node) == 0)
    json_f = jw_leaf_f;
  else
    json_f = jw_branch_f;

  if ((json = json_array()) != NULL)
    {
      if (node_branch_each(state, node, json_f, json) == 0)
        return json;
      json_decref(json);
    }

  return NULL;
}

static json_t* jw_node(const state_t *state, const node_t *node)
{
  json_t *json;

  if ((json = json_object()) == NULL)
    return NULL;

  json_object_set_new(json, "level", json_integer(node_level(node)));
  json_object_set_new(json, "count", json_integer(node_count(node)));
  json_object_set_new(json, "branches", jw_branch(state, node));

  return json;
}

static json_t* jw_state(const state_t *state)
{
  json_t *json;

  if ((json = json_object()) == NULL)
    return NULL;

  const size_t
    dims = state_dims(state),
    page_size = state_page_size(state),
    branch_size = state_branch_size(state),
    node_size = state_node_size(state),
    rect_size = state_rect_size(state),
    float_size = sizeof(rtree_coord_t);

  json_object_set_new(json, "dims", json_integer(dims));
  json_object_set_new(json, "page_size", json_integer(page_size));
  json_object_set_new(json, "float_size", json_integer(float_size));
  json_object_set_new(json, "rect_size", json_integer(rect_size));
  json_object_set_new(json, "branch_size", json_integer(branch_size));
  json_object_set_new(json, "node_size", json_integer(node_size));

  return json;
}

static json_t* jw_rtree(const rtree_t *rtree)
{
  json_t *json;

  if ((json = json_object()) == NULL)
    return NULL;

  json_object_set_new(json, "root", jw_node(rtree->state, rtree->root));
  json_object_set_new(json, "state", jw_state(rtree->state));

  return json;
}

int json_rtree_write(const rtree_t *rtree, FILE *stream)
{
  json_t *json;
  int err = 0;

  if ((json = jw_rtree(rtree)) != NULL)
    {
      if (json_dumpf(json, stream, JSON_INDENT(2)) != 0)
        err++;
      json_decref(json);
    }
  else
    err++;

  return err ? RTREE_ERR_JANSSON : RTREE_OK;
}

/* reader */

static bool jr_value_equal(json_t *object, const char *key, size_t value)
{
  json_t *json_value = json_object_get(object, key);

  if ((json_value == NULL) || (json_is_integer(json_value) == false))
    return false;

  json_int_t int_value = json_integer_value(json_value);

  return (int_value >= 0) && ((size_t)int_value == value);
}

static bool jr_state_is_consistent(json_t *json_state, state_t *state)
{
  return
    jr_value_equal(json_state, "dims", state_dims(state)) &&
    jr_value_equal(json_state, "page_size", state_page_size(state)) &&
    jr_value_equal(json_state, "float_size", sizeof(rtree_coord_t)) &&
    jr_value_equal(json_state, "rect_size", state_rect_size(state)) &&
    jr_value_equal(json_state, "branch_size", state_branch_size(state)) &&
    jr_value_equal(json_state, "node_size", state_node_size(state));
}

static state_t* jr_state(json_t *json)
{
  json_t *json_state;

  if ((json_state = json_object_get(json, "state")) == NULL)
    return NULL;

  if (! json_is_object(json_state))
    return NULL;

  size_t dims;

  {
    json_t *json_dims;

    if ((json_dims = json_object_get(json_state, "dims")) == NULL)
      return NULL;

    if (! json_is_integer(json_dims))
      return NULL;

    dims = json_integer_value(json_dims);

    if (dims > RTREE_DIMS_MAX)
      return NULL;
  }

  size_t page_size;

  {
    json_t *json_page_size;

    if ((json_page_size = json_object_get(json_state, "page_size")) == NULL)
      return NULL;

    if (! json_is_integer(json_page_size))
      return NULL;

    page_size = json_integer_value(json_page_size);
  }

  size_t node_size;

  {
    json_t *json_node_size;

    if ((json_node_size = json_object_get(json_state, "node_size")) == NULL)
      return NULL;

    if (! json_is_integer(json_node_size))
      return NULL;

    node_size = json_integer_value(json_node_size);
  }

  const size_t node_page = page_size / node_size;

  state_t *state;

  if ((state = state_new(dims, RTREE_NODE_PAGE(node_page))) != NULL)
    {
      if (jr_state_is_consistent(json_state, state))
        return state;
      else
        errno = EINVAL;
      state_destroy(state);
    }

  return NULL;
}

static node_t* jr_node(state_t*, json_t*);

static int jr_branch_leaf(json_t *json, branch_t *branch)
{
  const json_t *json_id = json_object_get(json, "id");
  if ((json_id == NULL) || (json_is_integer(json_id) == false))
    return 1;

  branch_set_id(branch, json_integer_value(json_id));

  return 0;
}

static int jr_branch_internal(state_t *state, json_t *json, branch_t *branch)
{
  json_t *json_node = json_object_get(json, "node");
  if ((json_node == NULL) || (json_is_object(json_node) == false))
    return RTREE_ERR_JANSSON;

  node_t *node = jr_node(state, json_node);
  if (node == NULL)
    return RTREE_ERR_JANSSON;

  branch_set_child(branch, node);

  return RTREE_OK;
}

static int jr_node_recurse(state_t *state, node_t *node, json_t *json_branches)
{
  const size_t dims = state_dims(state);
  const node_level_t level = node_level(node);
  size_t i;
  void *branches = node_get_branches(node);
  json_t *json_branch;

  if (json_array_size(json_branches) > state_branching_factor(state))
    return RTREE_ERR_INVAL;

  json_array_foreach(json_branches, i, json_branch)
    {
      if (json_is_object(json_branch) == false)
        return RTREE_ERR_JANSSON;

      branch_t *branch = branches_get(state, branches, i);

      {
        int err = branch_init(state, branch);
        if (err != RTREE_OK)
          return err;
      }

      json_t *json_rect = json_object_get(json_branch, "rect");

      if ( (json_rect == NULL) ||
           (json_is_array(json_rect) == false) ||
           (json_array_size(json_rect) != 2 * dims) )
        return RTREE_ERR_JANSSON;

      rtree_coord_t coord[2 * dims];
      json_t *json_coord;
      size_t j;

      json_array_foreach(json_rect, j, json_coord)
        {
          if (json_is_real(json_coord) == false)
            return RTREE_ERR_JANSSON;
          coord[j] = json_real_value(json_coord);
        }

      branch_set_rect(state, branch, coord);
      node_count_increment(node);

      if (level == 0)
        {
          int err = jr_branch_leaf(json_branch, branch);
          if (err != RTREE_OK)
            return err;
        }
      else
        {
          int err = jr_branch_internal(state, json_branch, branch);
          if (err != RTREE_OK)
            return err;
        }
    }

  return RTREE_OK;
}

static node_t* jr_node(state_t *state, json_t *json_node)
{
  json_int_t count;
  {
    json_t *json = json_object_get(json_node, "count");
    if ( (json == NULL) || (json_is_integer(json) == false) )
      return NULL;
    count = json_integer_value(json);
    if ((count < 0) || (state_branching_factor(state) < (size_t)count))
      return NULL;
  }

  json_int_t level;
  {
    json_t *json = json_object_get(json_node, "level");
    if ( (json == NULL) || (json_is_integer(json) == false) )
      return NULL;
    level = json_integer_value(json);
    if ((level < 0) || (NODE_LEVEL_MAX < level))
      return NULL;
  }

  json_t *json_branches = json_object_get(json_node, "branches");

  if ( (json_branches == NULL) ||
       (json_is_array(json_branches) == false) ||
       (json_array_size(json_branches) != (size_t)count) )
    return NULL;

  node_t *node;

  if ((node = node_new(state)) != NULL)
    {
      node_set_level(node, level);

      int err = jr_node_recurse(state, node, json_branches);
      if (err == 0)
        return node;

      node_destroy(state, node);
    }

  return NULL;
}

static node_t* jr_root(state_t *state, json_t *json)
{
  json_t *json_root;

  if ((json_root = json_object_get(json, "root")) == NULL)
    return NULL;

  return jr_node(state, json_root);
}

static rtree_t* jr_rtree(json_t *json)
{
  if (! json_is_object(json))
    return NULL;

  state_t *state;

  if ((state = jr_state(json)) != NULL)
    {
      node_t *root;

      if ((root = jr_root(state, json)) != NULL)
        {
          rtree_t *rtree;

          if ((rtree = rtree_alloc()) == NULL)
            errno = ENOMEM;
          else
            {
              rtree->state = state;
              rtree->root = root;

              return rtree;
            }
          node_destroy(state, root);
        }
      state_destroy(state);
    }

  return NULL;
}

rtree_t* json_rtree_read(FILE *stream)
{
  const size_t flags = JSON_REJECT_DUPLICATES;
  json_t *json;

  if ((json = json_loadf(stream, flags, NULL)) != NULL)
    {
      rtree_t *rtree = jr_rtree(json);
      json_decref(json);
      return rtree;
    }

  return NULL;
}

#else

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wunused-parameter"
int json_rtree_write(const rtree_t *rtree, FILE *stream)
{
  errno = ENOSYS;
  return RTREE_ERR_NOJSON;
}
#pragma GCC diagnostic pop

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wunused-parameter"
rtree_t* json_rtree_read(FILE *stream)
{
  errno = ENOSYS;
  return NULL;
}
#pragma GCC diagnostic pop

#endif
