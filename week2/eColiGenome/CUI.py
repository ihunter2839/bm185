import sys

infile = open("frequencies.txt")
outfile = open("cuiData.txt", "w" )
globalInfo = open("globalData.txt")

tots = globalInfo.readline()[:-1].split('\t')
#total number of codons in the genome
totCodons = int(tots[len(tots)-1])

infile.readline()
curGene = infile.readline()[:-1].split('\t')
while curGene[0] != "TOTALS":
	iden = curGene[0]
	if len(curGene) < len(tots):
		outfile.write(iden + '\n')
	#total number of codons in current gene
	else:
		curNumCodons = int(curGene[len(curGene)-1])
		curCUI = 0
		for i in range(1, len(curGene)-1):
			globFreq = float(tots[i]) / totCodons
			curFreq = float(curGene[i]) / curNumCodons
			curTerm = globFreq * curFreq
			curCUI += curTerm
		outfile.write(iden + '\t' + str(curCUI) + '\n')
	curGene = infile.readline()[:-1].split('\t')	

		
