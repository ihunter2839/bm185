import sys
import re

infile = open(sys.argv[1])

outfile = open(raw_input("file name: "), "w")

#primary key for blast table
match_count = 0

for l in infile:
	if l != '\n':
		#trim newline if it exists
		if l[-1] == '\n':
			l = l[:-1]
		out = [str(match_count)] + [s for s in l.split('\t')]
		#need to remove version number from pids
		out[1] = out[1].split(".")[0]
		out[2] = out[2].split("|")[1]
		out[2] = out[2].split(".")[0]
		scov = float(out[9]) / float(out[4])
		out.append(str(scov))
		outfile.write('\t'.join(out)+ '\n')
		match_count += 1
