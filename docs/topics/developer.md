# Developer's Guide

This document is intended for people interested in contributing to the further development of chanjo.

## Contributing

Currently the best resource on this topic is available at GitHub, in the [CONTRIBUTING.md][contrib] file.

## Building documentation

I use [GitBook][gitbook] for the documentation. For this one, you'll need a working [Node.js][node] installation. Fortunately with Miniconda this is easy!

```bash
$ conda install -c bokeh nodejs
$ npm install -g gitbook-cli
```

To build the documentation locally, you just run:

```bash
$ gitbook serve
```

...and open your browser to [http://localhost:4000](http://localhost:4000).

## License

The MIT License (MIT)


[gitbook]: https://www.gitbook.com/
[node]: https://nodejs.org/en/
[contrib]: https://github.com/robinandeer/chanjo/blob/master/CONTRIBUTING.md
