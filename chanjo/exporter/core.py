# -*- coding: utf-8 -*-
from __future__ import absolute_import

from toolz import pipe, concat, juxt, last
from toolz.curried import compose, map, take

from .producers import fetch_records
from ..store import Interval


def export_intervals(chanjo_db, include_header=True, bed_score=0):
  r"""Return BED-formatted interval lines from existing ``chanjo_db``.

  BED lines are ready to be printed or written to a file.

  Args:
    chanjo_db (session): ``sqlalchemy.orm.session`` object with a
      ``.query``-method
    include_header (bool, optional): whether to include BED header
    bed_score (int, optional): dummy score (0-1000) to insert at field 5
      to complete the BED format

  Yields:
    str: stringified and tab-delimited interval

  Examples:
    >>> from chanjo import export_intervals, Store
    ... # instantiate a new connection to a Chanjo database
    >>> db = Store('./coverage.sqlite')
    >>> with open('intervals.sorted.bed', 'w') as stream:
    ...   # write intervals in BED-format with appropriate headers
    ...   for bed_line in export_intervals(db):
    ...     stream.write(bed_line + '\n')
  """
  if include_header:
    yield '#chrom\tchromStart\tchromEnd\tname\tscore\tstrand'

  # setup up which columns to fetch to make BED file
  # column 5 is just a silly default for the "score" field in BED
  i = Interval  # alias
  columns = (i.contig, i.start - 1, i.end, i.id, i.strand)

  # BED files are tab-delimited
  delimiter = '\t'

  # 1. fetch interval tuples from the database (producer)
  # 2. stringify each item in each subsequence (interval tuple)
  # 3. join lines on tab-character
  # 4. prepend the header
  bed_lines = pipe(
    fetch_records(chanjo_db, columns),
    map(map(str)),                        # convert fields to strings
    map(juxt(compose(list, take(4)),      # keep first 4 fields
             lambda _: [str(bed_score)],  # insert BED score
             compose(list, last))),       # keep last field
    map(concat),                          # flatten each item
    map(delimiter.join)                   # join on \t
  )

  for bed_line in bed_lines:
    yield bed_line
