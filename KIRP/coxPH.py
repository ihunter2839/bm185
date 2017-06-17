import sys
from lifelines import CoxPHFitter
import numpy as np
from pandas import DataFrame

exp_matrix = np.loadtxt(sys.argv[1])
tol = np.loadtxt(sys.argv[2])
infile = open(sys.argv[3])
gene_name = []
gene_pos = []
for i in infile:
    gene_name.append(i.split()[0])
    gene_pos.append(int(i.split()[1]))

num_cols = len(exp_matrix)
#list to hold expression vectors for all genes 
exp_vectors = []

#iterate through selected features, generate expression vectors
for j in range(0, len(gene_pos)):
    pos = gene_pos[j]
    exp_vectors.append([exp_matrix[i][pos] for i in range(0,num_cols)])

data_array = np.array([*exp_vectors, tol])
data_array = data_array.transpose()
data_frame = DataFrame(data_array, columns=[*gene_name, 'tol'])
cf = CoxPHFitter()
cf.fit(data_frame, 'tol')
cf.print_summary()