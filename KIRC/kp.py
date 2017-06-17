import sys
import numpy as np
from lifelines import KaplanMeierFitter
from lifelines import CoxPHFitter
import matplotlib.pyplot as plt

exp_matrix = np.loadtxt(sys.argv[1])
tol = np.loadtxt(sys.argv[2])
infile = open(sys.argv[3])
gene_name = []
gene_pos = []
for i in infile:
    gene_name.append(i.split()[0])
    gene_pos.append(int(i.split()[1]))

num_cols = len(exp_matrix)
mid = num_cols//2

for j in range(0, len(gene_pos)):
    pos = gene_pos[j]
    gene_exp = [exp_matrix[i][pos] for i in range(0,num_cols)]
    comb = [[gene_exp[i], tol[i]] for i in range(0, num_cols)]
    comb = sorted(comb, key=lambda x: x[0])
    low = comb[:mid]
    high = comb[mid:]
    #l_exp = [low[i][0] for i in range(0,mid)]
    l_tol = [low[i][1] for i in range(0, len(low))]
    l_out = [True]*len(l_tol)
    #h_exp = [high[i][0] for i in range(0,mid)]
    h_tol = [high[i][1] for i in range(0, len(high))]
    h_out = [True]*len(h_tol)

    kp = KaplanMeierFitter()
    label_low = 'Lower 50% (n = ' + str(len(low)) + ')'
    label_high = 'Upper 50% (n = ' + str(len(high)) + ')'
    len_high = len(high)
    kp.fit(l_tol, l_out, label=label_low)
    ax = kp.plot()
    kp.fit(h_tol, h_out, label=label_high)
    graph = kp.plot(ax=ax)
    plt.title("Survival Function of %s" %gene_name[j])
    graph.get_figure().savefig("%s_survival.png" %gene_name[j])

