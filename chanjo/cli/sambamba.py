# -*- coding: utf-8 -*-
import click
import logging
import subprocess

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
                help="multiple thresholds can be provided,"\
                     "for each one an extra column will be added,"\
                     "the percentage of bases in the region"\
                     "where coverage is more than this value"
)
@click.pass_context
def sambamba(context, bam_file, exon_bed, gene_bed, cov_treshold):
    """Run Sambamba from chanjo."""
    logger = logging.getLogger(__name__)
    #For testing only:
    logger = logging.getLogger("chanjo.cli.sambamba")
    logger.info("bam_file:{0}".format(bam_file))
    click.echo("bam_file:{0}".format(bam_file)) #For testing


def run_sambamba():
    """docstring for run_sambamba"""
    pass


if __name__ == '__main__':
    # from chanjo.log impo
    sambamba()
