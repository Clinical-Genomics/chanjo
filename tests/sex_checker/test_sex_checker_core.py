# -*- coding: utf-8 -*-
from chanjo.sex_checker import Gender, gender_from_bam, predict_gender


def test_Gender():
  # create a gender tuple
  gender = Gender(10.2, 8.1, 'male')

  assert gender.x_coverage == 10.2
  assert gender.y_coverage == 8.1
  assert gender.sex == 'male'


def test_predict_gender():
  assert predict_gender(x_coverage=10.2, y_coverage=8.1) == 'male'
  assert predict_gender(x_coverage=20.9, y_coverage=.01) == 'female'
  # shouldn't raise ``ZeroDivisionError``
  assert predict_gender(x_coverage=5.12, y_coverage=0) == 'female'

  # what does this even mean?
  assert predict_gender(x_coverage=0, y_coverage=10) == 'unknown'
