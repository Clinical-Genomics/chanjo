# -*- coding: utf-8 -*-
import codecs
import os
from functools import partial

import pytest
from click.testing import CliRunner

from chanjo.cli import root
from chanjo.load.link import link_elements
from chanjo.load.parse import bed, sambamba
from chanjo.load.sambamba import load_transcripts
from chanjo.store.api import ChanjoDB


@pytest.fixture
def reset_path():
    """Reset PATH environment variable temporarily."""
    path_env = os.environ["PATH"]
    os.environ["PATH"] = ""
    yield path_env
    os.environ["PATH"] = path_env


@pytest.fixture(scope="function")
def chanjo_db():
    _chanjo_db = ChanjoDB("sqlite://")
    _chanjo_db.set_up()
    yield _chanjo_db
    _chanjo_db.tear_down()


@pytest.fixture(scope="function")
def existing_db(tmpdir):
    db_path = tmpdir.join("coverage.sqlite3")
    chanjo_db = ChanjoDB(str(db_path))
    chanjo_db.set_up()
    yield chanjo_db
    chanjo_db.tear_down()


@pytest.fixture(scope="function")
def popexist_db(existing_db, exon_lines):
    with existing_db.begin(expire_on_commit=False) as session:
        result = link_elements(exon_lines)
        session.add_all(result.models)
        result = load_transcripts(exon_lines, sample_id="sample", group_id="group")
        session.add(result.sample)
        session.add_all(result.models)
    yield existing_db


@pytest.fixture(scope="function")
def populated_db(chanjo_db, exon_lines):
    exon_lines = list(exon_lines)
    result = link_elements(exon_lines)
    with chanjo_db.begin(expire_on_commit=False) as session:
        session.add_all(result.models)
        results = [
            load_transcripts(exon_lines, sample_id="sample", group_id="group"),
            load_transcripts(exon_lines, sample_id="sample2", group_id="group"),
        ]
        for result in results:
            session.add(result.sample)
            session.add_all(result.models)
    yield chanjo_db


@pytest.fixture
def exon_lines(sambamba_path):
    with codecs.open(sambamba_path, "r", encoding="utf-8") as stream:
        _exon_lines = [line for line in stream]
    return _exon_lines


@pytest.fixture
def bed_lines(bed_path):
    with codecs.open(bed_path, "r", encoding="utf-8") as stream:
        _bed_lines = [line for line in stream]
    return _bed_lines


@pytest.fixture
def bed_row():
    row = ["22", "32588888", "32589173", "22-32588888-32589173", "CCDS54521.1", "RFPL2"]
    return row


@pytest.fixture
def bed_exons(bed_lines):
    _exons = bed.chanjo(bed_lines)
    return _exons


@pytest.fixture
def sambamba_exons(exon_lines):
    _exons = sambamba.depth_output(exon_lines)
    return _exons


@pytest.fixture
def cli_runner():
    runner = CliRunner()
    return runner


@pytest.fixture
def invoke_cli(cli_runner):
    return partial(cli_runner.invoke, root)


@pytest.fixture
def bam_path():
    _bam_path = "tests/fixtures/ccds-mini.sorted.bam"
    return _bam_path


@pytest.fixture
def bed_path():
    _bed_path = "tests/fixtures/ccds-mini.bed"
    return _bed_path


@pytest.fixture
def sambamba_path():
    _sambamba_path = "tests/fixtures/sambamba.depth.bed"
    return _sambamba_path
