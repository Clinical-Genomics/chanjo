Changelog
==========

0.2.0
----------------
New CLI!

* New Command Line: "chanjo" replaces "chanjo-autopilot"
* Ability to save a temporary JSON file when running Chanjo in parallel (avoids writing to SQLite in several instances)
* New command line option: peaking into a database
* New command line option: building a new SQLite database skeleton
* New command line option: import temporary JSON files
* New command line option: reading coverage from any interval from BAM-file
* Many small bugfixes and minor improvements
* New dependency: path.py

v0.3.0
-----------------
* NEW: API - annotate: splice sites option
* NEW: CLI - annotate: splice sites option
* UPDATE: Much improved documentation
* UPDATE: Modern setuptools only installation
* UPDATE: New cleaner banner
* NEW: travis integration

v0.4.0
-----------------
* NEW: Table with Sample meta-data
* UPDATE: CLI creates sample entries
* UPDATE: SQL structure in docs
* UPDATE: Updated tests
* UPDATE: included test data (MANIFEST.in) - more on this later...

v0.5.0
-----------------
* NEW: MySQL support added
* CHANGE: A lot of internal restructuring from classes to functions
* IMPROVEMENT: New structure seems to significantly improve speed
* UPDATE: New tests for new functions
* UPDATE: New documentation covering new features/structure
* UPDATE: Small updates to the command line interface
