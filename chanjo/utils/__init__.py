#!/usr/bin/env python
# coding: utf-8

from .calculate import coverageMetrics, intervals
from .group import group
from .process import process


def chromosomes(prepend="", extra=[]):
  # Stringify
  base = map(str, range(1,23))
  return [prepend + chrom for chrom in base + ["X", "Y"] + extra]
