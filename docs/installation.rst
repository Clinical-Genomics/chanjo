=============
Installation
=============
**tl;dr** ``$ pip install chanjo``


Bulletproof install
--------------------
Chanjo targets **Unix** and **Python 2.7+/3.2+**. It depends on a few C extentions that significantly reduces runtime and simplifes the interface. To avoid hassle when installing them I definitivly recommend `Miniconda`_.

Miniconda is a slim distribution of Python that can be installed without root access. There's versions for Linux, Mac OSX, and Windows. It also includes an alternative package manager (conda) that will install binary (precompiled) versions of Python C extentions such as Numpy, Pysam, and SQLAlchemy. It makes the whole installation process quick *and* painless.

To install Miniconda, run:

.. code-block:: console

  $ wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
  $ bash Miniconda-latest-Linux-x86_64.sh -b
  $ export PATH="$HOME/miniconda/bin:$PATH"  # remember to add this to your path!

Now with Miniconda installed we setup a new conda environment.

.. code-block:: console

  $ conda create -n chanjo2 python=2 cython numpy sqlalchemy pip
  $ source activate chanjo2
  $ conda install -c https://conda.binstar.org/robinandeer pysam

And now we simply install Chanjo into the new environment without having to worry about tricky C dependencies.

.. code-block:: console

	$ pip install chanjo

.. note::
	If you are a Python purist and prefer the tried and true pip+virtualenv combo it will of course do the trick as well. For more detailed instructions head over to Kenneth Reitz's `Python Guide`_.

If you plan on using MySQL for your SQL database you also need a SQL adapter. My recommendation is 'pymysql'. It's written in pure Python and works on both version 2.x and 3.x.

.. code-block:: console

	$ pip install pymysql


Getting the code
-----------------
Would you like to take part in the development or tweak the code for any other reason? In that case, you should follow these simple steps and download the code from the `GitHub repo <https://github.com/robinandeer/chanjo/releases>`_.

.. code-block:: console

	$ git clone https://github.com/robinandeer/chanjo.git
	$ cd chanjo
	$ pip install --editable .


.. _Miniconda: http://conda.pydata.org/miniconda.html
.. _Python Guide: http://docs.python-guide.org/en/latest/
