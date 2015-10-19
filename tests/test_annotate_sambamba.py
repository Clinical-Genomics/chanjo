# -*- coding: utf-8 -*-
import os

from chanjo.annotate.sambamba import run_sambamba


def test_run_sambamba():
    bam = 'tests/fixtures/ccds.mini.sorted.bam'
    bed = 'tests/fixtures/CCDS.mini.bed'
    out = '/tmp/ccds.coverage.bed'
    thresholds = (10, 20)
    run_sambamba(bam, bed, outfile=out, cov_treshold=thresholds)
    assert os.path.exists(out)
