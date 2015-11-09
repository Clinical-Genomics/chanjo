# -*- coding: utf-8 -*-
from __future__ import division
from collections import namedtuple
import logging
import subprocess

logger = logging.getLogger(__name__)

SexGuess = namedtuple('SexGuess', ['x_coverage', 'y_coverage', 'sex'])


def predict_sex(x_coverage, y_coverage):
    """Make a simple yet accurate prediction of a samples sex.

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
    elif (y_coverage > 0) and (x_coverage / y_coverage < 10):
        # this is the entire prediction, it's usually very obvious
        return 'male'
    else:
        # the few reads mapping to the Y chromosomes are artifacts
        return 'female'


def sex_from_bam(bam_path, prefix=''):
    """Predict the sex from a BAM alignment file.

    Args:
        bam_path (path): path to a BAM alignment file
        prefix (str, optional): string to prefix to 'X', 'Y'

    Returns:
        SexGuess: tuple of X coverage, Y coverage, and sex prediction

    Examples:
        >>> sex_from_bam('alignment.bam', prefix='chr')
        SexGuess(x_coverage=123.31, y_coverage=0.13, sex='female')
    """
    # make up some sex chromosome regions
    regions = ["{}X:1-59373566".format(prefix),
               "{}Y:69362-11375310".format(prefix)]
    averages = []
    for region in regions:
        command = ["sambamba depth region -L {} {}".format(region, bam_path)]
        logger.debug("calling: %s", command)
        bed_out = subprocess.check_output(command, shell=True).decode('utf-8')
        bed_rows = [line.split() for line in bed_out.splitlines()
                    if not line.startswith('#')]
        if len(bed_rows) == 1:
            averages.append(float(bed_rows[0][4]))
        else:
            chromosome = region.split(':')[0]
            logger.warn("couldn't find any reads on %s-chromosome", chromosome)
            averages.append(0.)

    # make the guess
    x_coverage, y_coverage = list(averages)
    sex = predict_sex(x_coverage, y_coverage)
    return SexGuess(x_coverage, y_coverage, sex)
