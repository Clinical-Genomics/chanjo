# Demo

Chanjo comes bundled with a set of demo files that let's you familiarize yourself with the command line interface. This guide assumed you've followed the [installation guide](topics/installation.md).

## Demo files

First we need some files to work with. Chanjo comes with some pre-installed demo files we can use:

```bash
$ chanjo init --demo ./chanjo-demo
$ cd chanjo-demo
```
This will create a new folder (`./chanjo-demo`) in your current working directory and fill it with example files.

> You can name the new folder anything you like but it must not already exist!

## Setup and configuration

Chanjo went ahead and pre-filled a config-file for you under: `./chanjo-demo/chanjo.yaml`. For now it just references the SQLite database we will use. But since Chanjo will look for this file in the current working directory when you run the command we don't need to reference the database every time.

Let's set up the database:

```bash
$ chanjo db setup
```

> You can optionally point to a config file in a different location by using the `--config` flag like: `chanjo --config /path/to/chanjo.yaml`.

## Linking exons/transcripts/genes

Chanjo doesn't subscribe to any particular definition of exons/transcripts etc. You can take a look at the how exons/transcripts/genes are linked in: `ccds.min.bed`. Let's tell Chanjo which transcripts belong to which genes. You only need to run this command once.

```bash
$ chanjo link ccds.min.bed
```

## Loading annotations

After running `sambamba depth region` for a BED-file you can take the output and load it into the database. Let's also add a group identifier to indicate that the sample are related.

```bash
$ for file in *.coverage.bed; do echo "${file}"; chanjo load --group group1 "${file}"; done
```

## Extracting information

Chanjo can do some rudimentary metrics from the loaded data. You can start exploring what coverage looks like for the samples. Let's take a look at the mean values for our coverage metrics:

```
$ chanjo calculate mean --pretty
```

> So what is this "completeness"? Well, it’s pretty simple; the percentage of bases with at least "sufficient" (say; 10x) coverage.

## What's next?

The SQL schema has been designed to be a powerful tool on it’s own for studying coverage. It let's you quickly aggregate metrics across multiple samples and can be used as a general coverage API for accompanying tools.

One example of such a tool is [Chanjo-Report][report], a coverage report generator for Chanjo output. A report could look something like this.


[report]: https://github.com/robinandeer/Chanjo-Report
