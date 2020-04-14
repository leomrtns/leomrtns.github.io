---
title: "ultrametric trees and the molecular clock"
date: 2020-03-05
categories:
  - Phylogenetics
---

##  Molecular clock

Usually when we talk about molecular clocks, e.g. "this gene follows a clock", we are actually
talking about a **strict** molecular clock, where the number of substitutions (branch lengths on the
tree) are proportional to time with negligible error.

Otherwise, to disentangle the relation between the substitution rate and time (in years, let's say)
we need to model how time and substitution rate are related, through a "relaxed" molecular clock.
The unit of a branch length estimated by phylogenetic methods is in number of substitutions per site 
(and this tree is usually unrooted). 
However, some methods can use extra information or make extra assumptions and return a **dated**
tree, that is, one where the branch lengths are in units of years, Mya (million years ago), or some
other epoch measure. 

## Ultrametric trees
Ultrametric trees is one where the patristic distances between every three leaves follow the ultrametric property. 
I.e. the sum is replaced by a MAX() in the usual properties of a metric.
In practice it means that (1) the tree is rooted, and (2) all leaves look "aligned".

## Clock and ultrametric trees
Wikipedia seems to conflate the two (I fixed where I could, by the way), which means this confusion
is or will be quite common. 



## Consequences
If all the above is still too technical (and there are exceptions or nuances that I haven't
mentioned), some take home messages:
1. Even if you have an ultrametric tree (from e.g. UPGMA) using extant sequences (i.e. sequenced
   today or for all effects from the present), you still have the branch lengths in substitutions
   per site. You need the "clock rate" to convert from substitutions per site to days (or years, or Mya...).
2. I've been mentioning "substitutions" and not "mutations" because the former is the fraction of
   the later that were maintained in the next generation. The number or frequency of mutations may
   be much higher (physical errors in replication) but we don't care about them usually. When
   working with amino acids we may talk about "replacements" instead of "substitutions". 
3. If we observe a rooted, ultrametric-looking tree, we we can safely *infer* that the
   molecular clock holds (see, even I am automatically assuming the sequences are all
   contemporary!). On the other hand, if we only have an unrooted tree (and usually that's what we
   have), and we *assume* that the (strict) molecular clock holds, then we can try to find the root
   location that makes the tree looks as ultrametric as possible. That's what root finding
   algorithms do (midpoint rooting, or MAD)
