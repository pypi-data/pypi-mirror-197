#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 21:53:29 2022

@author: surya
test filter normalization
"""
#%%
import topopt.nso.problems as problems
import topopt.nso.models as models
import topopt.nso.topo_api as topo_api
import topopt.visual_tools.nn_model_v2 as nn

problem =problems.tensile_rod(16)
args = topo_api.specified_task(problem)
model = models.TounnModel(seed=0, args = args)
newmdl = nn.Tensorflow_NNModel(model) 
#%%
parameter = newmdl.get_parameters(all_params = True)
parlis = list(parameter.values())
#%%
import numpy as np
theta = parlis[0]
d = np.random.normal(size= theta.shape)
norm_d_onego = d * (np.linalg.norm(theta)/np.linalg.norm(d))
#%%
norm_d_filterwise = d.copy()
for i in range(theta.shape[1]):
    th = theta[:,i]
    norm_d_filterwise[:,i] = d[:,i] * (np.linalg.norm(th)/np.linalg.norm(d[:,i])) 
#%%
# compare --> not the same   
assert np.all(np.abs(norm_d_filterwise - norm_d_onego) < 1e-3)