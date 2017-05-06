# -*- coding: utf-8 -*-
from chanjo.load import utils


def test_groupby_tx(bed_exons, sambamba_exons):
    transcripts = list(utils.groupby_tx(bed_exons))
    assert len(transcripts) == 5

    # GIVEN sambamba lines
    transcripts = list(utils.groupby_tx(sambamba_exons, sambamba=True))
    assert len(transcripts) == 9
