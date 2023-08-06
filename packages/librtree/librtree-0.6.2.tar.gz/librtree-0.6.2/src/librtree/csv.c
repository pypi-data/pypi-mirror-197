#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "csv.h"

#include "rtree/error.h"
#include "rtree/types.h"

#include <errno.h>
#include <string.h>
#include <stdlib.h>

#define LINE_LEN 0x1000

static int parse(FILE *stream, rtree_t *rtree)
{
  const size_t dims = state_dims(rtree->state);
  rtree_coord_t rect[2 * dims];
  char line[LINE_LEN];

  /*
    Note that fgets(3) reads from the stream up to LINE_LEN - 1,
    or if an EOF or line-ending \n is found.  That's behaviour
    required by the C standard.  CSV files should really have
    CRLF line semantics, i.e., each line is terminated by \r\n,
    in that case, fgets will still read up to the \n, so the \r
    will be the last character written to the buffer.  That's OK.
    But, a line with just \r line endings will not be handled
    correctly by this code, fgets(3) will not see a line ending
    and so will read multiple lines into the buffer.  Such files
    might be found as output from old Macs, they are pretty rare,
    so probably not worth the hassle of handling this case.
  */

  while (fgets(line, LINE_LEN, stream) != NULL)
    {
      char *tok;

      if ((tok = strtok(line, ",")) == NULL)
        continue;

      rtree_id_t id = strtoul(tok, NULL, 0);

      for (size_t i = 0 ; i < 2 * dims - 1 ; i++)
        {
          if ((tok = strtok(NULL, ",")) == NULL)
            return RTREE_ERR_CSVPARSE;
          rect[i] = strtod(tok, NULL);
        }

      if ((tok = strtok(NULL, ",\n\r")) == NULL)
        return RTREE_ERR_CSVPARSE;
      rect[2 * dims - 1] = strtod(tok, NULL);

      if (rtree_add_rect(rtree, id, rect) != 0)
        return RTREE_ERR_CSVPARSE;
    }

  return RTREE_OK;
}

rtree_t* csv_rtree_read(FILE *stream, size_t dims, state_flags_t flags)
{
  if (stream == NULL)
    {
      errno = EINVAL;
      return NULL;
    }

  rtree_t *rtree;

  if ((rtree = rtree_new(dims, flags)) != NULL)
    {
      if (parse(stream, rtree) == RTREE_OK)
        return rtree;
      rtree_destroy(rtree);
    }

  return NULL;
}
