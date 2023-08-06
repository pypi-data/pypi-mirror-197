/*
  rtree/rectf.h
  Copyright (c) J.J. Green 2022
*/

#ifndef RTREE_RECTF_H
#define RTREE_RECTF_H

#ifdef __cplusplus
extern "C" {
#endif

#include <rtree/types.h>
#include <stddef.h>

/* rect-spherical-volume */

typedef rtree_coord_t (rectf_rsv_t)(size_t, const rtree_coord_t*);

rectf_rsv_t* rectf_spherical_volume(size_t);

/* rect-combine */

typedef void (rectf_rc_t)(size_t,
                          const rtree_coord_t*,
                          const rtree_coord_t*,
                          rtree_coord_t*);

rectf_rc_t* rectf_combine(size_t);

#ifdef __cplusplus
}
#endif
#endif
