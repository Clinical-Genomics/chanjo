# -*- coding: utf-8 -*-
import json

from chanjo.cli import root
from chanjo.store.models import Sample, TranscriptStat


def test_setup(cli_runner, tmp_path):
    # GIVEN an empty directory
    assert not list(tmp_path.iterdir())
    # WHEN setting up a new database
    db_name = "coverage.sqlite"
    db_path = tmp_path.joinpath(db_name)
    cli_runner.invoke(root, ["--database", str(db_path), "db", "setup"])
    # THEN the file is created
    assert list(tmp_path.iterdir()) == [db_path]


def test_setup_reset(cli_runner, popexist_db):
    # GIVEN an existing database with a single sample
    with popexist_db.begin() as session:
        assert session.first(Sample.select())
        # WHEN resetting it
        cli_runner.invoke(root, ["--database", popexist_db.uri, "db", "setup", "--reset"])
        # THEN the database should be empty
        assert session.first(Sample.select()) is None


def test_remove(cli_runner, popexist_db):
    # GIVEN an existing database with one sample
    sample_id = "sample"
    with popexist_db.begin() as session:
        assert session.first(Sample.select())
        assert session.all(TranscriptStat.select().where(TranscriptStat.sample_id == sample_id))
        # WHEN removing the sample from the CLI
        cli_runner.invoke(root, ["--database", popexist_db.uri, "db", "remove", sample_id])
        # THEN the sample should be deleted along with annotations
        assert session.first(Sample.select()) is None
        assert (
            len(session.all(TranscriptStat.select().where(TranscriptStat.sample_id == sample_id)))
            == 0
        )
        # WHEN removing a sample with non-existing id
        result = cli_runner.invoke(
            root, ["--database", popexist_db.uri, "db", "remove", "no-sample-id"]
        )
        # THEN context is aborted
        assert result.exit_code == 1


def test_samples(cli_runner, popexist_db):

    # GIVEN an existing database with one sample
    sample_id = "sample"
    with popexist_db.begin() as session:
        assert session.first(Sample.select())

    # WHEN fetching a sample from the database through the CLI
    result = cli_runner.invoke(
        root,
        [
            "--database",
            popexist_db.uri,
            "db",
            "samples",
            "--sample-id",
            sample_id,
            "--pretty",
        ],
    )

    # THEN command exits with 0 and the sample is retrieved as a JSON formatted string
    assert result.exit_code == 0
    result = json.loads(result.output)
    assert result[0]["id"] == sample_id


def test_transcripts(cli_runner, popexist_db):

    # GIVEN an existing database with one sample
    sample_id = "sample"
    with popexist_db.begin() as session:
        assert session.first(Sample.select())

    # WHEN fetching the transcripts for that case in the database
    result = cli_runner.invoke(
        root,
        [
            "--database",
            popexist_db.uri,
            "db",
            "transcripts",
            "--sample-id",
            sample_id,
            "--pretty",
        ],
    )

    # THEN the command exits with 0 and retrieves all transcripts for that case
    assert result.exit_code == 0
    result = json.loads(result.output)
    for transcript in result:
        assert transcript["sample_id"] == sample_id


def test_delete(cli_runner, popexist_db):

    # GIVEN an existing database with one sample
    sample_id = "sample"
    with popexist_db.begin() as session:
        assert session.first(Sample.select())

        # WHEN deleting a sample from the database through the CLI
        cli_runner.invoke(
            root, ["--database", popexist_db.uri, "db", "delete", "--sample-id", sample_id]
        )

        # THEN the sample is no longer in the database
        assert session.first(Sample.select()) is None


def test_delete_group(cli_runner, popexist_db):

    # GIVEN an existing database with one sample
    group_id = "group"
    sample_id = "sample"
    with popexist_db.begin() as session:
        assert session.first(Sample.select())

        # WHEN deleting a sample from the database through the CLI
        cli_runner.invoke(
            root, ["--database", popexist_db.uri, "db", "delete", "--group-id", group_id]
        )

        # THEN the sample is no longer in the database
        assert session.first(Sample.select()) is None
