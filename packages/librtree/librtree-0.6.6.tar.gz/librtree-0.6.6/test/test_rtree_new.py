import pytest
from librtree import RTree


def test_new_not_none():
    assert RTree(1) is not None

def test_new_expected_type():
    assert isinstance(RTree(1), RTree)

def test_new_zero_dimension():
    with pytest.raises(ValueError):
        RTree(0)

def test_new_negative_dimension():
    with pytest.raises(ValueError):
        RTree(-1)

def test_new_split_quadratic():
    assert RTree(1, split='quadratic') is not None

def test_new_split_linear():
    assert RTree(1, split='linear') is not None

def test_new_split_greene():
    assert RTree(1, split='greene') is not None

def test_new_split_invalid():
    with pytest.raises(ValueError):
        RTree(1, split='invalid')

def test_new_node_page_zero():
    assert RTree(1, node_page=0) is not None

def test_new_node_page_nonzero():
    assert RTree(1, node_page=4) is not None

def test_new_node_page_invalid():
    with pytest.raises(ValueError):
        RTree(1, node_page=4086)
