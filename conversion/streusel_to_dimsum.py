import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="""
Converts names of supersenses in the Streusel dataset to match DIMSUM conventions.
""")
parser.add_argument('file', help="Original file in TSV format", type=Path)
args = parser.parse_args()


columns = ['token_i', 'word', 'lemma', 'pos', 'mwe', 'mwe_offset', 'mwe_strength', 'supersense', 'sentence_id']
for line in args.file.open():
	line = line.strip("\n")

	if line == "":
		print()
	else:
		token = {k: v for k,v in zip(columns, line.split("\t"))}

		supersense = token['supersense'] 
		bio = token['mwe'][:1].upper() or "O"
		if supersense:
			# Delete supersense that start with `
			if supersense.startswith("`") or '?' in supersense:
				token['supersense'] = ""
			elif supersense.isupper(): 
				# NOUN sense
				token['supersense'] = "n." + supersense.lower()
			else:
				token['supersense'] = "v." + supersense.lower()

			token['supersense'] = token['supersense'].replace(" ", "_")

		if token['supersense']:
			token['mwe'] = bio + "-" + token['supersense']
		else:
			token['mwe'] = bio

		values = [token[key] for key in columns]
		print("\t".join(values))
