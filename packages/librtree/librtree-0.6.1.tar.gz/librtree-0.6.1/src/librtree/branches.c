/*
  The code here is to handle a void* buffer as an array of branch,
  we can't actually create an array of branch since its size is
  not known until runtime, so we have to perform those calculations
  ourselves.  Note that we just do the arithmatic here, no error
  checking -- so a over-sized index to branches_get()  will lead to
  a memory error, the caller is epected to do this check themselves
*/

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "rtree/branches.h"

extern branch_t* branches_get(const state_t*, void*, size_t);
extern void branches_set(const state_t*, void*, size_t, const branch_t*);
