# DiMSUM 2016 shared task data

December 28, 2015

Anders Johannsen  
Nathan Schneider  
Dirk Hovy  
Marine Carpuat

This release contains data and scripts for the [DiMSUM](http://dimsum16.github.io/) shared task at SemEval 2016.

## Data files

### `dimsum16.train`, task training data

__The training data combines and harmonizes three data-sets, the [STREUSLE 2.1](http://www.cs.cmu.edu/~ark/LexSem/) corpus of web reviews, as well as the Ritter and Lowlands [Twitter datasets](https://github.com/coastalcph/supersense-data-twitter). The Ritter and Lowlands datasets have been reannotated for MWEs and supersenses to improve their quality and to more closely follow the conventions used in the STREUSLE annotations.__ Our harmonization also consisted of: updating the POS tags to use the 17 [Universal POS categories](http://universaldependencies.github.io/docs/en/pos/all.html); naming supersenses in the form `n.person`; removing STREUSLE class labels that are not proper supersenses (such as <code>\`a</code> = auxiliary, <code>\`p</code> = preposition, `??` = unintelligible); removing weak MWE links in the STREUSLE data; separating the MWE position and supersense into different fields; and listing the supersense only for the first token of any expression.

In this final release of the training data, a couple differences between the component datasets remain:

- The Lowlands Twitter dataset replace usernames, URLs, and numbers by special symbols, while the original text is always preserved in the other datasets.
- The Universal POS tags in the Twitter datasets do not use the new subordinating conjunction category `SCONJ`. Subordinating conjunctions are instead labeled as adpositions (`ADP`) or conjunctions (`CONJ`).


### `dimsum16.test.blind`, task test input

This is in the same format as the training data, except without MWE and supersense annotations, which are to be predicted by the system:

  - there is no supersense label (column 8 is blank)
  - MWE tags (column 5) are all `O`, and MWE parent offsets (column 6) are all `0`, indicating that no MWEs are marked
  - sentence IDs (column 9) are unanalyzable to obscure the sentence's source dataset and its order relative to other sentences; the sentences in this file are listed in a random order

#### Composition

The test set consists of 16,500 words in 1,000 English sentences. The sentences are drawn from the following sources:

  - online reviews from the TrustPilot corpus ([Hovy et al. 2015](http://www.www2015.it/documents/proceedings/proceedings/p452.pdf))
  - tweets from the Tweebank corpus ([Kong et al. 2014](http://www.aclweb.org/anthology/D14-1108))
  - TED talk transcripts from the IWSLT MT evaluation campaigns, obtained from the WIT³ archive ([Cettolo et al. 2012](http://mt-archive.info/EAMT-2012-Cettolo.pdf)), some of which were used for the NAIST-NTT TED Talk Treebank ([Neubig et al. 2014](http://www.mt-archive.info/10/IWSLT-2014-Neubig.pdf))

More precise information on the composition and preparation of the test corpus will be announced after the end of the task evaluation period.

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
