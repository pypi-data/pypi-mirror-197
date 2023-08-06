import pytest
import os
import json

from librtree import RTree
from tempfile import TemporaryDirectory


@pytest.fixture
def rtree():
    rtree = RTree(2)
    rtree.add_rect(43, (0, 0, 1, 1))
    rtree.add_rect(44, (1, 1, 2, 2))
    return rtree

def test_json_write_hasattr(rtree):
    assert hasattr(rtree, 'json_write')

def test_json_write_callable(rtree):
    assert callable(rtree.json_write)

def test_json_write_none(rtree):
    with pytest.raises(ValueError, match=r'no fileno'):
        rtree.json_write(None)

def test_json_write_io_not_writeable(rtree):
    with TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, 'file.json')
        with open(path, 'w') as io:
            io.write('')
        with open(path, 'r') as io:
            with pytest.raises(RuntimeError, match=r'Invalid argument'):
                rtree.json_write(io)

def test_json_write_io_writeable(rtree):
    with TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, 'file.json')
        with open(path, 'w') as io:
            rtree.json_write(io)
        assert os.path.exists(path)
        with open(path, 'r') as io:
            data = json.load(io)
        ids = [
            branch['id']
            for branch in data['root']['branches']
        ]
        ids.sort()
        assert ids == [43, 44]
