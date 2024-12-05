# -*- coding: utf-8 -*-
"""
chanjo
~~~~~~~
Coverage analysis for clinical sequencing.

:copyright: (c) 2014 by Robin Andeer
:licence: MIT, see LICENCE for more details
"""
import logging

try:
    from importlib.metadata import version
except ImportError:  # Backport support for importlib metadata on Python 3.7
    from importlib_metadata import version


__banner__ = r"""
       ______               ________
 _________  /_______ _____________(_)_____
 _  ___/_  __ \  __ `/_  __ \____  /_  __ \
 / /__ _  / / / /_/ /_  / / /___  / / /_/ /   by Robin Andeer
 \___/ /_/ /_/\__,_/ /_/ /_/___  /  \____/
                            /___/
"""

__title__ = "chanjo"
__summary__ = "coverage analysis tool for clinical sequencing"
__uri__ = "http://www.chanjo.co/"

__version__ = version(__title__)
__codename__ = "Optimistic Otter"

__author__ = "Robin Andeer"
__email__ = "robin.andeer@gmail.com"

__license__ = "MIT"
__copyright__ = "Copyright 2016 Robin Andeer"

# the user should dictate what happens when a logging event occurs
logging.getLogger(__name__).addHandler(logging.NullHandler())
