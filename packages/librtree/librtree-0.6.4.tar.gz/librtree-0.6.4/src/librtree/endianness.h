/*
  endian.h

  This is an "internal" header, it is not used by any public headers
  and not installed; it handles the messing around that you need to
  do to get endinannes functions even close to portable.

  This is largely from https://github.com/mikepb/endian.h which is
  based on a Gist by Mathias Panzenböck, those are both released into
  the public domain.  It differs in that

  - it uses autoconf to determine the existence of headers and
    declarations, rather than "OS sniffing"

  - it is only interested in the little-endian versions of the macros
    since that's the only ones we use (one could add those in a fairly
    obvious fashion though)

  Copyright (c) J.J. Green 2020
*/

#ifndef ENDIANNESS_H
#define ENDIANNESS_H

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#if defined HAVE_ENDIAN_H

#include <endian.h>

#elif defined HAVE_SYS_ENDIAN_H

#include <sys/endian.h>

#ifndef HAVE_DECL_LE16TOH
#define le16toh(x) letoh16(x)
#endif
#ifndef HAVE_DECL_LE32TOH
#define le32toh(x) letoh32(x)
#endif
#ifndef HAVE_DECL_LE64TOH
#define le64toh(x) letoh64(x)
#endif

#elif defined HAVE_LIBKERN_OSBYTEORDER_H

#include <libkern/OSByteOrder.h>
#define htole16(x) OSSwapHostToLittleInt16(x)
#define le16toh(x) OSSwapLittleToHostInt16(x)
#define htole32(x) OSSwapHostToLittleInt32(x)
#define le32toh(x) OSSwapLittleToHostInt32(x)
#define htole64(x) OSSwapHostToLittleInt64(x)
#define le64toh(x) OSSwapLittleToHostInt64(x)

#elif defined HAVE_WINSOCK2_H

#include <winsock2.h>
#include <sys/param.h>
#if BYTE_ORDER == LITTLE_ENDIAN
#define htole16(x) (x)
#define le16toh(x) (x)
#define htole32(x) (x)
#define le32toh(x) (x)
#define htole64(x) (x)
#define le64toh(x) (x)
#elif BYTE_ORDER == BIG_ENDIAN
#define htole16(x) __builtin_bswap16(x)
#define le16toh(x) __builtin_bswap16(x)
#define htole32(x) __builtin_bswap32(x)
#define le32toh(x) __builtin_bswap32(x)
#define htole64(x) __builtin_bswap64(x)
#define le64toh(x) __builtin_bswap64(x)
#endif

#else

#error No compatible endianness header available

#endif

#endif
