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

from typing import Sequence, Tuple, List, Dict, Any, Union, Type, Optional, TYPE_CHECKING
from numbers import Real, Number
from numpy import ndarray

from apav.analysis.base import AnalysisBase
from apav.utils import validate
from apav import Roi, RangeCollection, Ion
from apav.core.histogram import histogram2d_binwidth
from apav.core.multipleevent import get_mass_indices
from apav.core.isotopic import Element
from scipy.ndimage import gaussian_filter
import numpy as n
import multiprocessing as mp

from apav.analysis.grid_transfer import transfer as _transfer


def ion_transfer(X: n.ndarray, Y: n.ndarray, Z: n.ndarray, pos: n.ndarray, stddev3: Number) -> ndarray:
    """
    Transfer an array of ion positions to a binned grid.

    :param X: 3D array of x-coordinates of grid
    :param Y: 3D array of y-coordinates of grid
    :param Y: 3D array of z-coordinates of grid
    :param pos: 2D array of positions
    :param stddev3: 3sigma standard deviation of gaussian distribution
    :return: 3D array of counts
    """
    if len(pos.shape) != 2:
        raise ValueError("Positions must be a 2D array")
    if pos.size == 0:
        raise ValueError("At least one ion position must be provided")
    if any(len(i.shape) != 3 for i in [X, Y, Z]):
        raise ValueError("All grid coordinate arrays must be three-dimensional")

    validate.positive_number(stddev3)

    if n.isclose(stddev3, 0):
        binx = X[1, 0, 0] - X[0, 0, 0]
        biny = Y[0, 1, 0] - Y[0, 0, 0]
        binz = Z[0, 0, 1] - Z[0, 0, 0]
        x_edge = n.concatenate([X[:, 0, 0] - binx / 2, [X[-1, 0, 0] + binx / 2]])
        y_edge = n.concatenate([Y[0, :, 0] - biny / 2, [Y[0, -1, 0] + biny / 2]])
        z_edge = n.concatenate([Z[0, 0, :] - binz / 2, [Z[0, 0, -1] + binz / 2]])
        counts, _ = n.histogramdd(pos, bins=(x_edge, y_edge, z_edge))
        return counts
    else:
        return _transfer(
            X.astype(n.double), Y.astype(n.double), Z.astype(n.double), pos.astype(n.double), float(stddev3)
        )


def make_coordinate_grids(
    extents: Sequence[Tuple[Number, Number]], bin_width: Union[Sequence[Number], Number], edges=False
) -> Tuple[ndarray, ndarray, ndarray]:
    """
    Generate 3D x/y/z coordinate arrays for indexing into compositional grids

    :param extents: The x/y/z extent to generate the grids for
    :param bin_width: The bin width of each bin, a single number or sequence of numbers for each dimension
    :param edges: Whether the coordinates represent the edges of the bins or centers
    """
    assert len(extents) == 3

    for i in extents:
        validate.interval(i)

    assert all(len(i) == 2 for i in extents)

    if hasattr(bin_width, "__iter__"):
        assert len(bin_width) == 3

    if isinstance(bin_width, (float, int)):
        bin_width = [
            bin_width,
        ] * 3

    bin_width = [float(i) for i in bin_width]

    validate.all_positive_nonzero(bin_width)

    ext_x, ext_y, ext_z = extents
    dx = n.abs(n.diff(ext_x)[0])
    dy = n.abs(n.diff(ext_y)[0])
    dz = n.abs(n.diff(ext_z)[0])
    nx = int(n.ceil(dx / bin_width[0]))
    ny = int(n.ceil(dy / bin_width[1]))
    nz = int(n.ceil(dz / bin_width[2]))

    x = n.array([ext_x[0] + i * bin_width[0] for i in range(nx)])
    y = n.array([ext_y[0] + i * bin_width[1] for i in range(ny)])
    z = n.array([ext_z[0] + i * bin_width[2] for i in range(nz)])

    if x[-1] % 1 == 0:
        x = n.concatenate([x, x[-1] + [bin_width[0]]])
        y = n.concatenate([y, y[-1] + [bin_width[1]]])
        z = n.concatenate([z, z[-1] + [bin_width[2]]])

    if edges is True:
        x -= bin_width[0] / 2
        y -= bin_width[1] / 2
        z -= bin_width[2] / 2

        x = n.concatenate([x, [x[-1] + bin_width[0]]])
        y = n.concatenate([y, [y[-1] + bin_width[1]]])
        z = n.concatenate([z, [z[-1] + bin_width[2]]])

    return n.meshgrid(x, y, z, indexing="ij")


class RangedGrid(AnalysisBase):
    """
    Compute the ionic and elemental composition spatially distributed among a structured grid
    """

    def __init__(
        self,
        roi: Roi,
        ranges: RangeCollection,
        bin_width: Number = 1,
        first_pass: bool = True,
        delocalization: Union[Number, Sequence[Number]] = n.array([3, 3, 1.5]),
        gauss_trunc: Number = 4,
    ):
        """
        :param roi: Parent the RangedGrid is competed on
        :param ranges: RangeCollection defining the ranges
        :param bin_width: symmetric bin width size
        :param first_pass: Whether the first pass delocalization is computed using a gaussian transfer function.
        :param delocalization: The delocalization distances (as 3 standard deviations of a normal distribution)
        :param gauss_trunc: Number of standard deviations to truncate the gaussian kernel for second pass delocalization
        """
        super().__init__(roi)
        self._ranges = validate.is_type(ranges, RangeCollection)
        self._voxel = float(validate.positive_nonzero_number(bin_width))

        if isinstance(delocalization, Real):
            self._delocalization = n.array([delocalization])
        else:
            self._delocalization = n.array(delocalization)

        if len(self._delocalization.shape) == 1 and self._delocalization.shape[0] == 1:
            self._delocalization = n.ones(3) * self._delocalization[0]

        if not all(i > 0 for i in self._delocalization):
            raise ValueError("Delocalization distances must be positive and non-zero")

        if self._delocalization.shape[0] != 3:
            raise ValueError(f"Unexpected delocalization shape, expected 3 got {self._delocalization.shape[0]}")

        self._gauss_trunc = validate.positive_nonzero_number(gauss_trunc)

        self._X = ndarray([])
        self._Y = ndarray([])
        self._Z = ndarray([])
        self._ion_counts = {}
        self._elem_counts_array = ndarray([])
        self._elem_frac = {}
        self._elem_counts = {}
        self._elem_cum_counts = None
        self._first_pass = first_pass

        self._calculate()

    @property
    def ranges(self) -> RangeCollection:
        """
        The ranges used for ranging the mass spectrum
        """
        return self._ranges

    @property
    def extents(self) -> Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]]:
        """
        Get the spatial extents (by center positions) of the grids
        """
        return (
            (self._X.min(), self._X.max()),
            (self._Y.min(), self._Y.max()),
            (self._Z.min(), self._Z.max()),
        )

    @property
    def first_pass(self) -> bool:
        """
        Whether to compute first pass delocalization
        """
        return self._first_pass

    @property
    def centers(self) -> Tuple[ndarray, ndarray, ndarray]:
        """
        The center positions of the structured grids

        For MxNxP voxels this returns 3 arrays of dimensions: Mx1x1, 1xNx1, 1x1xP
        """
        return self._X, self._Y, self._Z

    @property
    def bin_width(self) -> float:
        """
        Bin width of the voxels
        """
        return self._voxel

    @property
    def delocalization(self) -> ndarray:
        """
        Amount of smoothing used during the delocalization process
        """
        return self._delocalization

    @property
    def gauss_trunc(self) -> Number:
        """
        Where to truncate the gaussian kernel for second pass delocalization
        """
        return self._gauss_trunc

    @property
    def all_ionic_counts(self) -> Dict[Ion, ndarray]:
        """
        Get all ionic count grids in a dict
        """
        return self._ion_counts

    @property
    def all_elemental_frac(self) -> Dict[Element, ndarray]:
        """
        Get all elemental fraction grids as a dict
        """
        return self._elem_frac

    @property
    def all_elemental_frac_str(self) -> Dict[str, ndarray]:
        """
        Get all elemental fraction grids as a dictionary (using elemental symbols)
        """
        return {i.symbol: j for i, j in self._elem_frac.items()}

    @property
    def elemental_counts_total(self) -> Number:
        """
        Get the total (sum) of all elemental counts
        """
        return self._elem_cum_counts

    @property
    def elemental_counts_grid(self) -> ndarray:
        """
        Get an array of the cumulative elemental counts in each bin
        """
        return self._elem_counts_array

    def ionic_counts(self, ion: Ion) -> ndarray:
        """
        Get a single ionic counts grid
        :param ion: The ion of the grid to return
        """
        if ion not in self.all_ionic_counts.keys():
            raise ValueError("Ion {} does not exist in the RangedGrid".format(ion.hill_formula))
        return self.all_ionic_counts[ion]

    def elemental_frac(self, element: Union[str, Element]) -> ndarray:
        """
        Get a single elemental fraction grid
        :param element: the elemental of the grid to return (Element or str)
        """
        if isinstance(element, str):
            el = None
            for i, j in self.all_elemental_frac.items():
                if i.symbol == element:
                    el = i
                    break
            return self.all_elemental_frac[el]
        elif isinstance(element, Element):
            return self.all_elemental_frac[element]
        else:
            raise TypeError("Expected elemental symbol string or Element type, got {} instead".format(type(element)))

    def _calculate(self):
        """
        Compute the ranged grids
        """
        dims = self.roi.dimensions
        n_voxels = n.ceil(dims / self.bin_width).ravel().astype(int)

        dx, dy, dz = self.roi.xyz_extents
        range_elems = self.ranges.elements()

        self._ion_counts = {i.ion: n.zeros(n_voxels) for i in self.ranges.ranges}

        r = self.bin_width / 2
        X, Y, Z = make_coordinate_grids(self.roi.xyz_extents, self.bin_width)
        self._X = X
        self._Y = Y
        self._Z = Z

        if not self.first_pass:
            pass1_3sigma = 0
            stddev = self.delocalization / 3
        else:
            pass1_3sigma = self.bin_width / 2
            stddev = n.sqrt((self.delocalization / 3) ** 2 - n.tile(pass1_3sigma / 3, 3) ** 2)

        stddev_vox = stddev / self.bin_width

        init_counts = []
        final_counts = []

        def ranged_xyz(rng):
            low, up = rng.interval
            idx = n.argwhere((self.roi.mass >= low) & (self.roi.mass < up)).ravel()
            init_counts.append(idx.shape[0])
            return self.roi.xyz[idx].astype(float)

        N = len(self.ranges)
        nproc = min(N, mp.cpu_count())

        if self.first_pass:
            result = [ion_transfer(X, Y, Z, ranged_xyz(i), pass1_3sigma) for i in self.ranges]
        else:
            result = []
            for i, rng in enumerate(self.ranges):
                coords = ranged_xyz(rng)
                counts, _ = n.histogramdd(coords, bins=n_voxels)
                result.append(counts)

        for i, data in zip(self.ranges, result):
            final_counts.append(n.sum(data))
            nan = n.count_nonzero(n.isnan(data))
            if nan > 0:
                raise ArithmeticError(
                    "NaNs encountered during first pass delocalization, try picking a different bin width"
                )
            self._ion_counts[i.ion] += gaussian_filter(
                data,
                sigma=stddev_vox,
                # mode="constant",
                truncate=self.gauss_trunc,
            )

        self._elem_frac = {i: 0 for i in range_elems}
        self._elem_counts = {i: 0 for i in range_elems}
        elem_counts = self._elem_counts

        for ion, counts in self._ion_counts.items():
            for elem, mult in ion.comp_dict.items():
                elem_counts[elem] += mult * counts

        self._elem_counts_array = sum(array for array in elem_counts.values())

        norm = sum(i for i in elem_counts.values())
        self._elem_cum_counts = norm
        for key in elem_counts.keys():
            ary = elem_counts[key]
            self._elem_frac[key] = n.divide(ary, norm, where=ary > 0)


class DensityHistogram(AnalysisBase):
    """
    Compute density histograms on an Roi
    """

    def __init__(self, roi: Roi, bin_width=0.3, axis="z", multiplicity="all"):
        """
        :param roi: region of interest
        :param bin_width: width of the bin size in Daltons
        :param axis: which axis the histogram should be computed on ("x", "y", or "z")
        :param multiplicity: the multiplicity order to compute histogram with
        """
        super().__init__(roi)
        self.bin_width = validate.positive_nonzero_number(bin_width)
        self._multiplicity = validate.multiplicity_any(multiplicity)
        if multiplicity != "all":
            roi.require_multihit_info()

        self._histogram = None
        self._histogram_extents = None
        self._axis = validate.choice(axis, ("x", "y", "z"))
        self._bin_vol = None
        self._calculate_histogram()

    @property
    def multiplicity(self) -> Union[str, int]:
        return self._multiplicity

    @property
    def bin_vol(self) -> Number:
        return self._bin_vol

    @property
    def axis(self) -> str:
        return self._axis

    @property
    def histogram(self) -> ndarray:
        return self._histogram

    @property
    def histogram_extents(self) -> ndarray:
        return self._histogram_extents

    def _calculate_histogram(self):
        orient_map = {"x": 0, "y": 1, "z": 2}
        ax1, ax2 = (self.roi.xyz[:, val] for key, val in orient_map.items() if key != self.axis)
        ext_ax1, ext_ax2 = (self.roi.xyz_extents[val] for key, val in orient_map.items() if key != self.axis)
        ext = (ext_ax1, ext_ax2)

        if self.multiplicity == "all":
            self._histogram = histogram2d_binwidth(ax1, ax2, ext, self.bin_width)
        else:
            idx = get_mass_indices(self.roi.misc["ipp"], self.multiplicity)
            self._histogram = histogram2d_binwidth(ax1[idx], ax2[idx], ext, self.bin_width)

        self._histogram_extents = ext
