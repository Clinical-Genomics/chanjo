# -*- coding: utf-8 -*-
from datetime import datetime

import pytest
from sqlalchemy.orm.exc import FlushError
from pymongo.errors import DuplicateKeyError

from chanjo.store.api import ChanjoDB
from chanjo.store.models import Sample


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
