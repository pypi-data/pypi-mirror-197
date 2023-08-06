#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 11:33:20 2022

@author: surya
Test the loading of saved weights and problems with BN layers
1. Create a model
2. load weights
3. load dataset
4. check model output vs the dataset loss
"""
#%%
data_dir = '/home/surya/Desktop/PhD_work/Masters_extension/data_masters/' 
exp_code = 'Fatrtiny_wts_2'
seeds = [1]#np.arange(1, 16)
nelx = 4
nely=2
prob_code = exp_code[2:4]
test_point_res = 200 # pointer per axis
model_code = 'F-TouNN' 
model_args =   {
                'vol_const_hard': False,'sampling': {'default':(8,108)},   
                'var_batch' :  True,
                'resolution' : 1
                }
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
import numpy as np
import topopt.nso.topo_api as topo_api
import topopt.nso.models as models
import topopt.nso.problems as problems
import topopt.visual_tools.nn_model_v2 as nn
#%%
prob_code_det = {'tr' : 'tensile_rod',
                 'cf': 'cantilever_fine',
                 'cb': 'causeway_bridge',
		'mbb': 'mbb',
		'l': 'lshape',
		'dam': 'dam',
		'multi': 'multistory'
		}
problem = problems.PROBLEMS_BY_NAME[prob_code_det[prob_code]](nelx = nelx, width=nelx, height= nelx/2)
args = topo_api.specified_task(problem) 
model = models.TounnModel(seed = seeds[0], args = args, **model_args)  
#%%
#model(None)# --> this does not make any difference
step=10
wts_path = "{}{}/{}_model_{}/weights_{}.p".format(data_dir, exp_code, exp_code, seeds[0],step)
nn_mdl = nn.Tensorflow_NNModel(model, wts_path)
#%%
ds_path = "{}{}/{}_model_{}/{}_model_{}.nc".format(data_dir, exp_code, exp_code, seeds[0],
                                                   exp_code, seeds[0])
import xarray
ds = xarray.open_dataset(ds_path).sel(step=step)
#%%
assert np.all(np.abs(ds.design.values - nn_mdl.model(None)) < 1e-2)
