# -*- coding: utf-8 -*-
from chanjo.store.models import Sample, Transcript


def test_load(existing_db, invoke_cli, sambamba_path):
    # GIVEN processed sambamba depth output and empty database
    with existing_db.begin() as session:
        assert session.first(Sample.select()) is None
        db_uri = existing_db.uri
        result = invoke_cli(["--database", db_uri, "load", sambamba_path])
        # WHEN loading into database
        assert result.exit_code == 0
        assert session.first(Sample.select())


def test_load_conflict(popexist_db, invoke_cli, sambamba_path):
    # GIVEN an existing database with a sample
    db_uri = popexist_db.uri
    sample_id = "sample"
    with popexist_db.begin() as session:
        assert session.first(Sample.select()).id == sample_id
        # WHEN you try to add the same sample id twice
        result = invoke_cli(["--database", db_uri, "load", "--sample", sample_id, sambamba_path])
        # THEN it should fail
        assert result.exit_code != 0
        assert len(session.all(Sample.select())) == 1


def test_link(existing_db, invoke_cli, bed_path):
    # GIVEN chanjo bed file and an existing database
    db_uri = existing_db.uri
    # WHEN linking elements in the database
    result = invoke_cli(["--database", db_uri, "link", bed_path])
    # THEN database should be populated with all transcripts
    assert result.exit_code == 0
    with existing_db.begin() as session:
        assert len(session.all(Transcript.select())) == 5

        # WHEN loading again...
        result = invoke_cli(["--database", db_uri, "link", bed_path])
        # THEN it should error and rollback the session
        assert result.exit_code != 0
        assert len(session.all(Transcript.select())) == 5
