<p align="center">
  <a href="http://chanjo.co">
    <img height="235"
         width="244"
         src="https://raw.githubusercontent.com/robinandeer/chanjo/master/assets/chanjo-logo.png"/>
  </a>
</p>

# Chanjo [![PyPI version][fury-image]][fury-url] [![Build Status][travis-image]][travis-url]
Coverage analysis for clincal sequencing and beyond (documentation_).

```shell
$ cat intervals.bed
1  10 15 interval-1
2  45 55 interval-2
$ cat intervals.bed | chanjo annotate alignment.bam
#{"sample_id": "bavewira", ...}
1  10 15 interval-1  9.92231     0.97231
2  45 55 interval-2  14.23123 1.0
```

# Documentation
The [redesigned documentation](http://www.chanjo.co) has all the information you want; getting started guide, foolproof installation instructions, and in-depth overviews.

I can specifically recommend the fully [interactive demo](http://www.chanjo.co/en/latest/introduction.html#demo), complete with sample data to get you started right away.

# Installation
Complete instructions are available in the [documentation](http://www.chanjo.co) but installation (*can be*) as simple as running:

```shell
$ pip install chanjo
```

Contributors
-------------
Robin Andeer

Luca Beltrame ([lbeltrame](https://github.com/lbeltrame))


License
--------
MIT


[fury-url]: http://badge.fury.io/py/chanjo
[fury-image]: https://badge.fury.io/py/chanjo.png

[travis-url]: https://travis-ci.org/robinandeer/chanjo
[travis-image]: https://travis-ci.org/robinandeer/chanjo.png?branch=develop
