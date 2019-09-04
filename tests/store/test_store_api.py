# -*- coding: utf-8 -*-
from datetime import datetime

import pytest
from sqlalchemy.orm.exc import FlushError
from pymongo.errors import DuplicateKeyError

from chanjo.store.api import ChanjoDB
from chanjo.store.models import Sample
from chanjo.load.sambamba import load_transcripts
from chanjo.store.constants import STAT_COLUMNS




def test_dialect(chanjo_db):
    assert chanjo_db.dialect == 'sqlite'
    assert hasattr(chanjo_db, 'query')

def test_no_dialect():
    # GIVEN not explicity specifying SQLite dialect
    # WHEN setting up the API
    chanjo_db = ChanjoDB(':memory:')
    # THEN chanjo should guess it
    assert chanjo_db.dialect == 'sqlite'


def test_save(chanjo_db):
    # GIVEN a new sample
    sample_id = 'ADM12'
    new_sample = Sample(id=sample_id, group_id='ADMG1', source='alignment.bam')
    # WHEN added and saved to the database
    chanjo_db.add(new_sample)
    chanjo_db.save()
    # THEN is should exist in the database
    assert new_sample.id == sample_id
    assert isinstance(new_sample.created_at, datetime)
    assert Sample.query.get(sample_id) == new_sample

    # GIVEN sample already exists
    conflict_sample = Sample(id=sample_id, group_id='ADMG2')
    # WHEN saving it again with same id
    # THEN error is raised _after_ rollback
    with pytest.raises(FlushError):
        chanjo_db.add(conflict_sample)
        chanjo_db.save()

    new_sampleid = 'ADM13'
    chanjo_db.add(Sample(id=new_sampleid))
    chanjo_db.save()
    assert Sample.query.get(new_sampleid)


def test_add_many(chanjo_db):
    # GIVEN multiple new samples
    new_samples = [Sample(id='ADM12'), Sample(id='ADM13')]
    # WHEN added to the session
    chanjo_db.add(new_samples)
    chanjo_db.save()
    # THEN all samples should be added
    assert Sample.query.all() == new_samples

### Mongo DB tests

def test_mongo_dialect(chanjo_mongo_db):
    ## GIVEN a mongo database connection
    ## WHEN setting up the api with a connection to mongomock
    chanjo_db = chanjo_mongo_db
    ## THEN assert that the dialect is mongodb
    assert chanjo_db.dialect == 'mongodb'
    ## THEN assert that the uri is mongomock
    assert chanjo_db.uri == 'mongomock://'

def test_mongo_save(chanjo_mongo_db):
    chanjo_db = chanjo_mongo_db
    # GIVEN a new sample
    sample_id = 'ADM12'
    new_sample = Sample(id=sample_id, group_id='ADMG1', source='alignment.bam')
    # WHEN added and saved to the database
    chanjo_db.add(new_sample)
    chanjo_db.save()
    db_sample = chanjo_db.sample(sample_id)
    # THEN is should exist in the database
    assert db_sample.id == sample_id
    assert isinstance(db_sample.created_at, datetime)

    # GIVEN sample already exists
    conflict_sample = Sample(id=sample_id, group_id='ADMG2')
    # WHEN saving it again with same id
    # THEN error is raised _after_ rollback
    with pytest.raises(DuplicateKeyError):
        chanjo_db.add(conflict_sample)
        chanjo_db.save()

    new_sampleid = 'ADM13'
    chanjo_db.add(Sample(id=new_sampleid))
    chanjo_db.save()
    assert chanjo_db.sample(new_sampleid)

def test_mongo_add_many(chanjo_mongo_db):
    chanjo_db = chanjo_mongo_db
    # GIVEN multiple new samples
    new_samples = [Sample(id='ADM12'), Sample(id='ADM13')]
    # WHEN added to the session
    chanjo_db.add(*new_samples)
    chanjo_db.save()
    # THEN all samples should be added
    res = chanjo_db.samples()
    assert len(res) == len(new_samples)

def test_mongo_calculate_mean(populated_mongo_db, exon_lines):

    # GIVEN a populated mongodb and some mean on the completeness in tests/fixtures
    # sambamba.depth.bed
    chanjo_db = populated_mongo_db

    transcript_stats = list(load_transcripts(exon_lines,
                                             sample_id='sample',
                                             group_id='group').models)
    # Find expected mean coverage
    tot_coverage = 0
    for transcript_stat in transcript_stats:
        tot_coverage += transcript_stat.mean_coverage
    expected_mean = tot_coverage/len(transcript_stats)

    # Find expected mean for each completeness level
    expected_completeness = {}
    for transcript_stat in transcript_stats:
        for key, value in transcript_stat.__dict__.items():
            if 'completeness' in key:
                if key in expected_completeness.keys():
                    expected_completeness[key] += value
                else:
                    expected_completeness[key] = value
    # divide all fields by number of transcripts to get mean
    for key, value in expected_completeness.items():
        expected_completeness[key] = value/len(transcript_stats)

    # WHEN calculating mean stats on the db
    chanjo_mean = chanjo_db.mean().next()

    # THEN these should be as expected
    assert expected_mean == chanjo_mean['mean_coverage']

    for key, value in expected_completeness.items():
        if key in chanjo_mean.keys():
            assert value == chanjo_mean[key]

def test_compare_backends(populated_db, populated_mongo_db):
    # GIVEN a populated sql and mongodb database loaded with the same data

    # WHEN calling mean on the database api
    mongodb_results = populated_mongo_db.mean().next()
    columns = ['_id'] + STAT_COLUMNS
    sql_results = {column: value for column, value in zip(columns, populated_db.mean()[0])}

    # THEN the results should be the same
    for key, value in mongodb_results.items():
        if isinstance(value, str):
            assert mongodb_results[key] == sql_results[key]
        elif isinstance(value, float):
            # make sure floats have same number of decimals before comparing
            assert format(mongodb_results[key], '.5f') == format(sql_results[key], '.5f')
