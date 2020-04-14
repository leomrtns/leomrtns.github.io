---
title: "alignment free"
date: 2020-03-05
categories:
  - Phylogenetics
---
# Alignment-free phylogenomics
Recently I saw a [very nice paper](http://dx.doi.org/10.1186/s13015-020-00164-3) 
using coloured DBG for estimating phylogenies. 
My only remark is that I would not claim this method to be alignment-free, as the title implies,
since the coloured DBG involves an alignment procedure &mdash; it is 
more compact, and non-linear when compared to a multiple-sequence alignment, but still try to infer
the sitewise homology status of the sequences. 
And I say this as a compliment to their method :D 

So I went to look for potential causes for this confusion, starting with the wikipedia page. 
In its entry for [alignment-free sequence analysis](https://en.wikipedia.org/wiki/Alignment-free_sequence_analysis), 
I noticed the presence of a biased, not to say misleading table, comparing alignment-based and alignment-free methods.
This table was copied from a [paper](https://dx.doi.org/10.1186%2F1745-6150-8-3) which had already been
[criticised by David Posada](http://dx.doi.org/10.1007/s00239-013-9566-z) precisely for throwing
away the concept of homology.
That is why Roland Wittler, the author of the coloured DBG paper, can proudly claim his method to be
alignment-based.

To be clear, I am very fond of alignment-free methods, specially as a first approximation to further analysis.
But we must recognise that it is still closer to phenetics than to modern phylogenetics, since the
relation between similarity and homology is quite complex.
Even if we could come up with a perfect measure of distance between genomes, nature is not
parsimonious. 

Having said that I would like to go back to the [paper](https://dx.doi.org/10.1186%2F1745-6150-8-3) providing the problematic 
table in wikipedia. 
The main flaw in the comparison is that compare essentially a single-gene technique (alignment-based
phylogenetics) with a whole-genome algorithm (alignment-free). 

## Contiguity
The unfair comparison is highlighted when they mention that alignment-based approaches assume "contiguity (with gaps) 
of homologous regions".
This is true for one gene (or coding region, or a region with overall evidence for common ancestry). 
But then non-contiguous regions can be concatenated into a supermatrix, or the evolutionary history
of these non-contiguous regions can be summarised via [supertrees](http://dx.doi.org/10.1007/978-1-4939-6622-6_18).
In other words, there is a step where the homology of a whole region is assumed/inferred, but
alignment-based phylogenomics is not limited to this (single gene) alignment, and proposes
verifiable models for the evolution of big parts of the genome (all coding regions, for instance)
explicitly accounting for the "non-contiguity" between homologous regions.
The "dependency" on models and the "sensitivity" to recombination and rate heterogeneity are
strenghts, and not weaknesses, of model-based approaches. 

## all-against-all
Another problem with the table is that it claims that alignment based methods depend on
"all possible pairwise comparisons of whole sequences".
This is true in most cases (except for the gene/genome problem mentioned above), but not always.
If you are familiar with `snippy`, you'll know that you can do a reference-based alignment (and
other tools expand this to more than one reference genome). The `nextstrain` project is another
example where you don't need to compare all sequences, using a reference sequence instead. 

Maybe the authors would claim that they are comparing not all alignment-based, but only approaches "based on
multiple sequence alignment" (literally, from the column title in the table).
And usually 'multiple sequence alignment' algorithms are reference-free.
Usually, but not always, as for instance the [virulign](https://doi.org/10.1093/bioinformatics/bty851) software, 
or the supra-cited ones.
Even 'mainstream' multiple sequence alignment software can do so-called "profile"
alignments, where one or two sets or sequences are already aligned.
Furthermore these software also use alignment-free approaches in the initial all-against-all comparison, never
needing to compare all pairs of "whole sequences".

## heuristic solution
They compare the heuristics of alignment-based ("statistical significance of how alignment scores relate to homology is
difficult to assess") with the "exact solution" offered by alignment-free ("statistical significance of the sequence distances (and degree of similarity) can
be readily assessed").
Which, as I mentioned above, is a sin of phenetics &mdash; finding well-bounded distances somehow
precludes homology assessment.
This, and the "lack of sensitivity to biological variation" mentioned as another advantage of alignment-free methods, make
it ideal to find an exact solution to the wrong problem.

## conclusion

I may use alignment-free methods more often than not, and there have been incredibly powerful developments based on them.
Although, to rephrase the [critics](http://dx.doi.org/10.1007/s00239-013-9566-z), no novel evolutionary knowledge 
will be derived directly and explicitly from alignment-free approaches, without 

They may well be the tool of the future, but they are still a tool.
An I hope I am not ressurrecting the Systematics Wars.
And as a final note, this is not exactly a blog, and thus is subject to changes.
