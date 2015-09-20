#!/bin/bash
OUT=../dimsum16.train

python sst_to_dimsum.py original/lowlands.UPOS2.tsv lowlands > $OUT
python sst_to_dimsum.py original/ritter.UPOS2.tsv ritter >> $OUT
python streusle_to_dimsum.py original/streusle.upos.tags >> $OUT
