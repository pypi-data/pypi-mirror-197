import pytest
from librtree import RTree

from tempfile import TemporaryFile
from contextlib import contextmanager


@contextmanager
def csv_fixture(csv):
    with TemporaryFile(mode='w+') as io:
        io.write(csv)
        io.seek(0)
        yield io

def test_csv_read_callable():
    assert callable(RTree.csv_read)

def test_csv_read_io():
    with pytest.raises(ValueError, match=r'no fileno attribute'):
        RTree.csv_read(None, 2)

def test_csv_read_empty():
    with csv_fixture('') as io:
        rtree = RTree.csv_read(io, 2)
        assert rtree is not None
        assert isinstance(rtree, RTree)
        assert rtree.is_empty

def test_csv_read_nonempty():
    csv = '''
      1, 0, 0, 1, 1
      2, 1, 1, 2, 3
    '''.strip()
    with csv_fixture(csv) as io:
        rtree = RTree.csv_read(io, 2)
        assert rtree is not None
        assert isinstance(rtree, RTree)
        assert not rtree.is_empty

def test_csv_read_shortline():
    csv = '''
      1, 0, 0, 1, 1
      2, 1, 1, 2
    '''.strip()
    with pytest.raises(RuntimeError, match=r'reading csv'):
        with csv_fixture(csv) as io:
            RTree.csv_read(io, 2)

def test_csv_read_bad_split():
    with pytest.raises(ValueError, match=r'bad split'):
        with csv_fixture('') as io:
            RTree.csv_read(io, 2, split='unknown')

def test_csv_read_bad_node_page():
    with pytest.raises(TypeError, match=r'unsupported operand'):
        with csv_fixture('') as io:
            RTree.csv_read(io, 2, node_page='not an integer')
