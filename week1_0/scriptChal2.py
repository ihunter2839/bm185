import sys
import re

infile = open("RS.txt")
protPairs = {}
protProb = {}
numInter = {}
curLine = infile.readline()
cur = curLine.split('\t')

while curLine != "":
	if len(protPairs) <= 2000:
		if cur[0] in protPairs:
			if cur[3] > protProb[cur[0]]:
				protPairs[cur[0]] = cur[1]
				protProb[cur[0]] = cur[3]
		else:
			protPairs[cur[0]] = cur[1]
			protProb[cur[0]] = cur[3]
			numInter[cur[0]] = 0
	if cur[0] in protPairs:
		numInter[cur[0]] = numInter[cur[0]] + 1
	curLine = infile.readline()
	cur = curLine.split('\t')
for p1, p2 in protPairs.items():
	print(p1 + '\t' + p2 + '\t' + str(protProb[p1]) + '\t' + str(numInter[p1]))

