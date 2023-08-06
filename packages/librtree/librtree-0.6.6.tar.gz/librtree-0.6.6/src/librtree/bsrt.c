#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "bsrt.h"

#include "rtree/error.h"
#include "rtree/branches.h"

#include <errno.h>
#include <string.h>

#ifdef WITH_BSRT

#include "endianness.h"
#include "bounds.h"

#define BSRT_MAGIC "BSRt"
#define BSRT_FOOTER "fin"
#define BSRT_VERSION 2

/* magic number, 4 bytes */

static int write_magic(FILE *stream)
{
  if (fwrite(BSRT_MAGIC, 1, 4, stream) != 4)
    return RTREE_ERR_FWRITE;

  return RTREE_OK;
}

/* version, 2 bytes */

static int write_version(FILE *stream)
{
  uint16_t v = htole16(BSRT_VERSION);

  if (fwrite(&v, 2, 1, stream) != 1)
    return RTREE_ERR_FWRITE;

  return RTREE_OK;
}

/* state, 12 bytes */

static int write_state(state_t *state, FILE *stream)
{
  uint16_t v[6] =
    {
     htole16(state_dims(state)),
     htole16(state_page_size(state)),
     htole16(SIZEOF_RTREE_COORD_T),
     htole16(state_rect_size(state)),
     htole16(state_branch_size(state)),
     htole16(state_node_size(state))
    };

  if (fwrite(&v, 2, 6, stream) != 6)
    return RTREE_ERR_FWRITE;

  return RTREE_OK;
}

/*
  each node has a 4-byte header, the level (positive for an internal
  node, zero for a leaf node) and the count of branches.
*/

static int write_header(uint16_t level, uint16_t count, FILE *stream)
{
  uint16_t v;

  v = htole16(level);

  if (fwrite(&v, 2, 1, stream) != 1)
    return RTREE_ERR_FWRITE;

  v = htole16(count);

  if (fwrite(&v, 2, 1, stream) != 1)
    return RTREE_ERR_FWRITE;

  return RTREE_OK;
}

static int write_id(rtree_id_t id, FILE *stream)
{
#if SIZEOF_RTREE_ID_T == 2
  uint16_t v = htole16(id);
#elif SIZEOF_RTREE_ID_T == 4
  uint32_t v = htole32(id);
#elif SIZEOF_RTREE_ID_T == 8
  uint64_t v = htole64(id);
#else
#error rtree_id_t size not handled
#endif

  if (fwrite(&v, SIZEOF_RTREE_ID_T, 1, stream) != 1)
    return RTREE_ERR_FWRITE;

  return RTREE_OK;
}

/*
  Here we only byte-swap if we establish that the host float
  byte-order is big-endian, this saves time on little-endian
  hardware.  Note that in the big-endian case, we call htole32()
  which converts from the host integer byte-order to little-endian,
  this will only be correct if integer and float endianess are
  the same, this is not true in general (!), there exists real
  hardware with big-endian floats and little-endian integers.
  So it would be better to use be32tole32() here, but that does
  not exist (one could make it with htole32(be32toh()), but
  these are macros not functions, one would need to test this on
  real hardware first).
*/

static int write_rect(const state_t *state,
                      const rtree_coord_t *rect,
                      FILE *stream)
{
  size_t
    n = 2 * state_dims(state),
    k = SIZEOF_RTREE_COORD_T;

#ifdef FLOAT_WORDS_BIGENDIAN

  rtree_coord_t buffer[n];

  for (size_t i = 0 ; i < n ; i++)
    {
      /*
        The type-punning to/from char* here is legal (the standard
        makes an explicit exception), but cppcheck warns anyway, so
        we suppress those warnings
      */

      char p[k];

      /* cppcheck-suppress invalidPointerCast */
      *(rtree_coord_t*)p = rect[i];

#if SIZEOF_RTREE_COORD_T == 4
      /* cppcheck-suppress invalidPointerCast */
      *(uint32_t*)p = htole32(*(uint32_t*)p);
#elif SIZEOF_RTREE_COORD_T == 8
      /* cppcheck-suppress invalidPointerCast */
      *(uint64_t*)p = htole64(*(uint64_t*)p);
#else
#error rtree_coord_t size not handled
#endif

      /* cppcheck-suppress invalidPointerCast */
      buffer[i] = *(rtree_coord_t*)p;
    }

  if (fwrite(buffer, k, n, stream) != n)
    return RTREE_ERR_FWRITE;
  return RTREE_OK;

#else

  if (fwrite(rect, k, n, stream) != n)
    return RTREE_ERR_FWRITE;
  return RTREE_OK;

#endif
}

static int write_node(const state_t*, const node_t*, FILE*);

/* callbacks passed to node_branch_each() */

static int write_internal_branch(const state_t *state,
                                 const branch_t *branch,
                                 void *arg)
{
  FILE *stream = arg;
  int err;

  if ((err = write_rect(state, branch->rect, stream)) != 0)
    return err;

  const node_t *child = branch_get_child(branch);

  if ((err = write_node(state, child, stream)) != 0)
    return err;

  return 0;
}

static int write_leaf_branch(const state_t *state,
                             const branch_t *branch,
                             void *arg)
{
  FILE *stream = arg;
  int err;

  if ((err = write_rect(state, branch->rect, stream)) != 0)
    return err;

  rtree_id_t id = branch_get_id(branch);

  if ((err = write_id(id, stream)) != 0)
    return err;

  return 0;
}

/* write internal/leaf nodes */

static int write_internal_node(const state_t *state,
                               const node_t *node,
                               FILE *stream)
{
  int err;

  if ((err = write_header(node_level(node), node_count(node), stream)) != 0)
    return err;

  return node_branch_each(state, node, write_internal_branch, stream);
}

static int write_leaf_node(const state_t *state,
                           const node_t *node,
                           FILE *stream)
{
  int err;

  if ((err = write_header(node_level(node), node_count(node), stream)) != 0)
    return err;

  return node_branch_each(state, node, write_leaf_branch, stream);
}

static int write_node(const state_t *state,
                      const node_t *node,
                      FILE *stream)
{
  int err;

  if (node_level(node) > 0)
    err = write_internal_node(state, node, stream);
  else
    err = write_leaf_node(state, node, stream);

  return err;
}

static int write_footer(FILE *stream)
{
  size_t n = strlen(BSRT_FOOTER);
  if (fwrite(BSRT_FOOTER, 1, n, stream) != n)
    return RTREE_ERR_FWRITE;
  return RTREE_OK;
}

int bsrt_rtree_write(const rtree_t *rtree, FILE *stream)
{
  int err;

  if ((err = write_magic(stream)) != 0)
    return err;

  if ((err = write_version(stream)) != 0)
    return err;

  if ((err = write_state(rtree->state, stream)) != 0)
    return err;

  if ((err = write_node(rtree->state, rtree->root, stream)) != 0)
    return err;

  if ((err = write_footer(stream)) != 0)
    return err;

  return RTREE_OK;
}

/*
  reader functions, unlike the writer, all functions acting on
  file content after the version are version qualified, the idea
  being that later versions of the library should be able to
  read all previous versions of the format.
*/

static int read_magic(FILE *stream)
{
  char buffer[4];

  if (fread(buffer, 1, 4, stream) != 4)
    return 1;

  if (memcmp(buffer, BSRT_MAGIC, 4) == 0)
    return 0;

  errno = EINVAL;
  return 1;
}

static int read_version(FILE *stream, uint16_t *v)
{
  if (fread(v, 2, 1, stream) != 1)
    return 1;

  *v = le16toh(*v);

  return 0;
}

/* read v1 */

static int read_v1_header(FILE *stream, uint16_t v[5])
{
  if (fread(v, 2, 5, stream) != 5)
    return 1;

  for (size_t i = 0 ; i < 5 ; i++)
    v[i] = le16toh(v[i]);

  return 0;
}

static bool read_v1_state_consistent(uint16_t v[5], const state_t *state)
{
  return
    (v[0] == state_dims(state)) &&
    (v[1] == state_page_size(state)) &&
    (v[2] == SIZEOF_RTREE_COORD_T) &&
    (v[3] == state_rect_size(state)) &&
    (v[4] == state_branch_size(state));
}

/* see note above on float/double endianness */

static int read_v1_rect(FILE *stream,
                        const state_t *state,
                        rtree_coord_t *rect)
{
  size_t
    n = 2 * state_dims(state),
    k = SIZEOF_RTREE_COORD_T;

#ifdef FLOAT_WORDS_BIGENDIAN

  char buffer[n * k];

  if (fread(buffer, k, n, stream) != n)
    return 1;

  for (size_t i = 0 ; i < n ; i++)
    {
      char *p = buffer + i * k;

#if SIZEOF_RTREE_COORD_T == 4
      *(uint32_t*)p = le32toh(*(uint32_t*)p);
#elif SIZEOF_RTREE_COORD_T == 8
      *(uint64_t*)p = le64toh(*(uint64_t*)p);
#else
#error rtree_coord_t size not handled
#endif

      /* cppcheck-suppress invalidPointerCast */

      rect[i] = *(rtree_coord_t*)p;
    }

#else

  if (fread(rect, k, n, stream) != n)
    return 1;

#endif

  return 0;
}

static int read_v1_id(FILE *stream, rtree_id_t *id)
{
  if (fread(id, SIZEOF_RTREE_ID_T, 1, stream) != 1)
    return 1;

#if SIZEOF_RTREE_ID_T == 8
  *id = le64toh(*id);
#elif SIZEOF_RTREE_ID_T == 4
  *id = le32toh(*id);
#elif SIZEOF_RTREE_ID_T == 2
  *id = le16toh(*id);
#else
#error rtree_id_t size not handled
#endif

  return 0;
}

static node_t* read_v1_node(FILE*, const state_t*);

static int read_v1_branch_internal(FILE *stream,
                                   const state_t *state,
                                   branch_t *branch)
{
  if (branch_init(state, branch) != 0)
    return 1;

  if (read_v1_rect(stream, state, branch_get_rect_mutable(branch)) != 0)
    return 1;

  node_t *child;

  if ((child = read_v1_node(stream, state)) == NULL)
    return 1;

  branch_set_child(branch, child);

  return 0;
}

static int read_v1_branch_leaf(FILE *stream,
                               const state_t *state,
                               branch_t *branch)
{
  if (branch_init(state, branch) != 0)
    return 1;

  if (read_v1_rect(stream, state, branch_get_rect_mutable(branch)) != 0)
    return 1;

  rtree_id_t id;

  if (read_v1_id(stream, &id) != 0)
    return 1;

  branch_set_id(branch, id);

  return 0;
}

typedef int (branch_read_t)(FILE*, const state_t*, branch_t*);

static node_t* read_v1_node_generic(FILE *stream,
                                    branch_read_t *f,
                                    const state_t *state,
                                    uint16_t n)
{
  if (n > state_branching_factor(state))
    {
      errno = EINVAL;
      return NULL;
    }

  node_t *node;

  if ((node = node_new(state)) != NULL)
    {
      void *branches = node_get_branches(node);

      for (size_t i = 0 ; i < n ; i++)
        {
          branch_t *branch = branches_get(state, branches, i);
          if (f(stream, state, branch) != 0)
            break;
          node_count_increment(node);
        }

      if (node_count(node) == n)
        return node;

      errno = EINVAL;
      node_destroy(state, node);
    }

  return NULL;
}

static node_t* read_v1_node_internal(FILE *stream,
                                     const state_t *state,
                                     uint16_t n)
{
  return read_v1_node_generic(stream, read_v1_branch_internal, state, n);
}

static node_t* read_v1_node_leaf(FILE *stream,
                                 const state_t *state,
                                 uint16_t n)
{
  return read_v1_node_generic(stream, read_v1_branch_leaf, state, n);
}

static node_t* read_v1_node(FILE *stream, const state_t *state)
{
  uint16_t level;

  if (fread(&level, 2, 1, stream) != 1)
    return NULL;
  level = le16toh(level);
  if (level > RTREE_LEVELS_MAX)
    return NULL;

  uint16_t count;

  if (fread(&count, 2, 1, stream) != 1)
    return NULL;
  count = le16toh(count);
  if (count > RTREE_BRANCHES_MAX)
    return NULL;

  node_t *node;

  if (level > 0)
    node = read_v1_node_internal(stream, state, count);
  else
    node = read_v1_node_leaf(stream, state, count);

  if (node != NULL)
    node_set_level(node, level);

  return node;
}

static int read_v1_footer(FILE *stream)
{
  size_t n = strlen(BSRT_FOOTER);
  char buffer[n];

  if (fread(buffer, 1, n, stream) != n)
    return 1;

  if (memcmp(buffer, BSRT_FOOTER, n) == 0)
    return 0;
  else
    {
      errno = EINVAL;
      return 1;
    }
}

static rtree_t* read_v1(FILE *stream)
{
  uint16_t v[5];

  if (read_v1_header(stream, v) != 0)
    return NULL;

  size_t dims = v[0];

  if (dims > RTREE_DIMS_MAX)
    return NULL;

  state_t *state;

  if ((state = state_new(dims, RTREE_NODE_PAGE(1))) != NULL)
    {
      if (read_v1_state_consistent(v, state))
        {
          node_t *root;

          if ((root = read_v1_node(stream, state)) != NULL)
            {
              if (read_v1_footer(stream) == 0)
                {
                  rtree_t *rtree;

                  if ((rtree = rtree_alloc()) != NULL)
                    {
                      rtree->state = state;
                      rtree->root = root;
                      return rtree;
                    }
                }
              node_destroy(state, root);
            }
        }
      else
        errno = EINVAL;

      state_destroy(state);
    }

  return NULL;
}

/* read v2 */

static int read_v2_header(FILE *stream, uint16_t v[6])
{
  if (fread(v, 2, 6, stream) != 6)
    return 1;

  for (size_t i = 0 ; i < 6 ; i++)
    v[i] = le16toh(v[i]);

  return 0;
}

static bool read_v2_state_consistent(uint16_t v[6], const state_t *state)
{
  return
    (v[0] == state_dims(state)) &&
    (v[1] == state_page_size(state)) &&
    (v[2] == SIZEOF_RTREE_COORD_T) &&
    (v[3] == state_rect_size(state)) &&
    (v[4] == state_branch_size(state)) &&
    (v[5] == state_node_size(state));
}

static node_t* read_v2_node(FILE *stream, const state_t *state)
{
  return read_v1_node(stream, state);
}

static int read_v2_footer(FILE *stream)
{
  return read_v1_footer(stream);
}

static rtree_t* read_v2(FILE *stream)
{
  uint16_t v[6];

  if (read_v2_header(stream, v) != 0)
    return NULL;

  if ((v[5] == 0) || (v[1] < v[5]))
    return NULL;

  size_t
    dims = v[0],
    node_page = v[1] / v[5];
  state_t *state;

  if ((state = state_new(dims, RTREE_NODE_PAGE(node_page))) != NULL)
    {
      if (read_v2_state_consistent(v, state))
        {
          node_t *root;

          if ((root = read_v2_node(stream, state)) != NULL)
            {
              if (read_v2_footer(stream) == 0)
                {
                  rtree_t *rtree;

                  if ((rtree = rtree_alloc()) != NULL)
                    {
                      rtree->state = state;
                      rtree->root = root;
                      return rtree;
                    }
                }
              node_destroy(state, root);
            }
        }
      else
        errno = EINVAL;

      state_destroy(state);
    }

  return NULL;
}

rtree_t* bsrt_rtree_read(FILE *stream)
{
  if (read_magic(stream) != 0)
    return NULL;

  uint16_t version;

  if (read_version(stream, &version) != 0)
    return NULL;

  switch (version)
    {
    case 1:
      return read_v1(stream);
    case 2:
      return read_v2(stream);
    default:
      errno = EINVAL;
      return NULL;
    }
}

#else

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wunused-parameter"
int bsrt_rtree_write(const rtree_t *rtree, FILE *stream)
{
  errno = ENOSYS;
  return RTREE_ERR_NOBSRT;
}
#pragma GCC diagnostic pop

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wunused-parameter"
rtree_t* bsrt_rtree_read(FILE *stream)
{
  errno = ENOSYS;
  return NULL;
}
#pragma GCC diagnostic pop

#endif
