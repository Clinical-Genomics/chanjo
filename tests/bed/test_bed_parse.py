# -*- coding: utf-8 -*-
from chanjo.bed import parse

TEST_OUTPUT = 'tests/fixtures/test.sambamba.bed'


def test_extra_fields():
    columns = ['X-CCDS43917.1,X-CCDS55362.1,X-CCDS55363.1',
               'X-ASMTL,X-ASMTL,X-ASMTL']
    combos = [combo for combo in parse.extra_fields(columns)]
    assert len(combos) == 3
    assert combos[0] == ('X-CCDS43917.1', 'X-ASMTL')


def test_chanjo():
    with open(TEST_OUTPUT, 'r') as handle:
        data_rows = [data for data in parse.chanjo(handle)]

    data = data_rows[0]
    assert data['name'] == '1-69090-70007'
    assert data['score'] == 0
    assert data['strand'] == '+'
    assert list(data['elements']) == [('CCDS30547.1', 'OR4F5')]
