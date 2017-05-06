# -*- coding: utf-8 -*-
from chanjo.store.models import TranscriptStat
from chanjo.load import sambamba


def test_load_transcripts(exon_lines):
    # GIVEN sambamba depth output lines
    # WHEN loading transcript stats
    result = sambamba.load_transcripts(exon_lines, sample_id='sample',
                                       group_id='group')
    # THEN transcript models should be generated
    assert result.count == 9
    assert result.sample.id == 'sample'
    assert result.sample.group_id == 'group'
    assert isinstance(list(result.models)[0], TranscriptStat)

    # GIVEN no explicit sample id
    # WHEN loading transcript stats
    result = sambamba.load_transcripts(exon_lines)
    # THEN it should be picked up from file
    assert result.sample.id == 'ADM992A10'


def test_load_transcripts_with_threshold(exon_lines):
    # GIVEN a cutoff for "complete" exons at 100x
    threshold = 100
    # WHEN loading transcript stats
    result = sambamba.load_transcripts(exon_lines, threshold=threshold)
    # THEN some transcripts will have incomplete exons linked
    incompletes = [transcript for transcript in result.models
                   if transcript.incomplete_exons]
    assert len(incompletes) > 0
