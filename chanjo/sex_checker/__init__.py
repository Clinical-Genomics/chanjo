# -*- coding: utf-8 -*-
"""Component for predicting the gender from a BAM alignment file.

Accepts the path to a BAM file and optionally a prepend for the id of
the sex chromosomes.

The component reads coverage for subsections of each sex chromosome.
Based on the ratio between the average coverage across chromosomes it
makes a simple yet very accurate gender prediction.
"""
from __future__ import absolute_import

from .core import Gender, gender_from_bam, predict_gender
