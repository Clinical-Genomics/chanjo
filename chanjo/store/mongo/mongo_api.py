# -*- coding: utf-8 -*-
from __future__ import division
import logging
import os

from datetime import datetime

from .calculate import CalculateMixin
from chanjo.store.models import (Transcript, TranscriptStat, Sample, Exon)
from sqlalchemy.exc import IntegrityError
from pymongo.errors import (BulkWriteError, DuplicateKeyError)

from mongo_adapter import (MongoAdapter, get_client)

LOG = logging.getLogger(__name__)

class Session(object):
    """Mock a SQLAlchemy session"""
    def __init__(self, db):
        self.transcript_objs = []
        self.transcript_stats_objs = []
        self.sample_objs = []
        self.db = db
    
    def add_transcript(self, tx_obj):
        """Add a transcript object to the session"""
        self.transcript_objs.append(tx_obj)

    def add_sample(self, sample_obj):
        """Add a transcript object to the session"""
        self.sample_objs.append(sample_obj)

    def add_transcript_stat(self, tx_stat_obj):
        """Add a transcript statistics object to the session"""
        self.transcript_stats_objs.append(tx_stat_obj)
    
    def delete(self, obj):
        """Delete an object from the database
        
        If object is a sample: delete sample and all tx_stats
        
        Args:
            obj(dict)
        
        """
        if isinstance(obj, Sample):
            self.db.sample.delete_one({'_id': obj.id})
            self.db.transcript_stat.delete_many({'sample_id': obj.id})
    
    
    def rollback(self):
        """Remove all objects from database"""
        for obj in self.transcript_objs:
            self.db.transcript.delete_one({'_id': obj['_id']})

        for obj in self.transcript_stats_objs:
            self.db.transcript_stat.delete_one(
                {
                    'sample_id': obj['sample_id'],
                    'transcript_id': obj['transcript_id'],
                }
            )

        for obj in self.sample_objs:
            self.db.sample.delete_one({'_id': obj['_id']})
        
        self.clean
        
    def clean(self):
        """Clean all information"""
        self.transcript_objs = []
        self.sample_objs = []
        self.transcript_stats_objs = []
        
        return
        

class ChanjoMongoDB(MongoAdapter, CalculateMixin):
    """MongoAdapter based database object.

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

    def __init__(self, uri=None, debug=False, base=None):
        self.Model = base
        self.uri = uri
        self.client = None
        self.db = None
        self.session = None
        #These are objects to used to mock a session
        self.transcripts_bulk = []
        self.sample_bulk = []
        self.tx_stats_bulk = []
        
        self.tx_dict = None
        if uri:
            self.connect(uri, debug=debug)

    def setup(self, db_name='chanjo'):
        """Overrides the basic setup method"""
        if self.client == None:
            raise SyntaxError("No client available")
        
        if self.db is None:
            self.db = self.client[db_name]

        print(self.db)
        print(type(self.db))
        self.db_name = db_name
        self.session = Session(self.db)
        
        self.transcripts_collection = self.db.transcript
        self.sample_collection = self.db.sample
        self.transcript_stat_collection = self.db.transcript_stat
        
        
    def connect(self, db_uri, debug=False):
        """Configure connection to a SQL database.

        .. versionadded:: 2.1.0

        Args:
            db_uri (str): path/URI to the database to connect to
            debug (Optional[bool]): whether to output logging information
        """
        # connect to the mongo database
        if db_uri == "mongodb://":
            db_uri = "mongodb://localhost:27017"
            LOG.info('Set uri to %s', db_uri)
        self.uri = db_uri
        self.client = get_client(uri=db_uri)
        
        self.setup()

    @property
    def dialect(self):
        """Return database dialect name used for the current connection.

        NOT APPLICABLE FOR MONGODB

        Returns:
            dialect(str): 'mongodb'
        """
        return 'mongodb'

    def set_up(self):
        """Initialize a new database with the default tables and columns.
        
        This is not necessary in mongodb

        Returns:
            Store: self
        """
        # create the tables
        return self

    def tear_down(self):
        """Tear down a database (tables and columns).

        Returns:
            Store: self
        """
        # drop/delete the tables
        self.client.drop_database(self.db_name)
        return self
    
    def add(self, *objs):
        """Add objects to mocked session
        
        Args:
            objs(iterable): Could be different types of objects
        """
        for obj in objs:
            if isinstance(obj, Transcript):
                tx_obj = dict(
                        _id = obj.id,
                        gene_id = obj.gene_id,
                        gene_name = obj.gene_name,
                        chromosome = obj.chromosome,
                        length = obj.length,
                        )
            
                self.transcripts_bulk.append(tx_obj)
            
            elif isinstance(obj, Sample):
                sample_obj = dict(
                        _id = obj.id,
                        group_id = obj.group_id,
                        source = obj.source,
                        created_at = datetime.now(),
                        name = obj.name,
                        group_name = obj.group_name,
                        )
            
                self.sample_bulk.append(sample_obj)
                self.session.add_sample(sample_obj)
            
            elif isinstance(obj, TranscriptStat):
                if self.tx_dict is None:
                    self.tx_dict = self.transcripts_genes()
                
                tx_info = self.tx_dict[obj.transcript_id]
            
                tx_stats_obj = dict(
                        mean_coverage = obj.mean_coverage,
                        completeness_10 = obj.completeness_10,
                        completeness_15 = obj.completeness_15,
                        completeness_20 = obj.completeness_20,
                        completeness_50 = obj.completeness_50,
                        completeness_100 = obj.completeness_100,
                        threshold = obj.threshold,
                        sample_id = obj.sample_id,
                        transcript_id = obj.transcript_id,
                        gene_id = tx_info['gene_id'],
                        gene_name = tx_info['gene_name'],
                        )
                if obj._incomplete_exons is not None:
                    tx_stats_obj['_incomplete_exons'] = obj._incomplete_exons.split(',')
            
                self.tx_stats_bulk.append(tx_stats_obj)
                self.session.add_transcript_stat(tx_stats_obj)

    def clean(self):
        """Clean the bulks"""
        self.transcripts_bulk = []
        self.sample_bulk = []
        self.tx_stats_bulk = []

    def save(self):
        """Manually persist changes made to various elements. Chainable.

        .. versionchanged:: 2.1.2
            Flush session before commit.

        Returns:
            Store: ``self`` for chainability
        """
        if self.transcripts_bulk:
            self.transcripts_collection.insert_many(self.transcripts_bulk)

        if self.sample_bulk:
            for sample in self.sample_bulk:
                try:
                    self.sample_collection.insert_one(sample)
                except Exception as err:
                    # This means that the sample already exists so we do not want to remove
                    # All the previously inserted data
                    self.session.clean()
                    self.clean()
                    raise DuplicateKeyError('E11000 Duplicate key error', 11000)

        if self.tx_stats_bulk:
            self.transcript_stat_collection.insert_many(self.tx_stats_bulk)
        
        self.session.clean()
        self.clean()

        return self
    
    def sample(self, sample_id):
        """Fetch a sample from the database
        
        Args:
            sample_id(str)
        
        Returns:
            sample_obj(models.Sample)
        """
        LOG.info("Fetch sample %s", sample_id)
        sample_obj = self.sample_collection.find_one({'_id': sample_id})
        if not sample_obj:
            return None
        
        return Sample(id=sample_obj['_id'], group_id=sample_obj.get('group_id'), 
                      source=sample_obj.get('source'), created_at=sample_obj.get('created_at'))

    def samples(self):
        """Return all samples from database
        
        Args:
            sample_id(str)
        
        Returns:
            sample_objs(list(models.Sample))
        """
        LOG.info("Fetch all samples")
        sample_objs = []
        res = self.sample_collection.find()
        
        for sample in res:
            sample_objs.append(Sample(
                id=sample['_id'], 
                group_id=sample.get('group_id'), 
                source=sample.get('source'), 
                created_at=sample.get('created_at'))
            )
        
        return sample_objs


    def transcripts(self):
        """Return all transcripts
        
        Returns:
            res(pymongo.Cursor): An iterable with all transcripts in the database
        """
        return self.transcripts_collection.find({})
    
    def transcripts_genes(self):
        """Return a transcript_id as key and a dictionary with gene_id and gene_symbol
        
        Returns:
            transcripts(dict): {tx_id: {'gene_id': <int>, 'gene_name': <str>}}
        """
        transcripts = {}
        for tx in self.transcripts():
            transcripts[tx['_id']] = {
                'gene_id': tx['gene_id'],
                'gene_name': tx['gene_name'],
            }
        
        return transcripts
    
