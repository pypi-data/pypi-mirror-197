#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 11:44:30 2022

@author: surya

testing the gradient of cone-filter
"""
#%%
import tensorflow as tf
import sys
import os
# Add nso folder to path
cwd = os.getcwd()
sys.path.append(os.path.join(cwd, 'topopt', 'nso'))

import topo_api
import models
import problems
import autograd_lib
problem = problems.michell_centered_both(2, width =2, height = 4)
args = topo_api.specified_task(problem)
model = models.TounnModel(seed=1, args = args, vol_const_hard= False)
t_args = {
    'vol_const_hard' : False,
    'cont_scheme' : False,
    'alpha_start' : 0.2,
    'del_alpha':0.2,
    'alpha_end':100,
    'conv_filter':True,
    'p_start':1,
    'p_end':8,
    'del_p':0.2,
    'scale_loss':True}
#%%
def cone(x, args):
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
# everytime grade is prrinted - the erro message shows up again
# The rror is that Output seems independent of input.
#  warnings.warn("Output seems independent of input.")
#%%
# check numpy gradients!
args = model.env.args
logits = model(None)
shape = (args['nely'], args['nelx'])
logits = 0.0 + tf.cast(logits, tf.float64)
x = tf.reshape(logits, shape)
x_np = x.numpy()
y = autograd_lib.cone_filter(x_np, args['filter_width'], args['mask'])
cone_f = lambda x : autograd_lib.cone_filter(x, args['filter_width'], args['mask'])
#%%
import autograd
jac = autograd.elementwise_grad(cone_f)(x_np)
#### Final jac == grad from above cell-- so its working! - The error message is justa n artifact