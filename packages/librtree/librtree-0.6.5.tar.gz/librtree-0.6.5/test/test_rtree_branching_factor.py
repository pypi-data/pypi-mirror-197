import pytest
from librtree import RTree


def test_branching_factor_integer():
    rtree = RTree(1)
    assert isinstance(rtree.branching_factor, int)

def test_branching_factor_greater_than_one():
    rtree = RTree(1)
    assert rtree.branching_factor > 1
