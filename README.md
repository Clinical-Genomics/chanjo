![Chanjo Avatar](https://raw.github.com/robinandeer/chanjo2/master/assets/chanjo_logo.png)
=======

## What is it?
DNA sequencing is moving into clinical applications. We need tools to determine coverage for clinically relevant abstractions such as genes, transcripts, and exons.

Chanjo provides this functionality in a more intuitive way than dealing with BED-intervals.

### Coverning ideas

By focusing on the clinically relevant regions of the genome we also get statistics that tells us more about the actual performance of the sequenceing. Why include reads covering regions that we aren't interested in?

One example in exome sequencing are reads from unspecifically binding baits which add to the average read depth while in reality representing wasted coverage potential.

It will also be possible to set an upper limit for what read depths will be considered relevant. E.g. 50 reads are sufficient to reliably call genotypes for any position. Extreme regions can therefore be "held back" to not affect general statisctics.

## Main features
| Feature            | Description   |
| ------------------ | ------------- |
| BAM support        | Generate coverage directly from BAM alignments. Fit's right into your genomics pipeline. |
| Just what you need | Limit calculations to a list of genes of interest. |

## Installation
- [ ] Automatic pip install support

## Contributor list
Robin Andeer

## Credits, Inspiration, Alternatives

## License
MIT
