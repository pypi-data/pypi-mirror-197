from setuptools import Extension, setup
from Cython.Build import cythonize
import sys

if sys.platform == "win32":
    extension_args = {"extra_compile_args": ["/openmp"]}
elif sys.platform == "linux":
    extension_args = {"extra_compile_args": ["-fopenmp"], "extra_link_args": ["-fopenmp"]}
else:
    extension_args = {}

ext_modules = [
    Extension("apav.analysis.grid_transfer", ["./apav/pyx/grid_transfer.pyx"], **extension_args),
    Extension("apav.pyxutils", ["./apav/pyx/utils.pyx"], **extension_args),
]


if __name__ == "__main__":
    setup(
        ext_modules=cythonize(ext_modules, language_level=3),
    )
