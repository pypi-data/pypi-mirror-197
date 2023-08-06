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
import sys
from typing import TYPE_CHECKING, Tuple, Any
from numbers import Number
import os
from pathlib import Path

import numpy as n
from numpy import ndarray
from apav.pyxutils import _minmax

from apav.qt import QAction, QIcon

if TYPE_CHECKING:
    from apav.analysis.base import AnalysisBase

_thispath = Path(os.path.abspath(os.path.dirname(__file__)))

paths = {
    "toplevel": _thispath / ".." / "..",
    "testdata": _thispath / ".." / "tests",
    "icons": _thispath / ".." / "icons",
}


unicode_map = {
    "deg": "\u00B0",
    "degree": "\u00B0",
    "degrees": "\u00B0",
    "angstrom": "\u212B",
    "angstroms": "\u212B",
    "PHI": "\u03D5",
    "phi": "\u03C6",
    "alpha": "\u03B1",
    "BETA": "\u03D0",
    "beta": "\u03B2",
    "gamma": "\u03B3",
    "theta": "\u03B8",
    "mu": "\u03BC",
    "empty": "\u21B5",
}

_unit_suffix = {"nm": "nm", "nanometer": "nm", "nanometers": "nm", "pm": "pm", "picometer": "pm", "picometers": "pm"}


def data_path(filename: str) -> Path:
    """
    Get file path for a data in the test data directory
    :param filename: filename
    :return: path to file
    """
    fpath = paths["testdata"] / filename
    if not fpath.exists():
        raise FileNotFoundError(f"{filename} does not exist")
    assert fpath.is_file(), f"Filename {filename} is not a file"
    return fpath


def get_icon(name: str) -> QIcon:
    path = paths["icons"] / name
    if not path.exists():
        raise FileNotFoundError(f"Icon {name} was not found")
    assert path.is_file(), f"Icon {name} is not a file"
    return QIcon(str(path))


def make_action(text: str, slot, icon: str = None, tooltip: str = None, checked=None):
    retn = QAction()
    retn.setText(text)
    if icon is not None:
        retn.setIcon(get_icon(icon))
    if tooltip is not None:
        retn.setToolTip(tooltip)
    if isinstance(checked, bool):
        retn.setCheckable(True)
        retn.setChecked(checked)
    retn.triggered.connect(slot)
    return retn


def intervals_intersect(minmax1: Tuple[Number, Number], minmax2: Tuple[Number, Number]) -> bool:
    """
    Determine if two 1-dimensional intervals [first, last) overlap
    """
    if minmax2[0] <= minmax1[0] < minmax2[1]:
        return True
    elif minmax1[0] <= minmax2[0] < minmax1[1]:
        return True
    return False


def native_dtype_byteorder() -> str:
    """
    Get the native byte-order as '<' or '>' for dtype operations
    """
    return (">", "<")[sys.byteorder == "little"]


def array2native_byteorder(array: ndarray) -> ndarray:
    """
    Get an array in the native byte-order if it is different, otherwise return the original array
    :param array: array
    """
    sys_byteorder = native_dtype_byteorder()
    ary_bo = array.dtype.byteorder
    if ary_bo != sys_byteorder:
        return array.byteswap().newbyteorder(sys_byteorder)
    else:
        return array


def minmax(ary: ndarray) -> Tuple[Any, Any]:
    """
    Fast function for finding the min and max values of an array
    """
    assert n.issubdtype(ary.dtype, n.number), "Minmax can only operate on numeric arrays"
    return tuple(_minmax(ary.ravel()))


def unique_vals(array: ndarray) -> ndarray:
    """
    Faster implementation of numpy.unique for int8 or uint8 dtype
    :param array: input array
    """
    if array.dtype in (n.int8, n.uint8):
        return n.argwhere(n.bincount(array.ravel()) != 0).ravel()
    else:
        return n.unique(array)


def unit_string(unit: str, prefix_space: bool = False) -> str:
    """
    Make a unit string, i.e. angstrom symbol

    :param unit: unit
    :param prefix_space: add a space before the prefix
    :return: unit string
    """
    retn = ""
    if prefix_space is True:
        retn += " "
    try:
        return retn + unicode_map[unit]
    except KeyError:
        return retn + _unit_suffix[unit]


_NUMERALS = "0123456789abcdefABCDEF"
_HEXDEC = {v: int(v, 16) for v in (x + y for x in _NUMERALS for y in _NUMERALS)}
LOWERCASE, UPPERCASE = "x", "X"


def hex2rgbF(text: str) -> tuple:
    """
    Convert a hex/HTML color code to RGB fractions
    """
    text = text.replace("#", "")
    rgb = _HEXDEC[text[0:2]], _HEXDEC[text[2:4]], _HEXDEC[text[4:6]]
    return tuple([i / 255.0 for i in rgb])


class modifying:
    """
    Context manager for making changes to Analysis objects without unnecessary calculations. This may be
    useful when dealing with large data and multiple changes need to be made to the analysis, and you do not want to
    reuse the original analysis object. The analysis is automatically recalculated once the context manager exits.

    This is located here to avoid circular imports in the analysis-plotting namespaces.

    The below example code loads a large Roi, calculates a correlation histogram, then modifies 3 of the correlation
    histograms parameters. The correlation histogram is only computed 2 time, at instantiation and when the context
    manager exits.

    >>> from apav.analysis import CorrelationHistogram
    >>> from apav import Roi
    >>> large_roi = Roi.from_epos("path_to_large_roi.epos")
    >>> hist = CorrelationHistogram(large_roi, extents=((50, 100), (25, 75)), bin_width=0.01)
    >>>
    >>> with modifying(hist) as anl:
    >>>     anl.bin_width = 0.2
    >>>     anl.symmetric=True
    >>>     anl.multiplicity="multiples"
    """

    def __init__(self, analysis: "AnalysisBase"):
        self.analysis = analysis

    def __enter__(self):
        self.analysis._update_suppress = True
        return self.analysis

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.analysis._update_suppress = False
        self.analysis._process()
