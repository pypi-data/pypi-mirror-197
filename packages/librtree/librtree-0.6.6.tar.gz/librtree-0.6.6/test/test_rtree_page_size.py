import pytest
from librtree import RTree


def test_page_size_integer():
    rtree = RTree(1)
    assert isinstance(rtree.page_size, int)

def test_page_size_positive():
    rtree = RTree(1)
    assert rtree.page_size > 0

def test_page_size_dyadic():
    rtree = RTree(1)
    n = rtree.page_size
    assert n & (n - 1) == 0
