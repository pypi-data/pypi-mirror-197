import pytest
from librtree import RTree


def test_rect_size_integer():
    rtree = RTree(1)
    assert isinstance(rtree.rect_size, int)

def test_rect_size_positive():
    rtree = RTree(1)
    assert rtree.rect_size > 0
