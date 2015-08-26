# -*- coding: utf-8 -*-
"""
chanjo.builder.core
~~~~~~~~~~~~~~~~~~~~

Central pipeline for the Chanjo builder module.
"""
from __future__ import absolute_import
import errno
import os

from path import path

from ..store import Exon


def parse_line(line):
    naked_line = line.strip()
    row = naked_line.split('\t')
    data = {
        'chromosome': row[0],
        'start': int(row[1]),
        'end': int(row[2]),
        'id': row[3],
        'score': row[4],
        'strand': row[5],
        'transcripts': row[6].split(','),
        'genes': row[7].split(',')
    }

    return data


def build_exon(data):
    """Build exon object."""
    exon_obj = Exon(exon_id=data['id'], chromosome=data['chromosome'],
                    start=data['start'], end=data['end'])


def parse_bed(stream):
    """Parse BED file with definitions for exon/transcript/gene."""
    datas = (parse_line(line) for line in stream)
    exons = (build_exon(data) for data in datas)

    return exons


def init_db(chanjo_db, bed_stream, overwrite=False):
  """Build a new database instance from the Chanjo BED stream.

  Args:
    chanjo_db (Store): initialized Store class instance
    bed_stream (sequence): Chanjo-style BED-stream
    overwrite (bool, optional): whether to automatically overwrite an
      existing database, defaults to False
  """
  # check if the database already exists (expect 'mysql' to exist)
  # 'dialect' is in the form of '<db_type>+<connector>'
  if chanjo_db.dialect == 'mysql' or path(chanjo_db.uri).exists():
    if overwrite:
      # wipe the database clean with a warning
      chanjo_db.tear_down()
    elif chanjo_db.dialect == 'sqlite':
      # prevent from wiping existing database to easily
      raise OSError(errno.EEXIST, os.strerror(errno.EEXIST), chanjo_db.uri)

  # set up new tables
  chanjo_db.set_up()

  exon_objs = [exon for exon in parse_bed(bed_stream)]
  chanjo_db.add(exon_objs)

  # commit also the last contig
  chanjo_db.save()
