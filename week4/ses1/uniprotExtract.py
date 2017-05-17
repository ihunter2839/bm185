import sys
import os

os.system("wget -P dataFiles ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/README")

#open the file
infile = open("./dataFiles/README")
outfile = open("uniprotRes.txt", "w")

#skip the header
headLine = infile.readline()
headSplit = headLine.split(' ')
while headSplit[0] != "Proteome_ID":
	headLine = infile.readline()
	headSplit = headLine.split(' ')

#head line is now the column values
curLine = infile.readline()
count = 0
while curLine != "":
	curSplit = curLine.split(' ')
	outfile.write(curSplit[0] + '\n')
	if count < 4:
		command = "wget -P " + curSplit[0] + "  ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Bacteria/" + curSplit[0] + "*"
		os.system(command)
		count += 1
	curLine = infile.readline() 
