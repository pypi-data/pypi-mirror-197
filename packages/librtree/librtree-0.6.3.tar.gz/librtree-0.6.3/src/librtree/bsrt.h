/*
  bsrt.h
  Copyright (c) J.J. Green 2019
*/

#ifndef BSRT_H
#define BSRT_H

#include <stdio.h>

#include <rtree.h>

int bsrt_rtree_write(const rtree_t*, FILE*);
rtree_t* bsrt_rtree_read(FILE*);

#endif
