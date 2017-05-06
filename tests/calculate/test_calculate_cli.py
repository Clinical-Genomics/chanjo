# -*- coding: utf-8 -*-
import json

from chanjo.cli import root
from chanjo.store.models import Sample


def test_mean(popexist_db, cli_runner):
    # GIVEN an existing databse with one sample
    assert Sample.query.count() == 1
    # WHEN assessing the mean values metrics per sample
    res = cli_runner.invoke(root, ['-d', popexist_db.uri, 'calculate', 'mean'])
    # THEN the command should return JSON results
    assert res.exit_code == 0
    # ... returns some debug info to STDERR that we strip away
    lines = res.output.strip().split('\n')
    assert len(lines) == 1
    # ... the last row (no incl. empty line) is JSON formatted
    data = json.loads(lines[0].strip())
    assert data['sample_id'] == 'sample'
    assert isinstance(data['mean_coverage'], float)
