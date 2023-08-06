/*
  An array of binary values which are to be used as indexes
  for an array; so we can store each value in a bit, but the
  functions return size_t (since the array-index type)
*/

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "bindex.h"
#include "rtree/error.h"

#include <errno.h>
#include <stdlib.h>
#include <stdalign.h>
#include <string.h>

#define UL_BYTES sizeof(unsigned long)
#define UL_BITS (UL_BYTES << 3)

/* see note on branch_sizeof in branch.c */

static size_t bindex_sizeof(size_t n)
{
  const size_t s = offsetof(bindex_t, word) + n * UL_BYTES;
  return ((s - 1) / alignof(bindex_t) + 1) * alignof(bindex_t);
}

bindex_t* bindex_new(size_t n)
{
  size_t k = n / UL_BITS + 1;
  bindex_t *bindex;

  if ((bindex = malloc(bindex_sizeof(k))) != NULL)
    {
      bindex->n = n;
      memset(bindex->word, 0, k * UL_BYTES);
      return bindex;
    }

  return NULL;
}

void bindex_destroy(bindex_t *bindex)
{
  free(bindex);
}

static size_t first_unset(const unsigned long *words, size_t n_bits)
{
  size_t n_words = n_bits / UL_BITS + 1;

  for (size_t j = 0 ; j < n_words ; j++)
    {
      unsigned long word = ~words[j];

      if (word)
        {

#ifdef HAVE___BUILTIN_CTZL

          return j * UL_BITS + __builtin_ctzl(word);

#else

          for (size_t k = 0 ; k < UL_BITS ; k++)
            {
              if (1UL & (word >> k))
                return j * UL_BITS + k;
            }
#endif
        }
    }

  return n_bits;
}

static size_t next_unset(const unsigned long *words, size_t n_bits, size_t i)
{
  if (i < n_bits)
    {
      size_t
        j0 = i / UL_BITS,
        k0 = i % UL_BITS;
      unsigned long word;

#ifdef HAVE___BUILTIN_CTZL

      if ((word = ~words[j0] >> k0) != 0UL)
        return j0 * UL_BITS + __builtin_ctzl(word) + k0;

#else

      if ((word = ~words[j0]) != 0UL)
        {
          for (size_t k = k0 ; k < UL_BITS ; k++)
            {
              if (1UL & (word >> k))
                return j0 * UL_BITS + k;
            }
        }

#endif

      size_t j1 = j0 + 1;

      return first_unset(words + j1, n_bits - j1 * UL_BITS) + j1 * UL_BITS;
    }

  return n_bits;
}

size_t bindex_first_unset(const bindex_t *bindex)
{
  return first_unset(bindex->word, bindex->n);
}

size_t bindex_next_unset(const bindex_t *bindex, size_t i)
{
  return next_unset(bindex->word, bindex->n, i);
}

size_t bindex_get(const bindex_t *bindex, size_t i)
{
  if (i >= bindex->n)
    {
      errno = EDOM;
      return 0;
    }

  size_t
    j = i / UL_BITS,
    k = i % UL_BITS;

  return 1UL & (bindex->word[j] >> k);
}

int bindex_set(bindex_t *bindex, size_t i, size_t v)
{
  if (v > 1)
    return RTREE_ERR_INVAL;

  if (i >= bindex->n)
    return RTREE_ERR_DOM;

  size_t
    j = i / UL_BITS,
    k = i % UL_BITS;

  if (v)
    bindex->word[j] |= (1UL << k);
  else
    bindex->word[j] &= ~(1UL << k);

  return 0;
}
