#cython: language_level=3
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
import cython

from libc.stdio cimport printf
from cython cimport floating, integral
from cpython cimport array as carray
import numpy as n
from typing import Tuple, Any


ctypedef fused real:
    floating
    integral


@cython.boundscheck(False)
@cython.wraparound(False)
def _minmax(real[:] array) -> n.ndarray:
    cdef real retn[2]
    cdef real[:] retn_view = retn
    retn_view[0] = array[0]
    retn_view[1] = array[0]

    cdef real val = 0
    cdef Py_ssize_t i = 0
    with nogil:
        for i in range(array.shape[0]):
            val = array[i]
            if val > retn_view[1]:
                retn_view[1] = val
            if val < retn_view[0]:
                retn_view[0] = val

    return retn
