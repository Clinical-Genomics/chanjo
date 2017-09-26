# -*- coding: utf-8 -*-
from chanjo.store.models import Sample, Transcript


def test_load(existing_db, invoke_cli, sambamba_path):
    # GIVEN processed sambamba depth output and empty database
    assert Sample.query.count() == 0
    db_uri = existing_db.uri
    result = invoke_cli(['--database', db_uri, 'load', sambamba_path])
    # WHEN loading into database
    assert result.exit_code == 0
    assert Sample.query.count() == 1


def test_load_conflict(popexist_db, invoke_cli, sambamba_path):
    # GIVEN an existing database with a sample
    db_uri = popexist_db.uri
    sample_id = 'sample'
    assert Sample.query.first().id == sample_id
    # WHEN you try to add the same sample id twice
    result = invoke_cli(['--database', db_uri, 'load', '--sample', sample_id,
                         sambamba_path])
    # THEN it should fail
    assert result.exit_code != 0
    assert Sample.query.count() == 1


