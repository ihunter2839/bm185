import sys
import MySQLdb as sql

sqlConnection = sql.connect(host='bm185s_mysql.ucsd.edu', user='ihunter',
passwrd=raw_input("password: "), db='ihunter_db')
c = sqlConnection.cursor()

infile = open(sys.argv[1])

#skip the header
curLine = infile.readline()
while curLine[0] == "#":
	curLine = infile.readline()

#tu_id tu_name operon_name gene_names promoter_name evidence confidence
pos_list = [2, 3, 6]

while curLine != "":
	data_list = curLine[:-1].split('\t')
	operon = []
	for pos in pos_list:
		operon.append(data_list[pos])
	gene_list = operon[1].split(",")
	
