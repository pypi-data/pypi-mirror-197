import pytest
from librtree import RTree


@pytest.fixture
def rtree():
    rtree = RTree(2)
    rtree.add_rect(43, (0, 0, 1, 1))
    rtree.add_rect(44, (1, 1, 2, 2))
    return rtree


def test_to_bsrt_hasattr(rtree):
    assert hasattr(rtree, 'to_bsrt')

def test_to_bsrt_callable(rtree):
    assert callable(rtree.to_bsrt)

def test_to_bsrt_string(rtree):
    data = rtree.to_bsrt()
    assert isinstance(data, bytes)
    assert data[0:4] == b'BSRt'
