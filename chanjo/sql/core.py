# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from .models import Base, Superblock, Block, Interval, Interval_Block, \
  SuperblockData, BlockData, IntervalData, Sample


class ChanjoDB(object):
  """SQLAlchemy-based :class:`ChanjoDB`. It collects functionality
  needed to setup and interact with a SQLAlchemy session.

  .. code-block:: python

    >>> from chanjo.sql.core import ChanjoDB
    >>> db = ChanjoDB('data/elements.sqlite')

  .. note::

    For testing pourposes; use ":memory:" as the `path` argument to set
    up in-memory version of the database.

  Args:
    uri (str): Path/URI to the database to connect to
    dialect (str, optional): Connector + type of database: 'sqlite'/'mysql'
    debug (bool, optional): Whether to print logging information
  """
  def __init__(self, uri, dialect='sqlite', debug=False):
    super(ChanjoDB, self).__init__()
    self.uri = uri

    # Connect to the SQL database
    if dialect == 'sqlite':
      self.engine = create_engine('sqlite:///' + uri, echo=debug)

    else:
      # Build URI for MySQL containing:
      # <connector>+<sql_type>://<username>:<password>@<server>/<database>
      auth_path = '{type}://{uri}'.format(type=dialect, uri=uri)
      self.engine = create_engine(auth_path, pool_recycle=3600, echo=debug)

    # Make sure the same engine is propagated to the Base classes
    Base.metadata.bind = self.engine

    # Start a session
    self.session = sessionmaker(bind=self.engine)()

    # Shortcut to query
    self.query = self.session.query

    # ORM class shortcuts to enable fetching dynamically
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

  def setup(self):
    """Sets up a new database with the default tables and columns.

    Returns:
      ChanjoDB: self
    """
    # Create the tables
    Base.metadata.create_all(self.engine)

    return self

  def tare_down(self):
    """Tares down a database (tables and columns).

    Returns:
      ChanjoDB: self
    """
    # Create the tables
    Base.metadata.drop_all(self.engine)

    return self

  def commit(self):
    """Manually persist changes made to various elements. Chainable.

    Returns:
      ChanjoDB: ``self`` for chainability
    """
    # Commit/persist dirty changes to the database
    self.session.commit()

    return self

  def get(self, typ, type_id):
    """Fetches a specific element or ORM class. Calls itself recursively
    when asked to fetch an element.

    .. code-block:: python

      >>> db = ChanjoDB('path/to/element.sqlite')

      # Get a specific gene from the database
      >>> gene = db.get('gene', 'GIT1')

    Args:
      typ (str): Element key or 'class'
      type_id (str): Element ID or ORM class ID

    Returns:
      orm: Element or ORM class
    """
    if typ == 'class':
      return self.classes.get(type_id, None)

    # Get an ORM class (recursive)
    klass = self.get('class', typ)

    # Return the requested element object (or ``None``) if not found
    return self.session.query(klass).get(type_id)

  def find(self, klass_id, query=None, attrs=None):
    """If the 'query' parameter is a string `find` will fetch one
    element; just like `get`. If query is a list it will match element
    IDs to items in that list and return a list of elements. If 'query'
    is ``None`` all elements of that class will be returned.

    Args:
      klass_id (str): The type of element to find
      query (str/list, optional): Element Id(s)
      attrs (list, optional): List of columns to fetch

    Returns:
      object/list: Element(s) from the database
    """
    # Get an ORM class
    klass = self.get('class', klass_id)

    if attrs is not None:
      params = [getattr(klass, attr) for attr in attrs]
    else:
      params = (klass,)

    if query is None:
      # Return all `klass_id` elements in the database
      return self.session.query(*params).all()

    elif isinstance(query, list):
      # Return all `klass_id` elements in the database
      return self.session.query(*params).filter(klass.id.in_(query)).all()

    elif isinstance(query, str):
      # Call 'get' to return the single element
      return self.get(klass_id, query)

    else:
      raise ValueError("'query' must be 'None', 'list', or 'str'")

  def add(self, elements):
    """Add one or multiple new elements to the database and commit the
    changes. Chainable.

    Args:
      elements (orm/list): New ORM object instance or list of such

    Returns:
      ChanjoDB: ``self`` for chainability
    """
    if isinstance(elements, Base):
      # Add the record to the session object
      self.session.add(elements)

    elif isinstance(elements, list):
      # Add all records to the session object
      self.session.add_all(elements)

    return self

  def create(self, class_id, *args, **kwargs):
    """Creates a new instance of an ORM element object filled in with
    the given `attributes`.

    If attributes is a tuple they must be in the correct order.
    Supplying a `dict` doesn't require the attributes to be in any
    particular order.

    Args:
      class_id (str): Choice between "superblock", "block", "interval"
      \*args (tuple): List the element attributes in the *correct order*
      \**kwargs (dict): Element attributes in whatever order you like

    Returns:
      orm: The new ORM instance object
    """
    if args:
      # Unpack tuple
      return self.get('class', class_id)(*args)
    elif kwargs:
      # Unpack dictionary
      return self.get('class', class_id)(**kwargs)
    else:
      raise TypeError('Submit attributes as arguments or keyword arguments')

  def block_stats(self, sample_id):
    """Calculates block level metrics to annotate 'transcripts'.
    Requires all related intervals to already be properly annotated.

    What's happening is we sum read depths and adequately covered bases
    for each interval in a block and then divide those numbers by the
    total interval length of the block.

    .. note::
      Block annotation needs to be carried out before annotating
      superblocks!

    Args:
      sample_id (str): Sample Id to match with coverage annotations

    Returns
      list: List of tuples: ``(<block Id>, <coverage>, <completeness>)``
    """
    # Length of an interval (in number of bases, hence +1)
    interval_length = Interval.end - Interval.start + 1

    # Length of interval * mean coverage
    cum_interval_coverage = interval_length * IntervalData.coverage

    # Summed 'cumulative' coverage for all intervals (of a block)
    cum_block_coverage = func.sum(cum_interval_coverage)

    # Summed interval lengths of all intervals (of a block)
    total_block_length = func.sum(interval_length)

    # Cumulative block coverage divided by total block length
    mean_block_coverage = cum_block_coverage / total_block_length

    # Length of interval * mean completeness
    cum_interval_completeness = interval_length * IntervalData.completeness

    # Summed cumulative completeness for all intervals (of a block)
    cum_block_completeness = func.sum(cum_interval_completeness)

    # Cumulative block completeness divided by total block length
    mean_block_completeness = cum_block_completeness / total_block_length

    # Values to fetch
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
    """Calculates superblock level metrics to annotate genes. Requires all
    related blocks to already be properly annotated.

    What's happening is that we are simply taking the average of the metrics
    on the transcript level and applying that as gene metrics. This gives a
    decent, albeit not perfect, represenation of gene level metrics.

    .. note::

      Annotation of transcripts needs to be acomplished before annotating
      genes!

    Args:
      sample_id (str): Sample Id to match with coverage annotations

    Returns:
      list: List of tuples: ``(<gene_id>, <coverage>, <completeness>)``
    """
    return self.query(
      Block.superblock_id,
      func.avg(BlockData.coverage),
      func.avg(BlockData.completeness)
    ).join(BlockData, Block.id==BlockData.parent_id)\
     .filter(BlockData.sample_id == sample_id)\
     .group_by(Block.superblock_id)
