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
import numpy as n

import apav.analysis.massspectrum as ms
import apav as ap
from apav.core.isotopic import Element
from apav.analysis.spatial import RangedGrid, DensityHistogram, ion_transfer, make_coordinate_grids
from periodictable import elements as el


class TestCoordinateGrid:
    ext = [(-3.1, 5.5), (6.7, 9.2), (-5, 12)]

    def test_basic_call(self):
        result = make_coordinate_grids(self.ext, 1)

    def test_edges(self):
        make_coordinate_grids(self.ext, 1, edges=True)

    def test_correct_number_of_bins(self):
        binw = n.array([0.5, 0.7, 1.2])
        centers = make_coordinate_grids(self.ext, binw)

        for ax in range(3):
            ary = centers[ax]
            dims = n.abs(n.diff(n.array(self.ext))).ravel()
            nx, ny, nz = n.ceil(dims / binw)
            assert ary.shape == (nx, ny, nz)

    def test_correct_number_of_bins_integral_extents(self):
        ext = [(0, 3), (0, 3), (0, 3)]
        centers = make_coordinate_grids(ext, 1)

        for ax in range(3):
            assert centers[ax].shape == (4, 4, 4)

    def test_correct_number_of_bins_edges(self):
        binw = n.array([0.5, 0.7, 1.2])
        centers = make_coordinate_grids(self.ext, binw, edges=True)

        for ax in range(3):
            ary = centers[ax]
            dims = n.abs(n.diff(n.array(self.ext))).ravel()
            nx, ny, nz = n.ceil(dims / binw)
            assert ary.shape == (nx + 1, ny + 1, nz + 1)

    def test_edge_correct_result_shape(self):
        centers = make_coordinate_grids(self.ext, 1)
        edges = make_coordinate_grids(self.ext, 1, edges=True)

        for ax in range(3):
            assert all(i == j + 1 for i, j in zip(edges[ax].shape, centers[ax].shape))

    def test_edges_correct_result(self):
        binw = [1, 2, 3]
        centers = make_coordinate_grids(self.ext, binw)
        edges = make_coordinate_grids(self.ext, binw, edges=True)

        for ax in range(3):
            b = binw[ax]
            assert n.allclose(centers[ax], edges[ax][:-1, :-1, :-1] + b / 2)

    def test_different_bins(self):
        binw = [1, 2, 3]
        centers = make_coordinate_grids(self.ext, binw)

        for ax in range(3):
            b = binw[ax]
            diff = n.diff(centers[ax], axis=ax).mean()
            assert n.isclose(diff, b)

    def test_different_bins_edges(self):
        binw = [1, 2, 3]
        centers = make_coordinate_grids(self.ext, binw, edges=True)

        for ax in range(3):
            b = binw[ax]
            diff = n.diff(centers[ax], axis=ax).mean()
            assert n.isclose(diff, b)

    def test_no_zero_bin(self):
        with raises(ValueError):
            make_coordinate_grids(self.ext, 0)
        with raises(ValueError):
            make_coordinate_grids(self.ext, [0, 2, 3])

    def test_no_negative_bins(self):
        with raises(ValueError):
            make_coordinate_grids(self.ext, -1)
        with raises(ValueError):
            make_coordinate_grids(self.ext, [-1, 2, 3])

    def test_interval_validity(self):
        with raises(ValueError):
            make_coordinate_grids([(3, 1), (1, 2), (1, 2)], 1)

    def test_correct_number_of_intervals(self):
        with raises(AssertionError):
            make_coordinate_grids([(1, 2)], 1)

    def test_correct_interval_shape(self):
        with raises(ValueError):
            make_coordinate_grids([(1, 2, 3), (1, 2), (1, 2)], -1)


class TestIonTransfer:
    ext = [(0, 3), (0, 3), (0, 3)]
    X3, Y3, Z3 = make_coordinate_grids(ext, 1)
    pos = n.array([[1, 1, 1]])

    def test_basic_call(self):
        result = ion_transfer(self.X3, self.Y3, self.Z3, self.pos, 0.5)

    def test_number_of_atoms_conserved(self):
        pos = n.array(
            [
                [1, 1, 1],
                [0, 0, 0],
                [3, 3, 3],
            ]
        )
        result = ion_transfer(self.X3, self.Y3, self.Z3, pos, 0.5)
        assert n.isclose(result.sum(), pos.shape[0])

    def test_no_empty_pos(self):
        with raises(ValueError):
            ion_transfer(self.X3, self.Y3, self.Z3, n.array([[]]), 1)

    def test_pos_shape(self):
        with raises(ValueError):
            ion_transfer(self.X3, self.Y3, self.Z3, n.array([1, 1, 1]), 1)

    def test_no_negative_sigma(self):
        with raises(ValueError):
            ion_transfer(self.X3, self.Y3, self.Z3, self.pos, -1)

    def test_zero_sigma(self):
        # Zero sigma uses a different code path, check that the results are about the same as a very small sigma
        pos = n.array([[0, 0, 0], [1, 1, 1], [3, 3, 3]])
        result = ion_transfer(self.X3, self.Y3, self.Z3, pos, 0)
        temp = ion_transfer(self.X3, self.Y3, self.Z3, pos, 1e-4)

        assert n.allclose(result, temp)

    def test_x_shape(self):
        with raises(ValueError):
            ion_transfer(n.array([]), self.Y3, self.Z3, self.pos, 1)

    def test_y_shape(self):
        with raises(ValueError):
            ion_transfer(self.X3, n.array([]), self.Z3, self.pos, 1)

    def test_z_shape(self):
        with raises(ValueError):
            ion_transfer(self.X3, self.Y3, n.array([]), self.pos, 1)


class TestRangedGrid:
    def test(self, fake_precip_roi, fake_precip_range):
        grid = RangedGrid(fake_precip_roi, fake_precip_range)

    def test_from_file(self, si_roi, si_range):
        grid = RangedGrid(si_roi, si_range)

    def test_deloc_options(self, fake_precip_roi, fake_precip_range):
        grid_array = RangedGrid(fake_precip_roi, fake_precip_range, delocalization=n.array([3, 3, 3]))
        grid_tuple = RangedGrid(fake_precip_roi, fake_precip_range, delocalization=(3, 3, 3))
        grid_single = RangedGrid(fake_precip_roi, fake_precip_range, delocalization=3)

        assert n.allclose(grid_array.centers, grid_tuple.centers)
        assert n.allclose(grid_array.centers, grid_single.centers)

        assert n.allclose(grid_array.all_elemental_frac_str["C"], grid_tuple.all_elemental_frac_str["C"])
        assert n.allclose(grid_array.all_elemental_frac_str["C"], grid_single.all_elemental_frac_str["C"])

        with raises(ValueError):
            RangedGrid(fake_precip_roi, fake_precip_range, delocalization=(1, 2, 3, 4))

    def test_no_negative_deloc(self, fake_precip_roi, fake_precip_range):
        with raises(ValueError):
            RangedGrid(fake_precip_roi, fake_precip_range, delocalization=-3)

        with raises(ValueError):
            RangedGrid(fake_precip_roi, fake_precip_range, delocalization=(3, 2, -1))

        with raises(ValueError):
            RangedGrid(fake_precip_roi, fake_precip_range, delocalization=n.array([3, 2, -1]))

    def test_elem_frac(self, fake_precip_roi, fake_precip_range):
        grid = RangedGrid(fake_precip_roi, fake_precip_range)

        c_str = grid.elemental_frac("C")
        c_el = grid.elemental_frac(el.C)

        assert n.allclose(c_str, c_el)

        with raises(TypeError):
            grid.elemental_frac(4)

    def test_no_first_pass(self, fake_precip_roi, fake_precip_range):
        RangedGrid(fake_precip_roi, fake_precip_range, first_pass=False)

    def test_ion_counts(self, fake_precip_roi, fake_precip_range):
        grid = RangedGrid(fake_precip_roi, fake_precip_range)
        grid.ionic_counts(ap.Ion("C"))

        with raises(ValueError):
            grid.ionic_counts(ap.Ion("CuO"))

    # def test_parallel(self):
    #     """
    #     The grid calculation runs in parallel if the number of counts exceeds a certain value
    #     """
    #
    #     # Change the threshold value so the test finished fast
    #     temp = RangedGrid._parallel_exec_thresh
    #     RangedGrid._parallel_exec_thresh = 1000
    #     pos = n.random.uniform(-50, 50, (RangedGrid._parallel_exec_thresh, 3))
    #     m = n.ones(RangedGrid._parallel_exec_thresh)
    #     roi = ap.Roi(pos, m)
    #
    #     rng = ap.RangeCollection()
    #     rng.add(ap.Range("H", (0, 2)))
    #
    #     grid = RangedGrid(roi, rng)
    #
    #     RangedGrid._parallel_exec_thresh = temp


class TestDensityHistogram:
    def test(self, si_roi):
        dens = DensityHistogram(si_roi)

    def test_non_positive_bin(self, si_roi):
        with raises(ValueError):
            DensityHistogram(si_roi, bin_width=-1)
        with raises(ValueError):
            DensityHistogram(si_roi, bin_width=0)

    def test_axes(self, si_roi):
        x = DensityHistogram(si_roi, axis="x")
        y = DensityHistogram(si_roi, axis="y")
        z = DensityHistogram(si_roi, axis="z")

    def test_no_non_xyz(self, si_roi):
        with raises(ValueError):
            DensityHistogram(si_roi, axis="t")

    def test_multiplicity(self, si_roi):
        dens_all = DensityHistogram(si_roi, multiplicity="all")
        dens_mult = DensityHistogram(si_roi, multiplicity="multiples")
        dens_each = [DensityHistogram(si_roi, multiplicity=i) for i in si_roi.multiplicities]

        assert n.allclose(dens_all.histogram, sum(i.histogram for i in dens_each))
        assert n.allclose(dens_mult.histogram, sum(i.histogram for i in dens_each if i.multiplicity > 1))
