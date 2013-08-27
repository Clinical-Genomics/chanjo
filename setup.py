#!/usr/bin/env python
# -*- coding: utf-8 -*-

import chanjo

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="chanjo",
    description="A coverage analysis package for clinical sequencing.",
    author="Robin Andeer",
    author_email="robin.andeer@gmail.com",
    url="http://chanjo.herokuapp.com/",
    download_url="https://github.com/robinandeer/chanjo",
    version=chanjo.__version__,
    long_description="",
    install_requires=[
        "nose",
        "pysam",
        "numpy",
        "sqlalchemy",
        "interval",
        "bx-python",
        "docopt"
    ],
    packages=["chanjo"],
    scripts=["scripts/chanjo-autopilot.py"]
)