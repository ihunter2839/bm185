import sys

infile = open(sys.argv[1])

header = infile.readline()
curLine = infile.readline()[:-1]
total = 0
gc = 0

while curLine != "":
	for s in curLine:
		if s == "C" or s == "G":
			gc += 1
		total += 1
	curLine = infile.readline()[:-1]
print(float(gc)/total)
