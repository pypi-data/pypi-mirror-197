"""
This file is part of APAV.

APAV is a python package for performing analysis and visualization on
atom probe tomography data sets.

Copyright (C) 2018 Jesse Smith

APAV is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

APAV is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with APAV.  If not, see <http://www.gnu.org/licenses/>.
"""

from pytest import raises
from apav.utils import helpers as hlp
from apav.utils import version
import apav
import os
import numpy as n


def test_paths():
    for name, path in hlp.paths.items():
        assert path.exists()
        assert path.is_dir()
        # should not be empty
        assert len(os.listdir(path)) > 0


class TestDataPath:
    def test_does_not_exist(self):
        with raises(FileNotFoundError):
            hlp.data_path("not_real_file")

    def test_is_not_a_file(self):
        with raises(AssertionError):
            hlp.data_path(".")

    def test_existing_file(self):
        fpath = hlp.data_path("Si.pos")
        assert fpath.exists()


class TestGetIcon:
    def test_icon_does_not_exist(self):
        with raises(FileNotFoundError):
            hlp.get_icon("not_real_icon")

    def test_is_not_a_file(self):
        with raises(AssertionError):
            hlp.get_icon(".")

    def test_exists(self):
        icon = hlp.get_icon("saveas.svg")
        assert not icon.isNull()


def test_version():
    if apav.__version__ == "unknown":
        with raises(ValueError):
            version.version_tuple()
    else:
        version.version_tuple()


def test_array2native_byteorder():
    native = hlp.native_dtype_byteorder()
    non_native = "<" if native == ">" else ">"
    assert native != non_native

    ary_non_native = n.array([4], dtype=f"{non_native}f4")
    ary_native = hlp.array2native_byteorder(ary_non_native)

    assert n.allclose(ary_native, ary_non_native)
    assert ary_native.dtype.byteorder == native
    assert ary_non_native.dtype.byteorder == non_native


class TestMinMax:
    def test_floating(self):
        array = n.arange(5) - 2.5
        min, max = hlp.minmax(array)
        assert n.isclose(min, -2.5)
        assert n.isclose(max, 1.5)
        assert isinstance(min, float)
        assert isinstance(max, float)

    def test_integral(self):
        array = n.arange(9).astype(int)
        min, max = hlp.minmax(array)
        assert min == 0
        assert max == 8
        assert isinstance(min, int)
        assert isinstance(max, int)

    def test_nonnumeric_fails(self):
        array = n.array(["asdf", "1234"])
        with raises(AssertionError):
            min, max = hlp.minmax(array)

    def test_constant_array(self):
        val = -4
        array = n.ones(10000) * val
        min, max = hlp.minmax(array)
        assert n.isclose(min, val)
        assert n.isclose(max, val)


class TestUniqueVals:
    def test_equal_to_numpy_unique(self):
        array = n.arange(100).astype(n.int8)
        assert n.array_equal(hlp.unique_vals(array), n.unique(array))

    def test_accept_non_ints(self):
        array = n.arange(9) - 0.5
        hlp.unique_vals(array)
