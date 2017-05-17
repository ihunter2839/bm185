import sys
from Bio import SwissProt
import re
import os

downloadCommand = "wget -nc ftp://ftp.uniprot.org/pub/databases/uniprot/"
downloadCommand += "current_release/knowledgebase/taxonomic_divisions/uniprot_sprot_archaea.dat.gz"
os.system(downloadCommand)
os.system("gunzip uniprot_sprot_archaea.dat.gz")

infile = open("uniprot_sprot_archaea.dat")
outfile = open("ex4.txt", "w")

for record in SwissProt.parse(infile):
	outstring = str(record.taxonomy_id) + '\t'
	outstring += str(record.organism) + '\n'
	outfile.write(outstring)
