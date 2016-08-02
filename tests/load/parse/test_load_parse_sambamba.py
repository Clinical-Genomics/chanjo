# -*- coding: utf-8 -*-
import pytest

from chanjo.load.parse import sambamba
from chanjo.exc import BedFormattingError


def test_depth_output():
    exon_lines = ['# chrom chromStart chromEnd\n', '1 10 100\n']
    with pytest.raises(BedFormattingError):
        list(sambamba.depth_output(exon_lines))
