/*
  rtree/search.h
  Copyright (c) J.J. Green 2020
*/

#ifndef RTREE_SEARCH_H
#define RTREE_SEARCH_H

#ifdef __cplusplus
extern "C" {
#endif

#include <rtree/node.h>
#include <rtree/types.h>
#include <rtree/state.h>

typedef int (rtree_search_t)(rtree_id_t, void*);

int search(const state_t*,
           const rtree_coord_t*, const node_t*,
           rtree_search_t*, void*);

#ifdef __cplusplus
}
#endif

#endif
