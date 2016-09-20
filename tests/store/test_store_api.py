# -*- coding: utf-8 -*-
from datetime import datetime

import pytest
from sqlalchemy.orm.exc import FlushError

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
