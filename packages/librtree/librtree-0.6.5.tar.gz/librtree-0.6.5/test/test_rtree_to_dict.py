import pytest
from librtree import RTree


@pytest.fixture
def rtree():
    rtree = RTree(2)
    rtree.add_rect(43, (0, 0, 1, 1))
    rtree.add_rect(44, (1, 1, 2, 2))
    return rtree


def test_to_dict_hasattr(rtree):
    assert hasattr(rtree, 'to_dict')

def test_to_dict_callable(rtree):
    assert callable(rtree.to_dict)

def test_to_dict_output(rtree):
    data = rtree.to_dict()
    ids = [
        branch['id']
        for branch in data['root']['branches']
    ]
    ids.sort()
    assert ids == [43, 44]
