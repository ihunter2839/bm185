import sys
import numpy
#import matplotlib.pyplot as plt
import MySQLdb as sql

infile = open(sys.argv[1])

#skip header
curLine = infile.readline()
while curLine[0] == "#":
	curLine = infile.readline()

#columns in file OperonSet.txt
#name left_pos right_pos strand num_genes genes evidence confidence
#list of positions needed
pos_list = [0, 1, 2, 3, 5, 7]

#list of operons supported with 
#strong or confirmed confidence
operons = []


while curLine != "":
	data_list = curLine[:-1].split('\t')
	out = []
	for pos in pos_list:
		out.append(data_list[pos])
	#only use operons evidence >= strong
	if out[5] not in ["", "Weak"]:
		operons.append(out)
	curLine = infile.readline()

operons = sorted(operons, key=lambda x:int(x[1]))

#write to file
outfile = open("regulon_operon.txt", "w")
#unique id
count = 1
for operon in operons:
	operon = [str(count)] + operon
	outfile.write('\t'.join(operon) + '\n')
	count += 1


#calculate distances for null hypothesis
#h0: genes are not in same operon

db = sql.connect(host="bm185s-mysql.ucsd.edu", user="ihunter", 
passwd=raw_input("password: "), db="ihunter_db")
c = db.cursor()

#distances within operon
intra_dist =  []
#distances between operons
inter_dist = []

right = 2
left = 1

#list to hold previous operons positions
prevPos = []

for i in range(0, len(operons)-1):
	curOp = operons[i]
	nextOp = operons[i+1]
	#get intragenic distances
	#boolean flag that determines if operon is usable
	#for intragenic distances, that is, all b_numbers
	#were successfuly located
	skip = False
	genes = curOp[4].split(',')
	b_numbers = []
	pos = []

	for gene in genes:
		res = None
		if '<' not in gene:
			c.execute("select b_number from gene_operon where name='%s'" % gene)
			res = c.fetchone()
		if res == None:
			skip = True
		else:
			b_numbers.append(res[0])
	#if all of the genes have valid b_number
	if skip == False:
		for b in b_numbers:
			c.execute("select left_pos, right_pos, id from genes_sorted where b_number='%s'" % b)
			res = c.fetchone()
			#res should not be null, no need to check
			#false assumption, res can be null is operon does
			#not contain CDS
			if res == None:
				skip = True
			else:
				pos.append(res)
		if skip == False:
			pos = sorted(pos, key=lambda x: x[1])
			for i in range(0, len(pos)-1):
				intra_dist.append(pos[i+1][0] - pos[i][1])
		
		if len(pos) != 0:	
			prevGene_id = pos[0][2] - 1
			nextGene_id = pos[len(pos)-1][2] + 1
			c.execute("select right_pos, strand from genes_sorted where id=%i" % prevGene_id)
			res = c.fetchone()
			dir_dict = {'+':'forward', '-':'reverse'}
			
			if res != None:
				if dir_dict[res[1]] == curOp[3]:
					inter_dist.append(int(curOp[1]) - res[0])
			c.execute("select left_pos, strand from genes_sorted where id=%i" % nextGene_id)
			res = c.fetchone()
			if res!= None:
				if dir_dict[res[1]] == curOp[3]:
					inter_dist.append(res[0] - int(curOp[2]))
		
forData = open(raw_input("Send to file: "), "w")
forData.write(str(intra_dist) + '\n')
forData.write(str(inter_dist) + '\n')

#n. inter, patches = plt.hist(inter_dist, max(inter_dist), normed=True)
#n, intra, patches = plt.hist(intra_dist, max(intra_dist), normed=True)
#plt.show()


