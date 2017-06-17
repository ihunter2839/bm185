import sys
import numpy as np
import requests
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import RFE
from sklearn.linear_model import LassoCV
from sklearn.svm import SVR


exp_matrix = np.loadtxt(sys.argv[1])
tol = np.loadtxt(sys.argv[2])
gene_cols = open(sys.argv[3]).read()[:-1].split()

X, y = [exp_matrix, tol]

#lasso regression
use_lasso = input("Use lasso? ")
if "yes" in use_lasso:
    clf = LassoCV()
    #set an arbitrary threshold
    sfm = SelectFromModel(clf)
    sfm.fit(X,y)
    n_features = sfm.transform(X).shape[1]

    #continue to increment until top 5 features are 
    #located
    while n_features < 2:
        sfm.threshold = sfm.threshold / 1.5
        X_transform = sfm.transform(X)
        n_features = X_transform.shape[1]

    feats = sfm.get_support(indices=True)
    for feat in feats:
        print(gene_cols[feat])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    feat1 = X_transform[:,0]
    feat2 = X_transform[:,1]
    ax.scatter(feat1, feat2, tol)
    plt.xlabel("feat1")
    plt.ylabel("feat2")
    plt.show()

use_svr = input("Use svr? ")
if "yes" in use_svr:
    clf = SVR(kernel='linear', C=1.0, epsilon=0.2)
    clf.fit(X, y)
    selector = RFE(clf, 5, step=5)
    selector = selector.fit(X,y)
    gene_pos = selector.get_support(indices=True)
    for pos in gene_pos:
        print(gene_cols[pos] + '\t' + str(pos))


if True == False:
    pca = PCA()
    pca.fit(exp_matrix)

    selector = VarianceThreshold()
    selector.fit(exp_matrix)
    exp_vars = selector.variances_
    av_var = sum(exp_vars) / len(exp_vars)
    std_var = np.std(exp_vars)
    thresh = av_var + 2*std_var
    selector = VarianceThreshold(thresh)
    exp_reduce = selector.fit_transform(exp_matrix)
    cols = selector.get_support(indices=True)
    genes = [gene_cols[i] for i in cols]
    #genes = [gene_cols[i].split(".")[0] for i in cols]

    exp_reduce = pca.transform(exp_matrix)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = []
    y = []
    z = []
    for red in exp_reduce:
        x.append(red[0])
        y.append(red[1])
        z.append(red[2])
    ax.scatter(x,y,z)
    for i, label in enumerate(tol):
        ax.text(x[i], y[i], z[i], label)
    plt.show()