# -*- coding: utf-8 -*-
from __future__ import division
import logging
import os

from sqlservice import Database

log = logging.getLogger(__name__)
DEMO_DB = "sqlite://"


class ChanjoDB(Database):

    def __init__(
        self,
        uri: str,
        model_class = None,
    ):
        if uri and'mysql' in uri:
            pool_recycle = 3600
        elif uri:
            uri = f"sqlite:///{}"

        super(ChanjoDB, self).__init__(uri=uri)


    def set_up(self):
        """Initialize a new database with the default tables and columns.

        Returns:
            Store: self
        """
        # create the tables
        self.create_all()
        tables = self.metadata.tables.keys()
        log.info("created tables: %s", ', '.join(tables))
        return self




