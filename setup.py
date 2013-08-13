try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    "description": "A coverage analysis package for clinical exome"
                   "sequencing.",
    "author": "Robin Andeer",
    "author_email": "robin.andeer@gmail.com",
    "url": "http://chanjo.herokuapp.com/",
    "download_url": "https://github.com/robinandeer/chanjo2",
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
