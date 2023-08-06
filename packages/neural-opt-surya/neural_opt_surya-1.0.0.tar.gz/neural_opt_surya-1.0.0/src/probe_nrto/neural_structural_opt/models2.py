#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 16:09:51 2022

@author: surya
"""

import autograd
import autograd.core
import autograd.numpy as np
from autograd import elementwise_grad as egrad
from . import topo_api
import tensorflow as tf

layers = tf.keras.layers


def batched_topo_loss(params, envs, vol_const_hard = True, cone_filter=True, p =3.0):
    """ 
    vol_const_hard :  Whether to apply hard volume constraint [Using root finder]
        as done in Hoyer et al paper
    """
    losses = [env.objective(params[i], volume_contraint=vol_const_hard, 
                            cone_filter=cone_filter, p=p)
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

def convert_autograd_to_tensorflow2(func):
  @tf.custom_gradient
  def wrapper(x):
    vjp, ans = autograd.core.make_vjp(func, x.numpy())
    return ans, vjp
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
    self.J0 = 0.0 # Compliance with uniform grey init
    # self.p_value = 1.0 # penality for continuation scheme
    # self.alpha_reg = 100.0 # The regularizer for loss function

  def loss(self, logits, vol_const_hard =True, cone_filter=True, p = 3.0):
    # for our neural network, we use float32, but we use float64 for the physics
    # to avoid any chance of overflow.
    # add 0.0 to work-around bug in grad of tf.cast on NumPy arrays
    logits = 0.0 + tf.cast(logits, tf.float64)
    f = lambda x: batched_topo_loss(x, [self.env], 
                                    vol_const_hard = vol_const_hard,
                                    cone_filter=cone_filter, p=p)
    losses = convert_autograd_to_tensorflow(f)(logits) 
    return tf.reduce_mean(losses)

## Generalized F-TOuNN model -- contains 2 NNs

class GTounnModel(Model):
    # inputDim = 2*150; # x and y coordn of the point
    outputDim = 1; # if material/void at the point
    
    def __init__(self, seed=0, args=None, firstnet =
                 {'depth': 2, 'width':[20, 300], 'train': False},
                     depth=1, width=20, vol_const_hard= False):
      super().__init__(seed, args)
      set_random_seed(seed)
      self.seed = seed
      self.args = args
      self.firstnet = firstnet
      h = self.args['nely']
      w = self.args['nelx']
      inputDim = firstnet['width'][-1]          
      hw = h*w
      net = inputs = layers.Input((inputDim,), batch_size=hw)  ## h * w # only works with resolution = 1
      initializer = tf.keras.initializers.GlorotNormal()
      
      for i in range(depth):
          l = layers.Dense(units=width,
                           kernel_initializer=initializer, 
                           bias_initializer='zeros', activation =None)     
          net = l(net)
          net = layers.BatchNormalization(momentum=0.01)(net, training=True)
          net = tf.nn.leaky_relu(net, alpha =0.01) #to be consistent with PyTorch
      l = layers.Dense(units=self.outputDim, kernel_initializer=initializer, 
                           bias_initializer='zeros', activation =None)       
      net = l(net)
      if not vol_const_hard: # Need to verify -done
        net = tf.keras.layers.Activation("sigmoid")(net)
      output = tf.transpose(tf.reshape(net, [1,w,h]), perm=[0,2,1])
      self.core_model = tf.keras.Model(inputs=inputs, outputs=output)

      self.xy = self.generatePoints(self.args['nelx'], self.args['nely'])
      self.inputs = self.applyfirstnet(self.xy) 
        
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

    def applyfirstnet(self, x):
      h = self.args['nely']
      w = self.args['nelx']
      net = inputs = layers.Input((2,), batch_size=h*w)
      initializer = tf.keras.initializers.GlorotNormal()
      for i in range(self.firstnet['depth']):
          net = layers.Dense(units=self.firstnet['width'][i],
                                     kernel_initializer=initializer, 
                                     bias_initializer='zeros', activation ='tanh', 
                                     trainable = False)(net) 
      output = net
      mdl2 = tf.keras.Model(inputs=inputs, outputs=output)  
      xv = mdl2(x)    
      return xv

#%%
def global_normalization(inputs, epsilon=1e-6):
  mean, variance = tf.nn.moments(inputs, axes=list(range(len(inputs.shape))))
  net = inputs
  net -= mean
  net *= tf.math.rsqrt(variance + epsilon)
  return net


def UpSampling2D(factor):
  return layers.UpSampling2D((factor, factor), interpolation='bilinear')
#changed interpolation to 'nearest'

def Conv2D(filters, kernel_size, **kwargs):
  return layers.Conv2D(filters, kernel_size, padding='same', **kwargs)

#New CNN Model using conv2dtranspose

def Conv2DT(filters, kernel_size,resize, **kwargs):
    if resize == 2:
        return layers.Conv2DTranspose(filters= filters
            ,kernel_size =kernel_size,strides = 2,padding ='same',**kwargs)
    elif resize == 1:
        return layers.Conv2DTranspose(filters= filters
            ,kernel_size =kernel_size,strides = 1,padding ='same',**kwargs)
    else:
        print('Given resize is not compatible')
        return None
    
class AddOffset(layers.Layer):

  def __init__(self, scale=1):
    super().__init__()
    self.scale = scale

  def build(self, input_shape):
    self.bias = self.add_weight(
        shape=input_shape, initializer='zeros', trainable=True, name='bias')

  def call(self, inputs):
    return inputs + self.scale * self.bias

# Hoyer's architecture with CONV2dT - with controlled freezing - pending
class ConvModel(Model):

  def __init__(
      self,
      seed=0,
      args=None,
      latent_size=128, 
      dense_channels=32,
      resizes=(1, 2, 2, 2, 1),
      conv_filters=(128, 64, 32, 16, 1),
      offset_scale=10,
      kernel_size=(5, 5),
      latent_scale=1.0,
      dense_init_scale=1.0,
      activation=tf.keras.activations.tanh,
      conv_initializer=tf.initializers.VarianceScaling,
      normalization=global_normalization,
      latent_trainable = True,
      vol_const_hard = True,      
  ):
    super().__init__(seed, args)

    if len(resizes) != len(conv_filters):
      raise ValueError('resizes and filters must be same size')

    #Make model
    activation = layers.Activation(activation)
    total_resize = int(np.prod(resizes))
    h = self.env.args['nely'] // total_resize
    w = self.env.args['nelx'] // total_resize 
    net = inputs = layers.Input((latent_size,), batch_size=1)
        
    filters = h * w * dense_channels    
    dense_initializer = tf.initializers.orthogonal(
        dense_init_scale * np.sqrt(max(filters / latent_size, 1)))
    net = layers.Dense(filters, kernel_initializer=dense_initializer)(net)    
    net = layers.Reshape([h, w, dense_channels])(net)
    
    for resize, filters in zip(resizes, conv_filters):
      net = activation(net)
      net = normalization(net)
      net = Conv2DT(filters, kernel_size, resize,
                    kernel_initializer= conv_initializer)(net)      
      if offset_scale != 0:
        net = AddOffset(offset_scale)(net)   
    
    if not vol_const_hard: # Need to verify -done
      net = tf.keras.layers.Activation("sigmoid")(net)       
    outputs = tf.squeeze(net, axis=[-1])
    self.core_model = tf.keras.Model(inputs=inputs, outputs=outputs)

    latent_initializer = tf.initializers.RandomNormal(stddev=latent_scale)
    self.z = self.add_weight(
            shape=inputs.shape, initializer=latent_initializer, name='z',
            trainable = latent_trainable)  
    
  def call(self, inputs=None):
    return self.core_model(self.z)
#%%
# Equivalent CNN in tounn
class RffCNNModel(Model):
    # inputDim = 2*150; # x and y coordn of the point
    outputDim = 1; # if material/void at the point
    
    def __init__(self, seed=0, args=None, fourier_on = True, n_ffeatures =150,
                 rmin=6, rmax=30, vol_const_hard= False, filters =(20,1)
                 ):
      super().__init__(seed, args)
      #set_random_seed(seed)
      self.seed = seed
      self.args = args
      h = self.args['nely']
      w = self.args['nelx']
      if fourier_on:
          features = 2*n_ffeatures # (cos + sine) x n_fourier_features 
      # else:          
      #     inputDim =2 #(x,y) only          
      total_inp = h*w*features     
      net = inputs = layers.Input((total_inp,), batch_size=1)  
      net  = layers.Reshape([h, w, features])(net)     
      
      for i in filters:
          net = global_normalization(net)
          net = Conv2DT(i, kernel_size =(5,5), 
                        resize=1,kernel_initializer= tf.initializers.VarianceScaling)(net)    
          net = AddOffset(offset_scale=10)(net)

      if not vol_const_hard: # Need to verify -done
        output = tf.keras.layers.Activation("sigmoid")(net)

      self.core_model = tf.keras.Model(inputs=inputs, outputs=output)

      self.xy = self.generatePoints(self.args['nelx'], self.args['nely'],
                                        width = args['width'], height =args['height'])
      if fourier_on:
          coordnMap = np.zeros((2, n_ffeatures)) # random fourier features
          for i in range(coordnMap.shape[0]):
            for j in range(coordnMap.shape[1]):
              coordnMap[i,j] = np.random.choice([-1.,1.])*\
                          np.random.uniform(1./(2*rmax), 1./(2*rmin))
          self.coordnMap = tf.constant(coordnMap)
          self.z = self.applyFourierMapping(self.xy) # inputs
      else:
          self.z = self.xy
        
    def call(self, inputs=None):
        # if inputs is not None:
        #     ft_xy = self.applyFourierMapping(inputs)
        #     return self.core_model(ft_xy)        
        return self.core_model(self.z)
  
    def predict(self, xy_pts):
        ft_xy = self.applyFourierMapping(xy_pts)
        return self.core_model(ft_xy)
    
    def generatePoints(self, nelx, nely, resolution = 1, width = 20, height = 20): 
        """From up to bottom, row major - similar to FEM element numbering as per 88 lines code"""
        ctr = 0
        xy = np.zeros((resolution*nelx*resolution*nely,2))
        for i in range(resolution*nelx):
            for j in range(resolution*nely):
                xy[ctr,0] = (i + 0.5)/resolution
                xy[ctr,1] = (resolution*nely - j - 0.5)/resolution
                ctr += 1
        xy[:,0] = (xy[:,0]/nelx)*width
        xy[:,1] = (xy[:,1]/nely)*height
        return xy

    def applyFourierMapping(self, x):
      c = tf.cos(2*np.pi*tf.matmul(x,self.coordnMap)) # (hw, n_features)
      s = tf.sin(2*np.pi*tf.matmul(x,self.coordnMap))
      xv = tf.concat((c,s), axis = 1) # (hw,2*n_features)
      return xv
