# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 16:03:02 2022

@author: makso
"""

import numpy as np # tested with verison 1.16.4
from sklearn.preprocessing import StandardScaler # tested with verison 0.20.3
from sklearn.neighbors import KNeighborsRegressor # tested with verison 0.20.3
from sklearn.linear_model import Lasso # tested with verison 0.20.3

import argparse # tested with python verison 3.7
import os # tested with python verison 3.7
import time # tested with python verison 3.7

def load_data(TrnData,TestData,Split,GeneSplit):
    
    data_dir = '/d/hpc/projects/FRI/DL/mo6643/data/'
    
    # load dict to store all the data
    data_dict = {}
    

    Xgene_inds = np.loadtxt(data_dir+'%s_Xgenes_inds.txt'%GeneSplit,dtype=int)
    ygene_inds = np.loadtxt(data_dir+'%s_ygenes_inds.txt'%GeneSplit,dtype=int)
    
    # load the traning data
    trndata = np.load(data_dir+'%s_Trn_Exp.npy'%TrnData)
    if TrnData == 'RNAseq':
        trndata = np.arcsinh(trndata)
    Xtrn = trndata[:,Xgene_inds]
    ytrn = trndata[:,ygene_inds]
    data_dict['Xtrn-'+TrnData] = Xtrn
    data_dict['ytrn-'+TrnData] = ytrn
    
    # load the data to be used a test data
    for datatype in TestData:
            tstdata = np.load(data_dir+'%s_%s_Exp.npy'%(datatype,Split))
            if Split == 'Val':
                trimmed_inds = np.load(data_dir+'%s_trimmed_Val_inds.npy'%datatype)
                tstdata = tstdata[trimmed_inds,:]
            if datatype == 'RNAseq':
                tstdata = np.arcsinh(tstdata)
            Xtst = tstdata[:,Xgene_inds]
            ytst = tstdata[:,ygene_inds]
            data_dict['Xtst-'+datatype] = Xtst
            data_dict['ytst-'+datatype] = ytst
    return data_dict


def reorder_and_transpose(data_dict,TrnData,TestData):
    
    if TrnData == TestData[0]:
        data_dict['ytrn-'+TrnData], data_dict['Xtst-'+TrnData] = data_dict['Xtst-'+TrnData], data_dict['ytrn-'+TrnData]
    else:
        data_dict['ytrn-'+TestData[0]] = data_dict['Xtst-'+TestData[0]]
        data_dict['Xtst-'+TrnData] = data_dict['ytrn-'+TrnData]
        data_dict.pop('Xtst-'+TestData[0], None)
        data_dict.pop('ytrn-'+TrnData, None)
        
    for akey in data_dict:
        data_dict[akey] = np.transpose(data_dict[akey])
    
    return data_dict
    
def stdscale_data(data_dict,TrnData,TestData,Model):

    std_scale = StandardScaler().fit(data_dict['Xtrn-'+TrnData])
    # transform the Xtrn data
    data_dict['Xtrn-'+TrnData] = std_scale.transform(data_dict['Xtrn-'+TrnData])
    
    # use Xtrn scale to transform Val data
    if Model in ['SampleLasso','GeneKNN']:
        data_dict['Xtst-'+TrnData] = std_scale.transform(data_dict['Xtst-'+TrnData])
    else:
        for datatype in TestData:
            data_dict['Xtst-'+datatype] = std_scale.transform(data_dict['Xtst-'+datatype])
            
    return data_dict
    
def initialize_reg(Model,HyperParameter):
    
    if Model in ['SampleLasso','GeneLasso']:
        reg = Lasso(alpha=HyperParameter,fit_intercept=True,normalize=False,precompute=False,
                     copy_X=True,max_iter=1000,tol=0.001,warm_start=False,positive=False,
                     random_state=None,selection='random')
    elif Model in ['SampleKNN', 'GeneKNN']:
        reg = KNeighborsRegressor(n_neighbors=int(HyperParameter),weights='distance',algorithm='brute',
                                  leaf_size=30,p=2,metric='minkowski',metric_params=None,n_jobs=None)
    return reg

if __name__ == "__main__":
    
    tic = time.time()
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-m','--model',
                        default = 'GeneLasso',
                        type = str,
                        help = 'GeneLasso, SampleLasso, SampleKNN, GeneKNN')
    parser.add_argument('-hp','--hyperparameter',
                        default = 0.01,
                        type = float,
                        help = 'with k or alpha (k will be turned into an int)')
    parser.add_argument('-trnd','--trndata',
                        default = 'Microarray',
                        type = str,
                        help = 'Microarray, RNAseq')
    parser.add_argument('-tstd','--tstdata',
                        default = 'Microarray',
                        type = str,
                        help = 'Microarray, RNAseq, or RNAseq-Microarray')
    parser.add_argument('-s','--split',
                        default = 'Val',
                        type = str,
                        help = 'Val, Tst (always uses trimmed val)')
    parser.add_argument('-gs','--genesplit',
                        default = 'LINCS',
                        type = str,
                        help = 'GPL96-570, LINCS')
    parser.add_argument('-b','--betas',
                        default = 'yes',
                        type = str,
                        help = 'yes, no (Whether to sample LASSO betas or neighbors in KNN)')
    parser.add_argument('-mi','--modelinds',
                        default = '1,4,6,100',
                        type = str,
                        help = 'The models to do, comma separated')
    parser.add_argument('-sd','--savedir',
                        default = '/d/hpc/projects/FRI/DL/mo6643/results/main/',
                        type = str,
                        help = 'The base dir where all the specific directories are')
    args = parser.parse_args()
    Model = args.model
    HyperParameter = args.hyperparameter
    TrnData = args.trndata
    TestData = args.tstdata
    Split = args.split
    GeneSplit = args.genesplit
    Betas = args.betas
    ModelInds = args.modelinds
    SaveBaseDir = args.savedir
    
    
    # turn TestData into a list
    TestData = TestData.strip().split('-')
    
    # turn ModelInds into a list of ints 
    if Model in ['SampleLasso','GeneLasso']:
        ModelInds = ModelInds.strip().split(',')
        ModelInds = [int(item) for item in ModelInds]
    

    # make save dirs if don't exsits
    # need to move to slurm at some point
    save_dirs_dict = {}
    for datatype in TestData:
        save_dir_end = 'M--%s__H--%s__Trn--%s__Tst--%s__S--%s__GS--%s/'%(Model,HyperParameter,TrnData,
                                                                         datatype,Split,GeneSplit)
        save_dir = SaveBaseDir + save_dir_end
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        save_dirs_dict[datatype] = save_dir
    
    # might move this to the slurm as well
    if (Model == 'SampleLasso') and (len(TestData)!=1):
        raise ValueError('Only allowed on TestData for SampleLasso')
    if (Model == 'GeneKNN') and (len(TestData)!=1):
        raise ValueError('Only allowed on TestData for GeneLasso')
        
        
    print('Loading the data')
    # load the data
    data_dict = load_data(TrnData,TestData,Split,GeneSplit)

    print('Changing data for SampleLasso or GeneKNN')
    # change the data_dict a bit if using SampleLasso or GeneKNN
    if Model in ['SampleLasso','GeneKNN']:
        data_dict = reorder_and_transpose(data_dict,TrnData,TestData)

    print('Standard Scaling the data')
    # stdscale the data
    data_dict = stdscale_data(data_dict,TrnData,TestData,Model)

    print('Inializing the Regressor')
    # intialize the regressor
    reg = initialize_reg(Model,HyperParameter)

    '''
    This is the part of the code that will run and save the models.
    '''
    if Model == 'SampleKNN':
        print('Fitting and Saving SampleKNN')
        reg.fit(data_dict['Xtrn-'+TrnData],data_dict['ytrn-'+TrnData])
        for datatype in TestData:
            ypreds = reg.predict(data_dict['Xtst-'+datatype])
            np.save(save_dirs_dict[datatype]+'preds.npy',ypreds)
            if Betas == 'yes':
                top_nns_dist, top_nns_inds = reg.kneighbors(data_dict['Xtst-'+datatype])
                np.save(save_dirs_dict[datatype]+'dists.npy',top_nns_dist)
                np.save(save_dirs_dict[datatype]+'inds.npy',top_nns_inds)

    if Model == 'SampleLasso':
        print('Fitting and Saving a SampleLasso')
        for amodel in ModelInds:
            tic1 = time.time()
            # fit the model
            reg.fit(data_dict['Xtrn-'+TrnData],data_dict['ytrn-'+TestData[0]][:,amodel])
            ypreds = reg.predict(data_dict['Xtst-'+TrnData])
            np.save(save_dirs_dict[TestData[0]]+'preds__ModelInds--%i.npy'%amodel,ypreds)
            if Betas == 'yes':
                np.save(save_dirs_dict[TestData[0]]+'betas__ModelInds--%i.npy'%amodel,reg.coef_)
            print('Model number',amodel,'took',reg.n_iter_,'iterations to run')
            print('Model number',amodel,'took',time.time()-tic1,'seconds to train/predict/save')
                    
    if Model == 'GeneLasso':
        print('Fitting and Saving a GeneLasso')
        for amodel in ModelInds:
            tic1 = time.time()
            reg.fit(data_dict['Xtrn-'+TrnData],data_dict['ytrn-'+TrnData][:,amodel])
            for datatype in TestData:
                ypreds = reg.predict(data_dict['Xtst-'+datatype])
                np.save(save_dirs_dict[datatype]+'preds__ModelInds--%i.npy'%amodel,ypreds)
                if Betas == 'yes':
                    np.save(save_dirs_dict[datatype]+'betas__ModelInds--%i.npy'%amodel,reg.coef_)
            print('Model number',amodel,'took',reg.n_iter_,'iterations to run')
            print('Model number',amodel,'took',time.time()-tic1,'seconds to train/predict/save')
            
    if Model == 'GeneKNN':
        print('Fitting and Saving GeneKNN')
        reg.fit(data_dict['Xtrn-'+TrnData],data_dict['ytrn-'+TestData[0]])
        ypreds = reg.predict(data_dict['Xtst-'+TrnData])
        np.save(save_dirs_dict[datatype]+'preds.npy',ypreds)
        if Betas == 'yes':
            top_nns_dist, top_nns_inds = reg.kneighbors(data_dict['Xtst-'+TrnData])
            np.save(save_dirs_dict[TestData[0]]+'dists.npy',top_nns_dist)
            np.save(save_dirs_dict[TestData[0]]+'inds.npy',top_nns_inds)
            
    print('This script took %i minutes to run '%((time.time()-tic)/60))