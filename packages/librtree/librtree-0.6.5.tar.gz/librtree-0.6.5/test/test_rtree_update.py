import pytest
from librtree import RTree


@pytest.fixture
def rtree():
    rtree = RTree(2)
    rtree.add_rect(1, (0, 0, 1, 1))
    rtree.add_rect(2, (1, 1, 2, 3))
    return rtree

def test_update_identity(rtree):
    def cb(rect_id, rect, ignored):
        return rect
    rtree2 = rtree.clone()
    rtree2.update(cb, None)
    assert rtree == rtree2

def test_update_xshift(rtree):
    def cb(rect_id, rect, shift):
        x0, y0, x1, y1 = rect
        return (x0 + shift, y0, x1 + shift, y1)
    rtree2 = rtree.clone()
    rtree2.update(cb, 1)
    assert rtree != rtree2
    rtree2.update(cb, -1)
    assert rtree == rtree2

def test_update_bad_args(rtree):
    def cb(rect_id, rect):
        return rect
    with pytest.raises(TypeError, match=r'takes 2 positional'):
        rtree.update(cb, None)

def test_update_return_non_tuple(rtree):
    def cb(rect_id, rect, context):
        return None
    with pytest.raises(TypeError, match=r'non-tuple'):
        rtree.update(cb, None)

def test_update_return_bad_size(rtree):
    def cb(rect_id, rect, context):
        return (0, 0, 1, 1, 1)
    with pytest.raises(ValueError, match=r'5-tuple'):
        rtree.update(cb, None)

def test_update_return_bad_type(rtree):
    def cb(rect_id, rect, context):
        return (0, 0, None, 1)
    with pytest.raises(TypeError, match=r'contains non-float'):
        rtree.update(cb, None)
