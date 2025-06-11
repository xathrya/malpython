# building the cython module

# python3 setup.py build_ext --inplace

from setuptools import setup 
from Cython.Build import cythonize 

setup(
    ext_modules = cythonize("payload.pyx")
)

# things to make sure:
#   - cython is installed: pip3 install cython
#   - compiler exists (gcc, clang, or msvc)