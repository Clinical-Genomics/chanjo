# -*- coding: utf-8 -*-
"""
chanjo.store.core
~~~~~~~~~~~~~~~~~~
"""
from __future__ import absolute_import, division, unicode_literals

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from .models import (
  Base,
  Superblock,
  Block,
  Interval,
  Interval_Block,
  SuperblockData,
  BlockData,
  IntervalData,
  Sample
)


class Store(object):

  """SQLAlchemy-based database object.

  Bundles functionality required to setup and interact with various
  related genomic interval elements.

  Examples:
    >>> chanjo_db = Store('data/elements.sqlite')
    >>> chanjo_db.set_up()

  .. note::

    For testing pourposes use ``:memory:`` as the ``path`` argument to
    set up in-memory (temporary) database.

  Args:
    uri (str): path/URI to the database to connect to
    dialect (str, optional): connector + type of database:
      'sqlite'/'mysql'
    debug (bool, optional): whether to output logging information

  Attributes:
    uri (str): path/URI to the database to connect to
    engine (class): SQLAlchemy engine, defines what database to use
    session (class): SQLAlchemy ORM session, manages persistance
    query (method): SQLAlchemy ORM query builder method
    classes (dict): bound ORM classes
  """

  def __init__(self, uri, dialect='sqlite', debug=False):
    super(Store, self).__init__()
    self.uri = uri

    # connect to the SQL database
    if dialect == 'sqlite':
      self.engine = create_engine("sqlite:///%s" % uri, echo=debug)

    else:
      # build URI for MySQL containing:
      # <connector>+<sql_type>://<username>:<password>@<server>/<database>
      auth_path = "%(type)s://%(uri)s" % dict(type=dialect, uri=uri)
      self.engine = create_engine(auth_path, pool_recycle=3600, echo=debug)

    # make sure the same engine is propagated to the Base classes
    Base.metadata.bind = self.engine

    # start a session
    self.session = sessionmaker(bind=self.engine)()

    # shortcut to query method
    self.query = self.session.query

    # ORM class shortcuts to enable fetching models dynamically
    self.classes = {
      'superblock': Superblock,
      'block': Block,
      'interval': Interval,
      'interval_block': Interval_Block,
      'superblock_data': SuperblockData,
      'block_data': BlockData,
      'interval_data': IntervalData,
      'sample': Sample
    }

  @property
  def dialect(self):
    """Return database dialect name used for the current connection.

    Dynamic attribute.

    Returns:
      str: name of dialect used for database connection
    """
    return self.engine.dialect.name

  def set_up(self):
    """Initialize a new database with the default tables and columns.

    Returns:
      Store: self
    """
    # create the tables
    Base.metadata.create_all(self.engine)

    return self

  def tare_down(self):
    """Tare down a database (tables and columns).

    Returns:
      Store: self
    """
    # drop/delete the tables
    Base.metadata.drop_all(self.engine)

    return self

  def save(self):
    """Manually persist changes made to various elements. Chainable.

    Returns:
      Store: ``self`` for chainability
    """
    # commit/persist dirty changes to the database
    self.session.commit()

    return self

  def get(self, typ, type_id):
    """Fetch a specific element or ORM class.

    Calls itself recursively when asked to fetch an element.

    Args:
      typ (str): element key or 'class'
      type_id (str): element id or ORM model id

    Returns:
      model: element or ORM class

    Examples:
      >>> gene = db.get('gene', 'GIT1')
    """
    if typ == 'class':
      return self.classes.get(type_id, None)

    # get an ORM class (recursive)
    klass = self.get('class', typ)

    # return the requested element object (or ``None``) if not found
    return self.session.query(klass).get(type_id)

  def find(self, klass_id, query=None, attrs=None):
    """Fetch one or more elements based on the query.

    If the 'query' parameter is a string :meth:`~chanjo.Store.find`
    will fetch one element; just like `get`. If query is a list it will
    match element ids to items in that list and return a list of
    elements. If 'query' is ``None`` all elements of that class will
    be returned.

    Args:
      klass_id (str): type of element to find
      query (str/list, optional): element Id(s)
      attrs (list, optional): list of columns to fetch

    Returns:
      object/list: element(s) from the database
    """
    # get an ORM class
    klass = self.get('class', klass_id)

    if attrs is not None:
      params = [getattr(klass, attr) for attr in attrs]
    else:
      params = (klass,)

    if query is None:
      # return all `klass_id` elements in the database
      return self.session.query(*params).all()

    elif isinstance(query, list):
      # return all `klass_id` elements in the database
      return self.session.query(*params).filter(klass.id.in_(query)).all()

    elif isinstance(query, str):
      # call 'get' to return the single element
      return self.get(klass_id, query)

    else:
      raise ValueError("'query' must be 'None', 'list', or 'str'")

  def add(self, elements):
    """Add one or more new elements and commit the changes. Chainable.

    Args:
      elements (orm/list): new ORM object instance or list of such

    Returns:
      Store: ``self`` for chainability
    """
    if isinstance(elements, Base):
      # Add the record to the session object
      self.session.add(elements)

    elif isinstance(elements, list):
      # Add all records to the session object
      self.session.add_all(elements)

    return self

  def create(self, class_id, *args, **kwargs):
    r"""Create a new instance of an ORM element.

    If attributes are supplied as a tuple they must be in the correct
    order. Supplying a `dict` doesn't require the attributes to be in
    any particular order.

    Args:
      class_id (str): choice between "superblock", "block", "interval"
      \*args (tuple): list the element attributes in the *correct order*
      \**kwargs (dict): element attributes in whatever order you like

    Returns:
      orm: new ORM instance object
    """
    if args:
      # unpack tuple
      return self.get('class', class_id)(*args)

    elif kwargs:
      # unpack dictionary
      return self.get('class', class_id)(**kwargs)

    else:
      raise TypeError('Submit attributes as arguments or keyword arguments')

  def block_stats(self, sample_id):
    """Calculate block level metrics to annotate 'transcripts'.

    Requires all related intervals to already be properly annotated.

    What's happening is we sum read depths and adequately covered bases
    for each interval in a block and then divide those numbers by the
    total interval length of the block.

    .. note::

      Block annotation needs to be carried out before annotating
      superblocks!

    Args:
      sample_id (str): sample Id to match with coverage annotations

    Returns
      list: list of tuples: ``(<block Id>, <coverage>, <completeness>)``
    """
    # length of an interval (in number of bases, hence +1)
    interval_length = Interval.end - Interval.start + 1

    # length of interval * mean coverage
    cum_interval_coverage = interval_length * IntervalData.coverage

    # summed 'cumulative' coverage for all intervals (of a block)
    cum_block_coverage = func.sum(cum_interval_coverage)

    # summed interval lengths of all intervals (of a block)
    total_block_length = func.sum(interval_length)

    # cumulative block coverage divided by total block length
    mean_block_coverage = cum_block_coverage / total_block_length

    # length of interval * mean completeness
    cum_interval_completeness = interval_length * IntervalData.completeness

    # summed cumulative completeness for all intervals (of a block)
    cum_block_completeness = func.sum(cum_interval_completeness)

    # cumulative block completeness divided by total block length
    mean_block_completeness = cum_block_completeness / total_block_length

    # values to fetch
    interval_block_columns = Interval_Block.columns.values()
    interval_id = interval_block_columns[0]
    block_id = interval_block_columns[1]

    return self.query(
      block_id,
      mean_block_coverage,
      mean_block_completeness
    ).join(IntervalData, interval_id==Interval.id).join(IntervalData.parent)\
     .filter(IntervalData.sample_id==sample_id).group_by(block_id)

  def superblock_stats(self, sample_id):
    """Calculate superblock level metrics to annotate genes.

    Requires all related blocks to already be properly annotated.

    What's happening is that we are simply taking the average of the
    metrics on the transcript level and applying that as gene metrics.
    This gives a decent, albeit not perfect, represenation of gene
    level metrics.

    .. note::

      Annotation of transcripts needs to be acomplished before
      annotating genes!

    Args:
      sample_id (str): sample Id to match with coverage annotations

    Returns:
      list: list of tuples: ``(<gene_id>, <coverage>, <completeness>)``
    """
    return self.query(
      Block.superblock_id,
      func.avg(BlockData.coverage),
      func.avg(BlockData.completeness)
    ).join(BlockData, Block.id==BlockData.parent_id)\
     .filter(BlockData.sample_id == sample_id)\
     .group_by(Block.superblock_id)
