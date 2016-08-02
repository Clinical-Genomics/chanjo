# -*- coding: utf-8 -*-
from chanjo.load import link


def test_process(bed_lines):
    result = link.link_elements(bed_lines)
    models = list(result.models)
    assert result.count == 5  # 5 transcripts
