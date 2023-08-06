import pytest
from librtree import RTree

from tempfile import TemporaryFile
from contextlib import contextmanager


@pytest.fixture
def rtree():
    rtree = RTree(2)
    rtree.add_rect(43, (0, 0, 1, 1))
    rtree.add_rect(44, (1, 1, 2, 2))
    return rtree

@contextmanager
def json_fixture(rtree):
    with TemporaryFile(mode='w+') as io:
        io.write(rtree.to_json())
        io.seek(0)
        yield io

def test_json_read_hasattr():
    assert hasattr(RTree, 'json_read')

def test_json_read_callable():
    assert callable(RTree.json_read)

def test_json_read_roundtrip(rtree):
    with json_fixture(rtree) as io:
        rtree2 = RTree.json_read(io)
    assert rtree == rtree2
