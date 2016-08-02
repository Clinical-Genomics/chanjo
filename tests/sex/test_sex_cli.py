# -*- coding: utf-8 -*-
from chanjo.cli import root


def test_sex(cli_runner, bam_path):
    result = cli_runner.invoke(root, ['sex', bam_path])
    assert result.exit_code == 0
    assert 'female' in result.output


def test_sex_with_wrong_file(cli_runner, bam_path):
    bai_path = "{}.bai".format(bam_path)
    result = cli_runner.invoke(root, ['sex', bai_path])
    assert result.exit_code != 0
