# -*- coding: utf-8 -*-
import pytest

from chanjo.sambamba import run_sambamba

BAM = 'tests/fixtures/ccds.mini.sorted.bam'
BED = 'tests/fixtures/ccds.mini.bed'
THRESHOLDS = (10, 20)


def test_run_sambamba(tmpdir):
    out_path = tmpdir.join('ccds.coverage.bed')
    run_sambamba(BAM, BED, outfile=str(out_path), cov_treshold=THRESHOLDS)
    assert out_path.exists()


def test_run_sambamba_missing(tmpdir, reset_path):
    out_path = tmpdir.join('ccds.coverage.bed')
    with pytest.raises(OSError):
        run_sambamba(BAM, BED, outfile=str(out_path), cov_treshold=THRESHOLDS)
