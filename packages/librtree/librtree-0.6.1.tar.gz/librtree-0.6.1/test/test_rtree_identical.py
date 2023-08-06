import pytest
from librtree import RTree


def test_identical_different_class():
    rtree = RTree(2)
    assert rtree != 'rtree'

def test_identical_same_object():
    rtree = RTree(2)
    assert rtree == rtree

def test_identical_different_dimension():
    rtree1 = RTree(1)
    rtree2 = RTree(2)
    assert rtree1 != rtree2

def test_identical_empty():
    rtree1 = RTree(2)
    rtree2 = RTree(2)
    assert rtree1 == rtree2

def test_identical_not_empty():
    rtree1 = RTree(2)
    rtree2 = RTree(2)
    rtree1.add_rect(1, [0, 0, 1, 1])
    rtree2.add_rect(1, [0, 0, 1, 1])
    assert rtree1 == rtree2

def test_identical_different_ids():
    rtree1 = RTree(2)
    rtree2 = RTree(2)
    rtree1.add_rect(1, [0, 0, 1, 1])
    rtree2.add_rect(2, [0, 0, 1, 1])
    assert rtree1 != rtree2

def test_identical_different_rectangles():
    rtree1 = RTree(2)
    rtree2 = RTree(2)
    rtree1.add_rect(1, [0, 0, 1, 1])
    rtree2.add_rect(1, [0, 0, 1, 2])
    assert rtree1 != rtree2
