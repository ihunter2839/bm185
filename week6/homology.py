import sys
import MySQLdb as sql

#criteria for homologs
#60% of shorter seq must be covered
#use bitscore to rank 

#bi-directional best hit
#gene(e,i) --> gene(a,j)
#gene(a,j) --> gene(e,i)

#ortholog higher than paralog
#gene(e,i) --> gene(a,j)
#gene(a,j) --> !gene(e,i)
#BUT
#gene(e,i) --> gene(a,j) is more similar than
#gene(e,i) --> gene(e,k)

db = sql.connect(host='bm185s-mysql.ucsd.edu', 
user='ihunter', passwd=raw_input("password: "), db='ihunter_db')
c = db.cursor()

#add check for the qcovs and scovs
c.execute("select query_id, seq_id, bitscore from blast_ecoli where query_cov > .6 or seq_cov > .6")
res = c.fetchall()

#map the gene name to a tuple containing
#ecoli_gene --> (atume_gene, score)
#atume_gene --> (ecoli_gene, score) 
ecoli_dict = {}
atume_dict = {}

#fill ecoli_dict
for t in res:
	e_gene = t[0]
	a_gene = t[1]
	score = t[2]
	if e_gene not in ecoli_dict:
		ecoli_dict[e_gene] = (a_gene, score)
	else:
		if score > ecoli_dict[e_gene][1]:
			ecoli_dict[e_gene] = (a_gene, score)

c.execute("select query_id, seq_id, bitscore from blast_atume")
res = c.fetchall()

#fill atume_dict
for t in res:
	a_gene = t[0]
	e_gene = t[1]
	score = t[2]
	if a_gene not in atume_dict:
		atume_dict[a_gene] = (e_gene, score)
	else:
		if score > atume_dict[a_gene][1]:
			atume_dict[a_gene] = (e_gene, score)

#iterate through the dicts
ecoli_keys = ecoli_dict.keys()
atume_keys = atume_dict.keys()
#list to hold atume ids that have been 
atume_used = {}

outfile = open(raw_input("output file: "), "w")

for k in ecoli_keys:
	best_match = ecoli_dict[k][0]
	#check bi-directional best hit
	if atume_dict[best_match][0] == k:
		out = '\t'.join([k, best_match, "orthology", "BDBH"])
		outfile.write(out + '\n')
		atume_used[best_match] = True
	#check ortholog higher than paralog
	else:
		ortho_score = ecoli_dict[k][1]
		c.execute("select max(bitscore) from blast_ecoli_self where (query_id='%s' and seq_id!='%s')"%(k,k))
		#score of highest scoring paralog
		para_score = c.fetchone()
		if ortho_score > para_score[0]:
			out = '\t'.join([k, best_match, "orthology", "PHTO"])
			outfile.write(out + '\n')
			atume_used[best_match] = True

for k in atume_keys:
	if k not in atume_used:
		best_match = atume_dict[k][0]
		ortho_score = atume_dict[k][1]
		c.execute("select max(bitscore) from blast_atume_self where query_id='%s' and seq_id!='%s'"%(k,k))
		para_score = c.fetchone()
		if ortho_score > para_score[0]:
			out = '\t'.join([k, best_match, "orthology", "PHTO"])
			outfile.write(out + '\n')
			
	



