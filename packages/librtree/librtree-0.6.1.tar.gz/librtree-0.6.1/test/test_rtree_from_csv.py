import pytest
from librtree import RTree


@pytest.fixture
def csv():
    return '''
      1, 0, 0, 1, 1
      2, 1, 1, 2, 3
    '''.strip()

def test_from_csv_hasattr():
    assert hasattr(RTree, 'from_csv')

def test_from_csv_callable():
    assert callable(RTree.from_csv)

def test_from_csv_valid(csv):
    rtree = RTree.from_csv(csv, 2)
    assert isinstance(rtree, RTree)

def test_from_csv_no_dimension(csv):
    with pytest.raises(TypeError):
        RTree.from_csv(csv)

def test_from_csv_valid_split(csv):
    rtree = RTree.from_csv(csv, 2, split='linear')
    assert isinstance(rtree, RTree)

def test_from_csv_invalid_split(csv):
    with pytest.raises(ValueError, match=r'bad split'):
        RTree.from_csv(csv, 2, split='banana')
