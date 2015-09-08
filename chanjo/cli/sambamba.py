# -*- coding: utf-8 -*-
import sys
import click
import logging

from chanjo.annotate.sambamba import run_sambamba


@click.command()
@click.argument('bam_file',
                    type=click.Path(exists=True),
)
@click.option('-e', '--exon_bed',
                type=click.Path(exists=True),
                help="Path to a bed file with exon coordinates"
)
@click.option('-g', '--gene_bed',
                type=click.Path(exists=True),
                help="Path to a bed file with gene coordinates"
)
@click.option('-t', '--cov_treshold',
                multiple=True,
                type=int,
                help="multiple thresholds can be provided,"\
                     "for each one an extra column will be added,"\
                     "the percentage of bases in the region"\
                     "where coverage is more than this value"
)
@click.option('-o', '--outfile',
                    type=click.Path(exists=False),
                    help='Specify the path to a file where results should be stored.'
)
@click.pass_context
def sambamba(context, bam_file, exon_bed, gene_bed, cov_treshold, outfile):
    """Run Sambamba from chanjo."""
    logger = logging.getLogger(__name__)
    # For testing only:
    logger = logging.getLogger("chanjo.cli.sambamba")
    logger.info("Running chanjo sambamba")

    if not (exon_bed or gene_bed):
        logger.warning("Please provide a region file in BED format")
        sys.exit()
    if exon_bed and gene_bed:
        logger.warning("Only one region file at a time")
        sys.exit()

    region_file = exon_bed
    if gene_bed:
        region_file = gene_bed

    try:
        run_sambamba(bam_file, region_file, outfile, cov_treshold)
    except Exception as e:
        logger.debug(e)
        click.Abort()
