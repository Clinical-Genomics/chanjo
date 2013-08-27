..  _installation:

Installation
================
This section will instruct you on how to install Chanjo and get set up properly. Please read through carefulle as Chanjo depends on some C libraries that can be tricky to get working just right.

Chanjo is developed on Mac OSX and is targeted to run on UNIX platforms including Linux running Python 2.7.x.

Non-python dependencies
------------------------
These should be installed before attempting to install Chanjo.

**C-compiler**. First of all you need to have a C-compiler installed on your system. On OSX you can download the `Apple Developer Command Line Tools <https://developer.apple.com/downloads/index.action>`_. That option requires you to sign up for a free Apple developer account but is the most pain free solution.

`SAMtools <http://samtools.sourceforge.net/>`_ provides various utilities for manipulating alignments in the SAM format, including sorting, merging, indexing and generating alignments in a per-position format. Note that version 0.1.19 or above is required. `SAMtools` is used by the default :class:`CoverageAdapter` to interface with BAM alignment files.

::

  $ cd samtools-0.1.19/
  $ make

Don't forget to copy at least `samtools` from `misc` to a location in your ``$PATH``.

`SQLite <http://www.sqlite.org/>`_ is an embedded SQL database that ships with most operating systems. You probably don't have to worry about installing it yourself. However, if you are already setting up a new Python installation it doesn't hurt to include the newest version. In Chanjo, it is used by the default :class:`ElementAdapter`.

::

  $ brew install sqlite
  $ brew install python --framework

Installing Chanjo
------------------
Finally! Simply run::

    $ pip install chanjo

Required Python dependencies will be installed along side the main package.

Get the code
-------------
1. Download the code from the GitHub `repo <https://github.com/robinandeer/chanjo2/releases>`_::

    $ git clone https://github.com/robinandeer/chanjo2.git
    $ cd chanjo2

2. Preferably in a `virtualenv`, run::

    $ python setup.py install
