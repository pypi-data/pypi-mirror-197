#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 09:40:25 2022

@author: surya
To test teh cone filter
compare results with test_filter.m
"""
#%%
import os
import sys
cwd = os.getcwd()
sys.path.append(os.path.join(cwd, 'topopt', 'nso'))
import problems
import topo_api
import models
import autograd_lib as al
import tensorflow as tf
#%%
# Find compliance using hoyer's code and new code'
nelx = 4
problem = problems.mbb_beam(nelx,0.2, width =2, height=1)
args = topo_api.specified_task(problem)
# assert args['width'] == args['nelx'] and args['height'] == args['nely']
#%%
model =models.PixelModel(seed=0, args= args)
def my_tf_round(x, decimals = 2):
    multiplier = tf.constant(10**decimals, dtype=x.dtype)
    return tf.round(x * multiplier) / multiplier

zval = tf.random.normal(shape = (1,args['nely'],nelx), mean = 0.2, stddev = 0.05)
model.z = tf.Variable(my_tf_round(zval), trainable= True, dtype = tf.float32)
logits = model(None)
params = logits.numpy()
env_obj = topo_api.Environment(args)
x = env_obj.reshape(params)
#%%
args['filter_width'] = 1
elem_size = args['width']/ nelx
x_phy = al.cone_filter(x, args['filter_width'] /elem_size, args['mask'])
