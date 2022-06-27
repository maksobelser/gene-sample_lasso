# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 09:11:07 2022

@author: makso
"""

import numpy as np # tested with verison 1.16.4
import time # tested with python verison 3.7
import argparse
from sklearn.preprocessing import StandardScaler # tested with verison 0.20.3
from sklearn.linear_model import Lasso # tested with verison 0.20.3

tic = time.time()


parser = argparse.ArgumentParser()
parser.add_argument('-mi','--modelinds',
                    default = '1,4,6,100',
                    type = str,
                    help = 'The models to do, comma separated')
parser.add_argument('-s','--save_dir',
                    default = '/d/hpc/projects/FRI/DL/mo6643/results/',
                    type = str,
                    help = 'The folder where saved files are')
args = parser.parse_args()
ModelInds = args.modelinds
save_dir = args.save_dir

# make Model Inds a list of ints
ModelInds = ModelInds.strip().split(',')
ModelInds = [int(item) for item in ModelInds]


########## load the data and inds to slice data #####################
print('Loading the data')
data_dir = '/d/hpc/projects/FRI/DL/mo6643/data/'
data = np.load(data_dir + 'Microarray_Trn_Exp.npy')
# load the inds files
beta_trn_inds = np.loadtxt(data_dir + 'Beta_Trn_Inds.txt', dtype=int)
beta_tst_inds = np.loadtxt(data_dir + 'Beta_Tst_Inds.txt', dtype=int)
Xgenes = np.loadtxt(data_dir + 'GPL96-570_Xgenes_inds.txt', dtype=int)
ygenes = np.loadtxt(data_dir + 'GPL96-570_ygenes_inds.txt', dtype=int) 

    
############# Get results for Lasso ##################################
# transpose and split the data for Lasso
print('Slicing and Standarizing Data for Lasso')
data_Lasso = np.transpose(data)
Xdata_Lasso = data_Lasso[:,beta_trn_inds]
ydata_Lasso = data_Lasso[:,beta_tst_inds]
Xtrn_Lasso = Xdata_Lasso[Xgenes,:]
Xtst_Lasso = Xdata_Lasso[ygenes,:]
ytrn_Lasso = ydata_Lasso[Xgenes,:]
ytst_Lasso = ydata_Lasso[ygenes,:]
std_scale = StandardScaler().fit(Xtrn_Lasso)
Xtrn_Lasso = std_scale.transform(Xtrn_Lasso)
Xtst_Lasso = std_scale.transform(Xtst_Lasso)

print('Running LASSO')
# The best HP for this case is 0.001
reg = Lasso(alpha=0.001,fit_intercept=True,normalize=False,precompute=False,
             copy_X=True,max_iter=1000,tol=0.001,warm_start=False,positive=False,
             random_state=None,selection='random')
for amodel in ModelInds:
    tic1 = time.time()
    # fit the model
    reg.fit(Xtrn_Lasso,ytrn_Lasso[:,amodel])
    ypreds_Lasso = reg.predict(Xtst_Lasso)
    np.save(save_dir + 'Lasso_preds__ModelInds--%i.npy'%amodel,ypreds_Lasso)
    np.save(save_dir + 'Lasso_betas__ModelInds--%i.npy'%amodel,reg.coef_)
    print('Model number',amodel,'took',reg.n_iter_,'iterations to run')
    print('Model number',amodel,'took',time.time()-tic1,'seconds to train/predict/save')
print()

print('This script took %i minutes to run '%((time.time()-tic)/60))