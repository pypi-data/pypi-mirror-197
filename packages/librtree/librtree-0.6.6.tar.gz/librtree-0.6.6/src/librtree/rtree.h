/*
  rtree.h

  This is the bottom-level "public" header, it does not
  include all of the rtree headers, just enough to define
  the members of the (atypically) open structure rtree_t.

  Copyright (c) J.J. Green 2020
*/

#ifndef RTREE_H
#define RTREE_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

typedef struct rtree_t rtree_t;
typedef uint16_t rtree_height_t;

#include <rtree/types.h>
#include <rtree/state.h>
#include <rtree/node.h>
#include <rtree/postscript.h>
#include <rtree/search.h>
#include <rtree/error.h>

struct rtree_t
{
  state_t *state;
  node_t *root;
};

rtree_t* rtree_alloc(void);
int rtree_init(rtree_t*, size_t, state_flags_t);
rtree_t* rtree_new(size_t, state_flags_t);
rtree_t* rtree_clone(const rtree_t*);
void rtree_destroy(rtree_t*);
rtree_height_t rtree_height(const rtree_t*);
int rtree_search(const rtree_t*, const rtree_coord_t*, rtree_search_t*, void*);
int rtree_add_rect(rtree_t*, rtree_id_t, rtree_coord_t*);
int rtree_update(rtree_t*, rtree_update_t*, void*);
bool rtree_identical(const rtree_t*, const rtree_t*);
rtree_t* rtree_csv_read(FILE*, size_t, state_flags_t);
int rtree_json_write(const rtree_t*, FILE*);
rtree_t* rtree_json_read(FILE*);
int rtree_bsrt_write(const rtree_t*, FILE*);
rtree_t* rtree_bsrt_read(FILE*);
int rtree_postscript(const rtree_t*, const rtree_postscript_t*, FILE*);
const char* rtree_strerror(int);
size_t rtree_bytes(const rtree_t*);
bool rtree_empty(const rtree_t*);

#ifdef __cplusplus
}
#endif

#endif
