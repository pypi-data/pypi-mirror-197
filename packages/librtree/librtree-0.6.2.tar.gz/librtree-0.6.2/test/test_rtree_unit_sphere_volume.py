import pytest
from librtree import RTree
from math import pi

def test_branch_unit_sphere_volume_float():
    rtree = RTree(1)
    vol = rtree.unit_sphere_volume
    assert isinstance(vol, float)

def test_branch_unit_sphere_volume_1():
    rtree = RTree(1)
    vol = rtree.unit_sphere_volume
    assert vol == pytest.approx(2)

def test_branch_unit_sphere_volume_2():
    rtree = RTree(2)
    vol = rtree.unit_sphere_volume
    assert vol == pytest.approx(pi)

def test_branch_unit_sphere_volume_3():
    rtree = RTree(3)
    vol = rtree.unit_sphere_volume
    assert vol == pytest.approx(4 * pi / 3)
