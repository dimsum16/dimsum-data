Files
-----

- streusle.sst: Initial annotations, in human-readable and JSON formats, along with gold POS tags.
- streusle.tags: Automatic conversion of streusle.sst to the tagging scheme appropriate for training sequence models. A few intricately structured MWEs have been simplified to fit the tagging scheme, and lemmas from the WordNet lemmatizer have been added.
- streusle.tags.sst: Conversion of streusle.tags back to the .sst format, now with lemmas and tags.

# DiMSUM 2016 shared task data

## Files

### `dimsum16.train`, task training data

The training data combines and harmonizes three data-sets, the [STREUSLE 2.1](http://www.cs.cmu.edu/~ark/LexSem/) corpus of web reviews, as well as the Ritter and Lowlands [Twitter datasets](https://github.com/coastalcph/supersense-data-twitter).

In this initial release of the training data, a few differences between the component datasets remain:

- Gappy MWEs are not annotated in the Twitter datasets.
- The Twitter datasets replace usernames, hashtags, urls, and numbers by special symbols, while the original text is always preserved in the STREUSLE part. 

All sentences in the training data are marked with an identifier whose prefix indicate the source dataset. 

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
