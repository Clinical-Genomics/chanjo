Command Line Interface
=======================

::

    Chanjo CLI
    Central CLI for various Chanjo functionality.
    * "annotate": Process all or a subset of genes, get coverage from a BAM-file and commit changes to a SQLite database.
    * "read": Quick access getting coverage metrics from an interval in a BAM-file.
    * "peak": Peak into a SQLite database to look at coverage for a given gene.
    * "build": Builds a new skeleton SQLite database.
    * "import": Import temporary JSON file(s) after running Chanjo in parallell with the "annotate --json" flag.

    Usage:
      chanjo annotate <store> using <source> [<gene>... | --read=<file>] [--ccds=<file>] [--cutoff=<int>] [--sample=<str>] [--group=<int>] [--json=<file>] [--verbose] [-p | --print] [--force]
      chanjo read <chrom> <start> <end> using <source> [--cutoff=<int>] [--verbose]
      chanjo peak <store> <gene>... [--verbose] [--sample=<str>] [--group=<int>]
      chanjo build <store> using <ccds_path> [--force]
      chanjo <store> import <txt_path>...
      chanjo -h | --help
      chanjo --version

    Arguments:
      <store>     Path to new or existing SQLite database.
      <source>    Path to the BAM alignment file.
      <ccds_path> Path to CCDS database dump (text-file).
      <gene>      List of HGNC symbols for genes to annotate or peak at.
      <txt_path>  List of generated text-files to be imported into a datastore. See <store> for further info.
      <chrom>     Chromosome ID.
      <start>     Starting interval position (1-based).
      <end>       Ending interval position (1-based).

    Options:
      -h --help          Show this screen.
      --version          Show version.
      -r --read=<file>   Path to txt-file with one HGNC symbol per line.
      --ccds=<file>      Path to CCDS database dump. Also functions as a flag to signal building a new SQLite database.
      -c --cutoff=<int>  Cutoff to use for calculating completeness [default: 10].
      -s --sample=<str>  The sample ID to annotate with or peak at [default: 0-0-0U].
      -g --group=<int>   The sample ID to annotate with or peak at [default: 0].
      -j --json=<file>   Chanjo will write a temporary JSON-file that can be imported later. This is useful when parallelizing Chanjo.
      -f --force         Overwrite existing files without warning.
      -v --verbose       Show more extensive information about transcripts & exons.
      -p --print         Just print the variables to the console (debug).