# -*- coding: utf-8 -*-

from chanjo.cli import root
from chanjo.store.models import Sample, TranscriptStat


def test_setup(cli_runner, tmpdir):
    # GIVEN an empty directory
    assert tmpdir.listdir() == []
    # WHEN setting up a new database
    db_name = 'coverage.sqlite'
    db_path = tmpdir.join(db_name)
    cli_runner.invoke(root, ['--database', str(db_path), 'db', 'setup'])
    # THEN the file is created
    assert tmpdir.listdir() == [db_path]


def test_setup_reset(cli_runner, popexist_db):
    # GIVEN an existing database with a single sample
    assert Sample.query.count() == 1
    # WHEN resetting it
    cli_runner.invoke(root, ['--database', popexist_db.uri, 'db', 'setup',
                             '--reset'])
    # THEN the database should be empty
    assert Sample.query.count() == 0


def test_remove(cli_runner, popexist_db):
    # GIVEN an existing database with one sample
    sample_id = 'sample'
    assert Sample.query.get(sample_id)
    assert TranscriptStat.query.filter_by(sample_id=sample_id).count() > 0
    # WHEN removing the sample from the CLI
    cli_runner.invoke(root, ['--database', popexist_db.uri, 'db', 'remove',
                             sample_id])
    # THEN the sample should be deleted along with annotations
    assert Sample.query.get(sample_id) is None
    assert TranscriptStat.query.filter_by(sample_id=sample_id).count() == 0

    # WHEN removing a sample with non-existing id
    result = cli_runner.invoke(root, ['--database', popexist_db.uri, 'db',
                                      'remove', 'no-sample-id'])
    # THEN context is aborted
    assert result.exit_code == 1

### MONGO TESTS ###

def test_setup_reset_mongo(cli_runner, popexist_real_mongo_db):
    db = popexist_real_mongo_db
    # GIVEN an existing database with a single sample
    assert len(db.samples()) == 1
    # WHEN resetting it
    # CLI function does not work with mongomock
    cli_runner.invoke(root, ['--database', db.uri, '--backend', 'mongodb',
                             'db', 'setup', '--reset'])
    # THEN the database should be empty
    assert len(db.samples()) == 0

def test_mongo_remove(cli_runner, popexist_real_mongo_db):
    popexist_db = popexist_real_mongo_db
    # GIVEN an existing database with one sample
    sample_id = 'sample'
    assert popexist_db.sample(sample_id)
    assert sum(1 for i in popexist_db.transcript_stat_collection.find({'sample_id': sample_id})) > 0
    # WHEN removing the sample from the CLI
    cli_runner.invoke(root, ['--database', popexist_db.uri, '--backend', 'mongodb',
                             'db', 'remove', sample_id])
    # THEN the sample should be deleted along with annotations
    assert popexist_db.sample(sample_id) is None
    assert sum(1 for i in popexist_db.transcript_stat_collection.find({'sample_id': sample_id})) == 0

    # WHEN removing a sample with non-existing id
    result = cli_runner.invoke(root, ['--database', popexist_db.uri, '--backend', 'mongodb',
                                      'db', 'remove', 'no-sample-id'])
    # THEN context is aborted
    assert result.exit_code == 1
