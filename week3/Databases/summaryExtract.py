import sys

#pass in the summary file as the first argument
table = open(sys.argv[1])

#skip the opening line
table.readline()
#file to write the output
outfile = open("summaryResult.txt", "w")
#Read in header, remove the newline
#split the columns into a list

#need to extract
#name
#tax_id
#ftp_path
cols = table.readline()[:-1].split('\t')
namePos = cols.index("organism_name")
taxPos = cols.index("taxid")
urlPos = cols.index("ftp_path")

curLine = table.readline()[:-1]

while curLine != "":
	curSplit = curLine.split('\t')
	outstring = str(curSplit[namePos]) + '\t' + str(curSplit[taxPos])
	outstring += '\t' + str(curSplit[urlPos]) + '\n'
	outfile.write(outstring)
	curLine = table.readline()[:-1]


