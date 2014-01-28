..  _installation:

Installation
================
This section will instruct you, step-by-step, on how to install *Chanjo*.

.. note::

  *Chanjo* is developed on Mac OSX and is targeted to run on UNIX platforms, including Linux, running Python 2.7.x.


Installing Chanjo
------------------
Preferably in a virtualenv_, simply run:

.. code-block:: console

    $ pip install chanjo

Required Python dependencies will be installed alongside the main package. The ``chanjo`` commandline tool will automatically show up in your ``$PATH``.

.. note::

  I recommend installing `Chanjo` in a virtual environment. Don't know what that is? The excellent `Python Guide`_ has `more information`_ on the topic.

.. note::
  
  The exception to the "don't worry about Python dependencies"-rule is *database interfaces*. For example if you intend to use MySQL as data storage you should at some point install a driver by running: ``pip install MySQL-python``.


Setting up a new Python environment
------------------------------------
If you are experiencing difficult–to-fix problems (beyond installing *Chanjo*) it might be time to start fresh with a brand new copy of Python.

My recommendation for easily setting up a new Python environment is to download a pre-compiled version of ActivePython_. This will work even if you lack root access to the computer you're working on.

After downloading the appropriate version (Mac/Linux):

.. code-block:: console

  $ tar -xzf ActivePython-{{version}}.tar.gz
  $ cd ActivePython-{{version}}
  $ ./install.sh -I $HOME/opt/ActivePython-2.7
  $ export PATH=$HOME/opt/ActivePython-2.7/bin:$PATH

Of course, you really would need to add the last command somewhere in your ``.bash_profile`` or similar startup script to default to the ActivePython installation in the future.

Another nice thing about ActivePython is that virtualenv_ and ``pip`` comes preinstalled.


Non-Python dependencies
------------------------
C-compiler
~~~~~~~~~~~
You need a C-compiler installed on your system.

On OSX, the easiet way is to install Apple's `Developer command line tools`_. If you don't want to sign up for a free developer account you could try Kenneth Reitz's `GCC Installer for OSX`_.

My experience with Linux is that a proper C-compiler most often is already installed and ready to go.

SAMtools
~~~~~~~~~~
SAMtools_ provides various utilities for manipulating alignments in the SAM/BAM format, including sorting, merging, indexing and generating alignments in a per-position format. **>=v0.1.19** is required.

Technically *SAMtools* should be automatically installed alongside *Chanjo*. If you wish to assert more controll over the process, however, or are experience problems, this is how you would install it manually. It's actually not that difficult.

To install *SAMtools* you need to download the latest release from SAMtools' `downloads page`_.

.. code-block:: console

  $ cd samtools-0.1.19/
  $ make

Don't forget to add/copy the `samtools` binary from the `misc` folder to a location in your ``$PATH``.

SQLite or MySQL
~~~~~~~~~~~~~~~~~
`SQLite <http://www.sqlite.org/>`_ is an embedded SQL database that ships with most operating systems. You probably don't have to worry about installing it yourself. If you've gotten Python to work, chances are you're fine.

`MySQL <http://www.mysql.com/>`_ is a more heavy duty SQL database option that happens to be the most popular open source database in the world. Finding a tutorial that adresses your setup for installing it should be relatively easy since the community of users is vast. Here are the official `instructions <http://dev.mysql.com/doc/refman/5.1/en/linux-installation.html>`_.


Getting the code
------------------
If you want to take part in the development or tweak the code for any other reason you would follow these two simple steps.

1. Download the code from the `GitHub repo`_.

.. code-block:: console

    $ git clone https://github.com/robinandeer/chanjo.git
    $ cd chanjo

2. Preferably in a virtualenv_, run:

.. code-block:: console

  $ python setup.py install

.. _virtualenv: http://www.virtualenv.org/en/latest/
.. _Developer command line tools: https://developer.apple.com/downloads/index.action
.. _GCC Installer for OSX: https://github.com/kennethreitz/osx-gcc-installer
.. _Samtools: http://samtools.sourceforge.net/
.. _downloads page: http://sourceforge.net/projects/samtools/files/
.. _Python Guide: http://docs.python-guide.org/en/latest/
.. _more information: http://docs.python-guide.org/en/latest/dev/virtualenvs/
.. _GitHub repo: https://github.com/robinandeer/chanjo/releases
.. _ActivePython: http://www.activestate.com/activepython/downloads
