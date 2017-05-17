import sys
import os
import re

os.system("wget -P -nc dataFiles ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/README")

#open the file
infile = open("./dataFiles/README").read()
outfile = open("uniprotRes2.txt", "w")

ids = re.findall("UP[0-9]+", infile)
for s in ids:
	outfile.write(s + '\n')

for i in range(10, 14):
	command = "wget -P " + ids[i] + " ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Bacteria/" + ids[i] + "*"
	os.system(command)

