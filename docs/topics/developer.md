# Developer's Guide

This document is intended for people interested in contributing to the further development of chanjo.

## Contributing

Currently the best resource on this topic is available at GitHub, in the [CONTRIBUTING.md][contrib] file.

## Building documentation

We use [MkDocs][mkdocs] for the documentation. To build documentation local install `requirements-dev.txt`

```bash
$ pip install -r requirements-dev.txt
```

To build the documentation locally, you just run:

```bash
$ mkdocs serve
```

...and open your browser to [http://localhost:4000](http://localhost:4000).

## License

The MIT License (MIT)


[mkdocs]: https://www.mkdocs.org
[contrib]: https://github.com/Clinical-Genomics/chanjo/blob/master/CONTRIBUTING.md
