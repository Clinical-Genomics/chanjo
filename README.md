<p align="center">
  <a href="http://chanjo.co">
    <img height="235" width="244" src="docs/assets/logo.png"/>
  </a>
</p>

# Chanjo [![PyPI version][fury-image]][fury-url] [![Build Status][travis-image]][travis-url] [![Coverage Status][coveralls-image]][coveralls-url] [![bioconda-badge][bioconda-img]][bioconda-url]

Chanjo is coverage analysis for clinical sequencing. It's implemented in Python
with a command line interface that adheres to [UNIX pipeline philosophy][unix].

## Installation
Chanjo is distributed through `pip`. Install the latest stable release by
running:

```bash
pip install chanjo
```

... or locally for development:

```bash
git clone https://github.com/Clinical-Genomics/chanjo.git
cd chanjo
conda install --channel bioconda sambamba
pip install -r requirements-dev.txt --editable .
```

## Usage
Chanjo exposes a decomposable command line interface with a nifty config file
implementation.

```bash
chanjo init --setup
chanjo load /path/to/sambamba.output.bed
chanjo calculate mean
{"metrics": {"completeness_10": 90.92, "mean_coverage": 193.85}, "sample_id": "sample1"}
```

## Documentation
Read the Docs is hosting the [official documentation][docs].

If you are looking to learn more about handling sequence coverage data in
clinical sequencing, feel free to download and skim through my own
[Master's thesis][thesis] and article references.

## Features

### What Chanjo does
Chanjo leverages [Sambamba][sambamba] to annotate coverage and completeness
for a general BED-file. The output can then easily to loaded into a SQL
database that enables investigation of coverage across regions and samples.
The database also works as an API to downstream tools like the Chanjo
Coverage Report generator.

### What Chanjo doesn't
Chanjo is not the right choice if you care about coverage for every base across
the entire genome. Detailed histograms is something [BEDTools][bedtools]
already handles with confidence.

## Contributors
-   Robin Andeer ([robinandeer](https://github.com/robinandeer))
-   Luca Beltrame ([lbeltrame](https://github.com/lbeltrame))
-   John Kern ([kern3020](https://github.com/kern3020))
-   Måns Magnusson ([moonso](https://github.com/moonso))
-   Patrik Grenfeldt ([patrikgrenfeldt](https://github.com/patrikgrenfeldt))

## License
MIT. See the [LICENSE](LICENSE) file for more details.

## Contributing
Anyone can help make this project better - read [CONTRIBUTION](CONTRIBUTION.md)
to get started!


[unix]: http://en.wikipedia.org/wiki/Unix_philosophy
[docs]: http://www.chanjo.co/en/latest/
[bedtools]: http://bedtools.readthedocs.org/en/latest/
[thesis]: https://s3.amazonaws.com/tudo/chanjo/RobinAndeerMastersThesisFinal_2013.pdf
[sambamba]: http://lomereiter.github.io/sambamba/
[fury-url]: http://badge.fury.io/py/chanjo
[fury-image]: https://badge.fury.io/py/chanjo.png

[travis-url]: https://travis-ci.org/robinandeer/chanjo
[travis-image]: https://img.shields.io/travis/robinandeer/chanjo.svg?style=flat-square

[coveralls-url]: https://coveralls.io/r/robinandeer/chanjo
[coveralls-image]: https://img.shields.io/coveralls/robinandeer/chanjo.svg?style=flat-square

[bioconda-url]: http://bioconda.github.io
[bioconda-img]: https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat-square
