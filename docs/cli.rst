Command Line Interface
=======================

::

    Chanjo.
    Process all or a subset of exons, get coverage from a BAM alignment and
    commit changes to a SQLite database.

    Usage:
      chanjo.py <sql_path> <bam_path> [--ccds=<ccds_path>] [--cutoff=<int>] [--read=<path> | --pipe] [-p | --print]
      chanjo.py -h | --help
      chanjo.py --version

    Arguments:
      <sql_path>  path to the SQLite database file
      <bam_path>  path to the BAM alignment file

    Options:
      -h --help       Show this screen.
      --version       Show version.
      --ccds=<path>   Path to CCDS txt file, initiates creation of new database. 
      --cutoff=<int>  Lowest read depth to pass [default: 50].
      --read=<path>   Path to file with HGNC symbols.
      --pipe          Read piped list of HGNC symbols.
      -p --print      Just print the input variables to the console