import sys

infile = open(sys.argv[1])

#skip the header section
#all header comments being with #
curLine = infile.readline()
while curLine[0] == "#":
	curLine = infile.readline()

#columns
#regulon_id name bnumber left_pos right_pos strand product_name support PMID confidence
pos_list = [1, 2, 3, 4, 5, 9]

outfile = open("regulon_gene.txt", "w")
#list to hold data to be sorted before output
#sort genes according to their leftmost position
out_list = []

#parse the file
while curLine != "":
	data_list = curLine[:-1].split('\t')
	out = []
	for pos in pos_list:
		out.append(data_list[pos])
	#skip genes that lack left and right info
	if "" not in out[1:5]:
		out_list.append(out)
	curLine = infile.readline()

#outlist has been filled
for out in out_list:
	print(out)
#sort by the left position
out_list = sorted(out_list, key=lambda x:int(x[2]))

#print to file
#unique id for each gene
count = 1 
for out in out_list:
	out = [str(count)] + out
	outfile.write('\t'.join(out) + '\n')
	count += 1



