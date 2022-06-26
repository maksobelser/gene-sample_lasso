# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 09:12:32 2022

@author: makso
"""

import numpy as np
import time
import os

tic = time.time()

# select the number of model to do per job for Lasso
N = 2

# dir to put the slurm files
os.chdir('G:\\My Drive\\1_Faks\\2_Uporabna statistika Msc\\2. letnik\\Strojno ucenje\\Seminar\\Slurms\\')
slurm_dir = 'G:\\My Drive\\1_Faks\\2_Uporabna statistika Msc\\2. letnik\\Strojno ucenje\\Seminar\\Slurms\\'


# get the number of Inds to do
data_dir = 'C:\\Users\\makso\\DL_final_project\\data\\'
beta_tst_inds = np.loadtxt(data_dir + 'Beta_Tst_Inds.txt', dtype=int)
# find the len of beta_tst_inds
num_samps = len(beta_tst_inds)
# convert this to an ordered list from zero (real inds are used to slice data in betas_main.py)
samps_inds = list(range(num_samps))
# change int to str for using join later
samps_inds = [str(item) for item in samps_inds]
# make a comma separated elements in list
ModelInds_list = [','.join(samps_inds[n:n+N]) for n in range(0, len(samps_inds), N)]
print('The number of jobs to submit is',len(ModelInds_list))


mylist = ['#!/bin/bash']
mylist.append('### define resources needed:')
mylist.append('#SBATCH --job-name=lasso')
mylist.append('#SBATCH --output=lasso.out')
mylist.append('#SBATCH --time=12:00:00')
mylist.append('#SBATCH --nodes=1')
mylist.append('#SBATCH --ntasks-per-node=2')
mylist.append('#SBATCH --partition=gpu')
mylist.append('#SBATCH --cpus-per-task=12')
mylist.append('#SBATCH --gpus-per-task=1')
mylist.append('#SBATCH --mem-per-gpu=32G')

mylist.append('source ~/miniconda3/etc/profile.d/conda.sh # intialize conda')
mylist.append('conda activate geneGAN')
mylist.append('OUT_PATH=/d/hpc/projects/FRI/DL/mo6643/')

for idx, aModelInd_set in enumerate(ModelInds_list):
    mylist.append('python lasso.py -mi %s'%aModelInd_set)

with open(slurm_dir + 'beta_analysis-%s.sb'%idx, 'w') as thefile:
    for item in mylist:
        thefile.write("%s\n" % item)

print('This script took %i minutes to run '%((time.time()-tic)/60))