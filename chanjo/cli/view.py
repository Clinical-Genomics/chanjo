# -*- coding: utf-8 -*-
import logging

import click

from chanjo.store.api import ChanjoDB
from chanjo.store.models import TranscriptStat
from .calculate import dump_json

LOG = logging.getLogger(__name__)

@click.group()
@click.pass_context
def view(context):
    """View infromation from database."""
    if not context.obj['database']:
        LOG.warning("Please point to a database")
        context.abort()
    context.obj['db'] = ChanjoDB(uri=context.obj['database'])


@view.command()
@click.option('-s', '--sample', multiple=True, help='sample(s) to limit query to')
@click.option('-g', '--group', multiple=True, help='group(s) to limit query to')
@click.pass_context
def sample(context, sample, group):
    """View information on samples."""
    result = context.obj['db'].sample(sample, group)
    for res in result:
        click.echo("sample_id: {0}, group_id: {1}, source: {2}".format(
            res.id, res.group_id, res.source
        ))

@view.command()
@click.option('-i', '--gene-id', type=int, help='Gene id for a gene')
@click.option('--gene-symbol', help='Gene symbol for a gene')
@click.option('-p', '--pretty', is_flag=True)
@click.pass_context
def gene(context, gene_id, gene_symbol, pretty):
    """Display all transcripts for a gene"""
    if not (gene_id or gene_symbol):
        LOG.warning('Please specify a gene')
        context.abort()
        
    result = context.obj['db'].gene(gene_id, gene_symbol)
    if result.count() == 0:
        LOG.info("No genes found")
    
    for res in result:
        row = {
            'id': res.id,
            'gene_id': res.gene_id,
            'gene_name': res.gene_name,
            'chromosome': res.chromosome,
            'length': res.length,
        }
        click.echo(dump_json(row, pretty=pretty))

@view.command()
@click.option('-s', '--sample', help='sample to limit query to')
@click.pass_context
def incomplete(context, sample):
    """Wiew all transcripts with incomplete exons for a sample"""
    query = context.obj['db'].query(TranscriptStat).filter_by(sample_id=sample)
    result = query.filter(TranscriptStat._incomplete_exons.isnot(None))
    for res in result:
        print(res)
