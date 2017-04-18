import sys

if __name__ == "__main__":
	fileIn = open(sys.argv[1])
	out = ""
	while True:	
		tmp = fileIn.readline()
		if tmp == "":
			break
		out = out + tmp
	print(out.replace(",", "	"))
	

