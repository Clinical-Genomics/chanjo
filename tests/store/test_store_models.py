# -*- coding: utf-8 -*-
from chanjo.store.models import TranscriptStat, Exon


def test_TranscriptStat():
    # GIVEN a transcript stat with two incomplete exons
    exons = [Exon('1', 10, 100, 99.1), Exon('1', 200, 300, 80.5)]
    stat = TranscriptStat(mean_coverage=10.3, incomplete_exons=exons)
    # WHEN accessing them
    parsed_exons = list(stat.incomplete_exons)
    # THEN should be the same
    assert parsed_exons == exons
