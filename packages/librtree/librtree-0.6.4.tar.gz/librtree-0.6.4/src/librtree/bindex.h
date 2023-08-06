/*
  bindex.h
  Copyright (c) J.J. Green 2020
*/

#ifndef BINDEX_H
#define BINDEX_H

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <stddef.h>

typedef struct
{
  size_t n;
  unsigned long word[];
} bindex_t;

bindex_t* bindex_new(size_t);
void bindex_destroy(bindex_t*);

size_t bindex_get(const bindex_t*, size_t);
int bindex_set(bindex_t*, size_t, size_t);

size_t bindex_first_unset(const bindex_t*);
size_t bindex_next_unset(const bindex_t*, size_t);


#endif
