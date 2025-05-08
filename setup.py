#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages

# See also: https://github.com/kennethreitz/setup.py/blob/master/setup.py

NAME = 'commonlibs'
VERSION = "1.0.0"
AUTHOR = 'Aaron Dettmann'
EMAIL = 'dettmann@kth.se'
DESCRIPTION = 'Libraries used by different packages'
URL = 'https://github.com/airinnova/commonlibs'
REQUIRES_PYTHON = '>=3.11.11'
REQUIRED = [
    'numpy',
    'schemadict',
]
README = 'README.rst'
PACKAGE_DIR = 'src/lib/'
LICENSE = 'Apache License 2.0'

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=open("README.md").read(),
    url=URL,
    include_package_data=True,
    package_dir={'': PACKAGE_DIR},
    license=LICENSE,
    packages=find_packages(where=PACKAGE_DIR),
    python_requires=REQUIRES_PYTHON,
    install_requires=REQUIRED,
    # See: https://pypi.org/classifiers/
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
    ],
)
