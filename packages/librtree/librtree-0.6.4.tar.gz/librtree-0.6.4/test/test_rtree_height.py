import pytest
from librtree import RTree


def test_branch_height_integer():
    rtree = RTree(2)
    assert isinstance(rtree.height, int)

def test_branch_height_empty():
    rtree = RTree(2)
    assert rtree.height == 0

def test_branch_height_one():
    rtree = RTree(2)
    rtree.add_rect(47, (0, 0, 1, 1))
    assert rtree.height == 1

def test_branch_height_two():
    rtree = RTree(2)
    for i in range(rtree.branching_factor + 1):
        rtree.add_rect(i, (i, i, i + 1, i + 1))
    assert rtree.height == 2
