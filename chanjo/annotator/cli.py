# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json

import click
from path import path
from pysam import Samfile
from toolz import pipe
from toolz.curried import map

from .core import annotate_bed_stream
from .utils import get_sample_id
from ..utils import id_generator, serialize_interval, validate_stdin


@click.command()
@click.option('-s', '--sample', help='unique id (otherwise auto-generated)')
@click.option('-g', '--group', help='id to associate samples e.g. in trios')
@click.option('-c', '--cutoff', default=10, help='cutoff for completeness')
@click.option(
  '-e', '--extendby', default=0, help='extend intervals symetrically')
@click.option(
  '-p', '--prefix', default='', help='prefix a string to each contig')
@click.option(
  '-t', '--threshold',
  default=17000, help='base pair threshold to optimize BAM-file reading')
@click.argument('bam_path', type=click.Path(exists=True))
@click.argument(
  'in_stream', callback=validate_stdin, type=click.File(encoding='utf-8'),
  default='-', required=False)
@click.pass_context
def annotate(context, bam_path, in_stream, sample, group, cutoff,
             extendby, prefix, threshold):
  """Annotate intervals in a BED-file/stream.

  \b
  BAM_PATH: Path to BAM-file
  IN_STREAM: Chanjo-style BED-file with interval definitions
  """
  # connect to the BAM file
  with Samfile(bam_path) as bam:
    # user defined sample id or randomly generated
    sample = (sample or get_sample_id(bam.header) or id_generator())

  # step 1: metadata header
  metadata = dict(
    sample_id=sample,
    group_id=group,
    cutoff=cutoff,
    coverage_source=path(bam_path).abspath(),
    extension=extendby
  )
  click.echo("#%s" % json.dumps(metadata))

  # step 2: annotate list of intervals with coverage and completeness
  bed_lines = pipe(
    annotate_bed_stream(
      bed_stream=in_stream,
      bam_path=bam_path,
      cutoff=cutoff,
      extension=extendby,
      contig_prefix=prefix,
      bp_threshold=threshold
    ),
    map(serialize_interval(bed=True))    # stringify/bedify
  )

  # reduce/write the BED lines
  for bed_line in bed_lines:
    click.echo(bed_line)
