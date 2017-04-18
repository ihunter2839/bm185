import os

baseDir = "./dirtree"

outfile = open("pythonOutput", "w")

dirList = os.listdir(baseDir)

for dirs in dirList:
	subDirList = os.listdir(baseDir + "/" + dirs)
	for f in subDirList:
		infile = open(baseDir + "/" + dirs + "/" + f + "/" + "report.tbl")
		line = infile.readline()
		line = infile.readline()
		lineSplit = infile.readline().split('\t')
		outfile.write(dirs + " " + lineSplit[3] + '\n')
os.system("sort -k2 -k1 -r pythonOutput >> whatTheHell.txt")
