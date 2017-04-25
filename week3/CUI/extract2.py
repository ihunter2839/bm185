import sys
import string 

#Table containing the gene annotations in a tab-separated file
table = open("ProteinTable167_161521.txt")
#Genome for use when accessing sequences based on start/end from table
genFile = open("GCF_000005845.2_ASM584v2_genomic.fna")
#Output file
res = open("result2_1.txt", "w")
genome = ""
#Read the genome into a string without newlines
genFile.readline()
cur = genFile.readline()
while cur != "":
	genome = genome + cur[:-1]
	cur = genFile.readline()
	

#skip header
curTabLine = table.readline()
curTabLine = table.readline()
#while there are still genes in the table 
while curTabLine != "":
	#split the line around the tab separated values
	curSplit = curTabLine.split('\t')
	#Grab the individual values needed
	start = int(curSplit[2])
	end = int(curSplit[3])
	pol = curSplit[4]
	outString =  curSplit[7]
	res.write(outString + '\t')
	#If the gene is on the forward strand, use the 
	#reference sequence as is
	if pol == "+":
		gene = genome[start-1:end]
		res.write(gene + '\n')
	#otherwise, generate the complement
	else:
		geneComp = genome[start-1: end]
		#some fancy translation method with rather strange parameters
		#intab = characters located in current string
		intab = "ATCGatcgN"
		#outtab = for each index i in intab, substitute with index i from outtab
		outtab = "TAGCtagcN"
		#create the translation object
		trantab = string.maketrans(intab, outtab)
		gene = geneComp.translate(trantab)
		#reverse the complement
		gene = gene[::-1]
		res.write(gene + '\n')
	curTabLine = table.readline()
