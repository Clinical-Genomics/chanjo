# -*- coding: utf-8 -*-
from chanjo.sex import SexGuess, sex_from_bam, predict_sex


def test_SexGuess():
    # create a sex guess tuple
    sex = SexGuess(10.2, 8.1, 'male')

    assert sex.x_coverage == 10.2
    assert sex.y_coverage == 8.1
    assert sex.sex == 'male'


def test_predict_sex():
    assert predict_sex(x_coverage=10.2, y_coverage=8.1) == 'male'
    assert predict_sex(x_coverage=20.9, y_coverage=.01) == 'female'
    # shouldn't raise ``ZeroDivisionError``
    assert predict_sex(x_coverage=5.12, y_coverage=0) == 'female'
    # what does this even mean?
    assert predict_sex(x_coverage=0, y_coverage=10) == 'unknown'


def test_sex_from_bam(bam_path):
    # use fixtures bam - doesn't have coverage on Y chromosome
    result = sex_from_bam(bam_path)
    assert result.x_coverage > result.y_coverage
    assert result.sex == 'female'
