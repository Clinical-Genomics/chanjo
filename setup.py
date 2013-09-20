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
    license="MIT",
    maintainer="Robin Andeer",
    keywords=["coverage", "sequencing", "clinical", "exome"],
    platform="UNIX",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ],
    url="http://chanjo.readthedocs.org/",
    download_url="https://github.com/robinandeer/chanjo",
    version=chanjo.__version__,
    long_description="",
    install_requires=[
        "nose",
        "pysam",
        "numpy",
        "sqlalchemy",
        "interval",
        "docopt",
        "elemental"
    ],
    packages=["chanjo"],
    scripts=["scripts/chanjo-autopilot"]
)