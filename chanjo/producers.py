# -*- coding: utf-8 -*-
"""
chanjo.producers
~~~~~~~~~~~~~~~~~
Initial pipes in a pipeline, also known as 'producers'. Generate values
to feed into a pipeline. What makes them stand out is that they don't
have a ``stdin`` object to be piped to.
"""
from .pyxshell.pipeline import pipe


@pipe
def fetch_records(db, columns, order_columns=None):
  """Performs a simple SQL query to fetch a list of columns from a
  *single* SQLAlchemy ORM object (or table). Returns the results as a
  list of tuples.

  Args:
    db (session): ``sqlalchemy.orm.session`` object with a
      ``.query``-method
    columns (list): List of ``sqlalchemy.Column`` from a single ORM

  Returns:
    list: List of tuples with the results from the SQL query
  """
  # Initialize query
  query = db.query(*columns)

  # Order the results on request
  if order_columns:
    query = query.order_by(*order_columns)

  # Return the result set as a list of tuples
  for record in query.all():
    yield record


@pipe
def more(stream):
  """Like :func:`cat` but accepts a stream instead of opening a file to
  read from.

  Args:
    stream: File handle to read from

  Yields:
    str: line from the input stream
  """
  with stream as handle:
    for line in handle:
      yield line
