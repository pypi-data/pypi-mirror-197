# APAV: Python for Atom Probe Tomography
[![Documentation Status](https://readthedocs.org/projects/apav/badge/?version=latest)](https://apav.readthedocs.io/en/latest/?badge=latest)
[![coverage report](https://gitlab.com/jesseds/apav/badges/master/coverage.svg)](https://gitlab.com/jesseds/apav/commits/master)
[![pipeline status](https://gitlab.com/jesseds/apav/badges/master/pipeline.svg)](https://gitlab.com/jesseds/apav/-/commits/master)
[![License: GPL v2](https://img.shields.io/badge/License-GPL_v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
[![PyPI version](https://badge.fury.io/py/apav.svg)](https://badge.fury.io/py/apav)
[![status](https://joss.theoj.org/papers/ee06a37a09339a80f36b0a1ddeba6b27/status.svg)](https://joss.theoj.org/papers/ee06a37a09339a80f36b0a1ddeba6b27)

[//]: # ([![Conda]&#40;https://img.shields.io/conda/v/conda-forge/apav&#41;]&#40;&#41;)

APAV (Atom Probe Analysis and Visualization) is a Python package for analysis and
visualization of atom probe tomography datasets, some features:

* File read support for traditional (\*.pos, \*.epos, \*.ato, \*.rng, \*.rrng) or new (\*.apt) formats
* File write support for \*.pos and \*.epos
* Mass spectrum quantification with configurable background correction
* Calculation and configuration of correlation histograms
* Roi primitive shapes for localized analysis
* Most analyses can be parameterized by multiple-detection events
* Fast generation of the compositional grid using conventional 1st/2nd pass delocalization
* Calculation of arbitrary molecular isotopic distributions

# Basic usage
Essential APT analysis typically involves loading some data and doing some calculation(s). Import the core functions and classes:

    >>> import apav as ap

Load an apt file from AP Suite or some other source, along with a suitable range file (or build one programtically):

    >>> roi = ap.load_apt("data/NiTiHf.apt")
    >>> rng = ap.load_rrng("data/NiTiHf_FWHM.rrng")

Now import the analysis components and compute the total (uncorrected) decomposed composition:

    >>> import apav.analysis as anl
    >>> mass = anl.RangedMassSpectrum(roi, rng, decompose=True)
    >>> mass.print()
    Ion      Composition    Counts
    -----  -------------  --------
    Ti        0.307084     2381757
    Ni        0.595634     4619772
    Hf        0.0907196     703626
    O         0.00656261     50900

Estimate the (uncorrected) composition of a grain in the upper part of the ROI using a sphere:

    >>> precip_roi = ap.RoiSphere(roi, center=(-8.5, 2.1, -20), radius=20)
    >>> precip_mass = anl.RangedMassSpectrum(precip_roi, rng, decompose=True)
    >>> precip_mass.print()
    Ion      Composition    Counts
    -----  -------------  --------
    Ti        0.397016      261053
    Ni        0.532445      350102
    Hf        0.0665544      43762
    O         0.00398457      2620

Check the documentation for more analyses and background corrections.

# Documentation
Documentation is found at: https://apav.readthedocs.io/

# Support
Post discussion to the [GitLab issue tracker](https://gitlab.com/jesseds/apav/-/issues)

# FAQ
**Why use this over IVAS/AP Suite or program X?**

APAV is not intended to be an IVAS substitute or replacement. While much of the 
functionality may overlap, APAV fills feature gaps in IVAS/AP Suite that are lacking or otherwise non-existent.
Specifically:
1. Multiple-event analysis (i.e. correlation histograms, multiple event histograms, multiple event mass quantifications).
2. Manual control over mass spectrum analysis (background models, fit regions, binning, etc).
3. An API to easily interface into APT data for custom data analysis.

**Why is there no GUI for APAV?**

APAV is intended to be used as a python *library*. Perhaps a GUI will one day exist along side APAV (but not in replacement). For now, APAV includes
some custom interactive plotting tools for certain computations.


