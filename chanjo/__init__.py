# -*- coding: utf-8 -*-
"""
chanjo
~~~~~~~

Coverage analysis for clinical sequencing. It's intuatively documented
and embraces functional programming patterns.

:copyright: (c) 2014 by Robin Andeer
:licence: MIT, see LICENCE for more details
"""
from __future__ import absolute_import, unicode_literals
from .annotator import annotate_bed_stream
from .builder import init_db
from .converter import ccds_to_bed
from .exporter import export_intervals
from .importer import import_bed_stream, import_json
from .sex_checker import gender_from_bam
from .store import Store
from .utils import (
  average,
  BaseInterval,
  bed_to_interval,
  completeness,
  id_generator,
  serialize_interval,
  split
)

__banner__ = r"""
       ______               ________
 _________  /_______ _____________(_)_____
 _  ___/_  __ \  __ `/_  __ \____  /_  __ \
 / /__ _  / / / /_/ /_  / / /___  / / /_/ /   by Robin Andeer
 \___/ /_/ /_/\__,_/ /_/ /_/___  /  \____/
                            /___/
"""

__title__ = 'chanjo'
__summary__ = 'coverage analysis tool for clinical sequencing'
__uri__ = 'http://www.chanjo.co/'

__version__ = '2.0.0-beta'
__codename__ = 'Wistful Weasel'

__author__ = 'Robin Andeer'
__email__ = 'robin.andeer@gmail.com'

__license__ = 'MIT'
__copyright__ = 'Copyright 2014 Robin Andeer'
