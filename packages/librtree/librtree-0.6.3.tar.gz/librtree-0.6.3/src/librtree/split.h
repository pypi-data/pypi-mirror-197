/*
  split.h
  Copyright (c) J.J. Green 2020
*/

#ifndef SPLIT_H
#define SPLIT_H

#include <rtree/state.h>
#include <rtree/branch.h>
#include <rtree/node.h>

node_t* split_node(const state_t*, node_t*, branch_t*);

#endif
