# DiMSUM 2016 shared task data

September 25, 2015  
Anders Johannsen  
Nathan Schneider

## Files

### `dimsum16.train`, task training data

__The training data combines and harmonizes three data-sets, the [STREUSLE 2.1](http://www.cs.cmu.edu/~ark/LexSem/) corpus of web reviews, as well as the Ritter and Lowlands [Twitter datasets](https://github.com/coastalcph/supersense-data-twitter).__ This harmonization consisted of: updating the POS tags to use the 17 [Universal POS categories](http://universaldependencies.github.io/docs/en/pos/all.html); naming supersenses in the form `n.person`; removing STREUSLE class labels that are not proper supersenses (such as <code>\`a</code> = auxiliary, <code>\`p</code> = preposition, `??` = unintelligible); removing weak MWE links in the STREUSLE data; separating the MWE position and supersense into different fields; and listing the supersense only for the first token of any expression.

In this initial release of the training data, a few differences between the component datasets remain:

- MWE annotation is less comprehensive in the Twitter datasets: in particular, all MWEs are supersense-tagged noun or verb expressions, and none of the MWEs contain gaps. 
  * We may release an updated version of the training data that makes the MWE annotations in the Twitter data more consistent with the STREUSLE data.
  * MWE annotations in the test set will be comprehensive, similar to the STREUSLE data.
- The Twitter datasets replace usernames, hashtags, URLs, and numbers by special symbols, while the original text is always preserved in the STREUSLE part. 
- The Universal POS tags in the Twitter datasets do not use the new subordinating conjunction category `SCONJ`. Subordinating conjunctions are instead labeled as adpositions (`ADP`) or conjunctions (`CONJ`).


## File format

The DiMSUM files have tab-separated columns in the spirit of CoNLL, with blank lines to separate sentences.

Nine tab-separated columns:

1. token offset
2. word
3. lowercase lemma
4. POS
5. MWE tag
6. offset of parent token (i.e. previous token in the same MWE), if applicable
7. strength level encoded in the tag, if applicable. Currently not used
8. supersense label, if applicable
9. sentence ID

Fields 5, 6, and 8 need to be predicted at test time; the rest will be present in the input. Field 6 can be deterministically filled in given the tagging in field 5. Field 7 should be left blank. The file [TAGSET.md](TAGSET.md) describes the MWE and supersense tagsets.

All sentences in the training data are marked with an identifier whose prefix indicate the source dataset (field 9). In the test data, this field will contain a unique ID for the sentence, but the ID will be uninformative: it will not reveal the domain or document position of the sentence.