# -*- coding: utf-8 -*-
from chanjo.store import Exon, Exon_Transcript


def test_Exon_Transcript():
    # test table name
    assert Exon_Transcript.name == 'exon__transcript'


def test_Interval():
    # set up
    exon = Exon(exon_id='exon1', chromosome='chr1', start=10, end=1000)

    assert len(exon) == 991
