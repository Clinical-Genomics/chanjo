# Demo

Chanjo comes bundled with a set of demo files that let's you familiarize yourself with the command line interface. This guide assumed you've followed the [installation guide](../topics/installation.md).

## Demo files

First we need some files to work with. Chanjo comes with some pre-installed demo files we can use:

```bash
$ chanjo init --demo ./chanjo-demo
```
This will create a new folder (`./chanjo-demo`) in your current working directory and fill it with example files.

> You can name the new folder anything you like but it must not already exist!

A couple of demo files are now generated:

```bash
$ls chanjo-demo/
chanjo.coverage.sqlite3	chanjo.yaml		hgnc.min.bed		sample1.coverage.bed	
sample2.coverage.bed	sample3.coverage.bed
```

- **chanjo.coverage.sqlite3** this is the actual database, contains nothing at this stage.
- **chanjo.yaml** configuration file described [below](#configuration)
- **hgnc.min.bed** defenition of genes exons and transcripts are linked, described in detail [below](#linking)
- **sample.coverage.bed** coverage information for some example individuals

## Configuration {#configuration}

Chanjo went ahead and pre-filled a config-file for you under: `./chanjo-demo/chanjo.yaml`. For now it just references the SQLite database we will use. But since Chanjo will look for this file in the current working directory when you run the command we don't need to reference the database every time.

> You can optionally point to a config file in a different location by using the `--config` flag like: `chanjo --config /path/to/chanjo.yaml`.

## Linking exons/transcripts/genes {#linking}

Chanjo doesn't subscribe to any particular definition of exons/transcripts etc. We'll have a look at the top few lines of our demmo file to see how exons/transcripts/genes are linked: 
```bash
$head chanjo-demo/hgnc.min.bed
1	955550	955755	1-955552-955753	NM_198576	329	AGRN
1	957579	957844	1-957581-957842	NM_198576	329	AGRN
1	970655	970706	1-970657-970704	NM_198576	329	AGRN
1	976043	976262	1-976045-976260	NM_198576	329	AGRN
1	976551	976779	1-976553-976777	NM_198576	329	AGRN
1	976856	977084	1-976858-977082	NM_198576	329	AGRN
1	977334	977544	1-977336-977542	NM_198576	329	AGRN
1	978617	978839	1-978619-978837	NM_198576	329	AGRN
1	978916	979114	1-978918-979112	NM_198576	329	AGRN
1	979201	979405	1-979203-979403	NM_198576	329	AGRN
```
First three columns are standard [.bed][bed] format that describes the coordinates of a exon. Column number four is just an unique id for a exon, column five is the identifier of the transcript(s) that the exon belongs to. Column 6 and 7 are gene identifiers, first is the hgnc id then the hgnc symbol.
When a exon belongs to multiple transcripts the row would look like this:

```
11      612642  612802  11-612644-612800        NM_001572,XM_005252907,NM_004029,NM_004031      6122,6122,6122,6122     IRF7,IRF7,IRF7,IRF7
```  

Also remember that if the exon belongs to transcripts that resides in different genes they should be annotated in the same line.

Let's tell Chanjo which transcripts belong to which genes. You only need to run this command once.

```bash
$ cd chanjo-demo
$ chanjo link ./hgnc.min.bed
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
[bed]: https://genome.ucsc.edu/FAQ/FAQformat.html#format1