import pytest
from librtree import RTree


def test_dim_1():
    rtree = RTree(1)
    assert rtree.dim == 1

def test_dim_2():
    rtree = RTree(2)
    assert rtree.dim == 2

def test_dim_3():
    rtree = RTree(3)
    assert rtree.dim == 3
