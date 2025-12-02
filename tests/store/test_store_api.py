"""
Tests for store
"""

from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from chanjo.store.api import ChanjoDB
from chanjo.store.models import Sample, TranscriptStat


def test_dialect(chanjo_db):
    assert chanjo_db.dialect == "sqlite"


def test_no_dialect():
    # GIVEN not explicity specifying SQLite dialect
    # WHEN setting up the API
    chanjo_db = ChanjoDB(":memory:")
    # THEN chanjo should guess it
    assert chanjo_db.dialect == "sqlite"


def test_add_many(chanjo_db):
    # GIVEN multiple new samples
    new_samples = [Sample(id="ADM12"), Sample(id="ADM13")]
    with chanjo_db.begin() as session:
        # WHEN added to the session
        session.save_all(new_samples)
        # THEN all samples should be added
        assert session.all(Sample.select()) == new_samples


def test_fetch_samples(populated_db):

    # GIVEN a populated db and an existing sample-id
    store = populated_db
    sample_id = "sample"
    # WHEN fetching a sample
    samples = list(store.fetch_samples(sample_id=sample_id))
    # THEN only the sample with specified sample-id is found
    assert len(samples) == 1
    sample = samples[0]
    assert sample.id == sample_id


def test_fetch_samples_non_existing(populated_db):

    # GIVEN a populated db and a non existing sample-id
    store = populated_db
    sample_id = "no_sample"
    # WHEN fetching a sample
    samples = list(store.fetch_samples(sample_id=sample_id))
    # THEN no samples are found
    assert len(samples) == 0


def test_fetch_samples_by_group_id(populated_db):

    # GIVEN a populated db and an existing group-id
    store = populated_db
    group_id = "group"

    # WHEN fetching the samples in a group
    samples = list(store.fetch_samples(group_id=group_id))

    # THEN all samples in group are found
    assert len(samples) == 2
    for sample in samples:
        assert sample.id in ["sample", "sample2"]
        assert sample.group_id == group_id


def test_samples_group_non_existing(populated_db):

    # GIVEN a populated db and a non existing group-id
    store = populated_db
    group_id = "no_group"

    # WHEN fetching the samples in a group
    samples = list(store.fetch_samples(group_id=group_id))

    # THEN no samples are found
    assert len(samples) == 0


def test_fetch_transcripts(populated_db):

    # GIVEN a populated database and a sample-id
    store = populated_db
    sample_id = "sample"

    # WHEN fetching transcrips from database
    transcripts = list(store.fetch_transcripts(sample_id=sample_id))

    # THEN transcripts for that sample are found
    assert len(transcripts) != 0


def test_delete_sample(populated_db):

    # GIVEN a populated database and a sample-id
    store = populated_db
    sample_id = "sample"
    with populated_db.begin() as session:
        assert len(list(store.fetch_samples(sample_id=sample_id))) != 0
        assert session.all(TranscriptStat.select().where(TranscriptStat.sample_id == sample_id))
        assert len(list(store.fetch_transcripts(sample_id=sample_id))) != 0

        # WHEN deleting a sample
        store.delete_sample(sample_id=sample_id)

        # THEN that sample and all its transcripts are deleted from the database
        assert len(list(store.fetch_samples(sample_id=sample_id))) == 0
        assert (
            len(session.all(TranscriptStat.select().where(TranscriptStat.sample_id == sample_id)))
            == 0
        )
        assert len(list(store.fetch_transcripts(sample_id=sample_id))) == 0


def test_delete_group(populated_db):

    # GIVEN a populated database and a sample-id
    store = populated_db
    group_id = "group"
    assert len(list(store.fetch_samples(group_id=group_id))) != 0

    # WHEN deleting a sample
    store.delete_group(group_id=group_id)

    # THEN that sample and all its transcripts are deleted from the database
    assert len(list(store.fetch_samples(group_id=group_id))) == 0
