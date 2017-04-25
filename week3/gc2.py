import sys

genome = open(sys.argv[1]).read()

print( float(genome.count("C") + genome.count("G"))/ (len(genome) - genome.count('\n')))
