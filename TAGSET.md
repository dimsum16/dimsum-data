This document describes the labels used to annotate the DiMSUM data,
including counts for the training data in the 1.5 release.

Multiword Expressions
=====================

Multiword Expressions (MWEs) are contiguous or gappy groupings of tokens that function semantically as a lexical unit.
[STREUSLE MWE Guidelines](https://github.com/nschneid/nanni/wiki/MWE-Annotation-Guidelines) (In this release, unlike STREUSLE, we do not include weak MWEs.)

Token-level MWE-positional flags (5th field of the data) are as follows (with frequency counts):

    63264 O  Not part of or inside any MWE
      675 o  Not part of any MWE, but inside the gap of an MWE
     4208 B  First token of an MWE, not inside a gap
       24 b  First token of an MWE, inside the gap of another MWE
     5623 I  Token continuing an MWE, not inside a gap
       32 i  Token continuing an MWE, inside the gap of another MWE
    =====
    73826 tokens

Class Labels
============

Many of the lexical expressions (single-word and multiword) in the corpus
have been manually annotated with semantic classes called supersenses. There are 41 unique class labels. They are listed below with their token frequencies.

These supersenses appear in the 8th field of the data. For MWEs, they are only listed with the first (`B` or `b`) token, but should be interpreted as applying to the entire expression.

Noun Supersenses
----------------

All of the 26 noun supersenses defined in WordNet are attested, including a miscelleneous supersense that we call `n.other` (traditionally, `noun.Tops`), which applies to vague words like "stuff".
STREUSLE [guidelines](http://www.cs.cmu.edu/~ark/ArabicSST/corpus/guidelines.html),
[examples](http://www.cs.cmu.edu/~ark/ArabicSST/corpus/examples.html) for noun supersense annotation.

      902 n.act
      122 n.animal
     1226 n.artifact
      311 n.attribute
      153 n.body
      835 n.cognition
      886 n.communication
      650 n.event
       68 n.feeling
      830 n.food
     1750 n.group
      845 n.location
       35 n.motive
       62 n.natural_object
       23 n.other
     1867 n.person
       46 n.phenomenon
       10 n.plant
      386 n.possession
       29 n.process
      161 n.quantity
       40 n.relation
        7 n.shape
      122 n.state
       52 n.substance
     1173 n.time
    =====
    12591 noun supersense mentions

Verb Supersenses
----------------

All of the 15 verb supersenses defined in WordNet are attested in this corpus.
[STREUSLE verb supersense annotation guidelines](http://www.cs.cmu.edu/~ark/LexSem/vsst-guidelines.html)

      153 v.body
      539 v.change
     1310 v.cognition
     1225 v.communication
       51 v.competition
      114 v.consumption
      104 v.contact
      117 v.creation
      414 v.emotion
      765 v.motion
      241 v.perception
      398 v.possession
     1073 v.social
     3357 v.stative
        2 v.weather
    =====
     9863 verb supersense mentions
