"""Test calculate subcommand"""
import json

from chanjo.cli import root
from chanjo.store.models import Sample
from chanjo.cli.calculate import dump_json


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


def test_dump_json():
    # GIVEN some dict
    data = {'name': 'PT Anderson', 'age': 45}
    # WHEN dumping to JSON with pretty-option enabled
    json_str = dump_json(data, pretty=True)
    # THEN the output is formatted over multiple lines
    assert isinstance(json_str, str)
    assert len(json_str.split('\n')) == 4


def test_coverage(popexist_db, cli_runner):
    """test coverage command"""
    # GIVEN an existing databse with one sample
    assert Sample.query.count() == 1
    # WHEN assessing the omim coverage per sample
    res = cli_runner.invoke(root, ['-d', popexist_db.uri, 'calculate', 'coverage', '-s',
                                   'sample', '14825'])
    # THEN the command should return JSON results
    assert res.exit_code == 0
    # ... returns some debug info to STDERR that we strip away
    lines = res.output.strip().split('\n')
    assert len(lines) == 1
    # ... the last row (no incl. empty line) is JSON formatted
    data = json.loads(lines[0].strip())
    # THE dict should include mean_coverage and mean completeness for sample
    assert set(data['sample'].keys()) == set(['mean_coverage', 'mean_completeness'])
