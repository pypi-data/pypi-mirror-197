import pytest
from librtree import RTreeStyle

from tempfile import TemporaryFile
from contextlib import contextmanager


@contextmanager
def json_fixture(json):
    with TemporaryFile(mode='w+') as io:
        io.write(json)
        io.seek(0)
        yield io

def test_json_read_callable():
    assert callable(RTreeStyle.json_read)

def test_json_read_io():
    with pytest.raises(ValueError, match=r'no fileno attribute'):
        RTreeStyle.json_read(None)

def test_json_read_valid():
    json = '''
        [
          {
            "stroke": {
              "grey": 0.9,
              "width": 1.0
            }
          },
          {
             "fill": {
               "rgb": [0.9, 0.1, 0.1]
             }
          }
        ]
    '''
    with json_fixture(json) as io:
        style = RTreeStyle.json_read(io)
        assert style is not None
        assert isinstance(style, RTreeStyle)

def test_json_read_invalid_json():
    json = '[}'
    with json_fixture(json) as io:
        with pytest.raises(RuntimeError, match=r'reading style'):
            RTreeStyle.json_read(io)

def test_json_read_no_levels():
    json = '[]'
    with json_fixture(json) as io:
        with pytest.raises(RuntimeError, match=r'reading style'):
            RTreeStyle.json_read(io)

def test_json_read_empty_levels():
    json = '[{}, {}]'
    with json_fixture(json) as io:
        style = RTreeStyle.json_read(io)
        assert style is not None
        assert isinstance(style, RTreeStyle)
