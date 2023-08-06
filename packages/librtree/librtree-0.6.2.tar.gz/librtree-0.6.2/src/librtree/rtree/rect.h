/*
  rtree/rect.h
  Copyright (c) J.J. Green 2019
*/

#ifndef RTREE_RECT_H
#define RTREE_RECT_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdlib.h>
#include <stdbool.h>

#include <rtree/state.h>
#include <rtree/types.h>

int rect_init(const state_t*, rtree_coord_t*);

rtree_coord_t rect_volume(const state_t*, const rtree_coord_t*);
rtree_coord_t rect_spherical_volume(const state_t*, const rtree_coord_t*);
void rect_combine(const state_t*,
                  const rtree_coord_t *restrict,
                  const rtree_coord_t *restrict,
                  rtree_coord_t *restrict);
bool rect_intersect(const state_t*, const rtree_coord_t*, const rtree_coord_t*);
void rect_merge(const state_t*, const rtree_coord_t*, rtree_coord_t*);
void rect_copy(const state_t*, const rtree_coord_t*, rtree_coord_t*);
bool rect_identical(const state_t*, const rtree_coord_t*, const rtree_coord_t*);
int rects_alloc(const state_t*, size_t, rtree_coord_t**);
void rects_free(size_t, rtree_coord_t**);

#ifdef __cplusplus
}
#endif

#endif
