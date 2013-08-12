try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    "description": "A coverage analysis package for clinical exome"
                   "sequencing.",
    "author": "Robin Andeer",
    "url": "http://chanjo.herokuapp.com/",
    "download_url": "Where to download it.",
    "author_email": "robin.andeer@gmail.com",
    "version": "0.1",
    "install_requires": [
        "nose",
        "pysam",
        "autumn",
        "interval",
        "bx-python"
    ],
    "packages": ["chanjo"],
    "scripts": [],
    "name": "chanjo"
}

setup(**config)
