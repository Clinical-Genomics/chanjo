<p align="center">
  <a href="http://chanjo.co">
    <img height="235"
         width="244"
         src="artwork/logo.png"/>
  </a>
</p>

# Chanjo [![PyPI version][fury-image]][fury-url] [![Build Status][travis-image]][travis-url] [![Coverage Status][coveralls-image]][coveralls-url]

Chanjo is coverage analysis for clinical sequencing. It's implemented in Python with a command line interface that adheres to [UNIX pipeline philisophy][unix].

## Installation
Chanjo is distruibuted through "pip". Install the latest release by running:

```bash
$ pip install chanjo
```

... or locally for development:

```bash
$ git clone https://github.com/robinandeer/chanjo.git && cd chanjo
$ pip install --editable .
```

Do note that Chanjo is built on some of kind-of tricky dependencies. If you are experiencing any issues, help is just a click away in the [documentation][docs].

## Usage
Chanjo exposes a composable command line interface. You can always save intermediary files at any stage and customize every option. However, using a ``chanjo.toml`` config and UNIX pipes you can end up with something like:

```bash
$ chanjo convert CCDS.sorted.txt | chanjo annotate alignment.bam > coverage.bed
```

### Chanjo Report
A shamelessly plug for a neat little Chanjo plugin; [Chanjo-Report][report]. It allows you to extract metrics from Chanjo databases and generate coverage reports as either HTML or PDF.

After you install it using ``pip install chanjo-report`` you will notice a new subcommand under the Chanjo CLI.

```bash
$ chanjo report
#sample_id	group_id	cutoff	avg. coverage	avg. completeness	diagnostic yield	gender
vavaweho	group1	10	155.64825142540616	0.9829187630212934	0.8941083089800483	female
```

## Documentation
Read the Docs is hosting the [official documentation][docs].

I can specifically recommend the fully [interactive demo](http://www.chanjo.co/en/latest/introduction.html#demo), complete with sample data to get you started right away.

If you are looking to learn more about handling sequence coverage data in clinical sequencing, feel free to download and skim through my own [Master's thesis][thesis] and article references.

## Features

### What Chanjo does
Chanjo works on BAM alignment files and extracts interesting coverage related statistics. You use a BED-file to define which regions of the genome that you particularly care about. The output takes the shape of an extended BED-file.

An optional final step is to load data into a SQL database. This will aggregate data from exons to transcripts and genes. The database will later work as an API to downstream tools like the Chanjo Coverage Report generator.

### What Chanjo doesn't
Chanjo is not the right choice if you care about coverage for every base across the entire genome. Detailed histograms is something [BEDTools][bedtools] already handles with confidence.

## Contributors
- Robin Andeer
- Luca Beltrame ([lbeltrame](https://github.com/lbeltrame))
- John Kern ([kern3020](https://github.com/kern3020))

## License
MIT. See the [LICENSE](LICENSE) file for more details.

## Contributing
Anyone can help make this project better - read [CONTRIBUTION](CONTRIBUTION.md) to get started!


[unix]: http://en.wikipedia.org/wiki/Unix_philosophy
[docs]: http://www.chanjo.co/en/latest/
[bedtools]: http://bedtools.readthedocs.org/en/latest/
[thesis]: https://s3.amazonaws.com/tudo/chanjo/RobinAndeerMastersThesisFinal_2013.pdf
[report]: https://github.com/robinandeer/chanjo-report

[coveralls-url]: https://coveralls.io/r/robinandeer/chanjo
[coveralls-image]: https://img.shields.io/coveralls/robinandeer/chanjo.svg?style=flat

[fury-url]: http://badge.fury.io/py/chanjo
[fury-image]: https://badge.fury.io/py/chanjo.png

[travis-url]: https://travis-ci.org/robinandeer/chanjo
[travis-image]: https://img.shields.io/travis/robinandeer/chanjo.svg?style=flat
