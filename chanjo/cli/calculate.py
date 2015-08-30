# -*- coding: utf-8 -*-
import json
import logging

import click
from sqlalchemy.sql import func

from chanjo.compat import itervalues
from chanjo.store import Exon, ExonStatistic, Gene, Sample, Store, Transcript

logger = logging.getLogger(__name__)


def group_by_sample(results):
    samples = {}
    for sample_id, metric, value in results:
        if sample_id not in samples:
            samples[sample_id] = {'sample_id': sample_id}
        samples[sample_id][metric] = value

    return itervalues(samples)


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
                                       ExonStatistic.metric,
                                       func.avg(ExonStatistic.value))
                      .join(ExonStatistic.sample)
                      .group_by(Sample.sample_id, ExonStatistic.metric))
    if samples:
        results = results.filter(Sample.sample_id.in_(samples))

    for data in group_by_sample(results):
        json_dump = json.dumps(data)
        click.echo(json_dump)


@calculate.command()
@click.argument('gene_ids', nargs=-1)
@click.pass_context
def gene(context, gene_ids):
    """Report aggregate statistics for particular genes."""
    db = context.parent.db
    samples = {}
    for gene_id in gene_ids:
        logger.debug('figure out which transcripts the gene belongs to')
        tx_ids = (db.query(Transcript.transcript_id)
                    .join(Transcript.gene)
                    .filter(Gene.gene_id == gene_id).all())
        if len(tx_ids) == 0:
            raise AttributeError('gene id not in database: {}'.format(gene_id))
        else:
            tx_ids = tx_ids[0]

        results = (db.query(Sample.sample_id, ExonStatistic.metric,
                            func.avg(ExonStatistic.value))
                     .join(ExonStatistic.sample, ExonStatistic.exon,
                           Exon.transcripts)
                     .filter(Transcript.transcript_id.in_(tx_ids))
                     .group_by(Sample.sample_id, ExonStatistic.metric))

        for data in group_by_sample(results):
            if data['sample_id'] not in samples:
                samples[data['sample_id']] = {'sample_id': data['sample_id']}
            samples[data['sample_id']][gene_id] = data

    for sample_data in itervalues(samples):
        json_dump = json.dumps(sample_data)
        click.echo(json_dump)
