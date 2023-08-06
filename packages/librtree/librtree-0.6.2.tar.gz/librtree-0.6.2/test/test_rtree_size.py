import pytest
from librtree import RTree


def test_size_empty_integer():
    rtree = RTree(1)
    assert isinstance(rtree.size, int)

def test_size_empty_positive():
    rtree = RTree(1)
    assert rtree.size > 0
