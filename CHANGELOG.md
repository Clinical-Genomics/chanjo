# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## [2.3.1] - 2015-03-05
### Changed
- use custom "multi command class" to load dynamic entry point plugins

### Fixed
- some pylint improvements

## [2.3.0]
### Added
- New logging module accessible from the command line (-vvv)
- Add SQL schema drawing to "Code walkthrough"


## [2.2.1]
### Fixed
- Fix incorrectly references ID field in join statement (block_stats)


## [2.2.0]
### Added
- Read sample ID from BAM header
- Validate BED format in "annotate"
- Enable getting config values from "chanjo.toml" (``chanjo config annotate.cutoff``)

### Fixed
- Fix issue with hardlinks in Vagrant shared folders (setup.py)
- Change Travis CI setup using official guidelines
- Fix typography in docs
- Use io.open instead of codecs.open
- Use .sqlite3 extension for SQLite databases
- Better error message when overwriting existing databases


## [2.1.3]
### Fixed
- Fix misstake in "import" subcommand so it's finally working!


## [2.1.2]
### Fixed
- Fix bug in "import" where the program didn't flush the session before committing.
- Change "build_interval_data" to only create model without adding to the session.
- Use "scoped_session" with "sessionmaker".
- Flush session before each commit call in ``chanjo.Store.save()``


## [2.1.1]
### Fixed
- Fix interval assertion that didn't allow intervals to start and end on the same chromosomal position.


## [2.1.0]
### Added
- Add lazy loading of ``chanjo.Store` through new ``chanjo.Store.connect` method
- Much improved documentation of changes between releases

### Fixed
- Fix case where "demo" subcommand fails (``__package__` not set)

## [2.0.2]
### Fixed
- Rename misspelled method (non-breaking): ``chanjo.Store.tare_down` to ``chanjo.Store.tear_down`

### Fixed
- Fix some CSS selectors in theme
- Reorder API references in API docs


## [2.0.1]
### Fixed
- Fixes broken symlinked demo/fixture files
- Adds validation to check that stdin isn't empty
- Fixes link to logo on front page
- Adds John Kern as collaborator
- Adds link to Master's Thesis paper for reference in README
- Adds more FAQ


## [2.0.0]
Code name: "Wistful Weasel"

Being a major release, expect previous scripts written for Chanjo 1.x to be incompatible with Chanjo 2.x.

### Added
- New built-in "demo" subcommand in the CLI
- New public setuptools entry point for Chanjo plugins (CLI subcommands)
- New of
cial public Python API (stable until 3.x release). Read more in the new [API documentation][api-docs].
- New "sex-checker" bonus command to guess gender from BAM alignment.

- Command line interface updates
	- ``--out`` option removed across CLI. Use ``>|`` to redirect STDOUT instead.
	- ``--prepend` is now known as ``--prefix``
	- ``--db`` and ``--dialect`` must be supplied directly after "chanjo" on the command line (not after the subcommand). Like: ``chanjo --db ./coverage.sqlite import annotations.bed``.
	- ``--extend-by`` is now ``--extendby``

- Config file format has changed from JSON to [TOML][toml]. It's a more readable format (think INI) that also supports comments!

- Improves BED-format compliance. Chanjo will now expect the "score" field to be in position 5 (and strand in position 6). The Chanjo specific fields start from position 7.

- Major internal code restructuring. Essentially everything is built as plugins/self-contained components. Since no official Python API existed pre Chanjo 2, I won't go into any details here.

- Improves documentation.

- Last but not least, Chanjo will now code name releases according to animals in the Musteloidea superfamily :)

- Introduces a new compat module to better support Python 2+3.
- Trades command line framework from "docopt" to "click" to build more flexible nested commands.
- Adds a first hand `BaseInterval` object to unify handling of intervals inside Chanjo.
- BamFile no-longer requires numpy as a hard dependency. You still likely want to keep it though for performance reasons.


## [1.0.0]
Code name: "Rebel Raccoon"

First and current stable version of Chanjo.


## [0.6.0]
### Added
- BREAKING: changes group_id field to string instead of int.
- Exposes the threshold option to the CLI for optimizing BAM-file reading with SAMTools, fixes #58

## [0.5.0]
### Fixed
- UPDATE: Small updates to the command line interface
- UPDATE: New tests for new functions
### Added
- NEW: MySQL support added
- CHANGE: A lot of internal restructuring from classes to functions
- IMPROV
ENT: New structure seems to significantly improve speed
**Documentation**
- UPDATE: New documentation covering new features/structure


## [0.4.0]
- NEW: Table with Sample meta-data
- UPDATE: CLI creates sample entries
- UPDATE: SQL structure in docs
- UPDATE: Updated tests
- UPDATE: included test data (MANIFEST.in) - more on this later...


## [0.3.0]
- NEW: API - annotate: splice sites option
- NEW: CLI - annotate: splice sites option
- UPDATE: Much improved documentation
- UPDATE: Modern setuptools only installation
- UPDATE: New cleaner banner
- NEW: travis integration


## [0.2.0]
New CLI!

- New Command Line: "chanjo" replaces "chanjo-autopilot"
- Ability to save a temporary JSON file when running Chanjo in parallel (avoids writing to SQLite in several instances)
- New command line option: peaking into a database
- New command line option: building a new SQLite database skeleton
- New command line option: import temporary JSON files
- New command line option: reading coverage from any interval from BAM-file
- Many small bugfixes and minor improvements
- New dependency: path.py


[api-docs]: https://chanjo.readthedocs.org/en/latest/api.html
[toml]: https://github.com/toml-lang/toml
