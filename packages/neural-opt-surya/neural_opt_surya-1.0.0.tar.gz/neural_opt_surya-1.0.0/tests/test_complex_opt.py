#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  3 11:04:06 2022

@author: surya
Test LBFGS on complex optimization
1. Treat the complex variable z = x+iy as a (x,y)
2. Perform optimization
"""
#%%
import tensorflow as tf
import scipy.optimize as so
import numpy as np
x = tf.Variable(np.array(1.0), dtype =tf.float64)
y = tf.Variable(np.array(1.0), dtype =tf.float64)

with tf.GradientTape() as t:
    z = tf.dtypes.complex(x,y)
    fval = tf.math.abs(z)**2
grad = t.gradient(fval,z)# [x,y])
#Correctly calculates the Wirtinger derivative [w.r.t to z*]
#%%

