import pytest
from librtree import RTree


@pytest.fixture
def rtree():
    return RTree(2)


def test_add_rect_good_arguments(rtree):
    rtree.add_rect(47, (0, 0, 1, 1))

def test_add_rect_non_integer_id(rtree):
    with pytest.raises(TypeError):
        rtree.add_rect('not an integer', (0, 0, 1, 1))

def test_add_rect_non_iterable_coords(rtree):
    with pytest.raises(TypeError):
        rtree.add_rect(47, None)

def test_add_rect_non_float_coords(rtree):
    with pytest.raises(TypeError):
        rtree.add_rect(47, (0, 0, '1', 1))

def test_add_rect_too_few_coords(rtree):
    with pytest.raises(ValueError):
        rtree.add_rect(47, (0, 0, 1))

def test_add_rect_too_many_coords(rtree):
    with pytest.raises(ValueError):
        rtree.add_rect(47, (0, 0, 1, 1, 1))

def test_add_rect_inconsistent_coords(rtree):
    with pytest.raises(RuntimeError):
        rtree.add_rect(47, (1, 1, 0, 0))

def test_add_rect_degenerate_coords(rtree):
    rtree.add_rect(47, (0, 0, 0, 1))

def test_add_rect_list_of_coords(rtree):
    rtree.add_rect(47, [0, 0, 1, 1])
