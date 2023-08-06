import pytest
from librtree import RTree


def relax(rect_id, ignored):
    return 0

def append(rect_id, rect_ids_list):
    rect_ids_list.append(rect_id)
    return 0

def too_many_args(rect_id, arg, excess):
    return 0

def returns_non_int(rect_id, arg):
    return "0"

def test_search_empty():
    rtree = RTree(2)
    ids = []
    rect = (0, 0, 1, 1)
    result = rtree.search(append, rect, ids)
    assert result is None
    assert not ids

@pytest.fixture
def rtree_nonempty():
    rtree = RTree(2)
    rtree.add_rect(47, (0, 0, 1, 1))
    return rtree

def test_search_nonempty_disjoint(rtree_nonempty):
    rect = (2, 2, 3, 3)
    ids = []
    result = rtree_nonempty.search(append, rect, ids)
    assert result is None
    assert not ids

def test_search_nonempty_intersect(rtree_nonempty):
    rect = (0.5, 0.5, 1, 1)
    ids = []
    result = rtree_nonempty.search(append, rect, ids)
    assert result is None
    assert ids == [47]

def test_search_nonempty_bad_rect_size(rtree_nonempty):
    rect = (0.5, 0.5, 1)
    ids = []
    with pytest.raises(ValueError, match=r'bad coordinate tuple'):
        rtree_nonempty.search(append, rect, ids)
    assert not ids

def test_search_nonempty_callback_none(rtree_nonempty):
    ids = []
    rect = (0.5, 0.5, 1, 1)
    with pytest.raises(TypeError, match=r'not callable'):
        rtree_nonempty.search(None, rect, ids)

def test_search_nonempty_rect_none(rtree_nonempty):
    ids = []
    with pytest.raises(TypeError, match=r'not a tuple'):
        rtree_nonempty.search(append, None, ids)

def test_search_nonempty_context_none(rtree_nonempty):
    rect = (0.5, 0.5, 1, 1)
    result = rtree_nonempty.search(relax, rect, None)
    assert result is None

def test_search_nonempty_callback_too_many_args(rtree_nonempty):
    rect = (0.5, 0.5, 1, 1)
    with pytest.raises(TypeError, match=r'missing 1 required'):
        rtree_nonempty.search(too_many_args, rect, None)

def test_search_nonempty_callback_returns_non_int(rtree_nonempty):
    rect = (0.5, 0.5, 1, 1)
    match = r'integer is required|cannot be interpreted'
    with pytest.raises(TypeError, match=match):
        rtree_nonempty.search(returns_non_int, rect, None)
