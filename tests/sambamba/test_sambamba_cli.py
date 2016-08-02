# -*- coding: utf-8 -*-


def test_sambamba(invoke_cli, bam_path, bed_path):
    # GIVEN a small BAM file and corresponding BED file
    # WHEN running sambamba
    result = invoke_cli(['sambamba', '-r', bed_path, bam_path])
    # THEN command should complete succesfully
    assert result.exit_code == 0


def test_sambamba_with_bai(invoke_cli, bam_path, bed_path):
    # GIVEN a BAI-file instead of BAM
    bai_path = "{}.bai".format(bam_path)
    # WHEN running sambamba
    result = invoke_cli(['sambamba', '-r', bed_path, bai_path])
    # THEN command should exit with error
    assert result.exit_code != 0
