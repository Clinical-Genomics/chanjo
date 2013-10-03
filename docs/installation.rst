..  _installation:

Installation
================
This section will sequentially instruct you on how to install Chanjo.

FYI: Chanjo is developed on Mac OSX and is targeted to run on UNIX platforms, including Linux, running Python 2.7.x.

Non-python dependencies
------------------------
C-compiler
~~~~~~~~~~~
You need to have a C-compiler installed on your system.

On OSX, the easiet way is to install `Apple Developer Command Line Tools <https://developer.apple.com/downloads/index.action>`_. If you don't want to sign up for a free developer account you could try `this installer <https://github.com/kennethreitz/osx-gcc-installer>`_.

SAMtools
~~~~~~~~~~
`SAMtools <http://samtools.sourceforge.net/>`_ provides various utilities for manipulating alignments in the SAM/BAM format, including sorting, merging, indexing and generating alignments in a per-position format. **Version 0.1.19** or above is required.

To install you need to download the latest release from `this page <http://sourceforge.net/projects/samtools/files/>`_.

.. code-block:: console

  $ cd samtools-0.1.19/
  $ make

Don't forget to add/copy the `samtools` binary from the `misc` folder to a location in your ``$PATH``.

SQLite
~~~~~~~
`SQLite <http://www.sqlite.org/>`_ is an embedded SQL database that ships with most operating systems. You probably don't have to worry about installing it yourself.

Installing Chanjo
------------------
Preferably in a virtualenv_, simply run:

.. code-block:: console

    $ pip install chanjo

Required Python dependencies will be installed alongside the main package. The ``chanjo`` command line tool will (probably) be automatically added to your ``$PATH``.

.. note::

  I recommend installing `Chanjo` in a virtual environment. Don't know what they are? The excellent `Python Guide <http://docs.python-guide.org/en/latest/>`_ has `more information <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_ on the topic.

Get the code
-------------
1. Download the code from the GitHub `repo <https://github.com/robinandeer/chanjo/releases>`_.

.. code-block:: console

    $ git clone https://github.com/robinandeer/chanjo.git
    $ cd chanjo

2. Preferably in a virtualenv_, run:

.. code-block:: console

  $ python setup.py install

.. _virtualenv: http://www.virtualenv.org/en/latest/