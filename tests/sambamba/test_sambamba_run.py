# -*- coding: utf-8 -*-
import pytest

from chanjo.sambamba import run_sambamba

THRESHOLDS = (10, 20)


def test_run_sambamba(tmpdir, bed_path, bam_path):
    out_path = tmpdir.join('ccds.coverage.bed')
    run_sambamba(bam_path, bed_path, outfile=str(out_path),
                 cov_thresholds=THRESHOLDS)
    assert out_path.exists()


def test_run_sambamba_missing(tmpdir, reset_path, bed_path, bam_path):
    out_path = tmpdir.join('ccds.coverage.bed')
    with pytest.raises(OSError):
        run_sambamba(bam_path, bed_path, outfile=str(out_path),
                     cov_thresholds=THRESHOLDS)
