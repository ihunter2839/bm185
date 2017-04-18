import sys

if __name__ == "__main__":
	infile = open(sys.argv[1])
	outList = []
	curLine = infile.readline().split("\t")
	for i in range(0, 1999):
		curList = []
		curVal = curLine[0]
		nextVal = curVal
		while nextVal == curVal:
			outstr = curLine[3] + " " + curLine[0] + " " + curLine[1]
			curList.append(outstr)
			curLine  = infile.readline().split("\t")
			nextVal = curLine[0]
		curList.sort(reverse=True)
		outList.append(curList)
	for a in outList:
		for b in a:
			tmp = b.split(" ")
			print(tmp[1] + " " + tmp[2] + " " + tmp[0])

			
		
