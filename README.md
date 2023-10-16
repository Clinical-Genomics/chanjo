<p align="center">
  <a href="https://github.com/Clinical-Genomics/chanjo">
    <img height="235" width="244" src="docs/assets/logo.png"/>
  </a>
</p>

# Chanjo 
![Docker build - GitHub](https://github.com/Clinical-Genomics/chanjo/actions/workflows/docker_build_n_publish.yml/badge.svg)
[![PyPI version](https://badge.fury.io/py/chanjo.svg)](https://badge.fury.io/py/chanjo)
[![Coverage Status](https://coveralls.io/repos/github/Clinical-Genomics/chanjo/badge.svg?branch=master)](https://coveralls.io/github/Clinical-Genomics/chanjo?branch=master)


Chanjo is coverage analysis for clinical sequencing. It's implemented in Python
with a command line interface that adheres to [UNIX pipeline philosophy][unix].

If you find chanjo useful in your project, please cite the [article][publication].

## Installation
Chanjo is distributed through `pip`. Install the latest stable release by
running:

```bash
pip install chanjo
```

... or locally for development:

```bash
git clone https://github.com/Clinical-Genomics/chanjo.git
cd chanjo
conda install --channel bioconda sambamba
pip install -r requirements-dev.txt --editable .
```

## Usage
Chanjo exposes a decomposable command line interface with a nifty config file
implementation.

```bash
chanjo init --setup
chanjo load /path/to/sambamba.output.bed
chanjo calculate mean
{"metrics": {"completeness_10": 90.92, "mean_coverage": 193.85}, "sample_id": "sample1"}
```

## Docker

When running the dockerized version of [Chanjo](https://hub.docker.com/r/clinicalgenomics/chanjo) the setup process is slightly different. Chanjo depends on a configuration file `config.yaml` and either a sqlite database `chanjo.coverage.sqlite3` or a `MySQL database`, which are created at initialization. For convenience, we provide a docker-compose file containing a mariadb (MySQL-based) service and the chanjo-command line that can be used to set up a demo instance of Chanjo.
Since the database set up (chanjo init command) and sample data insertion are executed by two distinct instances of the same service (chanjo-cli), Docker [volumes](https://docs.docker.com/storage/volumes/) must be used to make sure that the database instance has data continuity during the two steps.
The following examples demonstrate how to set up Chanjo using the docker-compose file using the default definition of exons (init demo files are present in folder `chanjo/init/demo-files`). The config file and the creted database will be stored on the host in a folder named `data`, which is mirrored by folder `/home/worker/data` in the chanjo container . Other exon definitions can be used by mounting them to the container.

### Example with MySQL-based database (MariaDB)

```bash
# Build a docker image
docker-compose build
```
```bash
# Set up chanjo and populate demo database with exons definitions
docker-compose run --rm -v "${PWD}/data:/home/worker/data" -v "${PWD}/data/database:/home/worker/data/database" chanjo-cli bash -c "chanjo -d mysql+pymysql://chanjoUser:chanjoPassword@mariadb/chanjo4_test init --auto /home/worker/data && chanjo --config /home/worker/data/chanjo.yaml link /home/worker/data/hgnc.grch37p13.exons.bed"
```
This initial step will create a `data` folder containing 2 files:
- hgnc.grch37p13.exons.bed --> Exons definitions
- chanjo.yaml --> Contains the database URI, so in the next step you can use this config file instead of `-d mysql+pymysql://chanjoUser:chanjoPassword@mariadb/chanjo4_test`

```bash
# Load sample
docker-compose run --rm -v "${PWD}/data:/home/worker/data" -v "${PWD}/data/database:/home/worker/data/database" chanjo-cli bash -c "chanjo --config /home/worker/data/chanjo.yaml load /home/worker/app/chanjo/init/demo-files/sample1.coverage.bed"
```

### Example with SQLite database

```bash
# setup chanjo and save populate demo database with exon definitions
docker-compose run --rm -v "${PWD}/data:/home/worker/data" -v "${PWD}/data/database:/home/worker/data/database" chanjo-cli bash -c "chanjo init --auto /home/worker/data && chanjo --config /home/worker/data/chanjo.yaml link /home/worker/data/hgnc.grch37p13.exons.bed"
# load sample
docker-compose run --rm -v "${PWD}/data/chanjo.coverage.sqlite3:/home/worker/app/chanjo.coverage.sqlite3" -v "${PWD}/data:/home/worker/data" chanjo-cli bash -c "chanjo --config /home/worker/data/chanjo.yaml load /home/worker/app/chanjo/init/demo-files/sample1.coverage.bed"

## Documentation
Read the Docs is hosting the [official documentation][docs].

If you are looking to learn more about handling sequence coverage data in
clinical sequencing, feel free to download and skim through my own
[Master's thesis][thesis] and article references.

## Features

### What Chanjo does
Chanjo leverages [Sambamba][sambamba] to annotate coverage and completeness
for a general BED-file. The output can then easily to loaded into a SQL
database that enables investigation of coverage across regions and samples.
The database also works as an API to downstream tools like the Chanjo
Coverage Report generator.

### What Chanjo doesn't
Chanjo is not the right choice if you care about coverage for every base across
the entire genome. Detailed histograms is something [BEDTools][bedtools]
already handles with confidence.

## Contributors
-   Robin Andeer ([robinandeer](https://github.com/robinandeer))
-   Luca Beltrame ([lbeltrame](https://github.com/lbeltrame))
-   John Kern ([kern3020](https://github.com/kern3020))
-   Måns Magnusson ([moonso](https://github.com/moonso))
-   Patrik Grenfeldt ([patrikgrenfeldt](https://github.com/patrikgrenfeldt))

## License
MIT. See the [LICENSE](LICENSE) file for more details.

## Contributing
Anyone can help make this project better - read [CONTRIBUTION](CONTRIBUTION.md)
to get started!

[bedtools]: http://bedtools.readthedocs.org/en/latest/
[docs]: https://clinical-genomics.github.io/chanjo/
[publication]: https://f1000research.com/articles/9-615/v1
[sambamba]: http://lomereiter.github.io/sambamba/
[thesis]: https://s3.amazonaws.com/tudo/chanjo/RobinAndeerMastersThesisFinal_2013.pdf
[unix]: http://en.wikipedia.org/wiki/Unix_philosophy

