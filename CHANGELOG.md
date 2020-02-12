# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## [4.4.0] - 2020-02-12

### Added
- User can pass on file with row separated gene IDs for coverage calculation

## [4.3.0] - 2020-02-05

### Added
- added CLI commands

## [4.0.0] - 2016-08-02
Version 4 slims down Chanjo quite a bit.

### Added
- Lots of test, now 100% test coverage!
- Cascade rules to make sure stats records get deleted with parent sample

### Changed
- Switched from Read the Docs to GitBook for documentation
- Updated demo

### Removed
- Old database schema with explicit exon/gene records

## [3.4.1] - 2016-03-08
### Changed
- setup and tear down session in Flask app usage

## [3.4.0] - 2016-03-08
### Added
- All new transcript focused schema, generally activated by `--transcript` flag in CLI, this significantly reduces the database footprint and speeds up loading to only a few seconds for a full exome

## [3.3.1] - 2016-02-23
### Fixed
- properly report if a CLI subcommand is not found
- properly output results from "calculate region"
- show error message for unknown region ids
- fix sqlite issue when adding both `exon_obj` and `exon_id`

### Changed
- make schema more strict about which columns need to exist

## [3.3.0] - 2016-02-15
### Changed
- add indexes to models, especially to `exon_stat.metric` to speed up queries
- speed up loading by front-loading existing exons (~7 min)
- update resources bundled in the `bootstrap` command, now includes database with exons + slicing sites

### Fixed
- travis-ci setup for testing

## [3.2.1] - 2016-01-28
### Changed
- do a rollback of failed transactions on "save"

### Added
- show progress of load command on "info" level

## [3.2.0] - 2015-12-22
### Changed
- diagnostic yield function now accepts "exon_ids" explicitly and requires "sample_id" to be given

## [3.1.1] - 2015-11-19
### Fixed
- fixed bug in SQL relationship between gene and transcript

## [3.1.0] - 2015-11-16
### Added
- `sex` subcommand for guessing sex from BAM alignment, see #158

## [3.0.2] - 2015-11-04
### Fixed
- chanjo API: restrict converter queries to distinct/unique rows

## [3.0.1] - 2015-10-26
### Fixed
- import from root init, use root logger

## [3.0.0] - 2015-10-19
Code name: "Radical Red Panda"

This is a major new release. Please refer to the documentation for more details on what has been updated.

### Added
- Add functionality to run sambamba from chanjo
- Add calulate command to get basic statistics from database
- Add link command to specifically link genomic elements
- Add db command to interface and perform maintainance on database

### Removed
- Support for older versions of Chanjo

### Fixed
- Changed way of logging
- Added proper logstream handler


## [2.3.2] - 2015-03-21
### Fixed
- Refactor ``EntryPointsCLI`` to allow for external subcommands
- Updated documentation to reflect Chanjo 2.x CLI

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
