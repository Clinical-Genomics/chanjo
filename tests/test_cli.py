# -*- coding: utf-8 -*-
import os

import ruamel.yaml


def test_logging_to_file(tmpdir, invoke_cli):
    # GIVEN an empty directory
    assert tmpdir.listdir() == []
    # WHEN running the CLI to display some help for a subcommand
    log_path = tmpdir.join('stderr.log')
    result = invoke_cli(['--log-file', str(log_path), 'db'])
    assert result.exit_code == 0
    assert tmpdir.listdir() == [log_path]


def test_list_commands(invoke_cli):
    # WHEN using simplest command 'chanjo'
    result = invoke_cli()
    # THEN it should just work ;-)
    assert result.exit_code == 0


def test_missing_command(invoke_cli):
    # WHEN invoking a missing command
    result = invoke_cli(['idontexist'])
    # THEN context should abort
    assert result.exit_code != 0


def test_with_config(tmpdir, invoke_cli):
    # GIVEN a simple config file
    conf_path = str(tmpdir.join('chanjo.yaml'))
    db_path = str(tmpdir.join('coverage.sqlite3'))
    data = {'database': db_path}
    with open(conf_path, 'w') as handle:
        handle.write(ruamel.yaml.dump(data, Dumper=ruamel.yaml.RoundTripDumper))
    # WHEN launching CLI with config
    result = invoke_cli(['-c', conf_path, 'db', 'setup'])
    # THEN config values should be picked up
    assert result.exit_code == 0
    assert os.path.exists(db_path)
