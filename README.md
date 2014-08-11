<p align="center">
  <a href="http://chanjo.co">
    <img height="235"
         width="244"
         src="https://raw.githubusercontent.com/robinandeer/chanjo/master/artwork/logo.png"/>
  </a>
</p>

# Chanjo [![PyPI version][fury-image]][fury-url] [![Build Status][travis-image]][travis-url] [![Coverage Status][coveralls-image]][coveralls-url]

# Chanjo
Chanjo is coverage analysis for clinical sequencing. It's implemented in Python with a command line interface that adheres to [UNIX philisophy][unix].

## Installation
Chanjo is distruibuted through "pip". Install the latest release by running:

```bash
$ pip install chanjo
```

... or locally for development:

```bash
$ pip install --editable .
```

Complete instructions are available in the [documentation][docs] but installation (*can be*) as simple as running:

## Usage
Chanjo exposes a composable command line interface. You can always save intermediary files at any stage and customize every option. However, using a ``chanjo.toml`` config and UNIX pipes you can end up with something like:

```bash
$ chanjo convert CCDS.sorted.txt | chanjo annotate alignment.bam > coverage.bed
```

## Documentation
Read the Docs is hosting the [official documentation][docs].

I can specifically recommend the fully [interactive demo](http://www.chanjo.co/en/latest/introduction.html#demo), complete with sample data to get you started right away.

## Features

### What Chanjo does do
Chanjo works on BAM-alignment files and extracts interesting coverage related statistics. You use a BED-file to define which regions of the genome that you particularly care about. The output takes the shape of an extended BED-file.

An optional final step is to load data into a SQL database. This will aggregate data from exons to transcripts and genes. The database will later work as an API to downstream tools like the Chanjo Report generator.

### What Chanjo doesn't do
Chanjo is not the right choice if you care about coverage for every base across the genome. Detailed histograms is something that [BEDTools][bedtools] already handles with confidence.

## Contributors
Robin Andeer

Luca Beltrame ([lbeltrame](https://github.com/lbeltrame))

## License
MIT. See the [LICENSE](LICENSE) file for more details.

## Contributing
Anyone can help make this project better - read [CONTRIBUTION][CONTRIBUTION.md] to get started!


[unix]: http://en.wikipedia.org/wiki/Unix_philosophy
[docs]: http://www.chanjo.co/en/latest/
[bedtools]: http://bedtools.readthedocs.org/en/latest/

[coveralls-url]: https://coveralls.io/r/robinandeer/chanjo
[coveralls-image]: https://img.shields.io/coveralls/robinandeer/chanjo.svg

[fury-url]: http://badge.fury.io/py/chanjo
[fury-image]: https://badge.fury.io/py/chanjo.png

[travis-url]: https://travis-ci.org/robinandeer/chanjo
[travis-image]: https://travis-ci.org/robinandeer/chanjo.png?branch=master
