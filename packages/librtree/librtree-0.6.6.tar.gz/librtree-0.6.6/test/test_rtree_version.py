import pytest
from librtree import RTree


def test_tuple():
    assert type(RTree.version) is tuple

def test_length():
    assert len(RTree.version) == 3

def test_all_are_integers():
    for n in RTree.version:
        assert type(n) is int

def test_major_at_least_one():
    assert RTree.version[0] >= 1
