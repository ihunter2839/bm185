import sys

infile = open("result2.txt")
outfile = open("frequencies.txt", "w")

#generate a list of codons with stop codons at the end
bases = ['A', 'C', 'G', 'T']
codonList = [a + b + c for a in bases for b in bases for c in bases]
codonList.remove('TAA')
codonList.remove('TAG')
codonList.remove('TGA')
codonList.append('TAA')
codonList.append('TGA')
codonList.append('TAG')

#create header for file 
header = "Gene	"
for c in codonList:
	header += c + '\t'
header += "Total"
outfile.write(header + '\n')

#global count array
globCount = [0] * 64
globCodons = 0

curGene = infile.readline()
while curGene != "":
	#get the identifier and gene sequence
	line = curGene.split('\t')
	iden = line[0]
	gene = line[1][:-1]
	locCount = [0] * 64
	locCodons = 0
	#check that gene sequence is of a proper length
	if len(gene) % 3 != 0:
		outfile.write(iden + " length is not a multiple of 3" + '\n')
	#otherwise, gene is valid and codons can be scanned
	else:
		i = 0
		while i < len(gene):
			#grab codon
			cod = gene[i:i+3]
			#get the relative position of the codon in the table
			codInd = codonList.index(cod)
			#increment the count of the codon in the current gene
			locCount[codInd] += 1
			locCodons += 1
			#move to next codon
			i += 3
		#create string representing row in table
		outString = iden + '\t'
		for i in range(0, len(locCount)):
			#update the global counts
			globCount[i] += locCount[i]
			outString += str(locCount[i]) + '\t'
		outString += str(locCodons)
		#update global number of codons
		globCodons += locCodons
		outfile.write(outString + '\n')
	curGene = infile.readline()
outString = "TOTALS" + '\t'
#print global totals. This would more ideally be located at the start of the file to allow
#easy access to the global information for calculation of CUI
for c in globCount:
	outString += str(c) + '\t'
outString += str(globCodons)
outfile.write(outString)
	

		 	
