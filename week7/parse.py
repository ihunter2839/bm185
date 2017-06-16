#python parser.py genomesToParse.txt
import re
import sys
from Bio import SeqIO as sIO

#file containing paths to genbank files to parse
genToParse = open(sys.argv[1])

#Output files to be used to create the genomes, replicons,
#and genes tables
genomeOut = open("genomes.txt", "w")
repliconOut = open("replicons.txt", "w")
geneOut = open("genes2.txt", "w")
exonOut = open("exons.txt", "w")

#global counters to be used for
#genome_id
#replicon_id
#gene_id
genome_count_global = 0
replicon_count_global = 0
gene_count_global = 0
exon_count_global = 0

#list of values needed for genomes table
#also need (from local counters) 
#num_replicons
#num_genes
genomeFields = ["genome_id", "name", "tax_id", "domain", "num_replicons"]
genomeFields += ["num_genes", "size_bp", "assembly"]

#list of values needed for replicons table
#also need (from local counters)
#num_genes
repliconFields = ["replicon_id", "genome_id", "name", "type", "shape", "num_genes"]
repliconFields += ["size_bp", "accession", "release_date"]

#list of values needed for genes table
geneFields = ["gene_id", "genome_id", "replicon_id", "locus_tag", "protein_id", "name", "strand"]
geneFields += ["num_exons", "left_pos", "right_pos", "length", "product"]

exonFields = ["gene_id", "exon_id", "left_pos", "right_pos", "length"]

for genome in genToParse:
	#local counters for the 
	#num_replicons and
	#num_genes fields
	replicon_count_genome = 0
	gene_count_genome = 0
	genome_size = 0

	#counter for the record number
	#first record is the genome information
	record_count = 0

	print(genome)

	#dictionary to hold values for output 
	genomeData = {}
	genomeData["genome_id"] = str(genome_count_global)

	#iterate through records in the file genome
	#it is assumed there is a newline at the end of 
	#the genome path string

	#big ass list to hold all genes for sorting before
	#output to file
	geneList = []
	#same for exons
	exonList_2 = []
	
	for record in sIO.parse(genome[:-1], "genbank"):

		#count genes in current replicon
		#subtract 1 to account for source feature
		gene_count_replicon = 0
		replicon_size = 0

		#dictionary to hold values for output
		repliconData = {}
		repliconData["replicon_id"] = str(replicon_count_global)
		repliconData["genome_id"] = str(genome_count_global)
		repliconData["shape"] = record.annotations["topology"]
		#check if the description contains the word plasmid
		#Assumes that all plamids will be labeled 
		if "plasmid" in record.description.lower():
			repliconData["type"] = "plasmid"
		else:
			repliconData["type"] = "chromosome"
		#remove the version number from the accession
		repliconData["accession"] = record.id.split(".")[0]
		repliconData["release_date"] = record.annotations["date"]

		#if first record, record source information
		if replicon_count_genome == 0:
			assemMatch = re.search("GCF_[0-9]+", record.dbxrefs[2])
			genomeData["assembly"] = assemMatch.group(0)
			taxonomyList = record.annotations["taxonomy"]
			genomeData["domain"] = taxonomyList[0].lower()
		
		#iterate through the features list
		i = 0
		while i < len(record.features):
			feat = record.features[i]
			#first feature is source
			if i == 0:
				#if i == 0, the current feature is the source 
				if replicon_count_genome == 0:
					#data for the genome
					taxString = feat.qualifiers["db_xref"][0]
					taxMatch = re.search("taxon:([0-9]+)", taxString )
					genomeData["tax_id"] = taxMatch.group(1)
					genomeData["name"] = feat.qualifiers["organism"][0]
				#get info for replicon
				repliconData["name"] = feat.qualifiers["organism"][0]
				sizeRE = "\[([0-9]+):([0-9]+)\]"
				sizeMatch = re.search(sizeRE, str(feat.location))
				end = int(sizeMatch.group(2))
				start = int(sizeMatch.group(1))
				rep_size = end - start
				repliconData["size_bp"] = str(rep_size)
				genome_size += rep_size
				i += 1
			else:
				#iterate through features until CDS is located
				while "cds" not in feat.type.lower() and i < len(record.features):
					i += 1
					feat = record.features[i]
				geneData = {}
				geneData["gene_id"] = str(gene_count_global)
				geneData["genome_id"] = str(genome_count_global)
				geneData["replicon_id"] = str(replicon_count_global)
				geneData["locus_tag"] = feat.qualifiers["locus_tag"][0]
				try:
					#remove version number from accession
					splitString = feat.qualifiers["protein_id"][0].split(".")
					geneData["protein_id"] = splitString[0]
				except KeyError:
					geneData["protein_id"] = "unavailable"
				
				#some CDS do not have names. Replace with locus tag
				try:
					geneData["name"] = feat.qualifiers["gene"][0]
				except KeyError:
					geneData["name"] = geneData["locus_tag"]

				#some CDS do not have product description.
				#replace with "unavailable"
				try:
					geneData["product"] = feat.qualifiers["product"][0]
				except KeyError:
					geneData["product"] = "unavailable"

				if "-" in str(feat.location):
					geneData["strand"] = "-"
				else:
					geneData["strand"] = "+"
				
				geneData["left_pos"] = str(feat.location.start)
				geneData["right_pos"] = str(feat.location.end)

				locString = str(feat.location)
				#find all splice positions
				exonPos = [int(hit) for hit in re.findall("[0-9]+", locString)]
				geneLen = max(exonPos) - min(exonPos)
				geneData["length"] = str(geneLen)
				replicon_size += geneLen
				exonList = re.findall("[0-9]+\:[0-9]+", locString)
				geneData["num_exons"] = str(len(exonList))
				
				#write to file
				#out = '\t'.join(geneFields) + '\n'
				#out = ""
				#for field in geneFields:
				#	out += geneData[field] + '\t'
				#geneOut.write(out[:-1]+ '\n')
				geneList.append(geneData)

				for exon in exonList:
					exonData = ""
					exonData = {}
					exonData["gene_id"] = str(gene_count_global)
					exonData["exon_id"] = str(exon_count_global)
					pos = exon.split(":")
					exonData["left_pos"] = pos[0]
					exonData["right_pos"] = pos[1]
					exonData["length"] = str(int(pos[1]) - int(pos[0]))
					exon_count_global += 1
					#exonOut.write(exonData + '\n')
					exonList_2.append(exonData)

				gene_count_replicon += 1
				gene_count_global += 1
				i += 1

		repliconData["num_genes"] = str(gene_count_replicon)
		repliconData["size_bp"] = str(replicon_size)
		#out = '\t'.join(repliconFields) + '\n'
		#out = ""
		#for field in repliconFields:
		#	out += repliconData[field] + '\t'
		#repliconOut.write(out[:-1] + '\n')

		genome_size += replicon_size
		gene_count_genome += gene_count_replicon
		replicon_count_genome += 1
		replicon_count_global += 1


	genomeData["size_bp"] = str(genome_size)
	genomeData["num_replicons"] = str(replicon_count_genome)
	genomeData["num_genes"] = str(gene_count_genome)
	#out = '\t'.join(genomeFields) + '\n'
	#out = ""
	#for field in genomeFields:
	#	out += genomeData[field] + '\t'
	#genomeOut.write(out[:-1] + '\n')
	
	genome_count_global += 1

	geneList = sorted(geneList, key=lambda x: int(x["left_pos"]))
	exonList_2 = sorted(exonList_2, key=lambda x: int(x["left_pos"]))

	for gene in geneList:
		out = ''
		for field in geneFields:
			out += gene[field] + '\t'
		geneOut.write(out[:-1] +  '\n')
	for exon in exonList_2:
		out = ''
		for field in exonFields:
			out += exon[field] + '\t'
		exonOut.write(out[:-1] + '\n')
	

