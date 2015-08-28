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
$ ansible-galaxy install robinandeer.miniconda
$ git clone https://github.com/robinandeer/chanjo.git && cd chanjo
$ vagrant up
$ vagrant ssh
```

## Usage
Chanjo exposes a composable command line interface with a nifty config file implementation.

```bash
$ chanjo init --setup
$ chanjo load /path/to/sambamba.output.bed
$ chanjo calculate mean sample1
#sampleId	mean-coverage
sample10	176.513223249
```

## Documentation
Read the Docs is hosting the [official documentation][docs].

I can specifically recommend the fully [interactive demo](http://www.chanjo.co/en/latest/introduction.html#demo), complete with sample data to get you started right away.

If you are looking to learn more about handling sequence coverage data in clinical sequencing, feel free to download and skim through my own [Master's thesis][thesis] and article references.

## Features

### What Chanjo does
Chanjo leverages Sambamba to annotate coverage and completeness for a general BED-file. The output can then easily to loaded into a SQL database that enables investigation of coverage across regions and samples. The database also works as an API to downstream tools like the Chanjo Coverage Report generator.

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
