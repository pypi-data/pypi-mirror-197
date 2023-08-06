/*
  rtree/branches.h
  Copyright (c) J.J. Green 2020
*/

#ifndef RTREE_BRANCHES_H
#define RTREE_BRANCHES_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdlib.h>
#include <errno.h>
#include <string.h>

#include <rtree/state.h>
#include <rtree/branch.h>
#include <rtree/error.h>

inline branch_t* branches_get(const state_t *state, void *buffer, size_t i)
{
  const size_t branch_size = state_branch_size(state);
  char *bytes = (char*)buffer;
  return (branch_t*)(bytes + i * branch_size);
}

inline void branches_set(const state_t *state, void *buffer, size_t i,
                         const branch_t *src)
{
  memcpy(branches_get(state, buffer, i), src, state_branch_size(state));
}

#ifdef __cplusplus
}
#endif

#endif
