# -*- coding: utf-8 -*-
from __future__ import absolute_import
from tempfile import gettempdir

from mock import patch
import yaml

from test_utils import FakeZipFile, fake_urlretrieve


def test_init_demo(tmpdir, invoke_cli):
    # GIVEN empty directory
    assert tmpdir.listdir() == []
    # WHEN setting up demo on CLI
    target_dir = tmpdir.join('chanjo-demo')
    target_path = str(target_dir)
    result = invoke_cli(['init', '--demo', target_path])
    # THEN is should work and place 6 + 1 (config) in the folder
    assert result.exit_code == 0
    assert len(target_dir.listdir()) == 7


@patch('chanjo.compat.urlretrieve', fake_urlretrieve)
@patch('zipfile.ZipFile', FakeZipFile)
@patch('click.confirm', lambda param: True)
def test_init_bootstrap(tmpdir, invoke_cli):
    # GIVEN empty dir
    assert tmpdir.listdir() == []
    # WHEN boostrapping chanjo
    result = invoke_cli(['init', str(tmpdir)])
    # THEN it should place 2 + 1 (BED, DB, config) files in the target dir
    assert result.exit_code == 0
    assert len(tmpdir.listdir()) == 3


@patch('click.confirm', lambda param: False)
@patch('click.prompt', lambda param: "{}/cov.sqlite3".format(gettempdir()))
def test_init_no_bootstrap(tmpdir, invoke_cli):
    # GIVEN ...
    # WHEN opting out of bootstrap
    result = invoke_cli(['init', str(tmpdir)])
    # THEN it should work with custom database URI
    assert result.exit_code == 0
    conf_path = tmpdir.join('chanjo.yaml')
    with open(str(conf_path), 'r') as handle:
        data = yaml.load(handle)
    assert 'coverage.sqlite3' in data['database']
