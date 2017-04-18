import sys
import re

infile = open("TCDB.faa")
cur = infile.readline()
while cur != "":
	col2 = re.search("\|([0-9]|[A-Z]|[a-z]|\.|\s|\_)*?\|", cur)
	col1 = re.search("\|([0-9]|[A-Z]|\.)*?\s", cur)
	cur = infile.readline()
	seq = ""
	while cur != "" and cur[0] != ">":
		seq = seq + cur
		if seq[-1] == '\n':
			seq = seq[:-1]
		cur = infile.readline()
	print(col1.group(0)[1:-1] + "-" + col2.group(0)[1:-1] + " " + seq)


