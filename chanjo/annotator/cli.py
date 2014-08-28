# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json

import click
from path import path
from toolz import pipe

from .core import annotate_bed_stream
from ..cli import out_option, prefix_option, bam_path_argument, in_argument
from ..utils import id_generator, serialize_interval_plus


@click.command()
@click.option('--sample', help='unique sample id (otherwise auto-generated)')
@click.option('--group', help='group id to associate samples e.g. in trios')
@click.option('--cutoff', default=10, help='cutoff for completeness')
@click.option(
  '--extendby', default=0, help='dynamically extend intervals symetrically')
@prefix_option
@click.option(
  '--threshold',
  default=17000,
  help='base pair threshold for optimizing BAM-file reading')
@out_option
@bam_path_argument
@in_argument
@click.pass_context
def annotate(context, bam_path, in_stream, out, sample, group, cutoff,
             extendby, prefix, threshold):
  """Annotate intervals in a BED-file/stream.

  \b
  BAM_PATH: Path to BAM-file
  IN_STREAM: Chanjo-style BED-file with interval definitions
  """
  # user defined sample id or randomly generated
  sample = (sample or id_generator())

  # step 1: metadata header
  metadata = dict(
    sample_id=sample,
    group_id=group,
    cutoff=cutoff,
    coverage_source=path(bam_path).abspath(),
    extension=extendby
  )
  click.echo("#%s" % json.dumps(metadata), file=out)

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
    map(serialize_interval_plus)    # stringify/bedify
  )

  # reduce/write the BED lines
  for bed_line in bed_lines:
    click.echo(bed_line, file=out)
