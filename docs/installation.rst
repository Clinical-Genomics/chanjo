Installation
================
Chanjo is targeted to run on UNIX platforms including Linux and developed on MAC OSX. Chanjo works with Python 2.7.x.

Instructions
^^^^^^^^^^^^^
- pip

Get the code
^^^^^^^^^^^^^
1. Download a release from the GitHub `repo <https://github.com/robinandeer/chanjo2/releases>`_::

    git clone https://github.com/robinandeer/chanjo2.git
    cd chanjo2

2. Preferably in a `virtualenv`, run::

    $ python setup.py install

*N.B. pip installation support is in the works.*

Dependencies
------------------
Non-python dependencies
^^^^^^^^^^^^^^^^^^^^^^^^
C-compiler
***********
First of all you need to have a C-compiler installed on your system. On OSX you can download the `Apple Developer Command Line Tools <https://developer.apple.com/downloads/index.action>`_. That option requires you to sign up for a free Apple developer account but is the most pain free solution.

SAMtools (coverage adapter)
****************************
`SAMtools <http://samtools.sourceforge.net/>`_ provide various utilities for manipulating alignments in the SAM format, including sorting, merging, indexing and generating alignments in a per-position format. Note that version 0.1.19 or above is required. `SAMtools` is used by the default `Coverage Adapter` to interface with BAM alignment files.

SQLite (element adapter)
*************************
`SQLite <http://www.sqlite.org/>`_. is an embedded SQL database that ships with most operating systems. You probably don't have to worry about installing it yourself. However, if you are already setting up a new Python installation it doesn't hurt to include the newest version. In Chanjo, it is used by the default `Element Adapter`.

Python dependencies
^^^^^^^^^^^^^^^^^^^^^
All python dependencies should be automatically installed when you follow the instructions below.
