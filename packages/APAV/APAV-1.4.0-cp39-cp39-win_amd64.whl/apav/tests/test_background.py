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

from apav.analysis.background import Background, BackgroundCollection, _background_includes_overlap
import apav

from pytest import raises


class TestBackground:
    def test_constructor(self):
        Background((3, 5), (5, 6))

    def test_require_lmfit_model(self):
        with raises(TypeError):
            Background([3, 4], model="POWER")

    def test_interval_length_positive_nonzero(self):
        with raises(AssertionError):
            Background([])

    def test_multiple_fit_intervals(self):
        intervals = [(1, 4), (6, 7)]
        bkg = Background(intervals)

        for i in intervals:
            assert i in bkg.fit_intervals

    def test_no_intersecting_fit_intervals(self):
        with raises(Exception):
            bkg = Background([(1, 5), (3, 7)])

    def test_no_reversed_fit_intervals(self):
        with raises(Exception):
            Background((4, 3))

    def test_no_reversed_include_intervals(self):
        with raises(Exception):
            Background([3, 4], (4, 3))

    def test_require_length_2_fit_intervals(self):
        with raises(Exception):
            Background((2, 3, 4))

    def test_require_length_2_include_intervals(self):
        with raises(Exception):
            Background((1, 2), (2, 3, 4))
        with raises(Exception):
            Background((1, 2), [(4, 5), (2, 3, 4)])

    def test_multiple_include_intervals(self):
        intervals = [(1, 4), (6, 7)]
        bkg = Background((5, 6), intervals)

        for i in intervals:
            assert i in bkg.include_intervals

    def test_lower(self):
        intervals = [(1, 4), (6, 7)]
        bkg = Background(intervals)
        assert bkg.lower == 1

    def test_upper(self):
        intervals = [(1, 4), (6, 7)]
        bkg = Background(intervals)
        assert bkg.upper == 7

    def test_fit(self, si_roi):
        x, y = si_roi.mass_histogram()
        bkg = Background((1, 2))
        bkg.fit(x, y)

    def test_area(self, si_roi):
        bkg = Background((1, 2))
        with raises(AssertionError):
            bkg.area

        x, y = si_roi.mass_histogram()
        bkg.fit(x, y)

        area = bkg.area

    def test_eval(self, si_roi):
        x, y = si_roi.mass_histogram()
        bkg = Background((1, 2))
        with raises(AssertionError):
            bkg.eval(x)
        bkg.fit(x, y)

        y_fit = bkg.eval(x)

    def test_include_contains_mass(self):
        bkg = Background((1, 2), (4, 5))

        assert bkg.contains_mass(4)
        assert not bkg.contains_mass(5)  # half open interval

    def test_include_contains_range(self):
        bkg = Background((1, 2), (4, 5))
        assert not bkg.contains_range(apav.Range("Os", (6, 7)))
        assert not bkg.contains_range(apav.Range("Os", (2, 3)))
        assert bkg.contains_range(apav.Range("Os", (4.5, 7)))
        assert not bkg.contains_range(apav.Range("Os", (2, 4)))
        assert not bkg.contains_range(apav.Range("Os", (5, 7)))

    def test_reset(self):
        bkg = Background((1, 2))
        bkg.reset()


class TestBackgroundCollection:
    def test_constructor(self):
        bkgs = BackgroundCollection()
        bkg = [
            Background((1, 2)),
            Background((3, 4)),
            Background((4, 6)),
        ]
        bkgs2 = BackgroundCollection(bkg)

        for i in bkg:
            assert i in bkgs2.backgrounds

    def test_iter(self):
        bkg = [
            Background((1, 2)),
            Background((3, 4)),
            Background((4, 6)),
        ]
        bkgs = BackgroundCollection(bkg)

        # Had a bug causing successive iterations to not act properly, test this is corrected
        count = 0
        for i in bkgs:
            count += 1
        for i in bkgs:
            count += 1

        assert count == len(bkg) * 2

    def test_str_no_fit(self, si_roi):
        bkg = [
            Background((1, 2), (12, 13)),
            Background((3, 4), (14, 15)),
            Background((4, 6), (16, 17)),
        ]
        x, y = si_roi.mass_histogram()
        print(BackgroundCollection())
        print(BackgroundCollection(bkg))

    def test_str_with_fit(self, si_roi):
        bkg = [
            Background((1, 2), (12, 13)),
            Background((3, 4), (14, 15)),
            Background((4, 6), (16, 17)),
        ]
        x, y = si_roi.mass_histogram()

        bkgs = BackgroundCollection(bkg)
        bkgs.fit(x, y)

        print(bkgs)

    def test_getitem(self):
        bkg = [
            Background((1, 2), (12, 13)),
            Background((3, 4), (14, 15)),
            Background((4, 6), (16, 17)),
        ]
        bkgs = BackgroundCollection(bkg)
        for i, j in enumerate(bkg):
            assert bkgs[i] == j

    def test_add(self):
        bkgs = BackgroundCollection()
        b1 = Background((1, 2), (4, 5))
        bkgs.add(b1)
        assert len(bkgs) == 1

        with raises(TypeError):
            bkgs.add(5)

        with raises(RuntimeError):
            b2 = Background((1, 2), (4.5, 6))
            bkgs.add(b2)

    def test_find_background(self):
        b1 = Background((1, 2), (4, 5))
        rng1 = apav.Range("Os", (4.5, 7))
        rng2 = apav.Range("Os", (5, 7))
        rng3 = apav.Range("Os", (2, 4))

        rng4 = apav.Range("Os", (12, 14))
        bkgs = BackgroundCollection([b1])
        assert bkgs.find_background(rng1) == b1
        assert bkgs.find_background(rng2) is None
        assert bkgs.find_background(rng3) is None
        assert bkgs.find_background(rng4) is None


def test_background_includes_overlap():
    bkg1 = Background((1, 2), (3, 4))
    bkg2 = Background((1, 2), (3.5, 4.5))
    bkg3 = Background((1, 2), (4, 5))

    assert _background_includes_overlap(bkg1, bkg2) is True
    assert _background_includes_overlap(bkg1, bkg3) is False
