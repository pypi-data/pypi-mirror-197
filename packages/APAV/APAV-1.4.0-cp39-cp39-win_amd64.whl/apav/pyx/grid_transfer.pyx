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

import numpy as n
import cython
from cython cimport integral, floating
from libc cimport math
from cython.parallel cimport prange
cimport openmp
from multiprocessing import cpu_count

cdef integral low(integral val1, integral val2) nogil:
    if val1 > val2:
        return val2
    else:
        return val1


cdef integral high(integral val1, integral val2) nogil:
    if val1 > val2:
        return val1
    else:
        return val2


@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
def transfer(floating[:, :, :] X,
             floating[:, :, :] Y,
             floating[:, :, :] Z,
             floating[:, :] pos,
             floating stddev3):
    """
    C-extension for computing first pass delocalization based on a gaussian transfer function
    :param X: voxel centers array in x axis
    :param Y: voxel centers array in y axis
    :param Z: voxel centers array in z axis
    :param pos: Array of positions
    :param stddev3: Third standard deviation of gaussian
    """
    assert stddev3 > 0, "stddev3 must be positive non-zero"

    cdef double bin_width = X[1, 0, 0] - X[0, 0, 0]
    assert bin_width > 0, "Bin width must be positive non-zero"

    cdef double r = bin_width/2

    cdef int kernel_dim = 3  # 3x3 px
    cdef double XYZ_min[3]
    XYZ_min[0] = n.min(X)
    XYZ_min[1] = n.min(Y)
    XYZ_min[2] = n.min(Z)

    cdef int x_dim = X.shape[0]
    cdef int y_dim = Y.shape[1]
    cdef int z_dim = Z.shape[2]

    # Kernel dimensions must be odd
    assert kernel_dim % 2 == 1
    cdef int k_half = (kernel_dim - 1) // 2
    cdef int num_threads = cpu_count()

    retn = n.zeros((num_threads, X.shape[0], Y.shape[1], Z.shape[2]))
    cdef double[:, :, :, :] retn_view = retn

    cdef double s = stddev3/3

    cdef Py_ssize_t N0 = pos.shape[0]
    cdef Py_ssize_t N1 = pos.shape[1]
    assert N1 == 3

    cdef double x, y, z
    cdef Py_ssize_t i = 0
    cdef Py_ssize_t idx0 = 0
    cdef Py_ssize_t idx1 = 0
    cdef Py_ssize_t idx2 = 0

    cdef Py_ssize_t xid0 = 0
    cdef Py_ssize_t xid1 = 0
    cdef Py_ssize_t yid0 = 0
    cdef Py_ssize_t yid1 = 0
    cdef Py_ssize_t zid0 = 0
    cdef Py_ssize_t zid1 = 0

    cdef double kern_sum = 0
    cdef int thread_num = 0

    cdef Py_ssize_t kx, ky, kz
    cdef Py_ssize_t ix, iy, iz

    kern = n.zeros([num_threads, kernel_dim, kernel_dim, kernel_dim])
    cdef double[:, :, :, :] kern_view = kern

    with nogil:
        for i in prange(N0, num_threads=num_threads):
            thread_num = openmp.omp_get_thread_num()
            x = pos[i, 0]
            y = pos[i, 1]
            z = pos[i, 2]
            idx0 = int((x - (XYZ_min[0] - r)) // bin_width)
            idx1 = int((y - (XYZ_min[1] - r)) // bin_width)
            idx2 = int((z - (XYZ_min[2] - r)) // bin_width)

            xid0 = high(idx0 - k_half, 0)
            xid1 = low(idx0 + k_half + 1, x_dim)
            yid0 = high(idx1 - k_half, 0)
            yid1 = low(idx1 + k_half + 1, y_dim)
            zid0 = high(idx2 - k_half, 0)
            zid1 = low(idx2 + k_half + 1, z_dim)

            kern_sum = 0

            for ix, kx in enumerate(range(xid0, xid1)):
                for iy, ky in enumerate(range(yid0, yid1)):
                    for iz, kz in enumerate(range(zid0, zid1)):
                        kern_view[thread_num, ix, iy, iz] = math.exp(-((X[kx, ky, kz] - x) ** 2 +
                                                           (Y[kx, ky, kz] - y) ** 2 +
                                                           (Z[kx, ky, kz] - z) ** 2) / (2 * s ** 2))
                        kern_sum = kern_sum + kern_view[thread_num, ix, iy, iz]

            for ix, kx in enumerate(range(xid0, xid1)):
                for iy, ky in enumerate(range(yid0, yid1)):
                    for iz, kz in enumerate(range(zid0, zid1)):
                        retn_view[thread_num, kx, ky, kz] += kern_view[thread_num, ix, iy, iz] / kern_sum

    out = n.sum(retn, axis=0)

    return out