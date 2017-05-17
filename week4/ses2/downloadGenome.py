import sys
import os
import re

ecoliLine = open("ecoliLink.txt").read()
tumaLine = open("tumaLink.txt").read()

ftp1 = re.search(":\/\/ftp[a-zA-Z0-9\.\/\_]+", ecoliLine)
ftp2 = re.search(":\/\/ftp[a-zA-Z0-9\.\/\_]+", tumaLine)
link1 = "rsync" + ftp1.group(0)
link2 = "rsync" + ftp2.group(0)
#print(link1)
#print(link2)

command1 = "rsync -avzh " + link1 + " e_coli"
command2 = "rsync -avzh " + link2 + " a_tuma"

os.system(command1)
os.system(command2)

