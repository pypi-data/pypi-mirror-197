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
from apav.qt import *
import apav as ap
import apav.analysis as anl
from apav.visualization import plotting
from apav.visualization import base


def close_all_qt_windows():
    for win in QApplication.topLevelWindows():
        win.close()


class TestBaseVisualization:
    def test_export_image(self, qtbot):
        data = n.array([])

        vis = base.BaseVisualization(data)
        QTimer.singleShot(1000, close_all_qt_windows)
        vis.exportImage()

    def test_copy_image(self, qtbot):
        data = n.array([])

        vis = base.BaseVisualization(data)
        vis.copyImage()


# For now just test that each plot runs without error
class TestPlotsOpen:
    def test_correlation_plot(self, si_roi, qtbot):
        corr = ms.CorrelationHistogram(si_roi)
        plot = plotting.CorrelationHistogramPlot(corr)

        qtbot.addWidget(plot)
        plot.show()

    def test_spectrum_plot(self, si_roi, si_range, qtbot):
        plot = plotting.MassSpectrumPlot(si_roi)
        qtbot.addWidget(plot)
        plot.show()

    def test_ranged_spectrum_plot(self, si_roi, si_range, qtbot):
        spec = ms.RangedMassSpectrum(si_roi, si_range)

        plot = plotting.MassSpectrumPlotRanged(spec)
        qtbot.addWidget(plot)
        plot.show()

    def test_noise_spectrum_plot(self, si_roi, si_range, qtbot):
        spec = ms.NoiseCorrectedMassSpectrum(si_roi, si_range)

        plot = plotting.MassSpectrumPlotNoiseCorrected(spec)
        qtbot.addWidget(plot)
        plot.show()

    def test_local_spectrum_plot(self, si_roi, si_range, qtbot):
        spec = ms.LocalBkgCorrectedMassSpectrum(si_roi, si_range, anl.BackgroundCollection())

        plot = plotting.MassSpectrumPlotLocalBkgCorrected(spec)
        qtbot.addWidget(plot)
        plot.show()
