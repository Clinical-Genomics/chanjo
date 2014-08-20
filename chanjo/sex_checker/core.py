# -*- coding: utf-8 -*-
from __future__ import absolute_import, division
from collections import namedtuple

from toolz import pipe
from toolz.curried import map

from ..depth_reader import BamFile
from ..utils import average

Gender = namedtuple('Gender', ['x_coverage', 'y_coverage', 'sex'])


def predict_gender(x_coverage, y_coverage):
  """Make a simple yet accurate prediction of a samples gender.

  The calculation is based on the average coverage across the X and Y
  chromosomes. Note that an extrapolation from a subsection of bases is
  usually quite sufficient.

  Args:
    x_coverage (float): estimated average coverage on X chromosome
    y_coverage (float): estimated average coverage on Y chromosome

  Returns:
    str: prediction, ['male', 'female', 'unknown']
  """
  # algoritm doesn't work if coverage is missing for X chromosome
  if x_coverage == 0:
    return 'unknown'

  # this is the entire prediction, it's usually very obvious
  elif (y_coverage > 0) and (x_coverage / y_coverage < 10):
    return 'male'

  else:
    # the few reads mapping to the Y chromosomes are artifacts
    return 'female'


def gender_from_bam(bam_path, prepend=''):
  """Predict the gender from a BAM alignment file.

  Args:
    bam_path (path): path to a BAM alignment file
    prepend (str, optional): string to prepend to 'X', 'Y'

  Returns:
    Gender: tuple of X coverage, Y coverage, and sex prediction

  Examples:
    >>> gender_from_bam('alignment.bam', prepend='chr')
    Gender(x_coverage=123.31, y_coverage=0.13, sex='female')
  """
  # setup: connect to a BAM file
  bam = BamFile(bam_path)

  # step 0: fake some BED interval rows (already 1,1-based!)
  fake_bed_rows = [("%sX" % prepend, 1, 59373566),
                   ("%sY" % prepend, 69362, 11375310)]

  # step 1: run the pipeline
  sequence = pipe(
    fake_bed_rows,
    map(lambda interval: bam(*interval)),
    map(average)
  )

  # step: make the prediction
  x_coverage, y_coverage = list(sequence)
  sex = predict_gender(x_coverage, y_coverage)
  return Gender(x_coverage, y_coverage, sex)
