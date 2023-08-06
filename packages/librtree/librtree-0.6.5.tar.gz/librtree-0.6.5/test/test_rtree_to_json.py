import pytest
import json

from librtree import RTree


@pytest.fixture
def rtree():
    rtree = RTree(2)
    rtree.add_rect(43, (0, 0, 1, 1))
    rtree.add_rect(44, (1, 1, 2, 2))
    return rtree


def test_to_json_hasattr(rtree):
    assert hasattr(rtree, 'to_json')

def test_to_json_callable(rtree):
    assert callable(rtree.to_json)

def test_to_json_parsable(rtree):
    data = json.loads(rtree.to_json())
    ids = [
        branch['id']
        for branch in data['root']['branches']
    ]
    ids.sort()
    assert ids == [43, 44]
