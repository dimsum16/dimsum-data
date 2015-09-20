import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="""
Converts the three-column supersense-tagged datasets into the DIMSUM 
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
		if token['bio'] == "B":
			if i < (len(sent) - 2) and sent[i + 1]['bio'] == "I":
				token['mwe'] = "B"
				token['mwe_strength'] = ''
			else:
				token['mwe'] = "O"
		elif token['bio'] == "I":
			# token['mwe'] = sent[i - 1]['mwe'].replace("B-", "I-")
			token['mwe'] = "I"
			token['supersense'] = ''
			token['mwe_strength'] = ''
			token['mwe_offset'] = i

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
		token['lemma'] = parts[0].lower()
		token['pos'] = parts[1]
		token['bio'] = parts[2][0] if len(parts[2]) else "O"
		token['supersense'] = standardize_supersense(parts[2])
		token['sentence_id'] = "{}-{}".format(args.name, sentence_id)
		token['mwe'] = "O"

		sent.append(token)

if sent:
	add_mwe(sent)
	output_sent(sent)

