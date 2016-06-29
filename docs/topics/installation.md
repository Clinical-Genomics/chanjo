# Installation

## Guide

Chanjo targets **Unix** and **Python 2.7+/3.2+**. It relies on Sambamba for BAM processing, making it very simple to install. [Miniconda][miniconda] is still recommended, it’s a slim distribution of Python with a very nice package manager.

With [Miniconda][miniconda] and `conda` set up you can do:

```bash
$ source activate [myEnvironment]
$ conda install -c bioconda sambamba
$ pip install chanjo
```

## Optional dependencies

If you plan on using MySQL for your SQL database you also need another SQL-adapter. My recommendation is `pymysql`. It’s written in pure Python and works on both version 2.x and 3.x.

```bash
$ pip install pymysql
```

## Getting the code

Would you like to take part in the development or tweak the code for any other reason? In that case, you should follow these simple steps and download the code from the [GitHub repo][repo].

```bash
$ git clone https://github.com/robinandeer/chanjo.git
$ cd chanjo
$ pip install --editable .
```


[miniconda]: http://conda.pydata.org/miniconda.html
[repo]: https://github.com/robinandeer/chanjo/releases
