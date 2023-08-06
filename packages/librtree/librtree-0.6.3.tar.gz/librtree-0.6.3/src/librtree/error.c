#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <stdlib.h>

#include "rtree/error.h"

const char* strerror_rtree(int err)
{
  static const char nomsg[] = "unimplemented message";
  struct
  {
    int err;
    const char *msg;
  } *m, mtab[] =
      {
        { RTREE_OK, "Success" },
        { RTREE_ERR_INVAL, "Invalid argument" },
        { RTREE_ERR_DOM, "Argument outside domain" },
        { RTREE_ERR_NOMEM, "Out of memory" },
        { RTREE_ERR_CSVPARSE, "Error parsing CSV" },
        { RTREE_ERR_NOCSV, "Compiled without CSV support" },
        { RTREE_ERR_JANSSON, "Error from the Jansson library" },
        { RTREE_ERR_NOJSON, "Compiled without JSON support" },
        { RTREE_ERR_NOJSON, "Compiled without BSRT support" },
        { RTREE_ERR_GETBRANCH, "Error getting branch" },
        { RTREE_ERR_GETCHILD, "Error getting child node" },
        { RTREE_ERR_NODECLONE, "Error cloning node" },
        { RTREE_ERR_PICKBRANCH, "Error picking branch" },
        { RTREE_ERR_ADDRECT, "Error adding rectangle" },
        { RTREE_ERR_NOSUCHSPLIT, "No such splitting method" },
        { RTREE_ERR_DIMS, "Bad R-tree dimension" },
        { RTREE_ERR_EMPTY, "Empty R-tree" },
        { RTREE_ERR_BUFFER, "Buffer to small" },
        { RTREE_ERR_POSTSCRIPT, "Error generating PostScript" },
        { RTREE_ERR_USER, "User abort" },
        { RTREE_ERR_FWRITE, "Failed write" },
        { RTREE_ERR_SPLIT, "Error in split" },
        { -1, NULL }
      };

  for (m = mtab ; m->msg ; m++)
    if (m->err == err) return m->msg;

  return nomsg;
}
