#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "page.h"

#ifdef HAVE_UNISTD_H
#include <unistd.h>
#endif


int page_size(size_t *sz)
{

#if defined HAVE_SYSCONF

  long val = sysconf(_SC_PAGESIZE);

  if (val >= 1)
    {
      *sz = val;
      return 0;
    }
  else
    return 1;

#elif defined HAVE_GETPAGESIZE

  int val = getpagesize();

  if (val >= 1)
    {
      *sz = val;
      return 0;
    }
  else
    return 1;

#else
#warning Using default page-size (4,096 bytes)

  *sz = 0x1000;
  return 0;

#endif

}
