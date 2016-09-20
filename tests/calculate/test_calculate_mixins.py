# -*- coding: utf-8 -*-
from chanjo.store.models import Sample


def test_mean(populated_db):
    # GIVEN a database loaded with 2 samples
    assert Sample.query.count() == 2
    # WHEN calculating mean values across metrics
    query = populated_db.mean()
    # THEN the results should group over 2 "rows"
    results = query.all()
    assert len(results) == 2
    sample_ids = set(result[0] for result in results)
    assert sample_ids == set(['sample', 'sample2'])  # sample id
    result = results[0]
    for metric in filter(None, result[1:]):
        assert isinstance(metric, float)


def test_mean_with_samples(populated_db):
    # GIVEN a database loaded with 2 samples
    assert Sample.query.count() == 2
    # WHEN calculating mean values across metrics for a particular sample
    sample_id = 'sample'
    query = populated_db.mean(sample_ids=[sample_id])
    # THEN the results should be limited to that sample
    results = query.all()
    assert len(results) == 1
    result = results[0]
    assert result[0] == sample_id


def test_gene(populated_db):
    # GIVEN a database populated with a single sample
    assert Sample.query.count() == 2
    # WHEN calculating average metrics for a gene
    query = populated_db.gene_metrics('SAMD11')
    # THEN the results should add up to a single row
    results = query.all()
    assert len(results) == 2
    result = results[0]
    assert result[0] == 'sample'
    assert result[-1] == 'SAMD11'
