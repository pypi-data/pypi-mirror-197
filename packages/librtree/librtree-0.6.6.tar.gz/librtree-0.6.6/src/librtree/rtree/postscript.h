/*
  rtree/postscript.h
  Copyright (c) J.J. Green 2020
*/

#ifndef RTREE_POSTSCRIPT_H
#define RTREE_POSTSCRIPT_H

#ifdef __cplusplus
extern "C" {
#endif

typedef struct rtree_postscript_t rtree_postscript_t;

#include <stdio.h>
#include <rtree/node.h>
#include <rtree/extent.h>

typedef enum
  { model_none, model_grey, model_rgb, model_cmyk }
  colour_model_t;

typedef struct {
  colour_model_t model;
  union {
    float grey[1];
    float rgb[3];
    float cmyk[4];
  };
} colour_t;

typedef struct {
  struct {
    colour_t colour;
  } fill;
  struct {
    colour_t colour;
    float width;
  } stroke;
} style_level_t;

typedef struct {
  size_t n;
  style_level_t *array;
} style_t;

style_t* postscript_style_read(FILE*);
void postscript_style_destroy(style_t*);

struct rtree_postscript_t
{
  const style_t *style;
  extent_axis_t axis;
  float extent;
  float margin;
  const char *title;
};

int postscript_write(const state_t*, const node_t*,
                     const rtree_postscript_t*, FILE*);

#ifdef __cplusplus
}
#endif

#endif
