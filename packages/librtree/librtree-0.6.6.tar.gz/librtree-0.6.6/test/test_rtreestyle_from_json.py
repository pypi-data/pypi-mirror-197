import pytest
from librtree import RTreeStyle


def test_from_json_callable():
    assert callable(RTreeStyle.from_json)

def test_from_json_none():
    with pytest.raises(RuntimeError, match=r'reading style'):
        RTreeStyle.from_json(None)

def test_from_json_valid():
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
    style = RTreeStyle.from_json(json)
    assert style is not None
    assert isinstance(style, RTreeStyle)

def test_from_json_invalid_json():
    json = '[}'
    with pytest.raises(RuntimeError, match=r'reading style'):
        RTreeStyle.from_json(json)

def test_from_json_no_levels():
    json = '[]'
    with pytest.raises(RuntimeError, match=r'reading style'):
        RTreeStyle.from_json(json)

def test_from_json_empty_levels():
    json = '[{}, {}]'
    style = RTreeStyle.from_json(json)
    assert style is not None
    assert isinstance(style, RTreeStyle)
