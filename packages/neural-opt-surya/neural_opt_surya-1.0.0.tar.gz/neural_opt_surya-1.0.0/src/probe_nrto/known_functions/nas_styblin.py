#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 14:39:00 2022

@author: surya
Optuna: for neural search
Hyper parameter opt to find the optimal neural architecture for a function [More inits to global minima]

On Optuna:
    1. Study -  Details of all the trials - Entire details
        a. Can continue the study for more trails from where it was left off
    2. trial - One trial per run of the optimization [for each call of the objective with the hyper-params]
    3. Suggest api - Categorical, int or float x (step, log) [to define the parameter values]
        a. Difficulty increases exponentially with the number of parameters
    4.  Pruning algorithms and samplers
"""
#%%
import os
import sys
cwd = os.getcwd()
sys.path.append(os.path.join(cwd, 'benchmark_fns'))
import optuna 
import tensorflow as tf
import obj_models as models
import obj_funcs as of
import obj_utilities as utils
import autograd.numpy as np
import pickle
#%%
exp_name = 'optuna_1'
data_dir = '/home/surya/Desktop/PhD_work/Masters_extension/data_masters/' 

os.chdir(data_dir)
if not os.path.exists(str(exp_name)):
    os.makedirs(str(exp_name))
os.chdir( data_dir+str(exp_name))

def objective(trial):
    # define search space
    depth = trial.suggest_int("depth", 1, 11)
    width = trial.suggest_int("width", 5, 300, step = 10) # Should it be width per layer? No--too manyparameters
    activation = trial.suggest_categorical("act", ["tanh", "relu", "selu", "leaky", 'swish']) 
    if activation == 'leaky':
        activation = tf.nn.leaky_relu
        
    if activation in ['relu', 'leaky', 'swish']:    
        init = tf.keras.initializers.HeNormal # https://arxiv.org/pdf/1710.05941v2.pdf
    elif activation in ['selu']:
        init = tf.keras.initializers.LecunNormal # https://mlfromscratch.com/activation-functions-explained/#/
    else:
        init = tf.keras.initializers.GlorotNormal
        
    bias_val = trial.suggest_float("bias", 2, 4, step = 0.25)
    #init_scale = # conditional on the initializtion -- maybe use default value
    args = {'dim':2}
    all_inits = []
    max_iterations = 30
    func_obj = of.Styblinski(seed = 0, dim = args['dim']) # Need to check
    func_obj.o = 0
    glob_val = func_obj.global_minval # Need to check
    limit = np.abs(0.05 * glob_val)
    hits = {'pix':0, 'mdl':0}
    n_seeds = 2
    for i in range(n_seeds):
        tf.keras.backend.clear_session()
        model = models.FCNN_simple(seed=i, args = args, depth =depth, width= width,
                                   kernel_init = init, activation =activation, bias_val =bias_val)
        logit = model(None)
        # make pixel model
        pixmdl = models.PixelModel(seed = 0, args = args)
        pixmdl.z = tf.Variable(logit, trainable= True, dtype = tf.float32)
        # store init
        all_inits.append(logit.numpy()[0,:])
        # train the models
        dsmdl,_ = utils.train_lbfgs(model, func_obj, max_iterations)
        dspix,_ = utils.train_lbfgs(pixmdl, func_obj, max_iterations)
        # Check the value w.r.t global min
        glob_mdl = dsmdl.isel(step=-1).loss.values
        glob_pix = dspix.isel(step=-1).loss.values
        # count the relative number of hits = (hits neural/ total hits)
        if np.abs(glob_val - glob_pix) <= limit:
            hits['pix']+=1
        if np.abs(glob_val - glob_mdl) <= limit:
            hits['mdl']+=1
        del model
        del pixmdl    
    # Use stored inits to make det(cov(init))/ det(uniform)    
    totalhits = hits['mdl'] + hits['pix']
    if totalhits == 0:
        obj_val = 0
        return obj_val
    
    det = np.linalg.det(np.cov(np.array(np.array(all_inits).T))) # have to check
    scale = np.linalg.det(np.cov(np.random.uniform(0, 1, size = (n_seeds,2)).T)) 
    o1 = 0.9*(hits['mdl']/ totalhits)
    o2 = 0.1*det/scale
    print("=====================O1:{}, O2:{}==================".format(o1,o2))
    obj_val = o1 + o2
    all_details ={'pixhits': hits['pix'], 'modelhits': hits['mdl'], 'o1': o1, 'o2':o2,
                  'det': det, 'scale': scale}
    pickle.dump(all_details, open("Details_{}.p".format(trial.number), 'wb'))
    return obj_val
#%%
study = optuna.create_study(sampler=optuna.samplers.RandomSampler(seed = 0),
                            direction="maximize")
                            #pruner=optuna.pruners.MedianPruner())

study.optimize(objective, n_trials=3)
# Save study!

pickle.dump(study, open("study_1.p", 'wb'))
print("completed")
        
    

