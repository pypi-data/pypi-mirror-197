# Copyright 2020 Google LLC
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
"""Implementation of the Lanczos algorithm.
ALSO CONTAINS FUNCTIONS TO ESTIMATE THE Hessian trace and frobenius norm"""

import time
from typing import Any, Callable, Text, Tuple
import warnings
from scipy import linalg#new
from . import matrix_vector_product
from . import jax_density as jd#new
import numpy as np
import tensorflow.compat.v2 as tf

#S: return 'GPU' for has_gpu and 'GPU' for all atributes
class DeviceSelector(object):
  """Helper class to select GPU if available."""

  def __init__(self, only_gpu):
    self.default = "GPU" if self.has_gpu() and only_gpu else "CPU"
    self.accelerator = "CPU" if not self.has_gpu() else "GPU"

  def has_gpu(self):
    return bool(tf.config.experimental.list_physical_devices("GPU"))


def lanczos_algorithm(mvp_fn: Callable[[tf.Tensor], tf.Tensor],
                      dim: int,#number of parameters
                      order: int,
                      random_seed: int = 0,
                      only_gpu: bool = True,
                      init_rad = False) -> Tuple[tf.Tensor, tf.Tensor]:
  """Estimates an Hermitian matrix by using its product with arbitrary vectors.

  The Lanczos algorithm is described here:
  https://en.wikipedia.org/wiki/Lanczos_algorithm

  Args:
    mvp_fn: Matrix-vector product function. Function that takes as input a
      tensor of shape [`dim`, 1] and returns another tensor of the same shape.
      The returned tensor should be equal to Hv where v is the input vector and
      H is the symmetric matrix to estimate.
    dim: Dimension of the problem (number of columns and rows of the matrix to
      estimate.)
    order: Rank of the approximation to compute. `mvp_fn` will be called `order`
      times.
    random_seed: Random seed used for sampling the initial vector.
    only_gpu: Whether to use available GPUs for both the matrix vector product
      and the orthogonalization (if set to false, CPU will be used for
      orthogonalization). It is recommended to set this parameter to true and
      change it only if a memory error occurs.
      
      init_rad : True/False: whether to use rademacher vector as initial vector or not
  Returns:
    An estimation of the matrix defined by the matrix vector product function
      given. The matrix is returned as a tuple of two tensors (V,T) of shape
      [dim, order] and [order, order], where T is tridiagonal. The approximation
      of the matrix is then A = V T V^*.
  """
  device_selector = DeviceSelector(only_gpu)

  # Lanczos runs on CPU to save accelerator memory. Most of the computational
  # load takes place in the matrix vector function, which is still computed
  # on GPU if available.
  with tf.device(device_selector.default):
    # Runs Lanczos in float64 as numerical stability is an issue and the
    # bottleneck is calling `mvp_fn`.
    float_dtype = tf.float64
    tridiag = tf.Variable(tf.zeros((order, order), dtype=float_dtype))
    vecs = tf.Variable(tf.zeros((dim, order), dtype=float_dtype))
    
    if init_rad:
        np.random.seed(random_seed) # Added on 1 June 2021
        rad_vec = np.random.randint(2, size = dim)
        rad_vec = rad_vec.reshape(dim, 1) * 2 - 1 
        init_vec = tf.cast(tf.constant(rad_vec),float_dtype)
        init_vec = init_vec / tf.math.reduce_euclidean_norm(init_vec)
        
    else:
        init_vec = tf.random.uniform(
            (dim, 1), minval=-1, maxval=1, dtype=float_dtype, seed=random_seed)
        init_vec = init_vec / tf.math.reduce_euclidean_norm(init_vec)
    vecs[:, 0:1].assign(init_vec)
    beta = 0
    v_old = tf.zeros((dim, 1), dtype=float_dtype)

    for i in range(order):
      ts = time.time()
      v = vecs[:, i:i+1]
      with tf.device(device_selector.accelerator):
        tss = time.time()
        w = tf.cast(mvp_fn(tf.cast(v, tf.float32)), float_dtype)#S:changed
        time_mvp = time.time() - tss
            
      w = w - beta * v_old
      alpha = tf.matmul(w, v, transpose_a=True)
      tridiag[i:i+1, i:i+1].assign(alpha)
      w = w - alpha * v

      # Reorthogonalization
      for j in range(i):
        tau = vecs[:, j:j+1]
        coeff = tf.matmul(w, tau, transpose_a=True)
        w = w - coeff * tau

      beta = tf.math.reduce_euclidean_norm(w)
      if beta < 1e-6:
        warning_msg = ("Possible numerical stability issues in Lanczos: "
                       "got beta = {} in iteration {}".format(beta.numpy(), i))
        warnings.warn(warning_msg)

      if i + 1 < order:
        tridiag[i, i+1].assign(beta)
        tridiag[i+1, i].assign(beta)
        vecs[:, i+1:i+2].assign(w / beta)

      v_old = v

      info = "Iteration {}/{} done in {:.2f}s (MVP: {:.2f}s).".format(
          i, order,
          time.time() - ts, time_mvp)
      if i in [0,1]:
          print(info)

  return vecs, tridiag


def approximate_hessian(model,
                        loss_function: Callable[[tf.keras.Model, Any],
                                                tf.Tensor],
                        #dataset: tf.data.Dataset,
                        order: int,
                        #reduce_op: Text = "MEAN",
                        random_seed: int = 0,
                        only_gpu: bool = True) -> Tuple[tf.Tensor, tf.Tensor]:
  """Approximates the Hessian of a model using Lanczos algorithm.

  Will return an approximation of rank `order` as a tuple of vectors and
  tridiagonal matrices (V, T) such that H = V T V^*. The loss will be
  computed on the entire dataset `order` times.

  Args:
    model: The model for which we want to compute the Hessian.
            //Gradvis interface now
    loss_function: Loss function used to train the model. Takes as input a Keras
      model and a batch (any object yield by iterating on the dataset), and
      returns a scalar.
    dataset: Dataset on which the model is trained.
    order: Rank of the approximation of the Hessian. Setting order to the number
      of parameters recovers the full Hessian, modulo numerical errors.
    reduce_op: Whether the loss function averages or sum the per sample loss.
      Should be "MEAN" or "SUM".
    random_seed: Seed to use to sample the first vector in the Lanczos
      algorithm.
    only_gpu: Whether to use available GPUs for both the model's computation
      and the orthogonalization (if set to false, CPU will be used for
      orthogonalization). It is recommended to set this parameter to true and
      change it only if a memory error occurs.

  Returns:
    A tuple of tensors (V, T) such that H = V T V^* is an approximation of the
      Hessian.
  """
  #S: This fn returns the hessian-matrix vector product for a given vector v
  #at the model's current parameters
  def hessian_vector_product(v: tf.Tensor):
    return matrix_vector_product.model_hessian_vector_product(
        loss_function, model,v)#, dataset, v, reduce_op=reduce_op)
#S: w_dim = total number of model parameters
  w_dim = sum((np.prod(w.shape) for w in model.model.trainable_variables))
  return lanczos_algorithm(
      hessian_vector_product, w_dim, order, random_seed=random_seed,
      only_gpu=only_gpu)


def hessian_trace(nn_mdl,loss_func,n = 20, seed = 0):
    """
    Calculates the hessian trace in a stochastic way as E(v^T H v),
    where v is generated from a rademacher distribution
    n: number of times the routine has to run-- n 'v' vectors will be chosen
    "Based on Pyhessian Paper"
    seed: sets the random seed for the calculations
    
    returns:
        H_trace: returns  the calculated trace of the Hessian at the given point
        Traces: List of all traces at each step
        
    """
    
    Traces = []
    np.random.seed(seed)
    def hessian_vector_product(v: tf.Tensor):
        return matrix_vector_product.model_hessian_vector_product(
            loss_func, nn_mdl, v)
    w_dim = sum((np.prod(w.shape) for w in nn_mdl.model.trainable_variables))
    
    for i in range(n):
        #v = tf.random.normal((w_dim,1),mean= 0, stddev= 1,dtype = tf.float64,
         #                    seed= i)
           
        v = np.random.randint(2,size = w_dim)
        v = v.reshape(w_dim, 1) * 2 - 1 
        v = tf.cast(tf.constant(v),tf.float64)
        Hv = tf.cast(hessian_vector_product(tf.cast(v, tf.float32)),tf.float64)
        vHv = tf.tensordot(v,tf.transpose(Hv),2)
        Traces.append(vHv)
    H_trace = np.sum(np.array(Traces))/len(Traces)
    
    return H_trace#,Traces
    

def hessian_f_norm(nn_mdl,loss_func,n = 20, seed = 0):
    """
    Calculates the hessian's Forbenius norm in a stochastic way as E( ||H v||_2^2),
    where v is generated from a Normal distribution ~N(0,1)
    n: number of times the routine has to run-- n 'v' vectors will be chosen
    "Based on towards Understanding Generalization of DeepLearning: 
        Perspective of Loss Landscapes [19]"
    
    returns:
        f_norm_sq: the calculated frobenius norm square 
                    of the Hessian at the point
        
    """
    
    norm = []
    np.random.seed(seed)
    tf.random.set_seed(seed)
    
    def hessian_vector_product(v: tf.Tensor):
        return matrix_vector_product.model_hessian_vector_product(
            loss_func, nn_mdl, v)
    
    w_dim = sum((np.prod(w.shape) for w in nn_mdl.model.trainable_variables))
    
    for i in range(n):
        
        v = tf.random.normal((w_dim,1),mean= 0, stddev= 1,dtype = tf.float64)#,
                             #seed= i)        
        v = tf.cast(tf.constant(v),tf.float64)
        Hv = tf.cast(hessian_vector_product(tf.cast(v, tf.float32)),tf.float64)
        norm.append(tf.norm(Hv)**2)

    f_norm_sq = np.mean(norm)
    f_norm = np.sqrt(f_norm_sq)
    return f_norm   
        

def schatten_p_norm(model,loss_function,nvecs,p,m, seed = 0 ):
    ##have to use bidiagonal lanczos -- Currently not working

    n = sum((np.prod(w.shape) for w in model.model.trainable_variables))
    def hessian_vector_product(v: tf.Tensor):
        return matrix_vector_product.model_hessian_vector_product(
          loss_function, model,v)
    
    cnt_est = 0
    running_avg = np.zeros((nvecs,1))
    sum_v1 = np.zeros((nvecs,1))
    for i in range(1,nvecs+1):
        V,T = lanczos_algorithm(hessian_vector_product, n, m, seed =i, init_rad=True)
        U,s,v1 = linalg.svd(T.numpy())
        
        sigma = np.zeros((T.numpy().shape[0], T.numpy().shape[1]))
        for j in range(min(T.numpy().shape[0], T.numpy().shape[1])):
            sigma[j, j] = s[j]
        
        D = sigma
        V1 = v1.T
        theta = np.abs(np.diag(D))
        gamma2 = V1[0,:]**2
        
        thetap = theta**p
        count = gamma2@thetap
        sum_v1[i-1] = count*n
        cnt_est = cnt_est +  count
        running_avg[i-1] = n*(cnt_est/i)
    
    spnorm = running_avg[-1]
    return spnorm**(1/p)

        
def hessian_eigen_squaresum(model,loss_function,k, m, seed =1, T_list = []):  
    """
    Calculates teh sum of squares of the eigen values of the Hessian
    Based on paper [28].
    Inputs:
        model: GradVis model interface
        loss_function: function that returns the loss of "model.model"--
                        Usually PixelModel/ a Keras Model
        k: number of trials required to calculate the expected value
        m: The order of the T matrix to be used in Lanczos Algorithm
        seed: the random seed for the run
        P.S-- This seed only works in conjunction with the 'init_rad = True'
                argument for lanczos_algorithm
                Otherwise, lanczos_algorithm considers seed as 0 for every iteration
                
        T_list: List of T matrices (as list of numpy arrays), one T matrix 
                for each 'k' value : if k =10, need 10 T matrices
    Returns:
        trace_eigesq: The sum of the squares of eigen values of the Hessian
                =Sigma (lambda^2)
        all_T: List of all the generated T matrices in numpy format
                
    """
    #np.random.seed(seed)
    n = sum((np.prod(w.shape) for w in model.model.trainable_variables))
    def hessian_vector_product(v: tf.Tensor):
        return matrix_vector_product.model_hessian_vector_product(
          loss_function, model,v)
    outer_sum = 0
    all_T = []
    for i in range(k):
        if T_list == []:
            V,T = lanczos_algorithm(hessian_vector_product, n, m, i+seed, init_rad= True)
            all_T.append(T.numpy())
            eig_vals, all_weights = jd.tridiag_to_eigv([T.numpy()])
        else:
            eig_vals, all_weights = jd.tridiag_to_eigv(T[i:i+1])
            
        #each seed => new vector               
        tau2 =  all_weights#/np.linalg.norm(all_weights)#Added 28 June
        f_theta = eig_vals**2 #f(A) = A^2
        inner_sum = np.dot(tau2,f_theta.T).item()#convert array to value
        outer_sum += inner_sum
    
    trace_eigesq = n*outer_sum/k
    return trace_eigesq, all_T
 
            
            
        
        
    
    
    
    
    



    