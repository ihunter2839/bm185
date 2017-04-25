import sys
import numpy
import matplotlib
import pylab

cuiData = open("cuiData.txt")
#x holds the relative position of the gene in the genome
x = []
#y holds the CUI value for the gene at relative position i 
y = []

cur = cuiData.readline()
while cur != "":
	split = cur.split('\t')
	if len(split) > 1:
		x.append(float(split[0][1:]))
		y.append(float(split[1]))
	cur = cuiData.readline()
#Scatter plot of CUI value as a function of gene position
matplotlib.pyplot.scatter(x,y)
matplotlib.pyplot.xlabel(" Position of Gene")
matplotlib.pyplot.ylabel("CUI")
matplotlib.pyplot.show()

#Dictionary mapping CUI value to gene position
cuiToPos = dict(zip(y, x))
#Sort the CUI values
cuiSorted = sorted(cuiToPos.keys())
#Get a list of positions sorted by CUI value
posSorted = [cuiToPos[k] for k in cuiSorted]
#Plot it
fig = matplotlib.pyplot.figure()
ax = fig.add_subplot(111)
ax.plot(cuiSorted, 'or')
ax.set_xticklabels(posSorted)
matplotlib.pyplot.ylabel("Sorted CUI")
matplotlib.pyplot.xlabel("Gene Position")
matplotlib.pyplot.show()

#matplotlib.pyplot.plot(cuiSorted, 'or')
#matplotlib.pyplot.set_xticklabels(posSorted)
#matplotlib.pyplot.xlabel("Cui value")
#matplotlib.pyplot.ylabel("Position of gene")
#matplotlib.pyplot.show()


#first argument is the data 
#second argument is number of bins
#norm the area under the curve to 1
n, bins, patches = pylab.hist(y, 200, normed=True)
pylab.xlabel('CUI')
pylab.ylabel('Number of Occurences')
pylab.show()
