import pytest
from librtree import RTree


def test_branch_size_integer():
    rtree = RTree(1)
    assert isinstance(rtree.branch_size, int)

def test_branch_size_positive():
    rtree = RTree(1)
    assert rtree.branch_size > 0
