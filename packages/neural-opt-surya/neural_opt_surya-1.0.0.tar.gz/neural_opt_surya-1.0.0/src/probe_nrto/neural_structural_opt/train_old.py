# lint as python3
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

# pylint: disable=missing-docstring
# pylint: disable=superfluous-parens
import functools

import logging
# logging.basicConfig(filename='extra_data_opt.log', level=logging.DEBUG)

import autograd
import autograd.numpy as np
import models
import topo_physics
import scipy.optimize
import tensorflow as tf
import xarray
#FOR LS
import linesearch_personal as lsp
#S:from neural_structural_optimization import lsm_module 

import os
def weights_to_file(model,directory,filename):
    """ 
    Pickles the trainable weights into a file 
    For use of visualization of loss landscapes
    """
    import pickle
    #os.chdir(directory)
    new_param = dict()
    lis_tv = model.trainable_variables #returns a list of the trainable
    #variables of the CNN model
    for i,var in enumerate(lis_tv):
        key = model.trainable_variables[i].name
        new_param[key] = var.numpy()#can convert to numpy if needed    
    file_path = directory +'/'+filename+'.p'
    pickle.dump(new_param,open(file_path,'wb'))
    #return filename+'.p'


def optimizer_result_dataset(losses, frames, save_intermediate_designs=False, extra=None, p=3.0):
  # The best design will often but not always be the final one.
  best_design = np.nanargmin(losses)
  logging.info(f'Final loss: {losses[best_design]}')
  if save_intermediate_designs:
    ds = xarray.Dataset({
        'loss': (('p','step'), [losses]),
        'design': (('p','step', 'y', 'x'), [frames]),
    }, coords={'step': np.arange(len(losses)), 'p':[p]})
  else:
    ds = xarray.Dataset({
        'loss': (('p','step'), [losses]),
        'design': (('p','y', 'x'), [frames[best_design]]),
    }, coords={'step': np.arange(len(losses)), 'p':[p]})
  if extra is not None:
      ds_e = xarray.Dataset({
          'compliance': (('p','step'), [extra['compliance']]),
          'density': (('p', 'step'), [extra['density']]),
          'c_loss': (('p','step'), [extra['c_loss']])},
          coords = {'step':np.arange(len(losses)), 'p':[extra['p']]})
      ds = xarray.merge([ds,ds_e])      
  return ds


def train_tf_optimizer(
    model, max_iterations, optimizer, save_weights_path = '' , 
    n_saves = 10,save_intermediate_designs=True, 
    conv_criteria = False, limit = 0.5, t_args =None, **kwargs):
  """
    New!
    n_saves -- save weights of the model every n steps
    save_weights_path -- Path to folder to save the weight files
    conv_criteria = True => the weight saving is stopped early[based on 10 previous
                                                               weights]
    limit - 0.5%, if successive losses are less than this , stop saving
            weights
    """
  model(None)  # build model, if not built
  alpha_val = [0]
  model.J0 = model.loss(model(None), t_args['vol_const_hard'],
                 t_args['conv_filter']).numpy().item()
  
  if not t_args['vol_const_hard']:
      alpha_val.append(t_args['alpha_start'])
      
  pval = model.env.args['penal']*np.ones(max_iterations)
  if not t_args['cont_scheme']:
      t_args['p_start'] = model.env.args['penal']
      penal = np.arange(t_args['p_start'], t_args['p_end'], 
                         t_args['del_p'])
      
  tvars = model.trainable_variables
  
  flag =  False
  indices =[]
  if save_weights_path != '':
      filename = 'tf_opt'+'_weights_' 
      print("Filename used: ",filename)
      i=0
      while i < max_iterations:
          if i == 0:
              indices.append(i)
          i+=n_saves
          if i < max_iterations:
              indices.append(i)
      indices.append(max_iterations)
      weights_to_file(model,save_weights_path,filename+str(indices[0]))
      flag =  True

  losses = []
  frames = []

  gradient_stats_file  = kwargs.get('gradient_stats_file')
  if gradient_stats_file is not None:
    train_summary_writer = tf.summary.create_file_writer(gradient_stats_file)

  for i in range(max_iterations + 1):
    args =model.env.args
    with tf.GradientTape() as t:
      t.watch(tvars)
      logits = model(None)
      if i > len(pval)-1:
          penalty = args['penal']
      else:
          penalty = pval[i]
          
      J = model.loss(logits, t_args['vol_const_hard'],
                     t_args['conv_filter'], penalty)      
      if not t_args['vol_const_hard']:
          cur_density = tf.reduce_mean(logits)                
          loss = tf.cast(alpha_val[-1]*((args['volfrac']/cur_density) - 1)**2,
                           dtype=tf.float64) + J/model.J0
      else:
          loss = J/model.J0
          
    losses.append(loss.numpy().item())
    frames.append(logits.numpy())
    #Saving weight files to disk as pickled file: Applies convergence criterion as well
    if i == 0:#already saved initialization weight file
        pass
    else:
        if flag and i in indices[1:]:
            if conv_criteria and i > 10:
                last_losses = np.array(losses[-10:])
                per_change = -1*np.diff(last_losses)/ last_losses[:-1]*100
                if np.all(per_change <= limit):
                    #pass
                    flag = False
                    indices = indices[:i+1]
                f = weights_to_file(model,save_weights_path,filename+str(i))
                #truncate indices                                        
            else:
                f = weights_to_file(model,save_weights_path,filename+str(i)) 

    # if i % (max_iterations // 10) == 0:
    #   logging.info(f'step {i}, loss {losses[-1]:.2f}')

    if i < max_iterations:
      grads = t.gradient(loss, tvars)
      optimizer.apply_gradients(zip(grads, tvars))
      
      if gradient_stats_file is not None: 
        tb_save_grads(train_summary_writer, grads, tvars, loss, i)

  designs = [model.env.render(x, volume_contraint=True) for x in frames]
  return optimizer_result_dataset(np.array(losses), np.array(designs),
                                    save_intermediate_designs),indices


train_adam = functools.partial(
    train_tf_optimizer, optimizer=tf.keras.optimizers.Adam(1e-3))


def _set_variables(variables, x):
  shapes = [v.shape.as_list() for v in variables]
  values = tf.split(x, [np.prod(s) for s in shapes])
  for var, value in zip(variables, values):
    var.assign(tf.reshape(tf.cast(value, var.dtype), var.shape))


def _get_variables(variables):
  return np.concatenate([
      v.numpy().ravel() if not isinstance(v, np.ndarray) else v.ravel()
      for v in variables])

def tb_save_grads(train_summary_writer, grads, tvars, loss, i):
  with train_summary_writer.as_default():    
    for g, v in zip(grads, tvars):
      if g is not None:
        tf.summary.histogram("{}/grad_histogram".format(v.name), g, step = i)
        tf.summary.histogram("{}/LOG-grad_histogram".format(v.name),
                             np.log(np.abs(g)+1e-12), step = i)
      if v is not None:
        tf.summary.histogram("{}/weight_histogram".format(v.name), v, step = i)
        tf.summary.histogram("{}/LOG-weight_histogram".format(v.name),
                             np.log(np.abs(v)+1e-12), step = i)
    tf.summary.scalar('Objective', loss, step = i)

def train_lbfgs(
    model, max_iterations, save_weights_path = '' , n_saves = 1,
    save_intermediate_designs=True, init_model=None,
    conv_criteria = True, t_args = None,
    limit = 0.1, **kwargs):
  """
    Always includes the first and last checkpoint values
    Added arguments:
        save_weights_path: String
                    Where to save the weights of the model[path to folder]
        n_saves: Integer
                    Create savefiles every "n_saves" ierations-includes
                    first and last indices always
        #Saves the entire model as well at the designated indices
        
        t_args :  Arguments for training
            "conv_filter" : Apply cone filter to densities
            "vol_const_hard" : Apply hard volume constraint
            "cont_scheme" : Apply continuation scheme
            "p_start" : starting penalty - TopOpt penalization
            "p_end" : Final penalty value
            del_p :  changing p value
            "alpha_start" : start value of alpha
            "del_alpha" : Change in the alpha value
  """
  model(None)  # build model, if not built
  #Initial compliance for scaling
  model.J0 = model.loss(model(None), t_args['vol_const_hard'],
                 t_args['conv_filter']).numpy().item()
  
  pval = [model.env.args['penal']]# Penalty values
  alpha_val = [100]
  
  if t_args['cont_scheme']:
     pval = np.arange(t_args['p_start'], t_args['p_end'], 
                         t_args['del_p'])
  if not t_args['vol_const_hard']:
     alpha_val = np.arange(t_args['alpha_start'], t_args['alpha_end'],
                           t_args['del_alpha'])
      
  if init_model is not None:
    if not isinstance(model, models.PixelModel):
      raise TypeError('can only use init_model for initializing a PixelModel')
    model.z.assign(tf.cast(init_model(None), model.z.dtype))
  tvars = model.trainable_variables
  # Saving weights - TODO: Check this
  flag =  False
  indices =[]
  if save_weights_path != '':
      filename = 'lbfgs_weights_'
      print("Filename used: ",filename)
      i=0
      while i < max_iterations*len(pval):
          if i == 0:
              indices.append(i)
          i+=n_saves
          if i < max_iterations:
              indices.append(i)
      indices.append(max_iterations)
      weights_to_file(model,save_weights_path,filename+str(indices[0]))
      flag =  True
  # For tensorboard    
  gradient_stats_file  = kwargs.get('gradient_stats_file')
  if gradient_stats_file is not None:
    train_summary_writer = tf.summary.create_file_writer(gradient_stats_file)
    
  # Function returning the objective value and gradient
  def value_and_grad(x):
    _set_variables(tvars, x)
    nonlocal t_args
    nonlocal count
    args =model.env.args

    with tf.GradientTape() as t:
      t.watch(tvars)
      logits = model(None)
      J = model.loss(logits, t_args['vol_const_hard'],
                     t_args['conv_filter'], pval[count])      
      if not t_args['vol_const_hard']:           
          cur_density = tf.reduce_mean(logits)
          loss = tf.cast(alpha_val[count]*((cur_density/args['volfrac']) - 1)**2, #alpha =100
                               dtype=tf.float64) + J/model.J0
      else:
          loss = J#/model.J0
          
    grads = t.gradient(loss, tvars)
    # Read temp file created by lbfgsb.py
    file_s = open("./n_iterations_lbfgs.txt", 'r')
    iter_str = file_s.read()
    file_s.close()
    #print("Iter code: ", iter_str)
    code_lbfgs = iter_str.split(".")[-1]
    
    if len(code_lbfgs) != 1:
        pass
    else:
        losses_p.append(loss.numpy().item())
        frame_p.append(logits.numpy().copy())
        comp_p.append(J.numpy().copy())
        true_comp.append(model.loss(logits, t_args['vol_const_hard'],
                       t_args['conv_filter'], 3.0).numpy().item())
        if not t_args['vol_const_hard']:
            den_p.append(cur_density.numpy().copy())
        i = len(losses_p)-1 # Check losses_p vs losses
        nonlocal flag
        nonlocal indices        
        if flag and i in indices[1:]:#Check weight saving!!
            if conv_criteria and i-1 > 10:
                last_losses = np.array(losses_p[-10:])
                per_change = -1*np.diff(last_losses)/ last_losses[:-1]*100
                if np.all(per_change <= limit):
                    flag = False
                    indices = indices[:i]
                weights_to_file(model,save_weights_path,filename+str(i-1))
                #truncate indices                                        
            else:
                weights_to_file(model,save_weights_path,filename+str(i-1))                
    return float(loss.numpy()), _get_variables(grads).astype(np.float64)
  # Optimization starts here
  ds = []  
  count =0 # Index for penalty values and alpha
  for i in pval: 
      print("Current penalty: ", pval[count])
      losses_p =[]
      comp_p =[]
      den_p =[]
      frame_p = []
      true_comp = []
      x0 = _get_variables(tvars).astype(np.float64)
      
      if len(pval) == 1:
          pass
      else:
          if os.path.exists("./n_iterations_lbfgs.txt"):
              os.remove("./n_iterations_lbfgs.txt")
      
      # rely upon the step limit instead of error tolerance for finishing.
      _, _, info = scipy.optimize.fmin_l_bfgs_b(
          value_and_grad, x0, maxfun=max_iterations, factr=1, pgtol=1e-14, **kwargs)
      designs = [model.env.render(x, volume_contraint=True) for x in frame_p]
      
      if den_p == []:
          extra_details =None
      else:
          extra_details ={'c_loss':np.array(comp_p), 'density':np.array(den_p), 'p':i,
                      'compliance': np.array(true_comp)}
      ds_p = optimizer_result_dataset(np.array(losses_p), np.array(designs),
                              save_intermediate_designs, extra_details)
      logging.info("Continuation scheme with p =%d" %(i),info)
      ds.append(ds_p)
      count += 1
  
  ds= xarray.merge(ds)
  return ds, indices

###################GD WITH Line Search############################

def train_GD_LS(
    model, max_iterations, save_weights_path = '' , n_saves = 10,
    save_intermediate_designs=True, init_model=None,
    conv_criteria = False, limit = 0.5,
    amax = 1e-2, maxiter =20, use_prev_alpha = False, c2 = 0.9, mode = 'robust'    
):
  """
  Training a model with Gradient Descent with a line search
  amax: Maximum step size for line search
  maxiter: Maximum number of LS iterations to use
  use_prev_alpha: Whether to continue training with the previous alpha if LS fails
  """
  model(None)  # build model, if not built

  losses = []
  frames = []

  if init_model is not None:
    if not isinstance(model, models.PixelModel):
      raise TypeError('can only use init_model for initializing a PixelModel')
    model.z.assign(tf.cast(init_model(None), model.z.dtype))

  #tvars = model.trainable_variables
  
  flag =  False
  indices =[]
  if save_weights_path != '':
      filename = 'SGD_LS_weights_'
      print("Filename used: ",filename)
      #indices = []
      i=0
      while i < max_iterations:
          if i == 0:
              indices.append(i)
          i+=n_saves
          if i < max_iterations:
              indices.append(i)
      indices.append(max_iterations)
      _ = weights_to_file(model,save_weights_path,filename+str(indices[0]))
      flag =  True
      
  # gradient_stats_file  = kwargs.get('gradient_stats_file')
  # if gradient_stats_file is not None:
  #   train_summary_writer = tf.summary.create_file_writer(gradient_stats_file)
  
  # Implement GD with Line search
  #Loss function and its gradient
  def value(x):# Sets the model to x and finds teh loss value at that input
      _set_variables(tvars, x)
      logits = model(None)
      loss = model.loss(logits)
      return float(loss.numpy())

  def valuegrad(x):#grad of loss at x
    _set_variables(tvars, x)
    with tf.GradientTape() as t:
      t.watch(tvars)
      logits = model(None)
      loss = model.loss(logits)
    grads = t.gradient(loss, tvars)
    return _get_variables(grads).astype(np.float64)
  
  #Actual GD-LS starts
  prev_alpha = 1e-4
  all_alpha = []
  prev_fnval = None # to be given to the line_search as old_old_fval
  warning_tag = 'normal' # LS did not fail
  
  for i in range(max_iterations):
        tvars = model.trainable_variables        
        #Find search direction =  - direction of gradient = pk
        with tf.GradientTape() as t:
          t.watch(tvars)
          logits = model(None)
          loss = model.loss(logits)
        grads = t.gradient(loss, tvars)
        frames.append(logits.numpy().copy())
        losses.append(loss.numpy().copy())    
        
        #Do line search along pk
        pk = -1* _get_variables(grads).astype(np.float64)
        xk = _get_variables(tvars).astype(np.float64)
        
        if mode == 'robust':# amax doesn't play a role -- Use very high amax
            if i > 0:
                alpha_det = scipy.optimize.line_search(value, valuegrad, xk, pk,
                                               old_old_fval =prev_fnval,
                                                     amax = 10000000, c2 = c2)                
            else:
                alpha_det = scipy.optimize.line_search(value, valuegrad, xk, pk,                                               
                                                    amax = 10000000, c2 = c2)
        elif mode == 'switch':
            # Might be the best mode
            alpha_det = scipy.optimize.line_search(value, valuegrad, xk, pk,                                               
                                                    amax = amax, c2 = c2)
            if alpha_det[0] is None:# Switch to robust mode FROM this iteration
                print('LS failed; Switching to robust mode')
                warning_tag = 'LSfailed'
                mode = 'robust'
                if i > 0:
                    alpha_det = scipy.optimize.line_search(value, valuegrad, xk, pk,
                                               old_old_fval =prev_fnval,
                                                     amax = 10000000, c2 = c2)                
                else:
                    alpha_det = scipy.optimize.line_search(value, valuegrad, xk, pk,                                               
                                                    amax = 10000000, c2 = c2)
            
        elif mode == 'maxctrl':
            alpha_det = scipy.optimize.line_search(value, valuegrad, xk, pk, 
                                                      amax=amax, c2 =c2)  
            if alpha_det[0] is None:
                print('LS without old_old_fval failed: Trying with old_old_fval')
                warning_tag = 'LSfailed'
                alpha_det = scipy.optimize.line_search(value, valuegrad, xk, pk,
                                                old_old_fval =prev_fnval,
                                                      amax = 10000000, c2 = c2)             
        elif mode == 'puremax':
            alpha_det = scipy.optimize.line_search(value, valuegrad, xk, pk, 
                                                      amax=amax, c2 =c2)  
            
        else:
            print('Unrecognized mode; Please specify the correct mode')
            
                
        all_alpha.append(alpha_det[:-1] + (warning_tag,))        
       
        # Do GD
        if alpha_det[0] is None:
            #LS_failed = True
            print('Linesearch did not converge') 
            if use_prev_alpha:                               
                print('Using alpha = ',str(prev_alpha))
                x_new = xk + prev_alpha * pk
                # Set the new x onto the model
                _set_variables(tvars, x_new) 
            else:
                print('Finishing training')
                if save_weights_path != '':
                    _ = weights_to_file(model,save_weights_path,filename+str(i+1))
                indices = indices[:i+1]
                break
        else:
            x_new = xk + alpha_det[0] * pk
            # Set the new x onto the model
            _set_variables(tvars, x_new)    
            prev_alpha = alpha_det[0]
            
        prev_fnval = losses[i] # Uncomment this line to use the old_old_fval of line_search
        # Check for convergence
        #Will only enter this loop to check for convergence if the indice i+1
            # is in indices list
        if flag and i+1 in indices[1:]:
            if conv_criteria and len(losses) > 10:
                last_losses = np.array(losses[-10:])
                per_change = -1*np.diff(last_losses)/ last_losses[:-1]*100
                if np.all(per_change <= limit):
                    flag = False
                    l = (i+1)// n_saves
                    indices = indices[:l]   # problem for nsaves =10 etc.
                if flag:                        #maybe change to len(losses)
                    _ = weights_to_file(model,save_weights_path,filename+str(i+1))                                                       
            else:
                _ = weights_to_file(model,save_weights_path,filename+str(i+1))
               
        
  designs = [model.env.render(x, volume_contraint=True) for x in frames]
  if indices == []:
      return optimizer_result_dataset(
      np.array(losses), np.array(designs), save_intermediate_designs), all_alpha
  else:      
      return optimizer_result_dataset(
      np.array(losses), np.array(designs), save_intermediate_designs), indices, all_alpha
  
#################### GD with LS- faster option
def train_GD_LS_fast(
    model, max_iterations, save_weights_path = '' , n_saves = 10,
    save_intermediate_designs=True, init_model=None,
    conv_criteria = False, limit = 0.5,
    use_prev_alpha = False, mode = 'robust', amax = 10000000, c2 = 0.9
):
  """
  Training a model with Gradient Descent with a line search
  amax: Maximum step size for line search
  maxiter: Maximum number of LS iterations to use
  use_prev_alpha: Whether to continue iteration with the previous alpha if LS fails
  use_prev_fval: Whether to supplyu the old function value to teh LS algorithm
  
  Working:
      If use_prev_fval is True:
              Uses old_old_fval argument to do LS after the first iteration
              if LS fails:
                  Uses prev alpha to continue iff use_prev_alpha = True
                  else exits
      If use_prev_fval is False:
              Performs LS with old_old_fval = None
              If LS fails, tries LS with old_old_fval,
                  if that fails too, uses
                          previous alpha
  """
  model(None)  # build model, if not built

  losses = []
  frames = []

  if init_model is not None:
    if not isinstance(model, models.PixelModel):
      raise TypeError('can only use init_model for initializing a PixelModel')
    model.z.assign(tf.cast(init_model(None), model.z.dtype))

  #tvars = model.trainable_variables
  
  flag =  False
  indices =[]
  if save_weights_path != '':
      filename = 'SGD_LS_weights_'
      print("Filename used: ",filename)
      #indices = []
      i=0
      while i < max_iterations:
          if i == 0:
              indices.append(i)
          i+=n_saves
          if i < max_iterations:
              indices.append(i)
      indices.append(max_iterations)
      _ = weights_to_file(model,save_weights_path,filename+str(indices[0]))
      flag =  True
      
  # gradient_stats_file  = kwargs.get('gradient_stats_file')
  # if gradient_stats_file is not None:
  #   train_summary_writer = tf.summary.create_file_writer(gradient_stats_file)
  
  # Implement GD with Line search
  #Loss function and its gradient
  def value(x):# Sets the model to x and finds teh loss value at that input
      _set_variables(tvars, x)
      logits = model(None)
      loss = model.loss(logits)
      return float(loss.numpy())

  def valuegrad(x):#grad of loss at x
    _set_variables(tvars, x)
    with tf.GradientTape() as t:
      t.watch(tvars)
      logits = model(None)
      loss = model.loss(logits)
    grads = t.gradient(loss, tvars)
    return _get_variables(grads).astype(np.float64)
  
  #Actual GD-LS starts
  prev_alpha = 1e-4
  all_alpha =[]
  prev_fnval = None # to be given to the line_search as old_old_fval
  # LS_failed =  False
  warning_tag = 'normal' # LS did not fail
  for i in range(max_iterations):
        tvars = model.trainable_variables        
      #Find search direction =  - direction of gradient = pk
        with tf.GradientTape() as t:
          t.watch(tvars)
          logits = model(None)
          loss = model.loss(logits)
        grads = t.gradient(loss, tvars)
        frames.append(logits.numpy().copy())
        losses.append(loss.numpy().copy())    
        
        #Do line search along pk
        pk = -1* _get_variables(grads).astype(np.float64)
        xk = _get_variables(tvars).astype(np.float64)
        
        if mode == 'robust':# amax doesn't play a role -- Use very high amax
            if i > 0:
                alpha_det = lsp.line_search_wolfe1(value, valuegrad, xk, pk,
                                               old_old_fval =prev_fnval,
                                                     amax = 10000000, c2 = c2)                
            else:
                alpha_det = lsp.line_search_wolfe1(value, valuegrad, xk, pk,                                               
                                                    amax = 10000000, c2 = c2)
        elif mode == 'switch':
            # Might be the best mode -- But fails in the first iteration for amax<1
            alpha_det = lsp.line_search_wolfe1(value, valuegrad, xk, pk,                                               
                                                    amax = amax, c2 = c2)
            if alpha_det[0] is None:# Switch to robust mode FROM this iteration
                print('LS failed; Switching to robust mode')
                warning_tag = 'LSfailed'
                mode = 'robust'
                if i > 0:
                    alpha_det = lsp.line_search_wolfe1(value, valuegrad, xk, pk,
                                               old_old_fval =prev_fnval,
                                                     amax = 10000000, c2 = c2)                
                else:
                    alpha_det = lsp.line_search_wolfe1(value, valuegrad, xk, pk,                                               
                                                    amax = 10000000, c2 = c2)
            
        elif mode == 'maxctrl':
            alpha_det = lsp.line_search_wolfe1(value, valuegrad, xk, pk, 
                                                      amax=amax, c2 =c2)  
            if alpha_det[0] is None:
                print('LS without old_old_fval failed: Trying with old_old_fval')
                warning_tag = 'LSfailed'
                alpha_det = lsp.line_search_wolfe1(value, valuegrad, xk, pk,
                                                old_old_fval =prev_fnval,
                                                      amax = 10000000, c2 = c2)             
        elif mode == 'puremax':
            alpha_det = lsp.line_search_wolfe1(value, valuegrad, xk, pk, 
                                                      amax=amax, c2 =c2)  
            
        else:
            print('Unrecognized mode; Please specify the correct mode')
            

        # if use_prev_fval and i>0:
        #     alpha_det = lsp.line_search_wolfe1(value, valuegrad, xk, pk,
        #                                        old_old_fval =prev_fnval,
        #                                              **kwargs) 
        # else:
            # alpha_det = lsp.line_search_wolfe1(value, valuegrad, xk, pk, 
            #                                           **kwargs)  
            # if alpha_det[0] is None:
            #     print('LS without old_old_fval failed: Trying with old_old_fval')
            #     alpha_det = lsp.line_search_wolfe1(value, valuegrad, xk, pk,
            #                                     old_old_fval =prev_fnval,
            #                                           **kwargs) 
                
        all_alpha.append(alpha_det[:-1] + (warning_tag,))
        
        # Do GD
        if alpha_det[0] is None:
            # LS_failed = True
            print('Linesearch did not converge') 
            if use_prev_alpha:                               
                print('Using alpha = ',str(prev_alpha))
                x_new = xk + prev_alpha * pk
                # Set the new x onto the model
                _set_variables(tvars, x_new) 
            else:
                print('Finishing training')
                _ = weights_to_file(model,save_weights_path,filename+str(i+1))
                indices = indices[:i+1]
                break
        else:
            x_new = xk + alpha_det[0] * pk
            # Set the new x onto the model
            _set_variables(tvars, x_new)    
            prev_alpha = alpha_det[0]
            
        prev_fnval = losses[i] # Uncomment this line to use the old_old_fval of line_search
        # Check for convergence
        #Will only enter this loop to check for convergence if the indice i+1
            # is in indices list
        if flag and i+1 in indices[1:]:
            if conv_criteria and len(losses) > 10:
                last_losses = np.array(losses[-10:])
                per_change = -1*np.diff(last_losses)/ last_losses[:-1]*100
                if np.all(per_change <= limit):
                    flag = False
                    l = (i+1)// n_saves
                    indices = indices[:l]   # problem for nsaves =10 etc.
                if flag:                        #maybe change to len(losses)
                    _ = weights_to_file(model,save_weights_path,filename+str(i+1))                                                       
            else:
                _ = weights_to_file(model,save_weights_path,filename+str(i+1))
               
        
  designs = [model.env.render(x, volume_contraint=True) for x in frames]
  if indices == []:
      return optimizer_result_dataset(
      np.array(losses), np.array(designs), save_intermediate_designs), all_alpha
  else:      
      return optimizer_result_dataset(
      np.array(losses), np.array(designs), save_intermediate_designs), indices, all_alpha    

###################LBFGS- without LineSearch#################################

def two_loop_recursion(rho, sk, yk, del_f):
    """
    all are matrices or set of numpy vectors of--n x m
    """
    q = np.copy(del_f)
    alpha = []
    for i in range(len(sk)-1,-1,-1):
        alpha_i = rho[i] * np.dot(sk[i].T, q)
        alpha.append(alpha_i)
        q = q - alpha_i * yk[i]
    
    gamma_k = np.dot(sk[-1].T, yk[-1]) / np.dot(yk[-1].T, yk[-1])
    r = gamma_k * q # H^0_k * q = gamma_k * I * q
    
    alpha_rev = alpha[-1::-1]
    for j in range(len(sk)):
        beta = rho[j] * np.dot(yk[j].T, r)
        r = r + sk[j] * (alpha_rev[j] - beta)
        
    return r
        
def angle_between(a,b):
    a = a/np.linalg.norm(a)
    b = b/np.linalg.norm(b)
    angle = np.dot(a.T, b)
    return angle        
    
def train_lbfgs_nols(model, max_iterations, learning_rate,
                     m = 10, conv_criteria = True, limit = 0.1,
                     save_weights_path = '', n_saves = 1):
    
    """
    
    """
    model(None)  # build model, if not built
    
    losses = []
    frames = []
    
    
    #tvars = model.trainable_variables
    
    flag =  False
    indices =[]
    if save_weights_path != '':
        filename = 'lbfgs_LS_weights_'
        print("Filename used: ",filename)
        #indices = []
        i=0
        while i < max_iterations:
            if i == 0:
                indices.append(i)
            i+=n_saves
            if i < max_iterations:
                indices.append(i)
        indices.append(max_iterations)
        _ = weights_to_file(model,save_weights_path,filename+str(indices[0]))
        flag =  True
        
    # Initialize all the necessary variables
    sk = []
    yk = []
    rho = []
    prev_del_f = None
    
    for i in range(max_iterations):
        tvars = model.trainable_variables        
        
        with tf.GradientTape() as t:
          t.watch(tvars)
          logits = model(None)
          loss = model.loss(logits)
        grads = t.gradient(loss, tvars)      

        del_fk = _get_variables(grads).astype(np.float64)
        grad_norm =  np.linalg.norm(del_fk)
        xk = _get_variables(tvars).astype(np.float64)
        
        if grad_norm < 1e-9 * max(1, np.linalg.norm(xk)):#from 1989 paper
            print(f"Gradient norm %f is too low: division by zero possible" 
                      %(grad_norm))
            break
                    
        frames.append(logits.numpy().copy())
        losses.append(loss.numpy().copy())
                
        if i == 0:
            #perform GD
            xk1 = xk + learning_rate * -1* del_fk
            _set_variables(tvars, xk1)
            
        else:   
            yk.append(del_fk - prev_del_f)
            rho.append((1/(yk[-1].T @ sk[-1])).item())
            assert len(yk) == len(sk) and len(yk) == len(rho)
            rho = rho[-m:]
            yk = yk[-m:]
            sk = sk[-m:]
            assert len(yk) == len(sk) and len(yk) == len(rho)
            
            if yk[-1].T @ sk[-1] < 0:# from the 1980 paper-because of no linesearch
                print("Criteria is not fullfilled")
                break
            Hg = two_loop_recursion(rho, sk, yk, del_fk)
            #print("Angle is ",angle_between(Hg, del_fk))
            xk1 = xk + learning_rate * -1 * Hg
            _set_variables(tvars, xk1)
        
        # Storing and updating
        sk.append(xk1 - xk)
        prev_del_f = del_fk[:]
        
        if flag and i+1 in indices[1:]:
            if conv_criteria and len(losses) > 10:
                last_losses = np.array(losses[-10:])
                per_change = -1*np.diff(last_losses)/ last_losses[:-1]*100
                if np.all(per_change <= limit):
                    flag = False
                    l = (i+1)// n_saves
                    indices = indices[:l]   # problem for nsaves =10 etc.
                if flag:                        #maybe change to len(losses)
                    _ = weights_to_file(model,save_weights_path,filename+str(i+1))                                                       
            else:
                _ = weights_to_file(model,save_weights_path,filename+str(i+1))
        
    
    #####
    designs = [model.env.render(x, volume_contraint=True) for x in frames]
    if indices == []:
        return optimizer_result_dataset(
        np.array(losses), np.array(designs), True), indices
    else:      
        return optimizer_result_dataset(
        np.array(losses), np.array(designs), True), indices
        


def constrained_logits(init_model):
  """Produce matching initial conditions with volume constraints applied."""
  logits = init_model(None).numpy().astype(np.float64).squeeze(axis=0)
  return topo_physics.physical_density(
      logits, init_model.env.args, volume_contraint=True, cone_filter=False)


def method_of_moving_asymptotes(
    model, max_iterations, save_intermediate_designs=True, init_model=None,
    save_weights_path = '' , n_saves = 10, t_args = None
):
  #flag =  False
  indices =[]
  if save_weights_path != '':
      filename = 'MMA_weights_'
      print("Filename used: ",filename)
      #indices = []
      i=0
      while i < max_iterations:
          if i == 0:
              indices.append(i)
          i+=n_saves
          if i < max_iterations:
              indices.append(i)
      indices.append(max_iterations)
      _ = weights_to_file(model,save_weights_path,filename+str(indices[0]))
      #flag =  True
      
  import nlopt  # pylint: disable=g-import-not-at-top

  if not isinstance(model, models.PixelModel):
    raise ValueError('MMA only defined for pixel models')

  env = model.env
  if init_model is None:
    x0 = _get_variables(model.trainable_variables).astype(np.float64)
  else:
    x0 = constrained_logits(init_model).ravel()

  def objective(x):
    return env.objective(x, volume_contraint=False)

  def constraint(x):
    return env.constraint(x)

  def wrap_autograd_func(func, losses=None, frames=None):
    def wrapper(x, grad):
      if grad.size > 0:
        value, grad[:] = autograd.value_and_grad(func)(x)
      else:
        value = func(x)
      if losses is not None:
        losses.append(value)
        # _ = weights_to_file(model,save_weights_path,filename+str(len(losses)))
      if frames is not None:
        frames.append(env.reshape(x).copy())
      return value
    return wrapper

  losses = []
  frames = []

  opt = nlopt.opt(nlopt.LD_MMA, x0.size)
  opt.set_lower_bounds(0.0)
  opt.set_upper_bounds(1.0)
  opt.set_min_objective(wrap_autograd_func(objective, losses, frames))
  opt.add_inequality_constraint(wrap_autograd_func(constraint), 1e-8)
  opt.set_maxeval(max_iterations + 1)
  opt.optimize(x0)

  designs = [env.render(x, volume_contraint=False) for x in frames]
  return optimizer_result_dataset(np.array(losses), np.array(designs),
                                  save_intermediate_designs),indices


def optimality_criteria(
    model, max_iterations, save_intermediate_designs=True, init_model=None,
):
  if not isinstance(model, models.PixelModel):
    raise ValueError('optimality criteria only defined for pixel models')

  env = model.env
  if init_model is None:
    x = _get_variables(model.trainable_variables).astype(np.float64)
  else:
    x = constrained_logits(init_model).ravel()

  # start with the first frame but not its loss, since optimality_criteria_step
  # returns the current loss and the *next* design.
  losses = []
  frames = [x]
  for _ in range(max_iterations):
    c, x = topo_physics.optimality_criteria_step(x, env.ke, env.args)
    losses.append(c)
    if np.isnan(c):
      # no point in continuing to optimize
      break
    frames.append(x)
  losses.append(env.objective(x, volume_contraint=False))

  designs = [env.render(x, volume_contraint=False) for x in frames]
  return optimizer_result_dataset(np.array(losses), np.array(designs),
                                  save_intermediate_designs)


def train_batch(model_list, flag_values, train_func=train_adam):
  batch_hist = []
  for batch_ix in range(flag_values.trials):
    logging.info(f'Starting trial {batch_ix}')
    history = train_func(model_list[batch_ix], flag_values)
    batch_hist.append(history)

  batch_hist = xarray.concat(batch_hist, dim='batch')
  return batch_hist


def optimize_level_set(model, max_iterations, save_intermediate_designs=True,
              live_plotting = False ):
  if not isinstance(model, models.PixelModel):
    raise ValueError('optimality criteria only defined for pixel models')

  # if init_model is None:
  #   x = _get_variables(model.trainable_variables).astype(np.float64)
  # else:
  #   x = constrained_logits(init_model).ravel()

  # start with the first frame but not its loss, since optimality_criteria_step
  # returns the current loss and the *next* design.
  
  env = model.env
  lsf = lsm_module.LSF(env.args)
  

  losses = []
  frames = []
  vol = []
  phi_snaps = []
  for iT in range(max_iterations):
    if live_plotting:
      lsm_module.live_plot(lsf.Phi, losses, vol)
    
    c, x,vol, phi  = lsm_module.lsf_step(lsf, env.ke, env.args, iT, vol)
    
    losses.append(c)
    frames.append(x)
    phi_snaps.append(phi)
    
    if np.isnan(c):
      # no point in continuing to optimize
      break
    
    if vol[iT] ==0 and c > 1e6:
      break
      
    #Convergence check
    if (iT>env.args['lsf_params']['nRelax']) and (np.abs(vol[iT]-env.args['volfrac'])/env.args['volfrac']<1e-3) and (np.all(np.abs(losses[iT]-losses[iT-10:iT])/losses[iT]<1e-3)):
        break

    #losses.append(env.objective(x, volume_contraint=False))

  designs = [env.render(x, volume_contraint=False) for x in frames]
  return optimizer_result_dataset(np.array(losses), np.array(designs),
                                  save_intermediate_designs), phi_snaps, vol