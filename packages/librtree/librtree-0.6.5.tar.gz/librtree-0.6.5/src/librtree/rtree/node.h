/*
  rtree/node.h
  Copyright (c) J.J. Green 2019
*/

#ifndef RTREE_NODE_H
#define RTREE_NODE_H

#ifdef __cplusplus
extern "C" {
#if 0
}
#endif
#endif

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

typedef uint16_t node_level_t;
typedef uint16_t node_count_t;
typedef uint16_t node_height_t;

#define NODE_LEVEL_MAX UINT16_MAX
#define NODE_COUNT_MAX UINT16_MAX

typedef struct node_t node_t;

#include <rtree/types.h>
#include <rtree/state.h>
#include <rtree/branch.h>

struct node_t
{
  node_level_t level;
  node_count_t count;
  char branches[];
};

typedef int (rtree_update_t)(rtree_id_t, rtree_coord_t*, void*);
typedef int (nbe_cb_t)(const state_t*, const branch_t*, void*);

int node_init(const state_t*, node_t*);
node_t* node_new(const state_t*);
void node_destroy(const state_t*, node_t*);
node_t* node_clone(const state_t*, const node_t*);
int node_branch_each(const state_t*, const node_t*, nbe_cb_t*, void*);
int node_branch_each_level(const state_t*, const node_t*, node_level_t,
                           nbe_cb_t*, void*);
size_t node_num_branch(size_t, size_t);
int node_detach_branch(const state_t*, node_t*, size_t);
node_t* node_add_branch(const state_t*, node_t*, branch_t*);
int node_envelope(const state_t*, const node_t*, rtree_coord_t*);
node_t* node_add_rect(const state_t*, rtree_id_t, rtree_coord_t*,
                      node_t*, node_level_t);
int node_update(const state_t*, const node_t*, rtree_update_t*, void*);
bool node_identical(const state_t*, const node_t*, const node_t*);
node_height_t node_height(const state_t*, const node_t*);
size_t node_bytes(const state_t*, const node_t*);
bool node_nonempty(const state_t*, const node_t*);

inline node_count_t node_count(const node_t *node)
{
  return node->count;
}

inline void node_count_increment(node_t *node)
{
  node->count++;
}

inline void node_count_decrement(node_t *node)
{
  node->count--;
}

inline node_level_t node_level(const node_t *node)
{
  return node->level;
}

inline void node_set_level(node_t *node, node_level_t level)
{
  node->level = level;
}

inline void* node_get_branches(node_t *node)
{
  return node->branches;
}

#ifdef __cplusplus
}
#endif

#endif
