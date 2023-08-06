/*
  json.h
  Copyright (c) J.J. Green 2019
*/

#ifndef JSON_H
#define JSON_H

#include <stdio.h>

#include <rtree.h>

int json_rtree_write(const rtree_t*, FILE*);
rtree_t* json_rtree_read(FILE*);

#endif
