..	FORMAT:
		<version tag> "<code name>" (<data of release>)
		------------------------------------------------
		CATEGORIES:
		Bugfixes (restores expected functionality)
		Features (new functionality)
		Breaking (changes that might break previous functionality)
		Documentation (changes to documentation, inline or external)


This document contains all major version changes between Chanjo releases.


2.0.0 "Wistful Weasel" (Active development)
--------------------------------------------

Being a major release, expect previous scripts written for Chanjo 1.x to be incompatible with Chanjo 2.x.


1.0.0 "Rebel Raccoon" (Current stable)
-------------------------------------------

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
