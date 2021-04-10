
---
title: "short rants"
date: 2020-03-05
categories:
  - Misc
---

The episode of [Feynman vs. The Abacus](https://www.ee.ryerson.ca/~elf/abacus/feynman.html) shows that you can go along
way even without a deep understanding of the problem you are solving.
In this story from when Feynman visited Brazil, he competes with an abacus salesman who is very quick with simple artihmetics, 
but slower than Feynman with more complex operations like cubic root.
Feynman then realises that the salesman doesn't have a good grasp of mathematics or interest in approximation approaches, he
only knows how to move the beads mechanically.


It is natural to learn new concepts in a lecture, since they are usually tightened to cool results. 
There is however an expectation that we will investigate and read further afterwards. 
But I guess modern life forces us many times to limit our knowledge about the concept to said lecture, or to similarly
introductory texts.
And as we watch more and more lectures, read more and more introductions, we have the illusion of becoming very familiar 
with the concept when we are in fact proficient only with the one-liner description.
This is what I call "shallow" knowledge, when we are confident in knowing something (a concept, a term, a technique, a
pipeline, a definition) but without having in fact 
We are experts in eleveator pitches. 

As one example I think by now we are all experts in machine 
learning or AI, in that we can all give a one-hour introductory lecture on the subject. And in our minds, if a real
machine learning problems falls into our laps we are confident we can solve it after a few hour searching for the right
tools . In reality, however, "machine learning" as a term has the same breadth as "statistics", and even after many
introductory classes on Stats we know that to actually produce publication-ready results is no trivial task.

During the pandemics we all became familiar with another, extreme form of shallow knowledge: by repeating and reverberating simple terms and 
messages as "herd immunity", HQC and other quack treatments, many people became confident to discuss with and even
dismiss arguments by real experts. 
This example is closer to politics, where disinformation tactics are used, but we are not immune to it in academia,
where a simple message spreads faster than a complex one (even when the simpler message is wrong). 

There is a large gradient between "shallow" knowledge and "deep" knowledge, where we all fall somewhere in between for
every aspects of our fields. 
I focus mainly on the shallow extreme, following the Anna Karenina principle.


In short, we are increasingly using the wrong terminology and expandind methodologies when they are not appropriate.
And we are losing the capacity of fighting back, and of determining who to listen to and to read (a few expert,
hard-to-read papers or [masses of articles in simple English](https://royalsocietypublishing.org/doi/10.1098/rspb.2020.2581)?)

###

misnomers

There is a specific form of shallow knowledge which is very dear to me, that happens when terms start being used in a
new context, usually with conflicting meanings.
This can be due to a "founder effect" where a highly-cited paper or group use it, and in a quickly expanding field where a
term starts boucing around without a proper definition.
In both cases the term becomes popular, a standard, but conflicts with the original definition to the point of rendering
it useless.

if you are from the field, you know the implications of misusing a word. However if you are not actually familiar with
the term, you can change its meaning without feeling the consequences. E.g. "clade" in sars-cov-2: you don't care that
saying "clade B is not clade A" will make it harder for students to grasp the term.
A [recent tweet](https://twitter.com/leomrtns/status/1369437415388102663) made me think about this again. 


Btw you don't need to be from the field to car about the proper terms. In fact that is the reason why we have to respect
definitions: I don't need to be a graph theorist to know that a De Bruijn graph has edges between all neighbours, but if
I ever need to learn about it (to e.g. [find the most compact representation of all n-strings in an
alphabet a.k.a. a superstring](https://en.wikipedia.org/wiki/De_Bruijn_sequence)) or if I am reading a specialised article,
it will be much easier.
On the other hand if read an article that assumes a non-standard, conflicting definition it may be more difficult to learn from it (doing
the opposite of what an article should be about)

As a curiosity, when I [asked about it on a forum](https://bioinformatics.stackexchange.com/questions/146/how-to-make-a-distinction-between-the-classical-de-bruijn-graph-and-the-one-de)
people were up in arms against my ignorance, at the same time that they had to use a term to tell them apart (as I was
asking?)
BTW the tacit answer was "assembly DBG", as [commented later](https://lh3.github.io/2017/11/15/on-assembly-de-bruijn-graphs).
Maybe this is due to a lack of formal training in Computer Science, where they cannot take apart a data structure
(abstract concept) from its implementation?

###

Recently another aspect of shallow knowledge is when you review a paper: if you've heard of many packages and many fancy
method names, you may start sprinkling these terms into a revision, and asking for what ultimately are innapropriate methods.
And frankly, some things are so obvious that are not spelled out in any paper, not in a way consumable by the reviewer
without a deeper knowledge of the tools and methodologies. 

One example would be a reviewer failing to see that you cannot, in general, compare phylogenetic likelihoods between distinct alignments.
This is obvious if you have statistical phylogenetics training: each alignment column is a sample, an outcome of the
evolutionary process, and therefore a distinct alignemt is equivalent to a disctint data set (except of course for
models accounting for it).
Still it may be hard to convince them, since there are not many papers explicitly saying this. 



###
