#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "rtree/postscript.h"
#include "rtree/package.h"
#include "rtree/error.h"

#include <time.h>
#include <errno.h>
#include <stdbool.h>

#ifdef HAVE_TGMATH_H
#include <tgmath.h>
#else
#include <math.h>
#endif

#define POSTSCRIPT_LEVEL 1

typedef struct {
  struct {
    double width, height;
  } body;
  struct {
    double x, y;
  } offset;
  double margin, scale;
  uint32_t bbox[4];
} page_t;

typedef struct {
  const state_t *state;
  const node_t *root;
  const style_t *style;
  page_t page;
} ps_t;

#ifdef WITH_JSON

#include <jansson.h>

static bool clamped(float value)
{
  return (value >= 0.0) && (value <= 1.0);
}

static int psr_colour(json_t *json, colour_t *colour)
{
  json_t *json_colour;

  if (((json_colour = json_object_get(json, "grey")) != NULL) ||
      ((json_colour = json_object_get(json, "gray")) != NULL))
    {
      if (! json_is_number(json_colour))
        return 1;

      float value = json_number_value(json_colour);

      if (! clamped(value))
        return 1;

      colour->model = model_grey;
      colour->grey[0] = value;

      return 0;
    }

  if ((json_colour = json_object_get(json, "rgb")) != NULL)
    {
      if (! json_is_array(json_colour))
        return 1;

      if (json_array_size(json_colour) != 3)
        return 1;

      colour->model = model_rgb;

      size_t i;
      json_t *json_band;

      json_array_foreach(json_colour, i, json_band)
        {
          if (! json_is_number(json_band))
            return 1;

          float value = json_number_value(json_band);

          if (! clamped(value))
            return 1;

          colour->rgb[i] = value;
        }

      return 0;
    }

  if ((json_colour = json_object_get(json, "cmyk")) != NULL)
    {
      if (! json_is_array(json_colour))
        return 1;

      if (json_array_size(json_colour) != 4)
        return 1;

      colour->model = model_cmyk;

      size_t i;
      json_t *json_band;

      json_array_foreach(json_colour, i, json_band)
        {
          if (! json_is_number(json_band))
            return 1;

          float value = json_number_value(json_band);

          if (! clamped(value))
            return 1;

          colour->cmyk[i] = value;
        }

      return 0;
    }

  return 1;
}

static int psr_style_level(json_t *json, style_level_t *style_level)
{
  if (! json_is_object(json))
    return 1;

  json_t *json_fill;

  if ((json_fill = json_object_get(json, "fill")) == NULL)
    {
      style_level->fill.colour.model = model_none;
    }
  else
    {
      if (psr_colour(json_fill, &(style_level->fill.colour)) != 0)
        return 1;
    }

  json_t *json_stroke;

  if ((json_stroke = json_object_get(json, "stroke")) == NULL)
    {
      style_level->stroke.colour.model = model_none;
    }
  else
    {
      if (psr_colour(json_stroke, &(style_level->stroke.colour)) != 0)
        return 1;

      json_t *json_width;

      if ((json_width = json_object_get(json_stroke, "width")) == NULL)
        return 1;

      if (! json_is_number(json_width))
        return 1;

      style_level->stroke.width = json_number_value(json_width);
    }

  return 0;
}

static style_t* psr_style(json_t *json)
{
  if (! json_is_array(json))
    return NULL;

  size_t n = json_array_size(json);

  if (n == 0)
    return NULL;

  style_level_t *array;

  if ((array = calloc(n, sizeof(style_level_t))) != NULL)
    {
      size_t i;
      json_t *json_style;

      json_array_foreach(json, i, json_style)
        {
          style_level_t *style_level = array + i;

          if (psr_style_level(json_style, style_level) != 0)
            {
              free(array);
              return NULL;
            }
        }

      style_t *style;

      if ((style = malloc(sizeof(style_t))) != NULL)
        {
          style->n = n;
          style->array = array;
          return style;
        }

      free(array);
    }

  return NULL;
}

style_t* postscript_style_read(FILE *stream)
{
  const size_t flags = JSON_REJECT_DUPLICATES;
  json_t *json;

  if ((json = json_loadf(stream, flags, NULL)) != NULL)
    {
      style_t *style = psr_style(json);
      json_decref(json);
      return style;
    }

  return NULL;
}

#else

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wunused-parameter"
style_t* postscript_style_read(FILE *stream)
{
  errno = ENOSYS;
  return NULL;
}
#pragma GCC diagnostic pop

#endif

void postscript_style_destroy(style_t *style)
{
  if (style != NULL)
    free(style->array);
  free(style);
}

static int pw_header(FILE *stream, uint32_t *bbox, const char *title)
{
  time_t t; time(&t);
  struct tm *tm = gmtime(&t);
  size_t n = 1024;
  char time_string[n];
  if (strftime(time_string, n,  "%a, %d %b %Y %T %z", tm) == 0)
    return RTREE_ERR_BUFFER;

  fprintf(stream,
          "%%!PS-Adobe-3.0 EPSF-3.0\n"
          "%%%%LanguageLevel: %i\n"
          "%%%%Creator: %s %s\n"
          "%%%%Title: %s\n"
          "%%%%CreationDate: %s\n"
          "%%%%BoundingBox: %u %u %u %u\n"
          "%%%%DocumentData: Clean7Bit\n"
          "%%%%EndComments\n",
          POSTSCRIPT_LEVEL,
          rtree_package_name,
          rtree_package_version,
          title ? title : "librtree output",
          time_string,
          bbox[0], bbox[1], bbox[2], bbox[3]);

  return RTREE_OK;
}

static int pw_prologue(FILE *stream)
{
  fprintf(stream, "%%%%BeginProlog\n");
  fprintf(stream,
          "%% box\n"
          "/box {\n"
          "/h exch def\n"
          "/w exch def\n"
          "newpath\n"
          "0 0 moveto\n"
          "0 h lineto\n"
          "w h lineto\n"
          "w 0 lineto\n"
          "closepath\n"
          "} def\n");
  fprintf(stream,
          "%% filled box\n"
          "/R {\n"
          "gsave\n"
          "translate\n"
          "box\n"
          "fill\n"
          "grestore\n"
          "} def\n");
  fprintf(stream,
          "%% box interior stroke\n"
          "/I {\n"
          "gsave\n"
          "translate\n"
          "/h0 exch def\n"
          "/w0 exch def\n"
          "/d currentlinewidth def\n"
          "/d2 d 2 div def\n"
          "/w w0 d sub def\n"
          "/h h0 d sub def\n"
          "d2 d2 translate\n"
          "w h box\n"
          "stroke\n"
          "grestore\n"
          "} def\n");
  fprintf(stream, "%%%%EndProlog\n");

  return RTREE_OK;
}

static void pw_footer(FILE *stream)
{
  fprintf(stream,
          "showpage\n"
          "%%%%EOF\n");
}

typedef struct
{
  FILE *stream;
  page_t *page;
} rect_data_t;

static int rect_proc(const branch_t *branch, const char *proc, rect_data_t *data)
{
  const rtree_coord_t *rect = branch_get_rect(branch);
  page_t *page = data->page;
  float scale = page->scale;
  fprintf(data->stream,
          "%.2f %.2f %.2f %.2f %s\n",
          (rect[2] - rect[0]) * scale,
          (rect[3] - rect[1]) * scale,
          (rect[0] - page->offset.x) * scale,
          (rect[1] - page->offset.y) * scale,
          proc);
  return RTREE_OK;
}

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wunused-parameter"
static int rect_fill(const state_t *state, const branch_t *branch, void *arg)
{
  return rect_proc(branch, "R", (rect_data_t*)arg);

}
#pragma GCC diagnostic pop

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wunused-parameter"
static int rect_stroke(const state_t *state, const branch_t *branch, void *arg)
{
  return rect_proc(branch, "I", (rect_data_t*)arg);
}
#pragma GCC diagnostic pop

static int pw_rects_fill(const state_t *state, const node_t *root,
                                 unsigned level, rect_data_t *data)
{
  return node_branch_each_level(state, root, level, rect_fill, data);
}

static int pw_rects_stroke(const state_t *state, const node_t *root,
                                   unsigned level, rect_data_t *data)
{
  return node_branch_each_level(state, root, level, rect_stroke, data);
}

static int pw_state(const rtree_postscript_t *opts, ps_t *ps)
{
  rtree_coord_t rect[4];
  int err;

  if ((err = node_envelope(ps->state, ps->root, rect)) != RTREE_OK)
    return err;

  /*
    Given the desired output image width, the margin and the envelope
    of the R-tree, find the various parameters of the page.  Likewise
    for desired output height.
  */

  page_t *page = &(ps->page);
  uint32_t *bbox = page->bbox;

  bbox[0] = bbox[1] = 0;

  double
    env_width = rect[2] - rect[0],
    env_height = rect[3] - rect[1],
    margin = opts->margin,
    width, height, body_width, body_height, scale;

  switch (opts->axis)
    {
    case axis_width:
      width = opts->extent;
      body_width = width - 2 * margin;
      scale = body_width / env_width;
      body_height = env_height * scale;
      height = body_height + 2 * margin;
      bbox[2] = round(width);
      bbox[3] = ceil(height);
      break;
    case axis_height:
      height = opts->extent;
      body_height = height - 2 * margin;
      scale = body_height / env_height;
      body_width = env_width * scale;
      width = body_height + 2 * margin;
      bbox[2] = ceil(width);
      bbox[3] = round(height);
      break;
    default:
      return RTREE_ERR_INVAL;
    }

  page->body.height = body_height;
  page->body.width = body_width;
  page->scale = scale;
  page->offset.x = rect[0] - margin / scale;
  page->offset.y = rect[1] - margin / scale;

  return RTREE_OK;
}

int postscript_write(const state_t *state,
                     const node_t *root,
                     const rtree_postscript_t *opts,
                     FILE *stream)
{
  if ((state == NULL) ||
      (root == NULL) ||
      (opts == NULL) ||
      (opts->style == NULL))
    return RTREE_ERR_INVAL;

  if (state_dims(state) != 2)
    return RTREE_ERR_DIMS;

  if (node_count(root) == 0)
    return RTREE_ERR_EMPTY;

  ps_t ps = {
    .root = root,
    .state = state,
    .style = opts->style
  };

  int err;

  if (((err = pw_state(opts, &ps)) != RTREE_OK) ||
      ((err = pw_header(stream, ps.page.bbox, opts->title)) != RTREE_OK) ||
      ((err = pw_prologue(stream)) != RTREE_OK))
    return err;

  rect_data_t rect_data = { .stream = stream, .page = &(ps.page) };
  node_level_t max_level = node_level(root);

  for (size_t i = 0 ; i <= max_level ; i++)
    {
      if (i >= ps.style->n)
        break;

      style_level_t style_level = ps.style->array[i];
      node_level_t level = max_level - i;

      switch (style_level.fill.colour.model)
        {
        case model_grey:
          fprintf(stream, "%.3f setgray\n", style_level.fill.colour.grey[0]);
          err = pw_rects_fill(state, root, level, &rect_data);
          break;
        case model_rgb:
          fprintf(stream, "%.3f %.3f %.3f setrgbcolor\n",
                  style_level.fill.colour.rgb[0],
                  style_level.fill.colour.rgb[1],
                  style_level.fill.colour.rgb[2]);
          err = pw_rects_fill(state, root, level, &rect_data);
          break;
        case model_cmyk:
          fprintf(stream, "%.3f %.3f %.3f %.3f setcmykcolor\n",
                  style_level.fill.colour.cmyk[0],
                  style_level.fill.colour.cmyk[1],
                  style_level.fill.colour.cmyk[2],
                  style_level.fill.colour.cmyk[3]);
          err = pw_rects_fill(state, root, level, &rect_data);
          break;
        case model_none:
          break;
        }

      if (err != RTREE_OK)
        return err;

      switch (style_level.stroke.colour.model)
        {
        case model_grey:
          fprintf(stream, "%.3f setgray\n",
                  style_level.stroke.colour.grey[0]);
          fprintf(stream, "%.3f setlinewidth\n", style_level.stroke.width);
          err = pw_rects_stroke(state, root, level, &rect_data);
          break;
        case model_rgb:
          fprintf(stream, "%.3f %.3f %.3f setrgbcolor\n",
                  style_level.stroke.colour.rgb[0],
                  style_level.stroke.colour.rgb[1],
                  style_level.stroke.colour.rgb[2]);
          fprintf(stream, "%.3f setlinewidth\n", style_level.stroke.width);
          err = pw_rects_stroke(state, root, level, &rect_data);
          break;
        case model_cmyk:
          fprintf(stream, "%.3f %.3f %.3f %.3f setcmykcolor\n",
                  style_level.stroke.colour.cmyk[0],
                  style_level.stroke.colour.cmyk[1],
                  style_level.stroke.colour.cmyk[2],
                  style_level.stroke.colour.cmyk[3]);
          fprintf(stream, "%.3f setlinewidth\n", style_level.stroke.width);
          err = pw_rects_stroke(state, root, level, &rect_data);
          break;
        case model_none:
          break;
        }

      if (err != RTREE_OK)
        return err;
    }

  pw_footer(stream);

  return RTREE_OK;
}
