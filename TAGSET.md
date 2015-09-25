Multiword Expressions
=====================

Multiword Expressions (MWEs) are contiguous or gappy groupings of tokens that function semantically as a lexical unit. 
[STREUSLE MWE Guidelines](https://github.com/nschneid/nanni/wiki/MWE-Annotation-Guidelines) (In this release, unlike STREUSLE, we do not include weak MWEs.)

Token-level MWE-positional flags (5th field of the data) are as follows (with frequency counts):

    64126 O  Not part of or inside any MWE
      590 o  Not part of any MWE, but inside the gap of an MWE
     3850 B  First token of an MWE, not inside a gap
       21 b  First token of an MWE, inside the gap of another MWE
     5211 I  Token continuing an MWE, not inside a gap
       28 i  Token continuing an MWE, inside the gap of another MWE
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

      928 n.act
      123 n.animal
     1289 n.artifact
      299 n.attribute
      136 n.body
      817 n.cognition
     1012 n.communication
      544 n.event
       53 n.feeling
      833 n.food
     1678 n.group
      875 n.location
       33 n.motive
       73 n.natural_object
       20 n.other
     1967 n.person
       44 n.phenomenon
        9 n.plant
      379 n.possession
       31 n.process
      171 n.quantity
       55 n.relation
        9 n.shape
      140 n.state
       60 n.substance
     1319 n.time
    =====
    12897 noun supersense mentions
 
Verb Supersenses
----------------

All of the 15 verb supersenses defined in WordNet are attested in this corpus. 
[STREUSLE verb supersense annotation guidelines](http://www.cs.cmu.edu/~ark/LexSem/vsst-guidelines.html)

      119 v.body
      452 v.change
     1273 v.cognition
     1235 v.communication
       52 v.competition
      116 v.consumption
      118 v.contact
      120 v.creation
      393 v.emotion
      828 v.motion
      244 v.perception
      531 v.possession
     1201 v.social
     3431 v.stative
        2 v.weather
    =====
    10115 verb supersense mentions
