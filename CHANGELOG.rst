..	FORMAT:
		<version tag> "<code name>" (<data of release>)
		------------------------------------------------
		CATEGORIES:
		Bugfixes (restores expected functionality)
		Features (new functionality)
		Breaking (changes that might break previous functionality)
		Documentation (changes to documentation, inline or external)


This document contains all major version changes between Chanjo releases.

2.3.0 (Active Development)
--------------------------


2.2.1 (Current stable)
----------------------

**Bugfixes**

- Fix incorrectly references ID field in join statement (block_stats)


2.2.0
-----

**Features**

- Read sample ID from BAM header
- Validate BED format in "annotate"
- Enable getting config values from "chanjo.toml" (``chanjo config annotate.cutoff``)

**Bugfixes**

- Fix issue with hardlinks in Vagrant shared folders (setup.py)
- Change Travis CI setup using official guidelines
- Fix typography in docs
- Use io.open instead of codecs.open
- Use .sqlite3 extension for SQLite databases
- Better error message when overwriting existing databases


2.1.3
-----

**Bugfixes**

- Fix misstake in "import" subcommand so it's finally working!


2.1.2
-----

**Bugfixes**

- Fix bug in "import" where the program didn't flush the session before committing.
- Change "build_interval_data" to only create model without adding to the session.
- Use "scoped_session" with "sessionmaker".
- Flush session before each commit call in chanjo.Store.save()


2.1.1
-----

**Bugfixes**

- Fix interval assertion that didn't allow intervals to start and end on the same chromosomal position.


2.1.0
-----

**Features**

- Add lazy loading of `chanjo.Store` through new `chanjo.Store.connect` method


**Bugfixes**

- Fix case where "demo" subcommand fails (`__package__` not set)


**Documentation**

- Much improved documentation of changes between releases


2.0.2
------

**Bugfixes**

- Rename misspelled method (non-breaking): `chanjo.Store.tare_down` to `chanjo.Store.tear_down`


**Documentation**

- Fix some CSS selectors in theme
- Reorder API references in API docs


2.0.1
------

**Bugfixes**

- Fixes broken symlinked demo/fixture files
- Adds validation to check that stdin isn't empty


**Documentation**

- Fixes link to logo on front page
- Adds John Kern as collaborator
- Adds link to Master's Thesis paper for reference in README
- Adds more FAQ


2.0.0 "Wistful Weasel"
-----------------------

Being a major release, expect previous scripts written for Chanjo 1.x to be incompatible with Chanjo 2.x.

**Features**

- New built-in "demo" subcommand in the CLI
- New public setuptools entry point for Chanjo plugins (CLI subcommands)
- New official public Python API (stable until 3.x release). Read more in the new `API documentation`_.
- New "sex-checker" bonus command to guess gender from BAM alignment.

- Command line interface updates
  - :code:`--out` option removed across CLI. Use :code:`>|` to redirect STDOUT instead.
  - :code:`--prepend` is now known as :code:`--prefix`
  - :code:`--db` and :code:`--dialect` must be supplied directly after "chanjo" on the command line (not after the subcommand). Like: :code:`chanjo --db ./coverage.sqlite import annotations.bed`.
  - :code:`--extend-by` is now :code:`--extendby`

- Config file format has changed from JSON to `TOML`_. It's a more readable format (think INI) that also supports comments!

- Improves BED-format compliance. Chanjo will now expect the "score" field to be in position 5 (and strand in position 6). The Chanjo specific fields start from position 7.

- Major internal code restructuring. Essentially everything is built as plugins/self-contained components. Since no official Python API existed pre Chanjo 2, I won't go into any details here.

- Improves documentation.

- Last but not least, Chanjo will now code name releases according to animals in the Musteloidea superfamily :)

**Internal changes**

- Introduces a new compat module to better support Python 2+3.
- Trades command line framework from "docopt" to "click" to build more flexible nested commands.
- Adds a first hand `BaseInterval` object to unify handling of intervals inside Chanjo.
- BamFile no-longer requires numpy as a hard dependency. You still likely want to keep it though for performance reasons.


1.0.0 "Rebel Raccoon"
----------------------

First and current stable version of Chanjo.


0.6.0
------

**Features**

- BREAKING: changes group_id field to string instead of int.
- Exposes the threshold option to the CLI for optimizing BAM-file reading with SAMTools, fixes #58


0.5.0
------

**Bugfixes**

- UPDATE: Small updates to the command line interface
- UPDATE: New tests for new functions

**Features**

- NEW: MySQL support added
- CHANGE: A lot of internal restructuring from classes to functions
- IMPROVEMENT: New structure seems to significantly improve speed

**Documentation**

- UPDATE: New documentation covering new features/structure


0.4.0
------

- NEW: Table with Sample meta-data
- UPDATE: CLI creates sample entries
- UPDATE: SQL structure in docs
- UPDATE: Updated tests
- UPDATE: included test data (MANIFEST.in) - more on this later...


0.3.0
------

- NEW: API - annotate: splice sites option
- NEW: CLI - annotate: splice sites option
- UPDATE: Much improved documentation
- UPDATE: Modern setuptools only installation
- UPDATE: New cleaner banner
- NEW: travis integration


0.2.0
------

New CLI!

- New Command Line: "chanjo" replaces "chanjo-autopilot"
- Ability to save a temporary JSON file when running Chanjo in parallel (avoids writing to SQLite in several instances)
- New command line option: peaking into a database
- New command line option: building a new SQLite database skeleton
- New command line option: import temporary JSON files
- New command line option: reading coverage from any interval from BAM-file
- Many small bugfixes and minor improvements
- New dependency: path.py


.. _API documentation: https://chanjo.readthedocs.org/en/latest/api.html
.. _TOML: https://github.com/toml-lang/toml
