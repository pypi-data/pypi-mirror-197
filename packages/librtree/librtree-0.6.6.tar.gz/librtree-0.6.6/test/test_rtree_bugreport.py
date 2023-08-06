import pytest
from librtree import RTree


def test_string():
    assert type(RTree.bugreport) is str

def test_expected_email():
    assert RTree.bugreport == 'j.j.green@gmx.co.uk'
