#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 17 10:45:05 2022

@author: surya
Test implementation of continuation scheme and soft volume constraint
Also, testing two ways of including gradient calculation of loss
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
# Add nso folder to path
cwd = os.getcwd()
sys.path.append(os.path.join(cwd, 'topopt', 'nso'))

import topo_api
import models
import train_new as train
import problems
import topo_physics
import autograd.numpy as np
import autograd_lib
problem = problems.michell_centered_both(2, width =2 , height=4)
args = topo_api.specified_task(problem)
model = models.TounnModel(seed=1, args = args, vol_const_hard= False)
t_args = {
    'vol_const_hard' : False,
    'cont_scheme' : False,
    'alpha_start' : 0.2,
    'del_alpha':0.2,
    'alpha_end':100,
    'conv_filter':False,
    'p_start':1,
    'p_end':8,
    'del_p':0.2,
    'scale_loss':True}

#%%
# testing current implementgation of gradient for lbfgs_soft
def mean_density(logits, args, cone_filter = False):
    """  To include mean density calculations in the gradienttape for loss sensitivities"""
    shape = (args['nely'], args['nelx'])
    logits = 0.0 + tf.cast(logits, tf.float64)
    mask = tf.constant(args['mask'], dtype =tf.float64)
    
    x = tf.reshape(logits, shape)
    x = x * mask
    if cone_filter:
      f = lambda y : autograd_lib.cone_filter(y, args['filter_width'], args['mask'])
      x = models.convert_autograd_to_tensorflow(f)(x)   
      print("Inside filter!!!!")    
    cur_density = tf.reduce_mean(x)/ tf.reduce_mean(mask)
    return cur_density

args = model.env.args 
tvars = model.trainable_variables    
pval = [3.0]
count = 0 
alpha_val = [0.1]
model.J0 = 239.1
with tf.GradientTape() as t:
  t.watch(tvars)
  logits = model(None)
  J = model.loss(logits, False, t_args['conv_filter'], pval[count])  
  cur_density = mean_density(logits, args, t_args['conv_filter'])
  loss = tf.cast(alpha_val[count]*((cur_density/args['volfrac']) - 1)**2, 
                       dtype=tf.float64) + J/model.J0 
grads = t.gradient(loss, tvars)
#%%
# Tesing just cone filter
def cone(x, args, apply = True):
    if apply:
        f = lambda y : autograd_lib.cone_filter(y, args['filter_width'], args['mask'])
        x = models.convert_autograd_to_tensorflow(f)(x)
    return x

args = model.env.args
logits = model(None)
shape = (args['nely'], args['nelx'])
logits = 0.0 + tf.cast(logits, tf.float64)
x = tf.reshape(logits, shape)

with tf.GradientTape() as t:
    t.watch(x)
    y = cone(x, args)
grad = t.gradient(y,x)    
    
#%%
#Test LBFGS
#1. Hard volume constraint
#   - Computational graph seems ok 
#   - Tested against original train.py --works well
#2. Soft volume constraint
#   - Same result with a constant alphavalue ~90 to 100
#   - result depends on the scheme chosen
#3. Hard + continuation scheme
# - Works well
#4. Soft + continuation scheme

if os.path.exists("./n_iterations_lbfgs.txt"):
    os.remove("./n_iterations_lbfgs.txt")
ds,indices = train.train_lbfgs_soft(model, 10, save_intermediate_designs=False, 
                                conv_criteria = False, t_args = t_args)

#%%
# With adam
lr = 0.01
ds,_ = train.train_tf_opt_soft(
    model, 500, optimizer=tf.keras.optimizers.Adam(lr), 
    save_intermediate_designs=False, 
    conv_criteria = False, t_args = t_args)
#%%
if os.path.exists("./n_iterations_lbfgs.txt"):
    os.remove("./n_iterations_lbfgs.txt")
# ds_all = []
# for i in range(6):
#     tf.keras.backend.clear_session()
#     model = models.CNNModel_c2dt_corr(seed=i, args = args, vol_const_hard= True)
#     ds,indices = train.train_lbfgs(model, 75, save_intermediate_designs=False, 
#                                conv_criteria = False, t_args = t_args)
#     ds_all.append(ds.expand_dims({'seed':[i]}))
#     del model
# import xarray
# fds = xarray.merge(ds_all)
#%%
# Gradient 1
model.J0 = 50
args = model.env.args  
tvars = model.trainable_variables    
with tf.GradientTape() as t:
  t.watch(tvars)
  logits = model(None)
  J = model.loss(logits, False, True, 3.0)  
  logits = 0.0 + tf.cast(logits, tf.float64)
  cur_density = topo_physics.mean_density(logits.numpy().reshape(args['nely'], args['nelx']),
                                  args, False, True)
  loss = tf.cast(100*((cur_density/args['volfrac']) - 1)**2, 
                       dtype=tf.float64) + J/model.J0 
grads = t.gradient(loss, tvars)

#%%
# Gradient version 2 -- This is the correct way
model.J0 = 50
import autograd.numpy as np
import autograd_lib
def mean_density(logits, args, cone_filter = False):
    shape = (args['nely'], args['nelx'])
    x = tf.reshape(0.0 + tf.cast(logits, tf.float64), shape)
    x = x * args['mask']
    if cone_filter:
      f = lambda x : autograd_lib.cone_filter(x, args['filter_width'], args['mask'])
      x = models.convert_autograd_to_tensorflow2(f)(x)    
    cur_density = tf.reduce_mean(x)/ np.mean(args['mask'])
    return cur_density

args = model.env.args  
tvars = model.trainable_variables    
with tf.GradientTape() as t:
  t.watch(tvars)
  logits = model(None)
  J = model.loss(logits, False, True, 3.0)  
  cur_density = mean_density(logits, args, True)
  loss = tf.cast(100*((cur_density/args['volfrac']) - 1)**2, 
                       dtype=tf.float64) + J/model.J0 
grads2 = t.gradient(loss, tvars)
#%%
logits = model(None)
cur_densitynp = topo_physics.mean_density(logits.numpy().reshape(args['nely'], args['nelx']),
                                args, False, True)

cur_density = mean_density(logits, args, True)
#%%
# y = x^2, z =x^3 and c = y+z What is dc/dx
x = tf.Variable(1.0)
with tf.GradientTape() as t:
    y = x**2
    z = 1.0#x**3
    c = y+z
g =t.gradient(c,x)

#%%
# Simpler
import autograd.numpy as np
import autograd_lib
def mean_density(logits, args, cone_filter = False):
    shape = (args['nely'], args['nelx'])
    x = tf.reshape(0.0 + tf.cast(logits, tf.float64), shape)
    x = x * args['mask']
    if cone_filter:
      f = lambda x : autograd_lib.cone_filter(x, args['filter_width'], args['mask'])
      x = models.convert_autograd_to_tensorflow2(f)(x)    
    cur_density = tf.reduce_mean(x)/ np.mean(args['mask'])
    return cur_density
model.J0 = 50
args = model.env.args  
tvars = model.trainable_variables    
with tf.GradientTape() as t:
  t.watch(tvars)
  logits = model(None)
  J = model.loss(logits, False, False, 3.0)  
  logits = 0.0 + tf.cast(logits, tf.float64)
  cur_density = mean_density(logits, args, False)#topo_physics.mean_density(logits.numpy().reshape(args['nely'], args['nelx']),
                                  #args, False, False)
  loss = tf.cast(100*((cur_density/args['volfrac']) - 1)**2, 
                       dtype=tf.float64) + J/model.J0 
grads = t.gradient(loss, tvars)

#%%
model.J0 = 50
args = model.env.args  
tvars = model.trainable_variables 
cur_density = mean_density(logits, args, False)#topo_physics.mean_density(model(None).numpy().reshape(args['nely'], args['nelx']),
                                  #args, False, False)   
with tf.GradientTape() as t:
  t.watch(tvars)
  logits = model(None)
  J = model.loss(logits, False, False, 3.0)  
  logits = 0.0 + tf.cast(logits, tf.float64)
  loss = tf.cast(100*((cur_density/args['volfrac']) - 1)**2, 
                       dtype=tf.float64) + J/model.J0 
grads2 = t.gradient(loss, tvars)
    

 
