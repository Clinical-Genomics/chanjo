#!/usr/bin/env python
# coding: utf-8

import autumn
from autumn.util import AutoConn
from autumn.model import Model
from autumn.db.relations import ForeignKey, OneToMany
from interval import Interval, IntervalSet
from utils import Interval as Ival
import collections
import os


class ElementAdapter(object):
  """
  Chanjo adapter for interfacing with a SQLite database with element data from
  the CCDS database.
  ----------

  :param dbPath: [str]  Path to the SQLite database. This is required at setup.
  :param new:    [bool] Set up new or overwrite/reset current database.

  Usage:
    from chanjo.sqlite import ElementAdapter
    path = "/path/to/sqlite.db"
    adapter = ElementAdapter(path)
  """
  def __init__(self, db_path, new=False):
    super(ElementAdapter, self).__init__()

    self.classes = None

    if not os.path.isfile(db_path) or new:
      # Prepare new database
      self.connect(db_path, new=True)
    else:
      # Set up connection to database
      self.connect(db_path)

  def connect(self, path, new=False):
    """
    Private: Opens a connection to an existing or new SQLite database file.
    ----------

    :param path: [str] The path to the SQLite database file
    :param new:  [bool] You are opening a connection to a novel database?
                 (Default: False)
    """
    # get a database connection object
    # Doesn't have to exist in the first place!
    self.db = AutoConn(path)

    # Unless setting up a new database
    if not new:
      self._defaultORM()

  def get(self, elemClass, elemIDs):
    """
    Public: Get one or multiple elements by ID.

    :param elemClass: [str]         Choices: "gene", "transcript" or "exon"
    :param elemIDs:   [str/list]    An element ID or list of IDs
    :returns:         [object/list] One element or list of elements

    Usage:
      gene = adapter.get("gene", "EGFR")
      genes = adapter.get("gene", ["TTN", "GIT1", "EGFR"])

      # Change an attribute
      gene.coverage = 10.0

      # Persist changes
      gene.save()
    """
    singleElement = False
    # Test if just a single ID was submitted
    if isinstance(elemIDs, str):
      elemIDs = (elemIDs, )
      singleElement = True
    else:
      # Otherwise make sure we have an iterable
      if not isinstance(elemIDs, collections.Iterable):
        print("Input must be ID string or list of IDs.")
        return None

    elements = range(0,len(elemIDs))
    for count, elem_id in enumerate(elemIDs):

      elements[count] = self.getClass(elemClass).get(elem_id)

    # Return a single element if that was requested
    if singleElement:
      return elements[0]
    else:
      # If a list of element ID was submitted, return a list of elements
      return elements

  def set(self, elemClass, elemTuple):
    """
    Public: Create and persist and new element to the database.

    :param elemClass: [str]   Choices: "gene", "transcript" or "exon"
    :param elemTuple: [tuple] Tuple of attributes in order!
    """
    self.getClass(elemClass)(*elemTuple).save()

  def getClass(self, elemClass):
    """
    Public: Get direct access to an element class.

    :param elemClass: [str]    Choices: "gene", "transcript" or "exon"
    :returns:         [object] The raw element class ORM object
    """
    return self.classes[elemClass]

  def setup(self, gs_cols="", tx_cols="", ex_cols=""):
    # code to create the database tsable
    # This is where custom annotations whould be added!
    if len(gs_cols) == 0:
      comma = ""
    else:
      comma = ","

    _genes_sql = """
    DROP TABLE IF EXISTS Gene;
    CREATE TABLE Gene (
      id TEXT PRIMARY KEY,
      chrom TEXT,
      strand TEXT,
      start INT{comma}{columns}
    );""".format(comma=comma, columns=gs_cols)

    if len(tx_cols) == 0:
      comma = ""
    else:
      comma = ","

    _transcripts_sql = """
    DROP TABLE IF EXISTS Transcript;
    CREATE TABLE Transcript (
      id TEXT PRIMARY KEY,
      chrom TEXT,
      strand TEXT,
      gene_id TEXT,
      FOREIGN KEY (gene_id) REFERENCES Gene(id){comma}{columns}
    );""".format(comma=comma, columns=tx_cols)
    
    if len(ex_cols) == 0:
      comma = ""
    else:
      comma = ","

    _exons_sql = """
    DROP TABLE IF EXISTS Exon;
    CREATE TABLE Exon (
      id TEXT PRIMARY KEY,
      chrom TEXT,
      strand TEXT,
      start INT,
      end INT,
      coverage REAL,
      completeness REAL,
      cutoff INT{comma}{columns}
    );""".format(comma=comma, columns=ex_cols)

    _genes_exons_sql = """
    DROP TABLE IF EXISTS Exon_Gene;
    CREATE TABLE Exon_Gene (
      gene_id TEXT,
      exon_id TEXT,
      PRIMARY KEY (gene_id, exon_id),
      FOREIGN KEY (gene_id) REFERENCES Gene(id),
      FOREIGN KEY (exon_id) REFERENCES Exon(id)
    );"""

    _transcripts_exons_sql = """
    DROP TABLE IF EXISTS Exon_Transcript;
    CREATE TABLE Exon_Transcript (
      transcript_id TEXT,
      exon_id TEXT,
      PRIMARY KEY (transcript_id, exon_id),
      FOREIGN KEY (transcript_id) REFERENCES Transcript(id),
      FOREIGN KEY (exon_id) REFERENCES Exon(id)
    );"""

    # create the tables, dropping any previous tables of the same name
    autumn.util.create_table(self.db, _genes_sql)
    autumn.util.create_table(self.db, _transcripts_sql)
    autumn.util.create_table(self.db, _exons_sql)
    autumn.util.create_table(self.db, _genes_exons_sql)
    autumn.util.create_table(self.db, _transcripts_exons_sql)

    self._defaultORM()

  def _defaultORM(self):
    # create ORM class; Autumn introspects the database to find out columns
    class Gene(Model):
      db = self.db
      transcripts = OneToMany("Transcript", field="gene_id")
      _intervals = None
      _exons = None

      class Meta:
        table = "Gene"

      @property
      def exons(self):
        if not self._exons:
          self._exons = [combo.exon for combo in Exon_Gene.get(gene_id=self.id)]

        return self._exons

      @property
      def exonLength(self):
        """
        Returns the combined length of all related exons.
        N.B. Modifying the __len__ breaks something...
        """
        return sum([interval.upper_bound - interval.lower_bound
                    for interval in self.intervals])

      @property
      def intervalSet(self):
        """
        Returns all the non-overlapping exonic intervals.
        """
        if not self._intervals:
          self._intervals = IntervalSet([Interval(exon.start, exon.end)
                                        for exon in self.exons])

        return self._intervals

      @property
      def intervals(self):
        return [Ival(i.lower_bound, i.upper_bound)
                for i in self.intervalSet]

      def simpleSpliceIntervals(self):
        return [Ival(i.lower_bound-2, i.upper_bound+2)
                for i in self.intervals]


    class Transcript(Model):
      db = self.db
      gene = ForeignKey(Gene, field="gene_id")
      _exons = None

      class Meta:
        table = "Transcript"

      @property
      def exons(self):
        if not self._exons:
          self._exons = [combo.exon for combo in
                         Exon_Transcript.get(transcript_id=self.id)]

        return self._exons

      @property
      def exonLength(self):
        """
        Returns the combined length of all related exons.
        """
        return sum([len(exon) for exon in self.exons])

      @property
      def intervals(self):
        """
        Exons aleady have start and end attributes.
        """
        return self.exons

      def coverage(self):
        """
        Public: calculates coverage based on exon annotations.
        """
        # Initialize
        readCount = 0
        baseCount = 0

        # Go through each exon (never overlaps!)
        for exon in self.exons:

          # Add the number of bases
          baseCount += len(exon)

          # Add the number of reads
          readCount += len(exon) * exon.coverage

        return readCount / float(baseCount)

      def completeness(self):
        """
        Public: calculates completeness based on exon annotations.
        """
        # Initialize
        passedCount = 0

        # Go through each exon (never overlaps!)
        for exon in self.exons:

          # Add the number of bases
          passedCount += len(exon) * exon.completeness

        # Should be int...
        return passedCount
      

    class Exon(Model):
      db = self.db
      gene = ForeignKey(Gene)
      _transcripts = None
      _genes = None

      class Meta:
        table = "Exon"

      def __len__(self):
        return self.end - self.start

      @property
      def spiceStart(self):
        return self.start - 2

      @property
      def spiceEnd(self):
        return self.end + 2

      @property
      def transcripts(self):
        if not self._transcripts:
          self._transcripts = [combo.transcript for combo in
                               Exon_Transcript.get(exon_id=self.id)]

        return self._transcripts

      @property
      def genes(self):
        if not self._genes:
          self._genes = [combo.gene for combo in Exon_Gene.get(exon_id=self.id)]

        return self._genes

    class Exon_Gene(Model):
      db = self.db
      gene = ForeignKey(Gene, field="gene_id")
      exon = ForeignKey(Exon, field="exon_id")

      class Meta:
        table = "Exon_Gene"

    class Exon_Transcript(Model):
      db = self.db
      transcript = ForeignKey(Transcript, field="transcript_id")
      exon = ForeignKey(Exon, field="exon_id")

      class Meta:
        table = "Exon_Transcript"

    # Shortcuts
    self.classes = {
      "gene": Gene,
      "transcript": Transcript,
      "exon": Exon,
      "exon_gene": Exon_Gene,
      "exon_transcript": Exon_Transcript
    }  
