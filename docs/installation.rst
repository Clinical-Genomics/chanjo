=============
Installation
=============
**tl;dr** Cross your fingers and ``$ pip install chanjo``

Bulletproof install
--------------------
Chanjo targets **Unix** and **Python 2.6-7 and 3.2+**. It depends on a few C extentions that significantly reduces runtime and simplifes the interface. To avoid all the possible hassle of installing them I definitivly recommend choosing `Miniconda`_.

Miniconda includes an alternative package manager that will install binary (precompiled) versions of Python C extentions such as Numpy, Pysam, and SQLAlchemy. It makes the whole process quick *and* painless.

.. code-block:: console
	
	$ wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh | bash

Follow the on-screen instructions. There's versions for Linux, Mac OSX, and Windows. Now with Miniconda installed we setup a new conda environment.

.. code-block:: console

	$ conda create -n chanjo3 python=3.3
	$ source activate chanjo3
	$ conda install numpy sqlalchemy cython

And now we simply install Chanjo into the new environment.

.. code-block:: console

	$ pip install chanjo

.. note::
	If you are a Python purist and prefer the tried and true pip+virtualenv combo it will of course do the trick as well. For more detailed instructions head over to Kenneth Reitz's `Python Guide`_.

If you plan on using MySQL for your SQL database you also need an adapter. My recommendation is 'pymysql'. It's written in pure Python and works on both version 2.x and 3.x.

.. code-block:: console

	$ pip install pymysql

Getting the code
-----------------
Would you like to take part in the development or tweak the code for any other reason? In that case, you should follow these simple steps and download the code from the `GitHub repo <https://github.com/robinandeer/chanjo/releases>`_.

.. code-block:: console

	$ git clone https://github.com/robinandeer/chanjo.git
	$ cd chanjo
	$ python setup.py develop

Bonus
-------
Some extra goodies just for you.

Sphinx theme
~~~~~~~~~~~~~~
Like the custom Sphinx theme? My plan is to make it available as soon as I have the time.


.. _Miniconda: http://conda.pydata.org/miniconda.html
.. _Python Guide: http://docs.python-guide.org/en/latest/
