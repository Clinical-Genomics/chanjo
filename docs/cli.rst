Command Line Interface
=======================

.. code-block:: console

  $ chanjo -h

  Chanjo CLI

  Usage:
    chanjo annotate <store> using <source> [<gene>... | --read=<file>] [--ccds=<file>] [--cutoff=<int>] [--sample=<str>] [--group=<int>] [--json=<file>] [--verbose] [-p | --print] [--force]
    chanjo read <chrom> <start> <end> using <source> [--cutoff=<int>] [--verbose]
    chanjo peak <store> <gene>... [--verbose] [--sample=<str>] [--group=<int>]
    chanjo build <store> using <ccds_path> [--force]
    chanjo <store> import <json_path>...
    chanjo -h | --help
    chanjo --version

  Commands:
    annotate            Annotate genes in a SQLite database
    read                Coverage for an interval in a BAM-file
    peak                Peak at coverage metrics for an *annotated* gene
    build               Builds a new skeleton SQLite database
    import              Import annotations after using "--json" option

  Arguments:
    <store>             Path to new or existing SQLite database
    <source>            Path to the BAM alignment file (.bam)
    <ccds_path>         Path to CCDS database dump (.txt)
    <gene>              List of HGNC symbols
    <json_path>         List of JSON-files to import
    <chrom>             Chromosome ID
    <start>             Starting interval position (1-based)
    <end>               Ending interval position (1-based)

  Options:
    -h --help           Show this screen
    --version           Show version
    -r --read=<file>    Text file with one HGNC symbol per line
    --ccds=<file>       Path to CCDS database dump (build new database)
    -c --cutoff=<int>   Cutoff for completeness [default: 10]
    -s --sample=<str>   Sample ID [default: 0-0-0U]
    -g --group=<int>    Group/Family ID [default: 0]
    -j --json=<file>    Write temp JSON-file for later import (parallel)
    -f --force          Force overwrite of existing files
    -v --verbose        Show more print info
    -p --print          *Only* print CLI parameters (debug)
