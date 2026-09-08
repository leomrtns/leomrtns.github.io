---
image: /assets/design/posts/invariant-sites.svg
image-alt: An alignment highlighting constant and variable columns
title: Not all invariant sites are created the same
date: '2022-08-16'
author: Leo Martins
categories:
- phylogenetics
description: Why removing invariant sites is usually a bad idea for maximum likelihood
  tree inference
aliases:
- /jupyterblog/phylogenetics/2022/08/16/lnl_uncertainty.html
toc: true
---

A while back we had an [interesting discussion regarding the exclusion of invariant sites in maximum likelihood
phylogenetic inference](https://bitsandbugs.org/2019/11/06/two-easy-ways-to-run-iq-tree-with-the-correct-number-of-constant-sites/).
Since this discussion usually comes up again and again, I would like to add a bit of context.

First, I understand that there are situations where it is unavoidable to exclude "uninteresting" sites to speed up
calculations, and in many practical situations we expect the results to be unchanged. In these cases, and listening to
the justification for it, I wonder why using a slower likelihood method instead of a much faster distance-based method.
But that's a different story.

So, in a nutshell, the problem lies when we have a large alignment where most of the sites (columns in the alignment)
are constant, i.e. there is no polymorphism (SNPs) and thus we assume they do not affect the tree estimation. Their
removal should not affect the topology, but the branch lengths are indeed affected by the number of constant sites.

Removing constant sites biases your data set towards fast-evolving sites, thus the name ASC ("ascertainment bias" is a
type of selection bias). The obvious effect is that all estimated branch lengths will be very large, since they are
given in substitutions per site and at least one of the sequences has a SNP at a given position. For instance, if you
have two genomes of 1000bp but only 10 sites are polymorphic (i.e. SNPs, the other 900 are identical on both sequences),
then their distance is 1/100 substitutions per site; however if you only look at the 10 SNPs then their distance is 1
substitution per site!

When you have several sequences and a tree it gets more complicated since maximum likelihood methods like IQTREE2
estimate the instantaneous rate matrix &mdash; from the HKY model, for instance. Which describes the probability of A
becoming a C etc. and it must take into account the many constant sites in order to have a good estimate of the
Prob(A->A) and so forth. If there are no constant sites the rate matrix will inflate Prob(A->C) and collapse Prob(A->A)
and thus branch lengths will be inflated in a non-linear way for most models (otherwise we could just correct by
dividing branch lengths by an amount, like 100 in example above). The topology may also be affected. The bias correction
is done by replacing the unconditional probabilities Prob(A->C) by conditional ones Prob(A->C "given that" all constant
sites were removed).

## Removing invariant sites and telling the tree inference program about it

One solution for this problem is to calculate how many (constant) sites you are excluding and then adding this
information to the phylogenetic inference software (the link above contains instructions on how to to this with IQTREE2;
the same can be done for BEAST or RaxML).

We may be tempted to use an explicit "ascertainment bias correction" model, but we have to be careful since the ASC
method implemented in iqtree2 assumes that we do not know how many constant sites we are excluding (see
[https://www.biorxiv.org/content/10.1101/186478v1](https://www.biorxiv.org/content/10.1101/186478v1), and
[http://dx.doi.org/10.1093/sysbio/syv053](http://dx.doi.org/10.1093/sysbio/syv053) for details). Which is true for
morphological data, but not in general for genomes, since we can count (`snp-sites -C`) the constant sites we are
excluding. Therefore we have more precise estimation by informing iqtree2 the number of excluded sites (the option
"-fconst") as discussed in the link above
[https://bitsandbugs.org/2019/11/06/two-easy-ways-to-run-iq-tree-with-the-correct-number-of-constant-sites/](https://bitsandbugs.org/2019/11/06/two-easy-ways-to-run-iq-tree-with-the-correct-number-of-constant-sites/).
Notice that `-fconst` creates artificial columns in the alignment with the constant sites, and therefore is not
compatible with `+ASC`. That is, if you call iqtree with both  `+ASC` and `-fconst` then ASC will complain that there
are constant sites in the alignment (which were added by `-fconst`!)


RaxML handles more ASC models:
[https://github.com/amkozlov/raxml-ng/wiki/Input-data#evolutionary-model](https://github.com/amkozlov/raxml-ng/wiki/Input-data#evolutionary-model),
where the `STAM` model is equivalent to `-fconst` and the `LEWIS` model is equiv to `+ASC` in IQTREE2.

## Sometimes it's better not to do anything

My suggestion in the discussion linked above and in general, is to leave the original data as is without trying to
remove sites and correcting later. This is because if the sites are "truly" invariant then they won't add to the
computational time (as explained by Alexis Stamatakis in
[https://groups.google.com/g/raxml/c/JuwXlf576Sw](https://groups.google.com/g/raxml/c/JuwXlf576Sw) for instance). This
is also what IQTREE2 does, as mentioned above: it adds four artificial columns to the alignment weighted by their
counts. This is because most likelihood algorithms compress the alignments into distinct "patterns", weighted by how
many times we see them in the alignment.

There is an important difference, however, which is the inclusion of gaps and Ns in the "invariant" sites. For instance,
take the following alignments (one line per sequence, spaces to ease visualisation):

```config
alignment 1
>seq1 NNNNCCTCCC CGGTTCCAAC CTTCCAAAAA
>seq2 NNNNCCTCCC CGGTTCCAAC CCCTTATAAA
>seq3 ----CCTCCC CGGTTCCTTG GCCTTAACAA
>seq4 ----CCTCCC CGGAAGGTTG GCCTTAAAGA
>seq5 ----CCTCCT TTTAAGGTTG GCCTTAAAAT

alignment 2
>seq1 AAAACCTCCC CGGTTCCAAC CTTCCAAAAA
>seq2 NNNNCCTCCC CGGTTCCAAC CCCTTATAAA
>seq3 ----CCTCCC CGGTTCCTTG GCCTTAACAA
>seq4 ----CCTCCC CGGAAGGTTG GCCTTAAAGA
>seq5 ----CCTCCT TTTAAGGTTG GCCTTAAAAT

alignment 3
>seq1 NNNNCCTCCC CGGTTCCAAC CTTCCAAAAA
>seq2 AAAACCTCCC CGGTTCCAAC CCCTTATAAA
>seq3 AAAACCTCCC CGGTTCCTTG GCCTTAACAA
>seq4 ----CCTCCC CGGAAGGTTG GCCTTAAAGA
>seq5 ----CCTCCT TTTAAGGTTG GCCTTAAAAT
```

The only difference between the alignments are the first four sites: in alignment 1 we only have gaps and Ns. In
alignments 2 and 3 we have `AAAA` in a few samples, instead.
**All 3 alignments are identical after removal of constant sites** with `snp-sites`, since the first four sites do not have SNPs!
Which is what I meant in the discussion linked above when I said

> One thing to consider is that a column composed of “AAAA” is distinct from one composed of “AANN” or “AA-A”, although all 3 of them will be removed by snp-sites -c.

If we fix the topology and the branch lengths (`iqtree2 -s ${file}.aln -te fixed.tre -blfix -m JC`) then the
log-likelihood of the three alignments will be -115.559 for alignment 1, -121.104 for alignment 2, and -122.123 for
alignment 3. So the likelihood is different for the three alignments (I'm using the Jukes-Cantor model to avoid handling
extra parameters). Using `snp-sites` to remove the invariant sites and to count the frequencies would not fix the
problem since alignments 2 and 3 have the same number of "invariant sites": `5,4,0,1`. To make a long story short, I ran
the 3 alignments under a fixed tree (topology and branch lengths) as above and asking IQTREE2 to optimise the branch
lengths (`iqtree2 -s ${i} -te fixed.tre --prefix ${i%aln}best_length -m JC`). I also used only the constant sites with
the `snp-sites` correction, as in

```bash
snp-sites -c $i > ${i%aln}snpsites
iqtree2 -fconst $(snp-sites -C ${i}) -s ${i%aln}snpsites -m JC --prefix ${i%aln}const
```
We have the results as below, where we can see that not only the likelihoods, but the tree branch lengths are different:

iqtree file | log-likelihood | ML tree
---- | ---- | ----
alignment1.aln | -115.559 | (seq1:0.1886473604,seq2:0.0303274053,(seq3:0.0284331913,(seq4:0.0258689619,seq5:0.2463693196):0.2138883204):0.2087029810);
alignment1.best_length | -115.559 | (seq1:0.1886473604,seq2:0.0303274053,(seq3:0.0284331913,(seq4:0.0258689619,seq5:0.2463693196):0.2138883204):0.2087029810);
alignment1.const | -115.559 | (seq1:0.1886475517,seq2:0.0303274177,(seq3:0.0284339867,(seq4:0.0258696236,seq5:0.2463695763):0.2138875505):0.2087022795);
alignment2.aln | -121.104 | (seq1:0.1886473604,seq2:0.0303274053,(seq3:0.0284331913,(seq4:0.0258689619,seq5:0.2463693196):0.2138883204):0.2087029810);
alignment2.best_length | -121.104 | (seq1:0.1886473604,seq2:0.0303274053,(seq3:0.0284331913,(seq4:0.0258689619,seq5:0.2463693196):0.2138883204):0.2087029810);
alignment2.const | -124.433 | (seq1:0.1577276882,seq2:0.0281664193,(seq3:0.0272139809,(seq4:0.0254304079,seq5:0.2041776675):0.1736347105):0.1705027642);
alignment3.aln | -122.123 | (seq1:0.1886473604,seq2:0.0303274053,(seq3:0.0284331913,(seq4:0.0258689619,seq5:0.2463693196):0.2138883204):0.2087029810);
alignment3.best_length | -122.045 | (seq1:0.1888748916,seq2:0.0261918048,(seq3:0.0246320132,(seq4:0.0257728057,seq5:0.2464608488):0.2140593199):0.1757918053);
alignment3.const | -124.433 | (seq1:0.1577274163,seq2:0.0281664193,(seq3:0.0272140466,(seq4:0.0254297568,seq5:0.2041783024):0.1736349260):0.1705029865);

Notice that all trees are identical for `alignment*.aln` since we fix the tree and branch lengths. Also, alignments 2
and 3 have practically identical trees after the SNP-sites correction (`const` trees), the difference in branch lengths
is negligible due to stochastic effects. However the optimal branch lengths are quite distinct under a full optimisation
(`best_length` trees). This is because the Prob(A->N) and Prob(A->A) are not the same, which will affect the estimation
of model parameters and branch lengths.

So it boils down to the amount of gaps and uncertainty in our data set: on one extreme, we can assume that all constant
sites which were removed were *bona fide* ACGT only; on the other hand, removal of "constant" sites may lump into the
same category truly invariant sites with regions of high uncertainty. In the former case, we don't need to remove them
since most software (BEAST, IQTREE, RaxML) can easily merge constant sites into a few patterns with no detriment of
speed. In the latter case, the patterns of gaps and ambiguous bases within an alignment column can inform the model and
branch lengths and thus should not be removed. (Notice that in this case the speed will suffer more since every pattern
of Ns and indels must be calculated separately).

Thus if you use `snp-sites` to remove constant sites and you observe a fantastic speedup, you should worry that it
removed more than truly constant sites. Because, as we saw above, it does not consider gaps and Ns. To recap:

```bash
Alignment A with truly, bona fide constant sites:
>seq1 N-AC
>seq2 N-AC
>seq3 --AC
>seq4 --AC
>seq5 --AC

Alignment B with no true constant sites: they look constant (no SNPs!) but have distinct phylogenetic signal:
>seq1 AAAA----
>seq2 N-A---AA
>seq3 --AA---A
>seq4 --A-A---
>seq5 ----AA--
```

The sites from alignment B represent each a distinct pattern, and are not merged by the phylogenetic software. They contain
unique phylogenetic information.
However they would all be excluded from a SNPs-only alignment, leading to a speed up.

## What to do then?

So maybe your data set has more gaps and uncertainty than you would hope. Most real data sets look much more like
alignment B than alignment A.
What I usually do is to first estimate the tree with SNPs only, and then use this tree as an initial (or fixed) topology
for the whole data set, where branch lengths and model parameters can be optimised.
This is because the SNPs are good enough for estimating the topology &mdash;tree branching, without branch lengths&mdash; , which is
the most time-consuming part.

I also avoid at all costs using the standard generation of parsimony trees in IQTREE, since it does not use the site
patterns ([https://groups.google.com/g/iqtree/c/vjyLDpc1e1Q/m/68svHwSMAQAJ](https://groups.google.com/g/iqtree/c/vjyLDpc1e1Q/m/68svHwSMAQAJ))
and can be extremely slow.
Another approach might be to remove sites which look constant (i.e. no SNPs) and with high levels of uncertainty/gaps.
This could help cases where the tree inference is slow even under a fixed topology.


All files and script used are available [as an XZ compressed tar file](20220816.blogentry.txz).
