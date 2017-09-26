# -*- coding: utf-8 -*-
import logging

import click

from chanjo.sambamba import run_sambamba

LOG = logging.getLogger(__name__)


@click.command()
@click.option('-r', '--regions', type=click.Path(exists=True), required=True,
              help='Path to a bed file with exon coordinates')
@click.option('-t', '--cov-threshold', 'cov_thresholds', multiple=True, type=int,
              help=("multiple thresholds can be provided,"
                    "for each one an extra column will be added,"
                    "the percentage of bases in the region"
                    "where coverage is more than this value"))
@click.option('-o', '--outfile', type=click.Path(exists=False),
              help='Specify path to a file where results should be stored.')
@click.argument('bam_file', type=click.Path(exists=True))
@click.pass_context
def sambamba(context, bam_file, regions, cov_thresholds, outfile):
    """Run Sambamba from chanjo."""
    LOG.info("Running chanjo sambamba")
    try:
        run_sambamba(bam_file, regions, outfile, cov_thresholds)
    except Exception:
        LOG.exception('something went really wrong :_(')
        context.abort()
