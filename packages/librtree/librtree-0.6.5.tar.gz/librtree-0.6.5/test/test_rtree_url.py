import pytest
from librtree import RTree


def test_string():
    assert type(RTree.url) is str

def test_expected_url():
    assert RTree.url == 'https://gitlab.com/jjg/librtree'
