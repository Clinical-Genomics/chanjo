=============
Installation
=============

Guide
---------
Chanjo targets **Unix** and **Python 2.7+/3.2+**. Since chanjo relies on Sambamba for BAM processing, it's now very simple to install. I do still recommend `Miniconda`_, it's a slim distribution of Python with a very nice package manager.

.. code-block:: console

    $ pip install chanjo


Vagrant dev/testing environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You can also set up a local development environment in a virtual machine through Vagrant_. This will handle the install for you automatically through Ansible provisioning! After downloading/cloning the repo:

.. code-block:: console

    $ vagrant up
    $ vagrant ssh


Sambamba
----------
You will also need a copy of Sambamba which you can simply grab from their `GitHub repo`_ where they serve up static binaries - just drop the latest in your path and you are good to go!

.. code-block:: console

    $ wget -P /tmp/ https://github.com/lomereiter/sambamba/releases/download/v0.5.8/sambamba_v0.5.8_linux.tar.bz2
    $ tar xjfv /tmp/sambamba_v0.5.8_linux.tar.bz2 -C /tmp/
    $ mv /tmp/sambamba_v0.5.8 ~/bin/sambamba
    $ chmod +x ~/bin/sambamba


Optional dependecies
---------------------
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


.. _GitHub repo: https://github.com/lomereiter/sambamba/releases
.. _Miniconda: http://conda.pydata.org/miniconda.html
.. _Vagrant: https://www.vagrantup.com/
