import argparse
from pathlib import Path
from mwe_simplify import simplify

parser = argparse.ArgumentParser(description="""
- Converts names of supersenses in the STREUSLE dataset to match DiMSUM conventions.
- Performs simplification of BIO notation
""")
parser.add_argument('file', help="Original file in TSV format", type=Path)
args = parser.parse_args()

def adjust_supersense(token):
	supersense = token['supersense'] 
	if supersense:
		# Delete supersenses that start with ` or contain question marks
		if supersense.startswith("`") or '?' in supersense:
			token['supersense'] = ""
		elif supersense.isupper(): 
			# NOUN sense
			token['supersense'] = "n." + supersense.lower()
		else:
			token['supersense'] = "v." + supersense.lower()

		token['supersense'] = token['supersense'].replace(" ", "_")


columns = ['token_i', 'word', 'lemma', 'pos', 'mwe', 'mwe_offset', 'mwe_strength', 'supersense', 'sentence_id']
last_supersense = None
sent = []
for line in args.file.open():
	line = line.strip("\n")

	if line == "":
		bios = [token['mwe'][0] for token in sent]
		simplified_bios = simplify(bios, 'weak', policy='all')[0]
		for token, bio in zip(sent, simplified_bios):
			token['mwe'] = bio
			if token['mwe_strength'] == '~':
				token['mwe_offset'] = 0
			token['mwe_strength'] = ''


		for token in sent:
			values = [str(token[key]) for key in columns]
			print("\t".join(values))
		print()
		
		sent.clear()
	else:
		token = {k: v for k,v in zip(columns, line.split("\t"))}
		adjust_supersense(token)
		sent.append(token)
