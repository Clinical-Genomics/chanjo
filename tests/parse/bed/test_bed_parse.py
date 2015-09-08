# -*- coding: utf-8 -*-
import pytest

from chanjo.exc import BedFormattingError
from chanjo.parse import bed

TEST_OUTPUT = 'tests/fixtures/test.sambamba.bed'


def test_extra_fields():
    columns = ['X-CCDS43917.1,X-CCDS55362.1,X-CCDS55363.1',
               'X-ASMTL,X-ASMTL,X-ASMTL']
    combos = [combo for combo in bed.extra_fields(columns)]
    assert len(combos) == 3
    assert combos[0] == ('X-CCDS43917.1', 'X-ASMTL')


def test_chanjo():
    with open(TEST_OUTPUT, 'r') as handle:
        data_rows = [data for data in bed.chanjo(handle)]

    data = data_rows[0]
    assert data['name'] == '1-69090-70007'
    assert data['score'] == 0
    assert data['strand'] == '+'
    assert list(data['elements']) == [('CCDS30547.1', 'OR4F5')]


def test_chanj_with_sambamba():
    bed_lines = ["# chrom\tchromStart\tchromEnd\treadCount\tmeanCoverage"
                    "\tsampleName",
                 "1\t69089\t70007\t232\t25.4946\tADM992A10\t"]

    with pytest.raises(BedFormattingError):
        list(bed.chanjo(bed_lines))
