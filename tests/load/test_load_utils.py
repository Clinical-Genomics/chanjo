# -*- coding: utf-8 -*-
from chanjo.load.utils import exon, _exon_kwargs


DATA = {'chrom': 'chr1', 'chromStart': 100, 'chromEnd': 220, 'name': 'exon1',
        'score': 0, 'strand': '+', 'sampleName': 'sample1', 'readCount': 10,
        'meanCoverage': 6.341, 'thresholds': {10: 95.421, 20: 86.21, 100: 10.21}}


def test_exon():
    exon_obj = exon(DATA)
    assert exon_obj.chromosome == 'chr1'
    assert exon_obj.exon_id == 'exon1'


def test__exon_kwargs():
    kwargs = _exon_kwargs(DATA)
    assert kwargs['chromosome'] == 'chr1'
    assert kwargs['exon_id'] == 'exon1'
