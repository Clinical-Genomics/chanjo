# -*- coding: utf-8 -*-
import os

import yaml


def test_logging_to_file(tmp_path, invoke_cli):
    # GIVEN an empty directory
    assert not list(tmp_path.iterdir())
    # WHEN running the CLI to display some help for a subcommand
    log_path = tmp_path.joinpath("stderr.log")
    result = invoke_cli(["--log-file", str(log_path), "db", "delete"])
    assert result.exit_code == 0
    assert list(tmp_path.iterdir()) == [log_path]


def test_list_commands(invoke_cli):
    # WHEN using simplest command 'chanjo'
    result = invoke_cli(["--help"])
    assert result.exit_code == 0
    # THEN it should show command options
    assert "db" in result.output


def test_missing_command(invoke_cli):
    # WHEN invoking a missing command
    result = invoke_cli(["idontexist"])
    # THEN context should abort
    assert result.exit_code != 0


def test_with_config(tmpdir, invoke_cli):
    # GIVEN a simple config file
    conf_path = str(tmpdir.join("chanjo.yaml"))
    db_path = str(tmpdir.join("coverage.sqlite3"))
    data = {"database": db_path}
    with open(conf_path, "w") as handle:
        yaml.dump(data, handle, default_flow_style=False)
    # WHEN launching CLI with config
    result = invoke_cli(["-c", conf_path, "db", "setup"])
    # THEN config values should be picked up
    assert result.exit_code == 0
    assert os.path.exists(db_path)
