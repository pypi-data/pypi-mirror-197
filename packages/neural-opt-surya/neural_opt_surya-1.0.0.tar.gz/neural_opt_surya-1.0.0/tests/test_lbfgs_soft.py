#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 16:03:47 2022

@author: surya
For testing L-BFGS with soft constraint and continuation scheme
1. To know where all it fails
"""
#%%
import tensorflow as tf
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  try:
    # Currently, memory growth needs to be the same across GPUs
    for gpu in gpus:
      tf.config.experimental.set_memory_growth(gpu, True)
    logical_gpus = tf.config.experimental.list_logical_devices('GPU')
    print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
  except RuntimeError as e:
    # Memory growth must be set before GPUs have been initialized
    print(e)

import sys
import os
# cwd = sys.path[0]
# sys.path.append(os.path.join(cwd, 'topopt', 'nso'))
# Add nso folder to path
cwd = os.getcwd()
sys.path.append(os.path.join(cwd, 'topopt', 'nso'))

import topo_api
import models
import train_new as train
import problems
import xarray
import time
import numpy as np
#%%
#################################################################
#User inputs:
data_dir = '../test_data/' 
exp_number = 'test'
optimizer = 'lbfgs' # 'adam' ,'mma'
prob_code = 'mi' # 'tr', 'cf', 'cb', 'mi'
nelx = 32
ht = 64
seeds_model = np.arange(1,3) 
max_iterations = 20
opt_args =      {
                'conv_criteria' : False,
                'limit' : 0.1,
                }

t_args =        {'vol_const_hard' : False, 'cont_scheme' : True,
                'alpha_start' : 0.2, 'del_alpha':4,'alpha_end':100,
                'conv_filter':False, 'scale_loss': False,
                'p_start':2, 'p_end':4, 'del_p':0.08}
model_args =   {
                'vol_const_hard': t_args['vol_const_hard']
                }
xarray_dets = {'problem': [prob_code], #['A', 'B', 'D','E']
               'model': ['F-TouNN'], #['Pix', 'CNN', 'TouNN', 'F-TouNN']
               'opt' : [optimizer]}  
###################################################################
#%%
opt_fn_det = {'lbfgs_True': train.train_lbfgs_hard,
              'lbfgs_False': train.train_lbfgs_soft,
              'adam_True': train.train_tf_opt_hard,
              'adam_False': train.train_tf_opt_soft,
              'mma_False': train.method_of_moving_asymptotes }    

opt_fn  = opt_fn_det[optimizer+'_'+str(t_args['vol_const_hard'])]

prob_code_det = {'tr' : 'tensile_rod',
                 'cf': 'cantilever_fine',
                 'cb': 'causeway_bridge',
                 'mi': 'michell'}
model_code =   {
              'Pix': models.PixelModel,  
              'CNN': models.CNNModel_c2dt_corr,
              'TouNN': models.TounnModel,
              'F-TouNN': models.TounnModel,
               }
problem = problems.PROBLEMS_BY_NAME[prob_code_det[prob_code]](nelx = nelx, width =nelx, height = ht)

# Code for each experiment
xd = xarray_dets
exp_name =  xd['model'][0][0]+ xd['opt'][0][0] + xd['problem'][0] + str(exp_number)           

#redirection to appropriate folder - to store model weights
os.chdir(data_dir)
cwd = os.getcwd()
if not os.path.exists(str(exp_name)):
    os.makedirs(str(exp_name))
os.chdir(cwd)
#%%
args = topo_api.specified_task(problem)
all_ds = []
time_taken = []

for j,seed in enumerate(seeds_model):
    os.chdir(cwd+'/'+str(exp_name))    
    tf.keras.backend.clear_session() # Clear GPU of all models     
    folder1 = str(exp_name) +'_model_' + str(seed) 
    if not os.path.exists(folder1):
        os.makedirs(folder1)        
    path = os.getcwd() + '/' + folder1
    os.chdir(path)   
    
    #create a model
    if xd['model'][0] == 'TouNN':
        model_args['fourier_on'] = False
    model = model_code[xd['model'][0]](seed = seed, args = args, **model_args)  
       
    #train
    if os.path.exists("./n_iterations_lbfgs.txt"):
        os.remove("./n_iterations_lbfgs.txt")
        
    start_time = time.time()
    if opt_args['conv_criteria']:
        ds, ind = opt_fn(model, max_iterations, save_weights_path = path , t_args = t_args, **opt_args)
    else:
        ds, ind = opt_fn(model, max_iterations, t_args = t_args, **opt_args)  
        
    dur = (time.time() - start_time)/60      
    ds.to_netcdf(folder1 +'.nc')
    
    print("Seed value = " + str(seed))
    ds = ds.expand_dims({'model_seed':[seed]}).drop(['design'])
    all_ds.append(ds)   
    print('Time for seed: ',dur)
    time_taken.append((seed,dur))
    if seed == seeds_model[-1]:
        pass
    else:
        del model
#%%
#save relevant experiment details as a dictionary
#indices, times
#os.chdir(data_dir+str(exp_name))
# exp_details = dict()
# exp_details['seed_time'] = time_taken#(seed,time)

# import pickle
# pickle.dump(exp_details,open(str(exp_name)+'_expt_details','wb'))

# steps = np.arange(max_iterations+1)
fds = xarray.merge(all_ds)
# Embed metadata into xarray!!!!
fds = fds.expand_dims(xarray_dets)
#fds.to_netcdf(str(exp_name)+'.nc')
#%%
#print values
print("Mean", fds.isel(step=-1).mean(dim='model_seed').values)
print("Median", fds.isel(step=-1).median(dim='model_seed').values)
print("Average time per seed",np.mean([y for x,y in time_taken]))

