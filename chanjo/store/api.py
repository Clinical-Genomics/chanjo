# -*- coding: utf-8 -*-
from __future__ import division
import logging
import os

from alchy import Manager
from chanjo.calculate import CalculateMixin
from .models import BASE
from .fetch import FetchMixin
from .delete import DeleteMixin

log = logging.getLogger(__name__)


class ChanjoDB(Manager, CalculateMixin, DeleteMixin, FetchMixin):
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
        self.Model = base
        self.uri = uri
        if uri:
            self.connect(uri, debug=debug)

    def connect(self, db_uri, debug=False):
        """Configure connection to a SQL database.

        .. versionadded:: 2.1.0

        Args:
            db_uri (str): path/URI to the database to connect to
            debug (Optional[bool]): whether to output logging information
        """
        config = {'SQLALCHEMY_ECHO': debug}
        if 'mysql' in db_uri:  # pragma: no cover
            config['SQLALCHEMY_POOL_RECYCLE'] = 3600
        elif '://' not in db_uri:
            # expect only a path to a sqlite database
            db_path = os.path.abspath(os.path.expanduser(db_uri))
            db_uri = "sqlite:///{}".format(db_path)
            self.uri = db_uri

        config['SQLALCHEMY_DATABASE_URI'] = db_uri

        # connect to the SQL database
        super(ChanjoDB, self).__init__(config=config, Model=self.Model)

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
        self.create_all()
        tables = self.Model.metadata.tables.keys()
        log.info("created tables: %s", ', '.join(tables))
        return self

    def tear_down(self):
        """Tear down a database (tables and columns).

        Returns:
            Store: self
        """
        # drop/delete the tables
        self.drop_all()
        return self

    def save(self):
        """Manually persist changes made to various elements. Chainable.

        .. versionchanged:: 2.1.2
            Flush session before commit.

        Returns:
            Store: ``self`` for chainability
        """
        try:
            # commit/persist dirty changes to the database
            self.commit()
        except Exception as error:
            log.debug('rolling back failed transaction')
            self.session.rollback()
            raise error
        return self
