import pytest
from librtree import RTree


def test_node_size_integer():
    rtree = RTree(1)
    assert isinstance(rtree.node_size, int)

def test_node_size_positive():
    rtree = RTree(1)
    assert rtree.node_size > 0
