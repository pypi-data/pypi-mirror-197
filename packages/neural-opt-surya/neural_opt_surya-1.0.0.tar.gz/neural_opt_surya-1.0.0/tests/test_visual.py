#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 14:17:22 2022

@author: surya
Test visualization
"""
#%%
import tensorflow as tf
import sys
sys.path.insert(1,"..")
from topopt.nso import topo_api
from topopt.nso import models
from topopt.nso import problems
from topopt.visual_tools import utilities_surya as util
import xarray
import os
import numpy as np
from topopt.visual_tools import Visualization as vis
from topopt.visual_tools import nn_model_v2 as nn
import topopt.visual_tools.trajectory_plots as tplots
import pickle
#%%
# Choose an experiment
data_dir ='/media/surya/surya_2/phd1/Masters_extension/data_masters/lenscale_expts_new/'
exp_name = 'TacfUHN64_32x16' 
use_pixmdl = True
nelx = 64
prob_code = exp_name[2:4]
model_args =   {
                'vol_const_hard': True,
                #'sampling': {'default':(int(rmin),int(rmax))},
                'var_batch': True,
                'resolution': 1,
                'depth':5,
                'fourier_on' : False
                }
t_args = {
          'cone_filter': False,
          'cont_scheme' : False ,
        'alpha_start' : 0.1,
        'del_alpha':0.05,
        'alpha_end':100,
        'p_start':2,
        'p_end':4.01,
        'del_p':0.01,
        }
#%%
# load main dataset & expt_details
ds = xarray.open_dataset("{}/{}/{}.nc".format(data_dir, exp_name, exp_name))
exp_details = pickle.load(open("{}/{}/{}_expt_details".format(data_dir, exp_name, exp_name),'rb'))
indices = exp_details['indices']
# Find typical seeds
prob_code_det = {'tr' : 'tensile_rod',
                 'cf': 'cantilever_fine',
                 'cb': 'causeway_bridge'
                }
problem = problems.PROBLEMS_BY_NAME[prob_code_det[prob_code]](nelx = nelx, width=32, height=16   )
args = topo_api.specified_task(problem)
vf = problem.density
typ_seeds, real_comp, medianval = util.find_typical_seeds(ds, vf=vf)
assert len(typ_seeds) >= 2
seeds = typ_seeds[:2]
#%% 
# get all the weight filenames
wt_files ={}
for seed in seeds:
    wt_steps =[]
    for step in indices[str(seed)]:
        wts_path = "{}{}/{}_model_{}/weights_{}.p".format(data_dir, exp_name, 
                                                      exp_name, seed, step)  
        wt_steps.append(wts_path)
    wt_files[str(seed)] = wt_steps

# create results folder if it doesnot exist
if not os.path.exists("{}{}/results_tst".format(data_dir,exp_name)):
    os.mkdir("{}{}/results_tst".format(data_dir,exp_name))
    
folder1 =  "{}{}/results_tst/random2d".format(data_dir, exp_name)
if not os.path.exists(folder1):
    os.mkdir(folder1)
    
folder2 =  "{}{}/results_tst/pca2d".format(data_dir, exp_name)
if not os.path.exists(folder2):
    os.mkdir(folder2)
    
#%%   
# ---------------------
seed = typ_seeds[0]
step=149
# ---------------------
# Find the penalty and alpha values
alphavals = np.arange(t_args['alpha_start'], t_args['alpha_end'], t_args['del_alpha'])
if t_args['cont_scheme']:
    pvals = np.arange(t_args['p_start'], t_args['p_end'], t_args['del_p'])    
else:
    pvals = np.ones(len(alphavals)) * t_args['p_start']
    
tf.keras.backend.clear_session()
model = models.TounnModel(seed = seed, args = args, **model_args) 
nn_mdl = nn.Tensorflow_NNModel(model, cone_filter = t_args['cone_filter'],
                               vol_const_hard= model_args['vol_const_hard'],
                               pixelmodel_init= use_pixmdl, pvalue ='NA')
# get all filenames for this seed
wt_steps =[]

wts_path = "{}{}/{}_model_{}/weights_{}.p".format(data_dir, exp_name, 
                                              exp_name, seed, step)  
wt_steps.append(wts_path)
    
# random filter normalized plots
max_ind = max(indices[str(seed)])
path_rand=  "{}{}/results_tst/random2d/seed_{}".format(data_dir, exp_name, seed)
if not os.path.exists(path_rand):
    os.mkdir(path_rand)
path_pca=  "{}{}/results_tst/pca2d/seed_{}".format(data_dir, exp_name, seed)
if not os.path.exists(path_pca):
    os.mkdir(path_pca)
    
# Correct the penalty and alphavalues for the current seed    
if len(pvals) < max_ind:
    temp1 =  pvals[-1] * np.ones(max_ind+1 - len(pvals))        
    pvals = np.concatenate((pvals, temp1))
if len(alphavals) < max_ind:
    temp2 =  alphavals[-1] * np.ones(max_ind+1 - len(alphavals))
    alphavals = np.concatenate((alphavals,temp2))
    
# start plotting   

print("---------------> Plotting step = ", step)
# ToDo : set the nn_model state to teh required location
nn_mdl.penalty = pvals[step]
nn_mdl.alphaval = alphavals[step]
nn_mdl.set_parameters(nn_mdl.load_parameters(wt_steps[0]))

filename = path_rand + "/step_"+str(step)
#check_loss.append(nn_mdl.calc_loss())
vis.visualize(nn_mdl, wt_steps[0:step+1], N = 25, path_to_file =filename
          , random_dir=True, proz=1)               
# if step >= 2:
#     filename = path_pca + "/step_"+str(step)
#     vis.visualize(nn_mdl, wt_steps[0:step+1], N = 25, path_to_file =filename
#               , random_dir=False, proz=1)
#%%
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['svg.fonttype'] = 'none'
fig, ax = plt.subplots(1,1, frameon=True)
results_dir = "{}{}/results_tst/".format(data_dir,exp_name)
r_dir = results_dir+'random2d/'
saved_file = "{}/seed_{}/step_{}.npz".format(r_dir,seed,step)
a = tplots.plot_loss_2D(saved_file, ax, is_log =True)
plt.show()
#%%
plt.close('all')
