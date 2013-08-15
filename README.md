![Chanjo Avatar](https://raw.github.com/robinandeer/chanjo2/master/assets/chanjo_logo.png)

## What is it?
DNA sequencing is moving into clinical applications. We need tools to determine
coverage for clinically relevant abstractions such as genes, transcripts, and
exons.

Chanjo provides this functionality in a more intuitive way than dealing with
BED-intervals.

### Coverning ideas

By focusing on the clinically relevant regions of the genome we also get
statistics that tells us more about the actual performance of the sequenceing.
Why include reads covering regions that we aren't interested in?

One example in exome sequencing are reads from unspecifically binding baits
which add to the average read depth while in reality representing wasted
coverage potential.

It will also be possible to set an upper limit for what read depths will be
considered relevant. E.g. 50 reads are sufficient to reliably call genotypes for
any position. Extreme regions can therefore be "held back" to not affect general
statisctics.

## Demo
```python
from chanjo import chanjo, sqlite, bam

# Instantiation
analyzer = chanjo.Analyzer()
elements = sqlite.ElementAdapter("tests/data/CCDS.db")
coverage = bam.CoverageAdapter("test/data/align.bam")

# Plug in the adapters
analyzer.setAdapters(coverage, elements)

# We are ready! Let's take a look at a gene
gene = analyzer.get("gene", "EGFR")

# Calculate coverage & completeness (don't worry about the third return value)
analyzer.coverage(gene.chrom, gene.simpleIntervals())
# => (8.42399129, 0.542334432, None)
```

## Main features
| Feature            | Description   |
| ------------------ | ------------- |
| BAM support        | Generate coverage directly from BAM alignments. Fit's right into your genomics pipeline. |
| Just what you need | Limit calculations to a list of genes of interest. |
| % coverage         | The bredth of coverage at sufficient coverage is treated as important as depth of coverage. |
| Test report export | Simple output that can be parsed to generate a genetic test report. |

## Contribute
If you feel like learning more about the project and contributing a good idea
would be to see if you can rewrite the current ElementAdapter (sqlite) to use
the popular python ORM SQLAlchemy as a replacement of Autumn.

Or why not go one step further and implement an adapter relying on a more
flexible NoSQL database.

## Installation
- [ ] Automatic pip install support

## Contributor list
Robin Andeer

## Credits, Inspiration, Alternatives

## License
MIT
