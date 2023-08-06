import pytest
from librtree import RTree


def test_is_empty_created():
    rtree = RTree(2)
    assert rtree.is_empty

def test_is_empty_rect_added():
    rtree = RTree(2)
    rtree.add_rect(3, (0, 0, 1, 1))
    assert not rtree.is_empty
