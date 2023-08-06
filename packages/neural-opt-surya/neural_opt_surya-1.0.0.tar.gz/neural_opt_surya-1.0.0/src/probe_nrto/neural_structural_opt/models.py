# Copyright 2019 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" 
Contains all the models tested for neural reparameterization.

A more elaborate description of this module may be included here.

Classes
-------
ClassOne
    A one-line summary of ClassOne contained in this module.
ClassTwo
    A one-line summary of ClassTwo contained in this module.
    
Functions
---------
function_one
    A one-line summary of function_one contained in this module.
function_two
    A one-line summary of function_two contained in this module.
    
https://github.com/tensorflow/tensorflow/issues/22208
regsiter gradient for bilinear resize
"""
#                                                                       Modules
# =============================================================================

# Standard
import random as py_random

# Third-party
import autograd
import autograd.core
import autograd.numpy as np
from autograd import elementwise_grad as egrad
import tensorflow as tf

# Locals
from probe_nrto.neual_structural_opt import topo_api

#                                                          Authorship & Credits
# =============================================================================
__author__ = 'Suryanarayanan (s.manojsanu@tudelft.nl)'
__credits__ = ['Suryanarayanan M S']
__status__ = 'Stable'
# =============================================================================
#
# =============================================================================


def batched_topo_loss(params: tf.Tensor, envs: list, 
                      vol_const_hard: bool = True,
                      cone_filter: bool = True, p: float = 3.0, 
                      den_proj: bool = False, beta: float = 1):
    """Calculates loss from a model's output using FE analysis.
 
    Parameters
    ----------
    params
        Output of model
    envs
        List of environments
	vol_const_hard
		Whether to apply the hard-volume contraint strategy
	cone_filter
		Whether to apply the cone filtering on the densities
	p
		SIMP penalty factor to be used
	den_proj
		Whether to use density projection
	beta
		Density projection parameter.	

    Returns
    -------
        loss: Compliance or Compliance + Volume constraint violation   
	
	""" 
	losses = [env.objective(params[i], volume_contraint=vol_const_hard, 
							cone_filter=cone_filter, p=p, den_proj=den_proj,
       						beta=beta)
					for i, env in enumerate(envs)]   
	return np.stack(losses)


def convert_autograd_to_tensorflow(func: function):
    """Handshakes functions written in Autograd to Tensorflow.    
    This allows the gradients to flow from the physics to 
    update the networks' weights.
    Main difference from Hoyer's work : Added the inner function -
    			Allows twice differentiability of the entire graph.
	Warning:
		If 'func' is a vector-valued function, the jacobian returned
		is summed over (due to the presence of egrad). If you want accurate
		Jacobians, comment out the inner first_grad function and make the
		wrapper return ans, vjp directly.
	
    Parameters
    ----------
    func
        A function written completely in Autograd.numpy
        
    Returns
    -------	
    wrapper
		A wrapper around the original function 'func' which allows
		tf tensor as input to 'func' and returns correct gradients
    """
    @tf.custom_gradient
    def wrapper(x):
        vjp, ans = autograd.core.make_vjp(func, x.numpy())
        
        #  Define the gradient and hessian of 'func'
        def first_grad(dy):            
            @tf.custom_gradient
            def jacobian(a):
                vjp2, ans2 =  autograd.core.make_vjp(egrad(func), a.numpy())
                return ans2, vjp2 # hessian               
            return dy * jacobian(x)  
        
        return ans, first_grad
    
    return wrapper


def set_random_seed(seed: int):
    """Set the gloabl random state.    

    Parameters
    ----------
    seed
        A function written completely in Autograd.numpy
        
    Returns
    -------	
    None
    """
	if seed is not None:
		py_random.seed(seed)
		np.random.seed(seed)
		tf.random.set_seed(seed)


class Model(tf.keras.Model):
    """Base model for all other models.
    Allows model sub-classing to create Keras models.
    
    Attributes
    ----------
    seed 
        Set the global state for randomness
    args 
        Dictionary with details about the boundary conditions.
        Can be created 'using topo_api.py' file.
    env
        An object of the Environment class
    J0 
        Intial compliance value - Useful for scaling.
        Calculated at the start of optimization

    Methods
    -------
    loss(self, logits, other_arguments)
        Calculates the loss using the current model's outputs
    """

	def __init__(self, seed: int = None, args : dict = None):
		super().__init__()
		set_random_seed(seed)
		self.seed = seed
		self.env = topo_api.Environment(args)
		# Initial compliance for scaling purposes
		self.J0 = 0.0 

	def loss(self, logits: tf.Tensor, vol_const_hard: bool = True, 
           cone_filter: bool = True, p: float = 3.0,
           den_proj: bool = False, beta: float = 1):
		"""Calculates the loss using the model's output

		Parameters
		----------
		logits
			Output of model
		vol_const_hard
			Whether to apply the hard-volume contraint strategy
		cone_filter
			Whether to apply the cone filtering on the densities
		p
			SIMP penalty factor to be used
		den_proj
			Whether to use density projection
		beta
			Density projection parameter.	

		Returns
		-------
			loss: Compliance or Compliance + Volume constraint violation 
		"""
		# for our neural network, we use float32, but we use float64 for the physics
		# to avoid any chance of overflow.
		# add 0.0 to work-around bug in grad of tf.cast on NumPy arrays
		logits = 0.0 + tf.cast(logits, tf.float64)
		f = lambda x: batched_topo_loss(x, [self.env], 
										vol_const_hard = vol_const_hard,
										cone_filter=cone_filter, p=p,
										den_proj=den_proj, beta=beta)
		losses = convert_autograd_to_tensorflow(f)(logits) 
		return tf.reduce_mean(losses)
    

class PixelModel(Model):
    """Dummy model for conventional topology optimization.
    Named as PixelModel because the model's variables are
    arranged as in an image [representing the density].    
    
    Attributes
    ----------
    z 
        The model's parameters

    Methods
    -------
    call(self, inputs)
        Simply returns the model's parameters as the output.
        This function is required by tensorflow
    """

	def __init__(self, seed: int = None, args : dict = None):
		super().__init__(seed, args)
		shape = (1, self.env.args['nely'], self.env.args['nelx'])
		z_init = np.broadcast_to(args['volfrac'] * args['mask'], shape)
		self.z = tf.Variable(z_init, trainable=True, dtype = tf.float32)

	def call(self, inputs=None):
		return self.z

#                                                         TOuNN & F-TOuNN Model
# =============================================================================
layers = tf.keras.layers


class TounnModel(Model):
    """Fully connected neural network model.
    This single model functions as both the TOuNN and the F-TOuNN models.
    1. https://github.com/UW-ERSL/TOuNN
    2. https://github.com/UW-ERSL/Fourier-TOuNN
    Both are coordinate-based networks representing the density field.
    TOuNN maps (x,y) in the design domain to density at that point
    F-TOuNN projects (x,y) using random Fourier features and uses this
    high dimensional vector as the input.
    
    Attributes
    ----------
    core_model
        The Keras model from the inputs to the output
    public_attribute_two : list
        Description of this public attribute.
    _non_public_attribute_one : tuple
        Description of this non-public attribute.
    _non_public_attribute_two : list
        Description of this non-public attribute.
    _non_public_attribute_three : float
        Description of this non-public attribute.
    Methods
    -------
    call(self, inputs=None)
        A one-line summary describing this public method.
    generatePoints(self, nelx, nely, resolution = 1, width = 20, height = 20)
        A one-line summary describing this non-public method.
    applyFourierMapping(self, x)
        A one-line summary describing this static non-public method.
    normalize(self, xy)
        A one-line summary describing this public method.
    """
    outputDim = 1; # if material/void at the point
        
    def __init__(self, seed: int = 0, args: dict = None,
                 depth: int = 1, width: int = 20,
                 fourier_features: bool = True, no_ffeatures: int = 150, 
                 sampling: dict = {'default': (6,30)},
                 vol_const_hard: bool = False, 
                 var_batch: bool = False, resolution: int = 1, 
                 normalize: bool = False
                 ):
		"""Defining the TOuNN and F-TouNN models using Keras and TF2.0.
		Creates the model based on the parameters chosen.
  
		Parameters
		----------
		seed
			Sets the global random state
		args
			Details about the boundary condition.
		depth
			Number of network hidden layers
		width
			Number of neurons in each hidden layer
		fourier_features
			Whether to use random Fourier features. 
   			True would imply using the F-TOuNN model
		no_ffeatures
			Number of fourier features to project onto.
			Only applicable for F-TOuNN (Needs 'fourier_features' to be True).
		sampling
			Details of the distrbution from which sampling of random fourier features
			has to be done (Needs 'fourier_features' to be True). The format adopted is
			{'key' : (param1, param2)}, where param1 and param2 are the distribution's parameters
			Options (Possible 'key's):
				'default': Disjoint uniform distribution (as in the paper)
					param1 - rmin
					param2 - rmax
				'gaussian': Gaussian distribution
					param1 - mean
					param2 - std
				'uniform': Uniform distribution
					param1 - lower limit
					param2 - higher limit	
				'fixed-k': Non-random distribution. Samples points such that the
						   magnitude of the wave vector is constant	
					param1 - wave vector magnitude
					param2 - None
				'fixed-dir': Non-random distribution. Samples points such that the
						   direction of the wave vector is constant
					param1 - Angle in degrees (w.r.t x axis)
					param2 - None  
		var_batch
			Whether to use variable_batch. This sets the Batchnorm layer to inference mode.
			When set to True, allows sampling a trained model at intermediate points.
		resolution
			The resolution at which points are sampled in the design domain.
			resolution=1 means the nelx*nely points are sampled  
		normalize
			Whether to normalize the inputs for TOuNN model
   
		Returns
		-------
			None 
		"""
        super().__init__(seed, args)
		self.seed = seed
      	self.args = args
      	h = self.args['nely']
		w = self.args['nelx']
		if fourier_features:
			inputDim = 2*no_ffeatures # (cos + sine) x n_fourier_features 
		else:          
			inputDim =2 #(x,y) only          
		hw = h*w
		if var_batch: # for inference - variable batch size 
			bs = resolution**2 * hw
			net = inputs = layers.Input((inputDim,), batch_size=bs)
		else:     
			assert resolution == 1
          net = inputs = layers.Input((inputDim,), batch_size=hw)  ## h * w # only works with resolution = 1
		initializer = tf.keras.initializers.GlorotNormal()      
		for i in range(depth):
			l = layers.Dense(units=width,
							kernel_initializer=initializer, 
							bias_initializer='zeros', activation =None)     
			net = l(net)
			if var_batch:
				net = layers.BatchNormalization(momentum=0.01)(net, training=False)
			else:             
				net = layers.BatchNormalization(momentum=0.01)(net, training=True)
			net = tf.nn.leaky_relu(net, alpha =0.01) #to be consistent with PyTorch
   
		l = layers.Dense(units=self.outputDim, kernel_initializer=initializer, 
							bias_initializer='zeros', activation =None)       
		net = l(net)
		if not vol_const_hard: # Need to verify -done
			net = tf.keras.layers.Activation("sigmoid")(net)
		if var_batch:
			output = tf.transpose(tf.reshape(net, [1,resolution*w, resolution*h]), 
									perm=[0,2,1]) #tf.reshape(net,[1,bs])          
		else:
			output = tf.transpose(tf.reshape(net, [1,w,h]), perm=[0,2,1])
		self.core_model = tf.keras.Model(inputs=inputs, outputs=output)

		self.xy = self.generatePoints(self.args['nelx'], self.args['nely'],
											width = args['width'], height =args['height'],
											resolution = resolution)
		if fourier_on:
			if list(sampling.keys())[0] == 'default':
				coordnMap = np.zeros((2, n_ffeatures)) # random fourier features
				rmin = sampling['default'][0]
				rmax = sampling['default'][1]
				for i in range(coordnMap.shape[0]):
					for j in range(coordnMap.shape[1]):
						coordnMap[i,j] = np.random.choice([-1.,1.])*\
								np.random.uniform(1./(2*rmax), 1./(2*rmin))
			elif list(sampling.keys())[0] == 'gaussian':
				mean = sampling['gaussian'][0]
				sigma = sampling['gaussian'][1]
				coordnMap = np.random.normal(scale = sigma, size = (2,n_ffeatures), loc =mean)
			elif list(sampling.keys())[0] == 'uniform':
				low_lim = sampling['uniform'][0]
				upp_lim =  sampling['uniform'][1]
				coordnMap = np.random.uniform(low = low_lim, size = (2,n_ffeatures), high =upp_lim)
			elif list(sampling.keys())[0] == 'fixed-k':
				r_med = sampling['fixed-k'][0]
				xvals = np.linspace(0.001, r_med, int(n_ffeatures/2))
				yvals1 = np.sqrt(r_med**2 - xvals**2)
				yvals2 =-1* yvals1
				x = np.hstack([xvals,xvals])
				y = np.hstack([yvals1,yvals2])
				coordnMap = np.vstack([x,y])
			else:
				slope = np.tan(sampling['fixed-dir'][0]* np.pi/180) # y=mx
				lim = np.sqrt(1/(1+slope**2))
				xvals = np.linspace(0, lim, int(n_ffeatures))
				yvals =slope * xvals
				coordnMap = np.vstack([xvals,yvals])      
				
			self.coordnMap = tf.constant(coordnMap)
			self.z = self.applyFourierMapping(self.xy) # inputs
		else:
			if normalize:
				self.z = self.normalize(self.xy)
			else:
				self.z = self.xy
        
    def call(self, inputs=None):      
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
  
    def normalize(self, xy): #xy ={(x,y)}
        ulx = self.args['width']
        uly = self.args['height']
        
        x = xy[:,0]
        y = xy[:,1]
        #scale x
        xnew = (2*x/ulx) - 1
        #scale y
        ynew = (2*y/uly) - 1
        return np.array([xnew,ynew]).T

class TounnModelFS(Model):
    """
    Utilizes shushu's code for generating the points in the grid.
    var_batch : If true, allows a different batch size to be used for higher resolution
    bs :  Applicable when var_batch = True, Sets the new batchsize    
    """
    outputDim = 1; # if material/void at the point    
    def __init__(self, seed=0, args=None, depth=1, 
                 width=20, n_terms =5, one_D=  True,
                 vol_const_hard= False, 
                 var_batch = False, resolution = 1):
      super().__init__(seed, args)
      self.seed = seed
      self.args = args
      h = self.args['nely']
      w = self.args['nelx']
      if one_D:
          inputDim = 4*n_terms # (cos + sine) x n_fourier_features x 2--> for x and y  
      else:
          inputDim = n_terms**2
      hw = h*w
      if var_batch: # for inference - variable batch size 
          bs = resolution**2 * hw
          net = inputs = layers.Input((inputDim,), batch_size=bs)
      else:     
          assert resolution == 1
          net = inputs = layers.Input((inputDim,), batch_size=hw)  ## h * w # only works with resolution = 1
      initializer = tf.keras.initializers.GlorotNormal()      
      for i in range(depth):
          l = layers.Dense(units=width,
                           kernel_initializer=initializer, 
                           bias_initializer='zeros', activation =None)     
          net = l(net)
          if var_batch:
              net = layers.BatchNormalization(momentum=0.01)(net, training=False)
          else:             
              net = layers.BatchNormalization(momentum=0.01)(net, training=True)
          net = tf.nn.leaky_relu(net, alpha =0.01) #to be consistent with PyTorch
      l = layers.Dense(units=self.outputDim, kernel_initializer=initializer, 
                           bias_initializer='zeros', activation =None)       
      net = l(net)
      if not vol_const_hard: # Need to verify -done
        net = tf.keras.layers.Activation("sigmoid")(net)
      if var_batch:
          output = tf.transpose(tf.reshape(net, [1,resolution*w, resolution*h]), 
                                perm=[0,2,1]) #tf.reshape(net,[1,bs])          
      else:
          output = tf.transpose(tf.reshape(net, [1,w,h]), perm=[0,2,1])
      self.core_model = tf.keras.Model(inputs=inputs, outputs=output)

      self.xy = self.generatePoints(self.args['nelx'], self.args['nely'],
                                        width = args['width'], height =args['height'],
                                                    resolution = resolution)
      if one_D: 
          self.z = self.apply1DFourierSeries(self.xy, n_terms) # inputs
      else:
          self.z = self.apply2DFourierSeries(self.xy, n_terms)
        
    def call(self, inputs=None):      
        return self.core_model(self.z)
    
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

    def apply1DFourierSeries(self, x, n_terms):
      xv = []  
      Lx = self.args['width']
      Ly = self.args['height']
      for pt in x:
          xval = pt[0]
          yval = pt[1]
          inp_node_vals = []
          for k in range(1,n_terms+1):
              sinx = np.sin(np.pi*k*xval/Lx).item()
              cosx = np.cos(np.pi*k*xval/Lx).item()
              siny = np.sin(np.pi*k*yval/Ly).item()
              cosy = np.cos(np.pi*k*yval/Ly).item()
              inp_node_vals.extend([sinx,cosx,siny,cosy])     
          xv.append(inp_node_vals)
      return tf.cast(tf.constant(xv), tf.float64)
  
    def apply2DFourierSeries(self, x, n_terms):
      xv = []  
      Lx = self.args['width']
      Ly = self.args['height']
      for pt in x:
          xval = pt[0]
          yval = pt[1]
          inp_node_vals = []
          for k in range(1,n_terms+1):
              for l in range(1,n_terms+1):
                  cosx = np.cos(np.pi*k*xval/Lx).item()
                  cosy = np.cos(np.pi*l*yval/Ly).item()
                  inp_node_vals.append(cosx * cosy)    
          xv.append(inp_node_vals)
      return tf.cast(tf.constant(xv), tf.float64)    
  
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
###################################################################################
# Hoyer's architecture with CONV2dT
class CNNModel_c2dt_corr(Model):
  """
   main difference :  Replaced CONV layer with CONV_TRANSPOSE layer,
                       vol_const_hard : IF true, constraints output using sigmoid
  """
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
################################# Generalized tounn model #################################
class GTounnModel(Model):
    # inputDim = 2*150; # x and y coordn of the point
    outputDim = 1; # if material/void at the point
    
    def __init__(self, seed=0, args=None, firstnet_params =
                 {'depth': 2, 'width':[20, 300], 'train': [False, False], 'activation': 'tanh',
                  'init':tf.keras.initializers.GlorotNormal() },
                     depth=1, width=20, vol_const_hard= False):
      super().__init__(seed, args)
      set_random_seed(seed)
      self.seed = seed
      self.args = args
      self.firstnet_params = firstnet_params
      h = self.args['nely']
      w = self.args['nelx']
      inputDim = firstnet_params['width'][-1]          
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

      self.xy = self.generatePoints(self.args['nelx'], self.args['nely'],
                                        width = args['width'], height =args['height'])
      self.inputs = self.applyfirstnet(self.xy) 
        
    def call(self, inputs=None):
      return self.core_model(self.inputs)

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

    def applyfirstnet(self, x):
      h = self.args['nely']
      w = self.args['nelx']
      net = inputs = layers.Input((2,), batch_size=h*w)
      initializer = self.firstnet_params['init']#tf.keras.initializers.GlorotNormal()
      for i in range(self.firstnet_params['depth']):
          net = layers.Dense(units=self.firstnet_params['width'][i],
                                     kernel_initializer=initializer, 
                                     bias_initializer='zeros', 
                                     activation =self.firstnet_params['activation'], 
                                     trainable = self.firstnet_params['train'][i])(net) 
      output = net
      mdl2 = tf.keras.Model(inputs=inputs, outputs=output)  
      self.firstnet = mdl2
      xv = mdl2(x)    
      return xv
  
#######Original hoyer's model ################ -- Not need to consider this part and below - For shushu
class CNNModel(Model):

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
      activation=tf.nn.tanh,
      conv_initializer=tf.initializers.VarianceScaling,
      normalization=global_normalization,
  ):
    super().__init__(seed, args)

    if len(resizes) != len(conv_filters):
      raise ValueError('resizes and filters must be same size')

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
      net = UpSampling2D(resize)(net)
      net = normalization(net)
      net = Conv2D(
          filters, kernel_size, kernel_initializer=conv_initializer)(net)
      if offset_scale != 0:
        net = AddOffset(offset_scale)(net)

    outputs = tf.squeeze(net, axis=[-1])

    self.core_model = tf.keras.Model(inputs=inputs, outputs=outputs)

    latent_initializer = tf.initializers.RandomNormal(stddev=latent_scale)
    self.z = self.add_weight(
        shape=inputs.shape, initializer=latent_initializer, name='z')

  def call(self, inputs=None):
    return self.core_model(self.z)    

######################### Simple FC architecture #TODO: check with TouNN
class FCNN_simple(Model):
# Sigmoid for last layer, non trainable latent input with size =1!!
  def __init__(
      self,
      seed=0,
      args=None,
      latent_size=1,
      depth_scale = 2, # NUmber of layers
      width_scale = 1, # To scale the width of the hidden layers
      latent_scale=1.0, # Random normal with std_dev =  scale
      latent_trainable = False,
      kernel_init = tf.keras.initializers.GlorotNormal,
      activation=tf.keras.activations.tanh,
  ):
    super().__init__(seed, args)

    h = self.env.args['nely'] 
    w = self.env.args['nelx'] 

    net = inputs = layers.Input((latent_size,), batch_size=1)
    num_neurons = h*w*width_scale   

    for _ in range(depth_scale):
      net = layers.Dense(num_neurons, kernel_initializer=kernel_init, activation =activation)(net)

    net = layers.Dense(h*w, kernel_initializer=kernel_init ,activation =
                       tf.keras.activations.linear)(net)
    outputs = layers.Reshape([1, h, w])(net)
    self.core_model = tf.keras.Model(inputs=inputs, outputs=outputs)

    latent_initializer = tf.initializers.RandomNormal(stddev=latent_scale)
    self.z = self.add_weight(
        shape=inputs.shape, initializer=latent_initializer, name='z', 
                        trainable= latent_trainable)

  def call(self, inputs=None):
    return self.core_model(self.z)

####################### FNO+ F-tounn model
class CNN_tounn(Model):
    """
    Utilizes shushu's code for generating the points in the grid.
    var_batch : If true, allows a different batch size to be used for higher resolution
    bs :  Applicable when var_batch = True, Sets the new batchsize    
    """
    outputDim = 1; # if material/void at the point    
    def __init__(self, seed=0, args=None, depth=1, 
                 width=20, n_ffeatures =150,
                 vol_const_hard= False, 
                 out_resolution = 4, # Should be in multiples of 2 
                 sampling_range = 0.2) :

      super().__init__(seed, args)
      self.seed = seed
      self.args = args
      h = self.args['nely']
      w = self.args['nelx']
      inputDim = 2*n_ffeatures # (cos + sine) x n_fourier_features           
      hw = h*w
      net = inputs = layers.Input((inputDim,), batch_size=hw*out_resolution**2)  ## h * w # only works with resolution = 1
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
      net = tf.transpose(tf.reshape(net, [1,w*out_resolution,h*out_resolution,1]), 
                            perm=[0,2,1,3])      
      #### Now to add the CNN part
      conv_initializer=tf.initializers.VarianceScaling
      for i in range(out_resolution//2):
          net = Conv2D(
              filters=10, kernel_size =(5,5), kernel_initializer=conv_initializer)(net)
          net = layers.AveragePooling2D(pool_size=(2, 2))(net)   
          
      net = Conv2D(
              filters=1, kernel_size =(5,5), 
              kernel_initializer=conv_initializer,activation=None)(net)  
      if not vol_const_hard: # Need to verify -done
        net = tf.keras.layers.Activation("sigmoid")(net)  
        
      output = tf.transpose(tf.reshape(net, [1,w,h]), 
                              perm=[0,2,1])
      self.core_model = tf.keras.Model(inputs=inputs, outputs=output)

      self.xy = self.generatePoints(self.args['nelx'], self.args['nely'],
                                        width = args['width'], height =args['height'],
                                        resolution = out_resolution)
      coordnMap = np.random.uniform(low = -1*sampling_range, size = (2,n_ffeatures),
                                    high = -1* sampling_range)
      self.coordnMap = tf.constant(coordnMap)
      self.z = self.applyFourierMapping(self.xy) # inputs
        
    def call(self, inputs=None):
       
        return self.core_model(self.z)  
    
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
  
######################### FNO models ################################ 
"""
Fourier Neural Operator as a Model
Model has been converted from Shushu's code (Originally in Pytorch)
More details are available in tst_FNO_TF_model.py
"""
#create spectralconv layer
class SpectralConv2d(layers.Layer):
    def __init__(self, in_channels, out_channels, modes1, modes2, scale=1):
        super().__init__()

        """
        2D Fourier layer. It does FFT, linear transform, and Inverse FFT.
        from https://github.com/zongyi-li/fourier_neural_operator   
        """

        self.in_channels = in_channels
        self.out_channels = out_channels
        self.modes1 = modes1 #Number of Fourier modes to multiply, at most floor(N/2) + 1
        self.modes2 = modes2

        self.scale = (1 / (in_channels * out_channels)) * scale
        
        shape = in_channels, out_channels, self.modes1, self.modes2
        a1 = np.random.uniform(size = shape)
        b1 = np.random.uniform(size = shape)
        # c1 = a1 + 1j*b1     
        
        # self.weights1 = tf.Variable(initial_value = self.scale*c1, trainable = True,
        #                             dtype = tf.complex64)        
        # c2 = c1 * np.random.uniform()
        # self.weights2 = tf.Variable(initial_value = self.scale*c2, trainable = True,
        #                             dtype = tf.complex64)
        self.r1 = tf.Variable(initial_value =a1, trainable = True,
                                     dtype = tf.float32)
        self.im1 = tf.Variable(initial_value =b1, trainable = True,
                                     dtype = tf.float32)    
        rand= np.random.uniform()
        self.r2 = tf.Variable(initial_value =rand*a1, trainable = True,
                                     dtype = tf.float32)
        self.im2 = tf.Variable(initial_value =rand*b1, trainable = True,
                                     dtype = tf.float32)    

    # Complex multiplication
    def compl_mul2d(self, input, weights):
        # (batch, in_channel, x,y ), (in_channel, out_channel, x,y) -> (batch, out_channel, x,y)
        return tf.einsum("bixy,ioxy->boxy", input, weights)

    def call(self, x):        
        batchsize = x.shape[0]
        x_ft = tf.signal.rfft2d(x)
        # ITEM ASSIGNMENT LOGIC 
        original = tf.zeros(shape = (batchsize, self.out_channels,  x.shape[-2], 
                             x.shape[-1]//2 + 1), dtype=tf.complex64)
        
        mask1_np = np.ones(shape = original.get_shape().as_list())#original.numpy().shape) 
        mask1_np[:,:, :self.modes1, :self.modes2] = 0.0
        
        mask2_np = np.ones(shape = original.get_shape().as_list()) 
        mask2_np[:,:, -self.modes1:, :self.modes2] = 0.0
        
        mask1 = tf.convert_to_tensor(mask1_np, dtype =tf.complex64)
        mask2 = tf.convert_to_tensor(mask2_np, dtype =tf.complex64)
        # Form the complex weights to be multiplied
        weights1 = self.scale*tf.dtypes.complex(self.r1, self.im1)
        other1 = self.compl_mul2d(x_ft[:, :, :self.modes1, :self.modes2], 
                                  weights1)
        weights2 = self.scale*tf.dtypes.complex(self.r2, self.im2)
        other2 = self.compl_mul2d(x_ft[:, :, -self.modes1:, :self.modes2], 
                                  weights2)
        padding1 = tf.constant([[0,0],
                               [0,0], 
                               [0,mask1_np.shape[-2] - other1.shape[-2]],
                               [0,mask1_np.shape[-1] - other1.shape[-1]]])
        padding2 = tf.constant([[0,0],
                               [0,0], 
                               [mask2_np.shape[-2] - other2.shape[-2],0],
                               [0,mask2_np.shape[-1] - other2.shape[-1]]])
        
        itm_assign1 = original * mask1 + tf.pad(other1, padding1) * (1 - mask1)
        out_ft = itm_assign1 * mask2 + tf.pad(other2, padding2) * (1-mask2)
        #Return to physical space
        x = tf.signal.irfft2d(out_ft, fft_length =x.shape[2:])
        return x
    
class FNOModel(Model):
    def __init__(self,
        seed=0,
        args=None,
        modes1=12,#12
        modes2=12, 
        width=32,#32
        num_fns=4, 
        activation=tf.nn.gelu,
        padding=9,
        linear=True,# True
        scale=1,
        vol_constraint=True,
        latent_scale = 1.0) :
        
        super().__init__(seed, args)
        l_activation = layers.Activation(activation)
        #Make the model
        #Make the input as dummy tensor of dims (1,w,h)
        h = args['nely'] 
        w = args['nelx']
        #Make a grid of (x,y) values in the domain w x h
        shape =(1,w,h)
        grid = self.get_grid(shape)
        
        #Layer 0 - input layer
        inputs = net = layers.Input(shape = grid.shape[1:], batch_size=1)
        #Layer 1 - FC layer - Lifting to higher dimensions
        # dense_k_init = tf.keras.initializers.HeUniform()
        # dense_b_init = tf.keras.initializers.HeUniform()
        dense_k_init = dense_b_init = tf.keras.initializers.VarianceScaling(
                    distribution ='uniform', scale = 1/3) # Same as Pytorch doc
        net = layers.Dense(width, kernel_initializer=dense_k_init,
                           bias_initializer = dense_b_init,
                           activation ='linear')(net)
        net = layers.Permute((3, 1, 2))(net) # Channel is index 0
        net = layers.ZeroPadding2D( ((0,padding),(0,padding)), 
                           data_format = 'channels_first')(net)  
        
        # For the spectral conv operations
        for i in range(num_fns):
            #Apply spectral conv layer
            net1 = SpectralConv2d(width, width, 
                                 modes1, modes2, scale=scale)(net)
            #Apply linear transformation
            #Same init scheme as menioned in Pytorch (except for the factor)
            if linear:            
                net2 = Conv2DT(width, 1, resize=1,
                            kernel_initializer=dense_k_init,
                            bias_initializer = dense_b_init,
                            activation = 'linear', 
                            data_format = 'channels_first')(net)
                # net2 = Conv2D(width, 1,
                #            kernel_initializer=dense_k_init,
                #            bias_initializer = dense_b_init,
                #            activation = 'linear', 
                #            data_format = 'channels_first')(net)   
                net = net1 + net2 
            else:
                net = net1
                
            if i != num_fns-1:
                net = l_activation(net)
        #Extract logits by removing padding
        net = net[:,:,:-padding,:-padding]
        net = layers.Permute((2, 3, 1))(net)        
        # Final FC layers
        net = layers.Dense(128, kernel_initializer=dense_k_init,
                           bias_initializer = dense_b_init,
                           activation =activation)(net)
        net = layers.Dense(1, kernel_initializer=dense_k_init,
                           bias_initializer = dense_b_init,
                           activation = 'linear')(net)
        if not vol_constraint:
            net = layers.Activation('sigmoid')(net)
        
        outputs = tf.squeeze(net, axis=[-1])        
        self.core_model = tf.keras.Model(inputs=inputs, outputs=outputs)
        
        latent_initializer = tf.initializers.RandomNormal(stddev=latent_scale, seed = seed)
        self.z = self.add_weight(
            shape=inputs.shape, initializer=latent_initializer, name='z')
        
    def get_grid(self, shape):
        batchsize, size_x, size_y = shape[0], shape[1], shape[2]
        gridx = tf.constant(np.linspace(0, 1, size_x), dtype=tf.float64)
        gridx = tf.tile(tf.reshape(gridx,(1, size_x, 1, 1)), [batchsize, 1, size_y, 1])
        gridy = tf.constant(np.linspace(0, 1, size_y), dtype=tf.float64)
        gridy = tf.tile(tf.reshape(gridy,(1, 1, size_y, 1)), [batchsize, size_x, 1, 1])
        return tf.concat((gridx, gridy), axis=-1)       
        
    def call(self, inputs=None):
      return self.core_model(self.z)
  
