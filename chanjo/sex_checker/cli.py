# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import click

from .._compat import text_type
from .core import gender_from_bam


@click.command('sex-check')
@click.option(
  '-p', '--prefix', default='', help='prefix a string to each contig')
@click.argument('bam_path', type=click.Path(exists=True))
@click.version_option('1.0')
def sex_check(bam_path, prefix):
  """Sex Check - predict gender from a BAM-alignment.

  \b
  BAM_PATH: path to BAM-file
  """
  # run the sex checker pipeline
  gender = gender_from_bam(bam_path, prefix=prefix)

  # print the results to the console for pipeability (csv)
  click.echo("#%(prefix)sX_coverage\t%(prefix)sY_coverage\tsex"
             % dict(prefix=prefix))
  click.echo('\t'.join(map(text_type, gender)))
