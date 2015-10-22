import argparse
from pathlib import Path
from nltk.corpus import wordnet as wn

parser = argparse.ArgumentParser(description="""
Converts the three-column supersense-tagged datasets into the DiMSUM 
shared-task format

""")
parser.add_argument('file', help="Original file in TSV format", type=Path)
parser.add_argument('name', help="Dataset name")
args = parser.parse_args()


def standardize_supersense(supersense):
    supersense = supersense[2:].replace("noun.", "n.") \
        .replace("verb.", "v.") \
        .replace("object", "natural_object") \
        .replace("Tops", "other")

    return supersense


def add_mwe(sent):
    for i in range(len(sent)):
        token = sent[i]
        token['mwe_strength'] = ''
        token['mwe'] = 'O'
        token['mwe_offset'] = 0

        if token['bio'] == 'B':
            next_none_o_tags = [sent[j]['bio'] for j in range(i + 1, len(sent))
                                if sent[j]['bio'] != 'O']
            #print(token)
            #print(next_none_o_tags)
            if next_none_o_tags and next_none_o_tags[0] == 'I':
                token['mwe'] = 'B'

        elif token['bio'] == 'I':
            token['mwe'] = 'I'
            token['supersense'] = ''
            for j in reversed(range(0, i)):
                # Token ids in the dimsum file format are 1-based, while
                # they are 0-based in this loop
                if sent[j]['mwe'] in ('B', 'I'):
                    token['mwe_offset'] = j + 1
                    break
                elif sent[j]['mwe'] == 'O':
                    # The gappy version of 'O'
                    sent[j]['mwe'] = 'o'

        assert 'mwe_offset' in token, "Token '%s' in\t%s" % (token, sent)


def output_sent(sent):
    # TAGS format
    #
    # 1. token offset
    # 2. word
    # 3. lowercase lemma
    # 4. POS
    # 5. full MWE+class tag
    # 6. offset of parent token (i.e. previous token in the same MWE), if applicable
    # 7. strength level encoded in the tag, if applicable: `_` for strong, `~` for weak
    # 8. class (usually supersense) label, if applicable
    # 9. sentence ID
    columns = ['token_i', 'word', 'lemma', 'pos', 'mwe', 'mwe_offset', 'mwe_strength', 'supersense', 'sentence_id']
    for token_i, token in enumerate(sent, 1):
        token['token_i'] = token_i
        values = [str(token.get(key, "")) for key in columns]
        print("\t".join(values))
    print()


sent = []
sentence_id = 1
for line in args.file.open():
    line = line.strip("\n")
    token = {}

    if line == "":
        add_mwe(sent)
        output_sent(sent)
        sentence_id += 1
        sent.clear()
    else:
        parts = line.split("\t")
        token['word'] = parts[0]
        lemma = ''

        if parts[0] in ['URL', 'NUMBER', '@USER']:
            lemma = parts[0]

        elif parts[1] in ['NOUN', 'VERB', 'ADJ', 'AUX']:
            wn_pos = 'v' if parts[1] == 'AUX' else parts[1][0].lower()
            lemma = wn.morphy(parts[0].lower(), wn_pos)

        if not lemma:
            lemma = parts[0].lower()

        token['lemma'] = lemma
        token['pos'] = parts[1]
        token['bio'] = parts[2][0] if len(parts[2]) else "O"
        token['supersense'] = standardize_supersense(parts[2])
        token['sentence_id'] = "{}-{}".format(args.name, sentence_id)
        token['mwe'] = "O"

        sent.append(token)

if sent:
    add_mwe(sent)
    output_sent(sent)

