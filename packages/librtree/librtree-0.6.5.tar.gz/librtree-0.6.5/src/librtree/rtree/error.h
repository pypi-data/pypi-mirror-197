/*
  rtree/error.h
  Copyright (c) J.J. Green 2020
*/

#ifndef RTREE_ERROR_H
#define RTREE_ERROR_H

#ifdef __cplusplus
extern "C" {
#endif

#define RTREE_OK 0
#define RTREE_ERR_INVAL 1
#define RTREE_ERR_DOM 2
#define RTREE_ERR_NOMEM 3
#define RTREE_ERR_CSVPARSE 4
#define RTREE_ERR_NOCSV 5
#define RTREE_ERR_JANSSON 6
#define RTREE_ERR_NOJSON 7
#define RTREE_ERR_NOBSRT 8
#define RTREE_ERR_GETBRANCH 9
#define RTREE_ERR_GETCHILD 10
#define RTREE_ERR_NODECLONE 11
#define RTREE_ERR_PICKBRANCH 12
#define RTREE_ERR_ADDRECT 13
#define RTREE_ERR_NOSUCHSPLIT 14
#define RTREE_ERR_DIMS 15
#define RTREE_ERR_EMPTY 16
#define RTREE_ERR_BUFFER 17
#define RTREE_ERR_POSTSCRIPT 18
#define RTREE_ERR_USER 19
#define RTREE_ERR_FWRITE 20
#define RTREE_ERR_SPLIT 21

const char* strerror_rtree(int);

#ifdef __cplusplus
}
#endif

#endif
