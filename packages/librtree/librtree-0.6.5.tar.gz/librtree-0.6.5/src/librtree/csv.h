/*
  csv.h
  Copyright (c) J.J. Green 2020
*/

#ifndef CSV_H
#define CSV_H

#include <stdio.h>

#include <rtree.h>
#include <rtree/state.h>

rtree_t* csv_rtree_read(FILE*, size_t, state_flags_t);

#endif
