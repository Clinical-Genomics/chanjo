# -*- coding: utf-8 -*-
from chanjo.store.models import Sample


def test_mean(populated_db):
    # GIVEN a database loaded with one sample
    assert Sample.query.count() == 1
    # WHEN calculating mean values across metrics
    query = populated_db.mean()
    # THEN the results should group over one "row"
    results = query.all()
    assert len(results) == 1
    sample = results[0]
    assert sample[0] == 'sample'  # sample id
    for metric in filter(None, sample[1:]):
        assert isinstance(metric, float)


def test_gene(populated_db):
    # GIVEN a database populated with a single sample
    assert Sample.query.count() == 1
    # WHEN calculating average metrics for a gene
    query = populated_db.gene_metrics('SAMD11')
    # THEN the results should add up to a single row
    results = query.all()
    assert len(results) == 1
    sample = results[0]
    assert sample[0] == 'sample'
    assert sample[-1] == 'SAMD11'
