import sys
import string 

table = open("ProteinTable167_161521.txt")
genFile = open("GCF_000005845.2_ASM584v2_genomic.fna")
res = open("result2.txt", "w")
genome = ""
genFile.readline()
cur = genFile.readline()
while cur != "":
	genome = genome + cur[:-1]
	cur = genFile.readline()
	

#skip header
curTabLine = table.readline()
curTabLine = table.readline()

while curTabLine != "":
	curSplit = curTabLine.split('\t')
	start = int(curSplit[2])
	end = int(curSplit[3])
	pol = curSplit[4]
	outString =  curSplit[7]
	res.write(outString + '\t')
	if pol == "+":
		gene = genome[start-1:end]
		res.write(gene + '\n')
	else:
		geneComp = genome[start-1: end]
		intab = "ATCGatcgN"
		outtab = "TAGCtagcN"
		trantab = string.maketrans(intab, outtab)
		gene = geneComp.translate(trantab)
		gene = gene[::-1]
		res.write(gene + '\n')
	curTabLine = table.readline()
