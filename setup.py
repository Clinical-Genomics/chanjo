#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Bootstrap distribute unless already installed
from chanjo.distribute_setup import use_setuptools
use_setuptools()

import os
import sys

from setuptools import setup, find_packages
import chanjo

# Shortcut for publishing to Pypi
# Source: https://github.com/kennethreitz/tablib/blob/develop/setup.py
if sys.argv[-1] == "publish":
  os.system("python setup.py sdist upload")
  sys.exit()

setup(
  name="chanjo",
  version=chanjo.__version__,
  packages=find_packages(exclude=["tests"]),
  scripts=[
    "scripts/chanjo"
  ],

  # Project dependencies
  install_requires = [
    "pysam",
    "numpy",
    "sqlalchemy",
    "docopt",
    "elemental",
    "path.py"
  ],

  # Packages required for testing
  tests_require = [
    "nose"
  ],

  # Metadate for upload to Pypi
  author="Robin Andeer",
  author_email="robin.andeer@gmail.com",
  description="A coverage analysis package for clinical sequencing.",
  long_description = (open('README.rst').read()),
  license="MIT",
  keywords="coverage sequencing clinical exome",
  platform="UNIX",
  url="http://chanjo.readthedocs.org/",
  download_url="https://github.com/robinandeer/chanjo",
  classifiers=[
    "Development Status :: 4 - Beta",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Programming Language :: Python :: 2.7",
    "Topic :: Scientific/Engineering :: Bio-Informatics"
  ]
)