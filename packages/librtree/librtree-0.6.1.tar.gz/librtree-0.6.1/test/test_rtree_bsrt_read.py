import pytest
from librtree import RTree

from tempfile import TemporaryFile
from contextlib import contextmanager


@pytest.fixture
def rtree():
    rtree = RTree(2)
    rtree.add_rect(43, (0, 0, 1, 1))
    rtree.add_rect(44, (1, 1, 2, 2))
    return rtree

@contextmanager
def bsrt_fixture(rtree):
    with TemporaryFile(mode='wb+') as io:
        io.write(rtree.to_bsrt())
        io.seek(0)
        yield io

def test_bsrt_read_hasattr():
    assert hasattr(RTree, 'bsrt_read')

def test_bsrt_read_callable():
    assert callable(RTree.bsrt_read)

def test_bsrt_read_roundtrip(rtree):
    with bsrt_fixture(rtree) as io:
        rtree2 = RTree.bsrt_read(io)
    assert rtree == rtree2
