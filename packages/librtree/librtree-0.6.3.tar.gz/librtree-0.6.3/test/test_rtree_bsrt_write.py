import pytest
import os

from librtree import RTree
from tempfile import TemporaryDirectory


@pytest.fixture
def rtree():
    rtree = RTree(2)
    rtree.add_rect(43, (0, 0, 1, 1))
    rtree.add_rect(44, (1, 1, 2, 2))
    return rtree

def test_bsrt_write_hasattr(rtree):
    assert hasattr(rtree, 'bsrt_write')

def test_bsrt_write_callable(rtree):
    assert callable(rtree.bsrt_write)

def test_bsrt_write_none(rtree):
    with pytest.raises(ValueError, match=r'no fileno'):
        rtree.bsrt_write(None)

def test_bsrt_write_io_not_writeable(rtree):
    with TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, 'file.bsrt')
        with open(path, 'w') as io:
            io.write('')
        with open(path, 'r') as io:
            with pytest.raises(RuntimeError, match=r'Invalid argument'):
                rtree.bsrt_write(io)

def test_bsrt_write_io_writeable(rtree):
    with TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, 'file.bsrt')
        with open(path, 'w') as io:
            rtree.bsrt_write(io)
        assert os.path.exists(path)
