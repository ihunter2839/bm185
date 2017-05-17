import MySQLdb

cnx = MySQLdb.connect(user='ihunter', passwd='Maxwell*', db='ihunter_db', host='bm185s-mysql.ucsd.edu')
cursor = cnx.cursor()
