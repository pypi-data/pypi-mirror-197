from distutils.core import setup, Extension
from Cython.Build import cythonize
from setuptools import setup, find_packages
import numpy as np
import os


os.environ['CFLAGS'] = '-O3 -Wno-cpp -Wno-unused-function'


setup(
    name='ms_entropy',
    version='0.2.0',
    license='Apache License 2.0',
    author='Yuanyue Li',
    url='https://github.com/YuanyueLi/SpectralEntropy',
    packages=['ms_entropy'],
    install_requires=['cython>=0.29.33', "numpy>=1.23.5", "cupy>=11.6.0"],
    keywords=[
        "ms entropy",
        "ms spectral entropy",
        "spectral entropy",
        "spectral similarity",
        "entropy similarity",
        "entropy",
        "entropy search",
        "flash entropy",
        "flash entropy similarity",
        "flash entropy search",
    ],
    package_dir={'': '.'},
    ext_modules=cythonize([
        Extension('ms_entropy.tools_cython',
                  [r"ms_entropy/tools_cython.pyx"]),
    ],
        annotate=False,
        compiler_directives={
        'language_level': "3",
        'cdivision': True,
        'boundscheck': False,  # turn off bounds-checking for entire function
        'wraparound': False  # turn off negative index wrapping for entire function
    }),
    include_dirs=[np.get_include()]
)

# python setup.py build_ext
