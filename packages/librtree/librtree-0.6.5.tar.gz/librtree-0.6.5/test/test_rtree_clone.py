import pytest
from librtree import RTree


def test_clone_empty():
    rtree = RTree(2)
    clone = rtree.clone()
    assert rtree == clone

def test_clone_not_empty():
    rtree = RTree(2)
    rtree.add_rect(47, (0, 0, 1, 4))
    clone = rtree.clone()
    assert rtree == clone
