#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 11 17:10:19 2022

@author: surya
Test FourierTouNN Model - from Shushu
"""
#%%
import sys
import os
cwd = '/home/surya/Desktop/PhD_work/Masters_extension/neural_opt/'
sys.path.append(os.path.join(cwd, 'topopt', 'nso'))
os.chdir("topopt")
import autograd
import autograd.core
import autograd.numpy as np
from autograd import elementwise_grad as egrad
from nso import topo_api
import tensorflow as tf
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)
layers = tf.keras.layers

def batched_topo_loss(params, envs):
  losses = [env.objective(params[i], volume_contraint=True)
            for i, env in enumerate(envs)]
  return np.stack(losses)


def convert_autograd_to_tensorflow(func):#S:func is completely written in numpy autograd
    @tf.custom_gradient
    def wrapper(x):
        vjp, ans = autograd.core.make_vjp(func, x.numpy())
        def first_grad(dy):
            
            @tf.custom_gradient
            def jacobian(a):
                vjp2, ans2 =  autograd.core.make_vjp(egrad(func), a.numpy())
                # def hessian(ddy):
                #     return ddy* egrad(egrad(func))(a.numpy())
                return ans2,vjp2 # hessian                    
                    
            
            return dy* jacobian(x)  
        return ans, first_grad
    
    return wrapper

def set_random_seed(seed):
  if seed is not None:
    np.random.seed(seed)
    tf.random.set_seed(seed)


class Model(tf.keras.Model):

  def __init__(self, seed=None, args=None):
    super().__init__()
    set_random_seed(seed)
    self.seed = seed
    self.env = topo_api.Environment(args)

  def loss(self, logits):
    # for our neural network, we use float32, but we use float64 for the physics
    # to avoid any chance of overflow.
    # add 0.0 to work-around bug in grad of tf.cast on NumPy arrays
    logits = 0.0 + tf.cast(logits, tf.float64)
    f = lambda x: batched_topo_loss(x, [self.env])
    losses = convert_autograd_to_tensorflow(f)(logits)
    return tf.reduce_mean(losses)

class TounnModel(Model):
    # inputDim = 2*150; # x and y coordn of the point
    outputDim = 1; # if material/void at the point
    
    def __init__(self, seed=0, args=None, depth=2, 
                 width=10, fourier_on = True, n_ffeatures =150,
                 rmin=3, rmax=16):
      super().__init__(seed, args)
      set_random_seed(seed)
      self.seed = seed
      self.args = args
      h = self.args['nely']
      w = self.args['nelx']
      if fourier_on:
          inputDim = 2*n_ffeatures # (cos + sine) x n_fourier_features 
      else:          
          inputDim =2 #(x,y) only
          
      hw = h*w
      net = inputs = layers.Input((inputDim,), batch_size=hw)  ## h * w
      initializer = tf.keras.initializers.GlorotNormal()
      
      for i in range(depth):
          l = layers.Dense(units=width,
                           kernel_initializer=initializer, 
                           bias_initializer='zeros', activation =None)     
          net = l(net)
          net = layers.BatchNormalization(momentum=0.01)(net, training=True)
          net = tf.nn.leaky_relu(net)
      l = layers.Dense(units=self.outputDim)       
      net = l(net)

      # net = tf.keras.layers.Activation("sigmoid")(net)
      output = tf.transpose(tf.reshape(net, [1,w,h]), perm=[0,2,1])
      self.core_model = tf.keras.Model(inputs=inputs, outputs=output)

      self.xy = self.generatePoints(self.args['nelx'], self.args['nely'])
      if fourier_on:
          coordnMap = np.zeros((2, n_ffeatures)) # random fourier features
          for i in range(coordnMap.shape[0]):
            for j in range(coordnMap.shape[1]):
              coordnMap[i,j] = np.random.choice([-1.,1.])*\
                          np.random.uniform(1./(2*rmax), 1./(2*rmin))
          self.coordnMap = tf.constant(coordnMap)
          self.inputs = self.applyFourierMapping(self.xy)
      else:
          self.inputs = self.xy
        
    def call(self, inputs=None):
      return self.core_model(self.inputs)

    def generatePoints(self, nx, ny, resolution = 1):
        # generate points in elements
      ctr = 0
      xy = np.zeros((resolution*nx*resolution*ny,2))
      for i in range(resolution*nx):
          for j in range(resolution*ny):
              xy[ctr,0] = (i + 0.5)/resolution
              xy[ctr,1] = (j + 0.5)/resolution

              ctr += 1
      return xy

    def applyFourierMapping(self, x):
      c = tf.cos(2*np.pi*tf.matmul(x,self.coordnMap))
      s = tf.sin(2*np.pi*tf.matmul(x,self.coordnMap))
      xv = tf.concat((c,s), axis = 1)
      return xv
#%%
args = {'nelx':32, 'nely': 64,'young': 1,
      'young_min': 1e-9,
      'poisson': 0.3,
      'g': 0}
model = TounnModel(seed =0, args=args )
model(None)
#%%
import torch
import torch.nn as nn
import numpy as np
class TopNet(nn.Module):
    def __init__(self, nnSettings, inputDim):
        self.inputDim = inputDim; # x and y coordn of the point
        self.outputDim = 1; # if material/void at the point
        super().__init__();
        self.layers = nn.ModuleList();
        # manualSeed = 1234; # NN are seeded manually
        # set_seed(manualSeed);
        current_dim = self.inputDim;
        for lyr in range(nnSettings['numLayers']): # define the layers
            l = nn.Linear(current_dim, nnSettings['numNeuronsPerLyr']);
            nn.init.xavier_normal_(l.weight);
            nn.init.zeros_(l.bias);
            self.layers.append(l);
            current_dim = nnSettings['numNeuronsPerLyr'];
        self.layers.append(nn.Linear(current_dim, self.outputDim));
        self.bnLayer = nn.ModuleList();
        for lyr in range(nnSettings['numLayers']): # batch norm
            self.bnLayer.append(nn.BatchNorm1d(nnSettings['numNeuronsPerLyr']));

    def forward(self, x):
        m = nn.LeakyReLU();
        ctr = 0;
        for layer in self.layers[:-1]: # forward prop
            x = m(self.bnLayer[ctr](layer(x)));
            ctr += 1;
        rho = 0.01 +torch.sigmoid(self.layers[-1](x)).view(-1); # grab only the first output
        return  rho;
#%%
nn_settings ={'numLayers': 2, 'numNeuronsPerLyr':10}
inputDim = 150
inp = torch.from_numpy(np.random.uniform(size = (2,150))).to(torch.float32)
mdl = TopNet(nn_settings,inputDim)
val = mdl.forward(inp)
#%%