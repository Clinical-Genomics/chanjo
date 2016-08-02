# -*- coding: utf-8 -*-
import click
import logging

from .run import run_sambamba

log = logging.getLogger(__name__)


@click.command()
@click.option('-r', '--regions', type=click.Path(exists=True), required=True,
              help='Path to a bed file with exon coordinates')
@click.option('-t', '--cov_treshold', multiple=True, type=int,
              help=("multiple thresholds can be provided,"
                    "for each one an extra column will be added,"
                    "the percentage of bases in the region"
                    "where coverage is more than this value"))
@click.option('-o', '--outfile', type=click.Path(exists=False),
              help='Specify path to a file where results should be stored.')
@click.argument('bam_file', type=click.Path(exists=True))
@click.pass_context
def sambamba(context, bam_file, regions, cov_treshold, outfile):
    """Run Sambamba from chanjo."""
    log.info("Running chanjo sambamba")
    try:
        run_sambamba(bam_file, regions, outfile, cov_treshold)
    except Exception as error:
        log.exception('something went really wrong :_(')
        context.abort()
