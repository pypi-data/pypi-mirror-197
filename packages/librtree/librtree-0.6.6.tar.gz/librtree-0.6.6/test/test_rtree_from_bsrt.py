import pytest
from librtree import RTree


@pytest.fixture
def rtree():
    rtree = RTree(2)
    rtree.add_rect(43, (0, 0, 1, 1))
    rtree.add_rect(44, (1, 1, 2, 2))
    return rtree

def test_from_bsrt_hasattr():
    assert hasattr(RTree, 'from_bsrt')

def test_from_bsrt_callable():
    assert callable(RTree.from_bsrt)

def test_from_bsrt_roundtrip(rtree):
    rtree2 = RTree.from_bsrt(rtree.to_bsrt())
    assert rtree == rtree2
