# -*- coding: utf-8 -*-
"""
chanjo.annotator
~~~~~~~~~~~~~~~~~

This module is responsible for the annotation of coverage and
completeness of intervals in BED-file.

Exposes the central functions and pipeline found deeper in the module.
"""
from __future__ import absolute_import

from .core import annotate_bed_stream
from .stages import (
  assign_relative_positions,
  calculate_metrics,
  extend_interval,
  group_intervals,
  merge_intervals,
  prepend,
  process_interval_group
)
