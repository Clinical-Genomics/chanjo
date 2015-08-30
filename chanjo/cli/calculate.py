# -*- coding: utf-8 -*-
import json

import click
from sqlalchemy.sql import func

from chanjo.store import Store, ExonStatistic, Sample


@click.group()
@click.pass_context
def calculate(context):
    """Calculate simple metrics from the database."""
    context.db = Store(uri=context.obj['database'])


@calculate.command()
@click.argument('samples', nargs=-1)
@click.pass_context
def mean(context, samples):
    """Report mean coverage for a list of samples."""
    results = (context.parent.db.query(Sample.sample_id,
                                       func.avg(ExonStatistic.value))
                      .filter(ExonStatistic.metric == 'mean_coverage')
                      .group_by(ExonStatistic.sample_id))
    if samples:
        results.filter(Sample.sample_id.in_(samples))

    for sample_id, mean_coverage in results:
        json_dump = json.dumps(dict(sample_id=sample_id,
                                    mean_coverage=mean_coverage))
        click.echo(json_dump)
