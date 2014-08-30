# -*- coding: utf-8 -*-


def fetch_records(db, columns, order_columns=None):
  """Fetch a list of columns from a *single* SQLAlchemy ORM object.

  Also works for a single table. Returns the results as a list of
  tuples.

  Args:
    db (session): ``sqlalchemy.orm.session`` object with a
      ``.query``-method
    columns (list): list of ``sqlalchemy.Column`` from a single ORM
    order_columns (list, optional): model columns to sort by

  Yields:
    tuple: requested columns from a matching record in the SQL query
  """
  # initialize query
  query = db.query(*columns)

  # order the results on request
  if order_columns:
    query = query.order_by(*order_columns)

  # execute the query and yield the result as a list of tuples
  for record in query.all():
    yield record
