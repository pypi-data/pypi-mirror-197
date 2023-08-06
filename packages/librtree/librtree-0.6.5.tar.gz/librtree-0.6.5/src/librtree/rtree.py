from __future__ import annotations

import librtree.pyrtree as prt  # type: ignore
import os
import json

from typing import Union, Tuple, Any, Callable, TextIO, BinaryIO


TupleInts = Tuple[int, ...]
TupleFloats = Tuple[float, ...]

class RTree:
    '''
    Instances of this class implememt the R-tree spatial index
    of Guttman-Green.
    '''

    url: str = prt.url
    '''
    The package's homepage
    '''

    bugreport: str = prt.bugreport
    '''
    The email address where bug-reports may be directed
    '''

    version: TupleInts = tuple(int(n) for n in prt.version.split('.'))
    '''
    The version of the C librtree package embedded
    '''

    @staticmethod
    def _split_flag(split: str) -> int:
        if split == 'quadratic':
            flag = prt.SPLIT_QUADRATIC
        elif split == 'linear':
            flag = prt.SPLIT_LINEAR
        elif split == 'greene':
            flag = prt.SPLIT_GREENE
        else:
            raise ValueError('bad split: %s' % split)
        return flag

    @staticmethod
    def _node_page_flag(node_page: int) -> int:
        return node_page << 2

    @property
    def _flags(self) -> int:
        return (
            self._split_flag(self._split) |
            self._node_page_flag(self._node_page)
        )

    def __init__(
            self,
            dim: int,
            split: str = 'quadratic',
            node_page: int = 0
    ) -> None:
        '''
        :param dim: the dimension of the tree, must be a postive
          integer
        :param split: one of 'linear', 'quadratic', 'greene', which
          determines the splitting strategy, the linear strategy is
          faster to build, the quadratic and greene strategies produce
          better-quality R-trees which are faster to query.
        :param node_page: the nodes-per-page value. This value can
          affect performance quite dramatically, particularly build
          time. A value which is too large would result in an infeasible
          branching factor for the R-tree and will cause the function
          to error with :code:`errno` set to :code:`EINVAL`. A value of
          zero is permitted and the default; in this case the function
          will choose a good value based on heuristics. You may get
          better performance for your use-case by manual experimentation,
          but zero is a good place to start.
        '''
        self._split = split
        self._node_page = node_page
        self._rtree = prt.RTree(dim, self._flags)

    @classmethod
    def _serialise(cls, f, rmode, wmode):
        rn, wn = os.pipe()
        if os.fork():
            os.close(wn)
            try:
                rio = os.fdopen(rn, rmode)
                result = rio.read()
            finally:
                rio.close()
                os.wait()
        else:
            os.close(rn)
            try:
                wio = os.fdopen(wn, wmode)
                f(wio)
            finally:
                wio.close()
                os._exit(0)
        return result

    @classmethod
    def _serialise_text(cls, f):
        return cls._serialise(f, 'r', 'w')

    @classmethod
    def _serialise_binary(cls, f):
        return cls._serialise(f, 'rb', 'wb')

    @classmethod
    def _deserialise(cls, source, rmode, wmode, f, *arg, **kwarg):
        rn, wn = os.pipe()
        if os.fork():
            os.close(wn)
            try:
                rio = os.fdopen(rn, rmode)
                try:
                    result = f(rio, *arg, **kwarg)
                finally:
                    rio.close()
            finally:
                os.wait()
        else:
            os.close(rn)
            try:
                wio = os.fdopen(wn, wmode)
                wio.write(source)
                wio.close()
            finally:
                os._exit(0)
        return result

    @classmethod
    def _deserialise_text(cls, source, f, *arg, **kwarg):
        return cls._deserialise(source, 'r', 'w', f, *arg, **kwarg)

    @classmethod
    def _deserialise_binary(cls, source, f, *arg, **kwarg):
        return cls._deserialise(source, 'rb', 'wb', f, *arg, **kwarg)

    @classmethod
    def csv_read(
            cls,
            io: TextIO,
            dim: int,
            split: str = 'quadratic',
            node_page: int = 0
    ) -> RTree:
        '''
        Build a new RTree instance from CSV stream.

        The CSV file (without header) should have the id in the first
        column, then twice as many floats as the dimension. Extra
        columns may be present and will be ignored (this useful feature
        is the reason that the dimension is a required argument).

        :param io: the stream from which to read CSV
        :param dim: the dimension of the tree
        :param split: splitting strategy
        :param node_page: node per page of memory

        .. code-block:: python

           with open('file.csv', 'r') as io:
               rtree = RTree.csv_read(io, 2)
        '''
        rtree: RTree = cls.__new__(cls)
        flags = cls._split_flag(split) | cls._node_page_flag(node_page)
        rtree._rtree = prt.RTree.csv_read(io, dim, flags)
        return rtree

    @classmethod
    def from_csv(
            cls,
            csv: str,
            dim: int,
            split: str = 'quadratic',
            node_page: int = 0
    ) -> RTree:
        '''
        Build a new RTree instance from CSV strint.

        :param csv: the CSV string
        :param dim: the dimension of the tree
        :param split: splitting strategy
        :param node_page: node per page of memory
        '''
        return cls._deserialise_text(
            csv,
            cls.csv_read,
            dim,
            split=split,
            node_page=node_page
        )

    @classmethod
    def json_read(cls, io: TextIO) -> RTree:
        '''
        Build a new RTree instance from JSON stream.

        :param io: the stream from which to read JSON

        .. code-block:: python

           with open('file.json', 'r') as io:
               rtree = RTree.json_read(io)
        '''
        rtree: RTree = cls.__new__(cls)
        rtree._rtree = prt.RTree.json_read(io)
        return rtree

    @classmethod
    def from_json(cls, json: str) -> RTree:
        '''
        Create a new RTree instance from JSON string

        :param io: the JSON string
        '''
        return cls._deserialise_text(json, cls.json_read)

    @classmethod
    def bsrt_read(cls, io: BinaryIO) -> RTree:
        '''
        Build a new RTree instance from BSRT stream.

        :param io: the stream from which to read BSRT bytes

        .. code-block:: python

           with open('file.bsrt', 'rb') as io:
               rtree = RTree.bsrt_read(io)
        '''
        rtree: RTree = cls.__new__(cls)
        rtree._rtree = prt.RTree.bsrt_read(io)
        return rtree

    @classmethod
    def from_bsrt(cls, bsrt: bytes) -> RTree:
        '''
        Create a new RTree instance from BSRT string

        :param io: the BSRT string
        '''
        return cls._deserialise_binary(bsrt, cls.bsrt_read)

    @property
    def dim(self) -> int:
        '''
        The dimension of the RTree instance
        '''
        return self._rtree.dim()

    @property
    def size(self) -> int:
        '''
        The total bytes allocated for the instance

        This method traverses the entire tree summing the
        contributions for each node (rather than maintaining a
        running count).  Performance-minded users may wish to
        cache this value (invalidating the cache when calling
        :meth:`add_rect` of course).
        '''
        return self._rtree.size()

    @property
    def page_size(self) -> int:
        '''
        The size in bytes in a page of memory
        '''
        return self._rtree.page_size()

    @property
    def node_size(self) -> int:
        '''
        The size in bytes of a node
        '''
        return self._rtree.node_size()

    @property
    def rect_size(self) -> int:
        '''
        The size in bytes of a rectangle
        '''
        return self._rtree.rect_size()

    @property
    def branch_size(self) -> int:
        '''
        The size in bytes of a branch
        '''
        return self._rtree.branch_size()

    @property
    def branching_factor(self) -> int:
        '''
        The number of branches from each node
        '''
        return self._rtree.branching_factor()

    @property
    def unit_sphere_volume(self) -> float:
        '''
        The volume of the unit sphere in the R-tree's dimension
        '''
        return self._rtree.unit_sphere_volume()

    @property
    def height(self) -> int:
        '''
        The height to the tree in the usual mathematical sense
        '''
        return self._rtree.height()

    @property
    def is_empty(self) -> bool:
        """
        Whether or not the tree is empty (has no rectangles)
        """
        return self._rtree.empty()

    def clone(self) -> RTree:
        '''
        A deep copy of the RTree
        '''
        rtree = self.__new__(self.__class__)
        rtree._rtree = self._rtree.clone()
        return rtree

    def add_rect(self, rect_id: int, coords: TupleFloats) -> None:
        ''' Add a rectangle to the RTree

        :param rect_id: the id of the rectangle. It is anticipated that
            the id will be used as an index for application specific
            data to which this rectangle relates, but this is entirely
            at the discretion of the caller, the library makes no use
            of the value, treating it as payload. In particular, the
            value may be non-unique and may be zero.
        :param coords: the extent of the rectangle, the minima for each
            dimension, then the maxima for each dimension.

        .. code-block:: python

           rtree = RTree(2)
           rtree.add_rect(7, (0, 0, 1, 1))
        '''
        self._rtree.add_rect(rect_id, tuple(coords))

    def __eq__(self, other: Any) -> bool:
        '''
        Equality of RTrees.

        This is a rather strict equality, not only must the tree have
        the same rectangles, they must be in the same order. Certainly
        :meth:`clone` will produce an instance which is equal in this
        sense.
        '''
        return (
            isinstance(other, type(self)) and
            self._rtree.identical(other._rtree)
        )

    def search(self, f: Callable, rect: TupleFloats, context: Any) -> None:
        '''
        Search the RTree for intersecting rectangles

        :param f: a callback function, it will be called as
          :code:`f(id, context)` for the :code:`id` of each of the
          rectangles in the tree which intersect the :code:`rect`
          argument.  Returns zero to continue, non-zero to terminate.
        :param rect: the search rectangle
        :param context: user context to ba passed to :code:`f`

        Example, generate a list of the ids:

        .. code-block:: python

           def f(id, ids):
               ids.append(id)
               return 0

           ids = []
           rtree.search(f, (0, 0, 1, 1), ids)
        '''
        self._rtree.search(f, rect, context)

    def update(self, f: Callable, context: Any) -> None:
        '''
        Update the RTree.  Modifies the rectangles in-place without
        changing the tree structure.  Provided that the changes are
        small, the search efficiency should be close to that of freshly
        built RTree.

        :param f: a callback function, it will be called as
          :code:`f(id, coords, context)` for the :code:`id` and the
          :code:`coords` of each rectangle in the tree, along with
          the :code:`context`.  It should return a tuple of modified
          rectangle extent
        :param context: to be passed as the last argument to each
          call to the callback function :code:`f`.
        '''
        self._rtree.update(f, context)

    def json_write(self, io: TextIO) -> None:
        '''
        Serialise to JSON stream

        :param io: A writable text stream to which to write the JSON

        Example:

        .. code-block:: python

           with open('file.json', 'w') as io:
               rtree.json_write(io)
        '''
        self._rtree.json_write(io)

    def bsrt_write(self, io: BinaryIO) -> None:
        '''
        Serialise to BSRT (binary serialised R-tree) stream

        :param io: A writable binary stream to which to write the BSRT

        Example:

        .. code-block:: python

           with open('file.bsrt', 'wb') as io:
               rtree.bsrt_write(io)
        '''
        self._rtree.bsrt_write(io)

    def to_json(self) -> str:
        '''
        Serialise to JSON string
        '''
        return self._serialise_text(self.json_write)

    def to_bsrt(self) -> bytes:
        '''
        Serialise to BSRT (binary serialised R-tree) bytes
        '''
        return self._serialise_binary(self.bsrt_write)

    def to_dict(self) -> dict:
        '''
        Serialise to Python dict
        '''
        return json.loads(self.to_json())
