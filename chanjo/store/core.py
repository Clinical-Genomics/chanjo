# -*- coding: utf-8 -*-
"""
chanjo.store.core
~~~~~~~~~~~~~~~~~~
"""
from __future__ import division
import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql.expression import ClauseElement

from .models import (BASE, Gene, Transcript, Exon, Sample)

logger = logging.getLogger(__name__)


class Store(object):

    """SQLAlchemy-based database object.

    Bundles functionality required to setup and interact with various
    related genomic interval elements.

    .. versionchanged:: 2.1.0
        Lazy-loadable, all "init" arguments optional.

    Examples:
        >>> chanjo_db = Store('data/elements.sqlite3')
        >>> chanjo_db.set_up()

    .. note::

        For testing pourposes use ``:memory:`` as the ``path`` argument to
        set up in-memory (temporary) database.

    Args:
        uri (Optional[str]): path/URI to the database to connect to
        debug (Optional[bool]): whether to output logging information
        base (Optional[sqlalchemy.ext.declarative.api.Base]): schema definition

    Attributes:
        uri (str): path/URI to the database to connect to
        base (sqlalchemy.ext.declarative.api.Base): shcema definition
        engine (class): SQLAlchemy engine, defines what database to use
        session (class): SQLAlchemy ORM session, manages persistance
        query (method): SQLAlchemy ORM query builder method
        classes (dict): bound ORM classes
    """

    def __init__(self, uri=None, debug=False, base=BASE):
        super(Store, self).__init__()
        self.uri = uri
        self.base = base
        if uri:
            self.connect(uri, debug=debug)

        # ORM class shortcuts to enable fetching models dynamically
        self.classes = {'gene': Gene, 'transcript': Transcript,
                        'exon': Exon, 'sample': Sample}

    def connect(self, db_uri, debug=False):
        """Configure connection to a SQL database.

        .. versionadded:: 2.1.0

        Args:
            db_uri (str): path/URI to the database to connect to
            debug (Optional[bool]): whether to output logging information
        """
        kwargs = {'echo': debug, 'convert_unicode': True}
        # connect to the SQL database
        if 'mysql' in db_uri:
            kwargs['pool_recycle'] = 3600
        elif '://' not in db_uri:
            # expect only a path to a sqlite database
            db_path = os.path.abspath(os.path.expanduser(db_uri))
            db_uri = "sqlite:///{}".format(db_path)

        self.engine = create_engine(db_uri, **kwargs)
        # make sure the same engine is propagated to the BASE classes
        self.base.metadata.bind = self.engine
        # start a session
        self.session = scoped_session(sessionmaker(bind=self.engine))
        # shortcut to query method
        self.query = self.session.query
        return self

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
        self.base.metadata.create_all(self.engine)
        tables = self.base.metadata.tables.keys()
        logger.info("created tables: %s", ', '.join(tables))
        return self

    def tear_down(self):
        """Tear down a database (tables and columns).

        Returns:
            Store: self
        """
        # drop/delete the tables
        self.base.metadata.drop_all(self.engine)
        return self

    def get_or_create(self, model, **kwargs):
        """Get or create a record in the database."""
        try:
            query = self.query(model).filter_by(**kwargs)
            instance = query.first()
            if instance:
                return instance, False
            else:
                self.session.begin(nested=True)
                try:
                    params = dict((key, value) for key, value
                                  in kwargs.iteritems()
                                  if not isinstance(value, ClauseElement))
                    instance = model(**params)
                    self.session.add(instance)
                    self.session.commit()
                    return instance, True
                except IntegrityError as error:
                    self.session.rollback()
                    instance = query.one()
                    return instance, False
        except Exception as exception:
            raise exception

    def save(self):
        """Manually persist changes made to various elements. Chainable.

        .. versionchanged:: 2.1.2
            Flush session before commit.

        Returns:
            Store: ``self`` for chainability
        """
        try:
            # commit/persist dirty changes to the database
            self.session.flush()
            self.session.commit()
        except Exception as error:
            logger.debug('rolling back failed transaction')
            self.session.rollback()
            raise error
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
            return self.query(*params).all()
        elif isinstance(query, list):
            # return all `klass_id` elements in the database
            return self.query(*params).filter(klass.id.in_(query)).all()
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
        if isinstance(elements, self.base):
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
            error_msg = 'Submit attributes as arguments or keyword arguments'
            raise TypeError(error_msg)
