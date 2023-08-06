import pytest
from librtree import RTreeStyle


def test_from_list_callable():
    assert callable(RTreeStyle.from_list)

def test_from_list_none():
    with pytest.raises(RuntimeError, match=r'reading style'):
        RTreeStyle.from_list(None)

def test_from_list_valid():
    levels = (
        {
            "stroke": {
                "grey": 0.9,
                "width": 1.0
            }
        },
        {
            "fill": {
                "rgb": (0.9, 0.1, 0.1)
            }
        }
    )
    style = RTreeStyle.from_list(levels)
    assert style is not None
    assert isinstance(style, RTreeStyle)

def test_from_list_no_levels():
    levels = []
    with pytest.raises(RuntimeError, match=r'reading style'):
        RTreeStyle.from_list(levels)

def test_from_list_empty_levels():
    levels = [{}, {}]
    style = RTreeStyle.from_list(levels)
    assert style is not None
    assert isinstance(style, RTreeStyle)
