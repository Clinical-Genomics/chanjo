# -*- coding: utf-8 -*-
from tempfile import gettempdir

import yaml
from mock import patch

from chanjo.testutils import FakeZipFile, fake_urlretrieve


def test_init_demo(tmp_path, invoke_cli):
    # GIVEN empty directory
    assert not list(tmp_path.iterdir())
    # WHEN setting up demo on CLI
    target_dir = tmp_path.joinpath("chanjo-demo")
    target_path = str(target_dir)
    result = invoke_cli(["init", "--demo", target_path])
    # THEN is should work and place 4 demo files + 1 sqlite db + 1 config
    assert result.exit_code == 0
    assert len(list(target_dir.iterdir())) == (4 + 1 + 1)


@patch("urllib.request.urlretrieve", fake_urlretrieve)
@patch("zipfile.ZipFile", FakeZipFile)
@patch("click.confirm", lambda param: True)
def test_init_bootstrap(tmp_path, invoke_cli):
    # GIVEN empty dir
    assert not list(tmp_path.iterdir())
    # WHEN bootstrapping chanjo
    result = invoke_cli(["init", str(tmp_path)])
    # THEN it should place 2 + 1 (BED, DB, config) files in the target dir
    assert result.exit_code == 0
    assert len(list(tmp_path.iterdir())) == 3


@patch("click.confirm", lambda param: False)
@patch("click.prompt", lambda param: "{}/cov.sqlite3".format(gettempdir()))
def test_init_no_bootstrap(tmp_path, invoke_cli):
    # GIVEN ...
    # WHEN opting out of bootstrap
    result = invoke_cli(["init", str(tmp_path)])
    # THEN it should work with custom database URI
    assert result.exit_code == 0
    conf_path = tmp_path.joinpath("chanjo.yaml")
    with open(str(conf_path), "r") as handle:
        data = yaml.safe_load(handle)
    assert "coverage.sqlite3" in data["database"]
