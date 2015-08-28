# -*- coding: utf-8 -*-
import click

import subprocess

@click.command()
@click.argument('bam_file',
                    type=click.Path(exists=True),
)
@click.option('-e', '--exon_bed',
                type=click.Path(exists=True),
)
@click.pass_context
def sambamba(context, bam_file, exon_bed):
    """Run Sambamba from chanjo."""
    click.echo("bam_file:{0}".format(bam_file))


def run_sambamba():
    """docstring for run_sambamba"""
    pass


if __name__ == '__main__':
    sambamba()
