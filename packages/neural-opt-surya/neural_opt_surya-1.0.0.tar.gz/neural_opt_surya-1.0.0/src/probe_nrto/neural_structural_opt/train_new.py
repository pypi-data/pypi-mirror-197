#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 12:52:43 2022

@author: surya
# New training module
Includes soft and hard volume constraints 
With continuation schemes
Notes on tensorboard:
    1. It stores info in different ways for LBFGS and tf-opts
    2. For LBFGS, for each penalty value (or alphavalue), variable number of steps are performed
        2a. Hence each pvalue is stored separately [i.e. for p=1.0 -> 10 steps, then p=1.5 -> 5 steps ]
        2b. The counting begins anew for each pvalue (or alphavalue)
    3. For tf-opts, each pvalue is only for one step, so no point in saving it separately
    
###
1. I accidentally name cone_filter as conv_filter but they are the same

"""
import autograd
import autograd.numpy as np
import logging
import tensorflow as tf
import xarray
import scipy.optimize
from . import models
from . import topo_physics
from . import autograd_lib

# For tensorboard - not need to check
def tb_save_grads_and_weights(train_summary_writer, grads, tvars, c, i, model, pval= 'NA'):
  """ For logging training details onto tensorboard
          - Weights
          - Gradients
          - Log(gradients)
          - preactivations!
    """
  with train_summary_writer.as_default():    
    for g, v in zip(grads, tvars):
      if g is not None:
        tf.summary.histogram("{}/grad_histogram/p_{}".format(v.name,pval), g, step = i)
        tf.summary.histogram("{}/weight_histogram/p_{}".format(v.name,pval), v, step = i)
        tf.summary.histogram("{}/LOG-grad_histogram/p_{}".format(v.name,pval), np.log(np.abs(g)+1e-12),
                                                  step = i)
        tf.summary.scalar('{}/weight_norm/p_{}'.format(v.name, pval), np.linalg.norm(v), step = i)
        tf.summary.scalar('{}/grad_norm/p_{}'.format(v.name, pval), np.linalg.norm(g), step = i)
    tf.summary.scalar('Compliance/p_{}'.format(pval), c, step = i)
    # for preactivations! --
    # https://stackoverflow.com/questions/41711190/keras-how-to-get-the-output-of-each-layer
    # inp = model.core_model.input
    # inp_val = model.z
    # for layer in model.core_model.layers[1:]:
    #     tf.keras.backend.clear_session()
    #     temp_mdl = tf.keras.Model(inputs = inp, outputs= layer.output)
    #     inter_val = temp_mdl(inp_val)
    #     tf.summary.histogram("{}/intermediate_histogram/p_{}".format(layer.name,pval), inter_val, step = i)
    #     del temp_mdl
     
def proj_density(x, beta):
    f = lambda eta : topo_physics.f_eta(x, beta, eta)
    eta = topo_physics.my_bisection(f, 0, 1, 1e-2)  
    x = (np.tanh(beta*eta) + np.tanh(beta*(x-eta)))/(np.tanh(beta*eta) + 
                                                     np.tanh(beta*(1-eta)))
    return x
    
    
def mean_density(logits, args, cone_filter = False,
                     den_proj =False, beta = 1):
    """  To include mean density calculations in the gradienttape for loss sensitivities"""
    shape = (args['nely'], args['nelx'])
    x = tf.reshape(0.0 + tf.cast(logits, tf.float64), shape)
    x = x * args['mask']
    
    if cone_filter:
      assert args['width']/args['nelx'] == args['height']/ args['nely']
      elem_size = args['width']/args['nelx']
      f = lambda x : autograd_lib.cone_filter(x, args['filter_width'] /elem_size, args['mask'])
      x = models.convert_autograd_to_tensorflow(f)(x)          
    if den_proj:
        # Heavyside projector
        f2 = lambda x : proj_density(x, beta)
        x = models.convert_autograd_to_tensorflow(f2)(x)         
    cur_density = tf.reduce_mean(x)/ np.mean(args['mask'])  
    return cur_density


    
def optimizer_result_dataset(losses, frames, save_intermediate_designs=True,
                             extra=None, p=3.0, alpha = None):# no need to check
  # The best design will often but not always be the final one.    
  if save_intermediate_designs:
    ds = xarray.Dataset({
        'loss': (('p','step'), [losses]),
        'design': (('p','step', 'y', 'x'), [frames]),
    }, coords={'step': np.arange(len(losses)), 'p':[p]})
  else:
    best_design = np.nanargmin(losses)
    ds = xarray.Dataset({
        'loss': (('p','step'), [losses]),
        'design': (('p','y', 'x'), [frames[best_design]]),
    }, coords={'step': np.arange(len(losses)), 'p':[p]})
    print("WARNING ---Best design here corresponds to the lowest total loss")
    
  if extra is not None:
      extra_dict = {k:(('p', 'step'), [v]) for k,v in extra.items()}
      ds_e = xarray.Dataset(extra_dict,
          coords = {'step':np.arange(len(losses)), 'p':[p]})
      ds = xarray.merge([ds,ds_e])   
  if alpha is None:
      ds = ds.expand_dims({'alpha':['NA']}) # For hard vol constraint
  else:
      ds = ds.expand_dims({'alpha':[alpha]})
      
  return ds

def _set_variables(variables, x):# no need to check
  shapes = [v.shape.as_list() for v in variables]
  values = tf.split(x, [np.prod(s) for s in shapes])
  for var, value in zip(variables, values):
    var.assign(tf.reshape(tf.cast(value, var.dtype), var.shape))


def _get_variables(variables):# no need to check
  return np.concatenate([
      v.numpy().ravel() if not isinstance(v, np.ndarray) else v.ravel()
      for v in variables])

def weight_saver(tot_iterations, save_weights_path, n_saves):# no need to check
    filename = 'weights_'
    #print("Filename used: ",filename)
    indices = []
    i=0
    while i < tot_iterations:
        indices.append(i)
        i+=n_saves
    indices.append(tot_iterations)   
    return filename, indices

def weights_to_file(model,directory,filename):# no need to check
    """ 
    Pickles the trainable weights into a file 
    For use of visualization of loss landscapes
    """
    import pickle
    new_param = dict()
    lis_v = model.variables #returns a list of the trainable
    #variables of the CNN model
    for i,var in enumerate(lis_v):
        key = model.variables[i].name
        new_param[key] = var.numpy()#can convert to numpy if needed    
    file_path = directory +'/'+filename+'.p'
    pickle.dump(new_param,open(file_path,'wb'))
    
################L-BFGS##################
def train_lbfgs_hard(
    model, max_iterations, save_weights_path = '' , n_saves = 1,
    save_intermediate_designs=True, conv_criteria = True, t_args = None,
    limit = 0.1, stats_file = None, **kwargs):
    """
          Trains models with hard volume constraint in place
          t_args :  Arguments for training
              "conv_filter" : Apply cone filter to densities [as in hoyer]
              "cont_scheme" : Apply continuation scheme
              "p_start" : starting penalty - TopOpt penalization
              "p_end" : Final penalty value
              del_p :  changing p value
              "scale_loss": Whether to scale the loss by initial loss
              "alpha_start": Starting alpha value for loss function [weight of volume constarint]
              "alpha_end": similar
              "del_alpha": 
    """   
    pval = [model.env.args['penal']]# Penalty values    
    if t_args['cont_scheme']:
       pval = np.arange(t_args['p_start'], t_args['p_end'], 
                           t_args['del_p'])        
    tvars = model.trainable_variables
    
    # Initial value for scaling compliance- as per paper
    pix_mdl = models.PixelModel(seed =0, args=model.env.args)
    pix_logits = pix_mdl(None)
    J0 = pix_mdl.loss(pix_logits, False, False, 3.0)
    model.J0 = J0.numpy().item()
    del pix_mdl
    
    # Saving weights 
    tot_itrs = max_iterations * len(pval)
    save_weights =  False
    indices =[]
    if save_weights_path != '':
        filename, indices = weight_saver(tot_itrs, save_weights_path, n_saves)
        save_weights =  True 
        
    # for tensorboard
    if stats_file is not None:
        train_summary_writer = tf.summary.create_file_writer(stats_file)  
        
    if save_weights: # save iniial weights
        weights_to_file(model,save_weights_path,filename+str(0))  
        
    if stats_file is not None: # Did not implement it yet!!!saving the first stats
        pass
       # real_comp_val = itr_details['real_comp'][0]
       # grad = itr_details['grads'][0]
       # tb_save_grads_and_weights(train_summary_writer, grad , tvars, 
       #                           real_comp_val, 0, model, pval =pval[count]) 
        
    def callback(x):
        _set_variables(tvars, x)
        nonlocal t_args
        nonlocal count 
        nonlocal weight_count
        nonlocal save_weights # For saving weights
        if weight_count == 0 and len(losses_p)==0: # first time running - saving initial weights
            losses_p.append(itr_details['loss'][0])
            comp_p.append(itr_details['compliance'][0])
            frame_p.append(itr_details['designs'][0])
            true_comp.append(itr_details['real_comp'][0])            
           
        losses_p.append(itr_details['loss'][-1])
        comp_p.append(itr_details['compliance'][-1])
        frame_p.append(itr_details['designs'][-1])
        true_comp.append(itr_details['real_comp'][-1])        
        logging.info("\n *Iteration %s" %(len(losses_p)-1))
        i = len(losses_p)-1 + weight_count # Check losses_p vs losses
        
        # For density projection -> Counts overal iterations to increase the beta
        # Currently-does not work with continuation scheme
        if t_args['den_proj']:
            change = np.max(np.abs(frame_p[-2].ravel() -
                                   frame_p[-1].ravel()))                       
            prev_beta = max(betas)
            if prev_beta < 100 and (i%t_args['beta_change'] ==0 or change <= 0.01):
                cur_beta =2 * prev_beta          
                print("Beta has been changed to ", cur_beta)   
            else:
                cur_beta = prev_beta
            betas.append(cur_beta)
        else:
            cur_beta =1
            
        if stats_file is not None: 
           real_comp_val = itr_details['real_comp'][-1]
           grad = itr_details['grads'][-1]
           tb_save_grads_and_weights(train_summary_writer, grad , tvars, 
                                     real_comp_val, i, model, pval =pval[count])        
        # clearing itr details
        for k,v in itr_details.items():
            itr_details[k] = []           
        
        nonlocal indices          
        if save_weights and i in indices:#Check weight saving!!
            if len(pval)==1: #--> Consider the convergence for weight saving
                if conv_criteria and i-1 > 10:
                    last_losses = np.array(losses_p[-10:])
                    per_change = -1*np.diff(last_losses)/ last_losses[:-1]*100
                    if np.all(per_change <= limit):
                        save_weights = False
                        indices = indices[:i]
                    weights_to_file(model,save_weights_path,filename+str(i))
                    #truncate indices                                        
                else:
                    weights_to_file(model,save_weights_path,filename+str(i))     
            else:
                weights_to_file(model,save_weights_path,filename+str(i))
        return None

    # Function returning the objective value and gradient        
    def value_and_grad(x):
      _set_variables(tvars, x)
      nonlocal t_args
      nonlocal count 
      
      with tf.GradientTape() as t:
        t.watch(tvars)
        logits = model(None)
        if t_args['den_proj']:
            J = model.loss(logits, True, t_args['conv_filter'], pval[count],
                           t_args['den_proj'], betas[len(losses_p[1:])])
        else:
            J = model.loss(logits, True, t_args['conv_filter'], pval[count],
                           t_args['den_proj'], 1.0)  
    
        if t_args['scale_loss']:
            loss = J/model.J0   
        else:
            loss = J
      grads = t.gradient(loss, tvars)
      logging.info("\n --Functioncall")
      # Log details of this function call
      itr_details['grads'].append(grads)
      itr_details['loss'].append(loss.numpy().item())
      itr_details['designs'].append(logits.numpy().copy())
      itr_details['compliance'].append(J.numpy().copy())
      if t_args['den_proj']:
          real_comp_val = model.loss(logits, True, t_args['conv_filter'], 3.0,
                                     t_args['den_proj'], betas[len(losses_p[1:])])
      else:
          real_comp_val = model.loss(logits, True, t_args['conv_filter'], 3.0,
                                     t_args['den_proj'], 1)
              
      itr_details['real_comp'].append(real_comp_val.numpy().item())      
      
      return float(loss.numpy()), _get_variables(grads).astype(np.float64)
    
    # Optimization starts here
    ds = []  
    count = 0 # Index for penalty values and alpha
    weight_count = 0
    betas = [0.1]
    itr_details = {'grads' :  [], 'loss':[],
                   'compliance': [], 'designs' :[],
                   'real_comp': []}    
    for i in pval:        
        print("Current penalty: ", pval[count])
        logging.info("\n Current penalty: %s" %(pval[count]))
        losses_p =[]
        comp_p =[]
        frame_p = []
        true_comp = []        
        x0 = _get_variables(tvars).astype(np.float64)    
        # rely upon the step limit instead of error tolerance for finishing.
        _, _, info = scipy.optimize.fmin_l_bfgs_b(
            value_and_grad, x0, maxfun=max_iterations, maxiter =max_iterations,
                            callback=callback,
                            factr=1, pgtol=1e-14,**kwargs)
        if not t_args['den_proj']:
            betas = list(np.ones(len(frame_p)))
        designs = [model.env.render(x, volume_contraint=True,
                                    cone_filter = t_args['conv_filter'],
                                    den_proj = t_args['den_proj'], beta=betas[b]) 
                                   for b,x in enumerate(frame_p)]
        extra_details ={'c_loss':np.array(comp_p), 'compliance': np.array(true_comp),
                        'betas': np.array(betas)}
        ds_p = optimizer_result_dataset(np.array(losses_p), np.array(designs),
                                save_intermediate_designs, extra_details, p=pval[count])
        ds.append(ds_p)
        count += 1
        weight_count+=len(losses_p)    
    if save_weights:
        indices = indices[:weight_count]
    ds= xarray.merge(ds)
    return ds, indices

def train_lbfgs_soft(
    model, max_iterations, save_weights_path = '' , n_saves = 1,
    save_intermediate_designs=True, conv_criteria = True, t_args = None,
    limit = 0.1, stats_file = None ,**kwargs):
    """
          Trains models with hard volume constraint in place
          t_args :  Arguments for training
              "conv_filter" : Apply cone filter to densities
              "cont_scheme" : Apply continuation scheme
              "p_start" : starting penalty - TopOpt penalization
              "p_end" : Final penalty value
              del_p :  changing p value
              del_alpha :  changing alpha value
              "alpha_start" : start value of alpha
              "alpha_end" : End value of alpha
    """
    pval = [model.env.args['penal']]# Penalty values  
    alpha_val = np.arange(t_args['alpha_start'], t_args['alpha_end'],
                          t_args['del_alpha'])    
    if t_args['cont_scheme']:
       pval = np.arange(t_args['p_start'], t_args['p_end'], 
                           t_args['del_p'])        
    tvars = model.trainable_variables
    
    # Initial value for scaling compliance- as per paper
    pix_mdl = models.PixelModel(seed =0, args=model.env.args)
    pix_logits = pix_mdl(None)
    J0 = pix_mdl.loss(pix_logits, False, False, 3.0)
    model.J0 = J0.numpy().item()
    del pix_mdl

    if stats_file is not None:
        train_summary_writer = tf.summary.create_file_writer(stats_file)  
        
    def callback(x):
        _set_variables(tvars, x)
        nonlocal t_args
        nonlocal count 
        nonlocal weight_count
        nonlocal save_weights # For saving weights        
        if weight_count == 0 and len(losses_p)==0: # first time running - saving initial weights
            losses_p.append(itr_details['loss'][0])
            comp_p.append(itr_details['compliance'][0])
            frame_p.append(itr_details['designs'][0])
            true_comp.append(itr_details['real_comp'][0])
            den_p.append(itr_details['density'][0])
            
        losses_p.append(itr_details['loss'][-1])
        comp_p.append(itr_details['compliance'][-1])
        frame_p.append(itr_details['designs'][-1])
        true_comp.append(itr_details['real_comp'][-1])        
        den_p.append(itr_details['density'][-1])
        logging.info("\n *Iteration %s" %(len(losses_p)-1))
        i = len(losses_p)-1 + weight_count # Check losses_p vs losses

        if stats_file is not None: 
           real_comp_val = itr_details['real_comp'][-1]
           grad = itr_details['grads'][-1]
           tb_save_grads_and_weights(train_summary_writer, grad , tvars, 
                                     real_comp_val, i, model, pval =pval[count])        
        # clearing itr details
        for k,v in itr_details.items():
            itr_details[k] = []           
        
        nonlocal indices          
        if save_weights and i in indices:#Check weight saving!!
              if len(np.unique(pval)) ==1:
                  if conv_criteria and i-1 > 10:
                      last_losses = np.array(losses_p[-10:])
                      per_change = -1*np.diff(last_losses)/ last_losses[:-1]*100
                      if np.all(per_change <= limit):
                          save_weights = False
                          indices = indices[:i]
                      weights_to_file(model,save_weights_path,filename+str(i))
                      #truncate indices                                        
                  else:
                      weights_to_file(model,save_weights_path,filename+str(i))   
              else:
                   weights_to_file(model,save_weights_path,filename+str(i)) 
        return None
    
    # Function returning the objective value and gradient
    def value_and_grad(x):
      _set_variables(tvars, x)
      nonlocal t_args
      nonlocal count
      args = model.env.args      
      with tf.GradientTape() as t:
        t.watch(tvars)
        logits = model(None)
        J = model.loss(logits, False, t_args['conv_filter'], pval[count])  
        cur_density = mean_density(logits, args, t_args['conv_filter'])
        loss = tf.cast(alpha_val[count]*((cur_density/args['volfrac']) - 1)**2, 
                             dtype=tf.float64) + J/model.J0 
      grads = t.gradient(loss, tvars)  
      # Log details of this function call
      logging.info("\n --Functioncall")
      itr_details['grads'].append(grads)
      itr_details['loss'].append(loss.numpy().item())
      itr_details['designs'].append(logits.numpy().copy())
      itr_details['compliance'].append(J.numpy().copy())
      real_comp_val = model.loss(logits, False, t_args['conv_filter'], 3.0)
      itr_details['real_comp'].append(real_comp_val.numpy().item()) 
      itr_details['density'].append(cur_density.numpy().item())
      
      return float(loss.numpy()), _get_variables(grads).astype(np.float64)
    
    # Optimization starts here
    ds = []  
    count = 0 # Index for penalty values and alpha
    weight_count=0
    itr_details = {'grads' :  [], 'loss':[],
                   'compliance': [], 'designs' :[],
                   'real_comp': [], 'density' : []}      
    if len(pval) ==1:
        decider = alpha_val
        flag_decider = 'alpha'
        pval = np.ones(len(alpha_val)) * pval[0]
    else:
        decider = pval
        flag_decider = 'pval'
        if len(alpha_val) < len(pval):
            diff = len(pval) - len(alpha_val)
            alpha_val = np.concatenate((alpha_val, alpha_val[-1]*np.ones((diff,))))             
    # Saving weights 
    save_weights =  False
    tot_itrs = max_iterations * len(decider)
    indices =[]
    if save_weights_path != '':     
        filename, indices = weight_saver(tot_itrs, save_weights_path, n_saves)
        save_weights =  True
    if save_weights:
        weights_to_file(model,save_weights_path,filename+str(0))  
        
    if stats_file is not None: 
        pass
       # real_comp_val = itr_details['real_comp'][0]
       # grad = itr_details['grads'][0]
       # tb_save_grads_and_weights(train_summary_writer, grad , tvars, 
       #                           real_comp_val, 0, model, pval =pval[count]) 
    # Decider is the factor for restrating L-BFGS
        # If penaly is the decider, it restarts L-BFGS for each penalty
        # L-BFGS is run for "max_iterations" for each penalty value
    for i in decider: 
        print("Current penalty & alpha value --(%0.1f, %0.1f)" %(pval[count], alpha_val[count])) 
        logging.info("\n Current penalty & alpha value --(%0.1f, %0.1f)" %(pval[count], alpha_val[count]))
        losses_p =[]
        comp_p =[]
        den_p = []
        frame_p = []
        true_comp = []
        # model.J0 = model.loss(model(None), False, t_args['conv_filter'], 
        #                       pval[count]).numpy().item() 
        x0 = _get_variables(tvars).astype(np.float64)
        # rely upon the step limit instead of error tolerance for finishing.
        _, _, info = scipy.optimize.fmin_l_bfgs_b(
            value_and_grad, x0, maxfun=max_iterations, maxiter =max_iterations, # fixed budget
                       callback=callback ,factr=1, pgtol=1e-14, **kwargs)        
        if len(losses_p) ==0:
            count += 1
            continue
        designs = [model.env.render(x, volume_contraint=False, cone_filter = t_args['conv_filter']) 
                                   for x in frame_p]
        extra_details ={'c_loss':np.array(comp_p), 'compliance': np.array(true_comp),
                        'density': np.array(den_p)}
        if flag_decider == 'pval':
            ds_p = optimizer_result_dataset(np.array(losses_p), np.array(designs),
                                save_intermediate_designs, extra_details, 
                                p=pval[count], alpha =None)
        else:
            ds_p = optimizer_result_dataset(np.array(losses_p), np.array(designs),
                                save_intermediate_designs, extra_details, 
                                p='vary', alpha =alpha_val[count])    
        ds.append(ds_p)
        count += 1  
        weight_count+=len(losses_p)
    if save_weights:
        indices = indices[:weight_count]
    ds= xarray.merge(ds)
    return ds, indices

############################# ADAM #####################################
def train_tf_opt_hard(
      model, max_iterations, 
      opt = 'adam',
      save_weights_path = '' , stats_file = None,
      n_saves = 1, save_intermediate_designs=True, 
      conv_criteria = False, limit = 0.1, t_args =None, **kwargs):
    """
      New!
      n_saves -- save weights of the model every n steps
      save_weights_path -- Path to folder to save the weight files
      conv_criteria = True => the weight saving is stopped early[based on 10 previous
                                                 weights]
      limit - 0.5%, if successive losses are less than this , stop saving
      weights
      """
    if opt == 'adam':
        optimizer = tf.keras.optimizers.Adam(0.1, amsgrad = True, 
                                     epsilon = 1e-8,
                                     global_clipnorm = 0.01) 
    else:
        print("Falling back to SGD optimizer")
        optimizer = tf.keras.optimizers.SGD(1e-8)
    pval = [model.env.args['penal']]# Penalty values    
    if t_args['cont_scheme']:
       pval = np.arange(t_args['p_start'], t_args['p_end'], 
                           t_args['del_p'])        
    tvars = model.trainable_variables
    
    # Initial value for scaling compliance- as per paper
    pix_mdl = models.PixelModel(seed =0, args=model.env.args)
    pix_logits = pix_mdl(None)
    J0 = pix_mdl.loss(pix_logits, False, False, 3.0)
    model.J0 = J0.numpy().item()
    del pix_mdl
    
    # Saving weights
    flag =  False
    indices =[]
    if save_weights_path != '':
        filename, indices = weight_saver(max_iterations, save_weights_path, n_saves)
        flag =  True
    # for tensorboard    
    if stats_file is not None:
        train_summary_writer = tf.summary.create_file_writer(stats_file)
    losses = []
    frames = []
    comp_p = []
    true_comp = []     
    betas = [0.1]
    for i in range(max_iterations + 1):
        if i >= len(pval):
          penal = pval[-1]
        else:
          penal = pval[i]   
        with tf.GradientTape() as t:
          t.watch(tvars)
          logits = model(None)   
          with t.stop_recording():
              if t_args['den_proj']:
                  if len(frames) == 0:
                      change =1
                      prev_beta = cur_beta = betas[0]
                  else:
                      change = np.max(np.abs(logits.numpy().ravel() - frames[-1].ravel()))                       
                      prev_beta = max(betas)
                      if prev_beta < 100 and (i%t_args['beta_change'] ==0 or change <= 0.01):
                          cur_beta =2 * prev_beta          
                          print("Beta has been changed to ", cur_beta)   
                      else:
                          cur_beta = prev_beta
                  betas.append(cur_beta)
              else:
                  cur_beta =1
          J = model.loss(logits, True, t_args['conv_filter'], penal,
                                     t_args['den_proj'], cur_beta)      
          if t_args['scale_loss']:
              loss = J/model.J0
          else:
              loss = J      
        grads = t.gradient(loss, tvars)
        losses.append(loss.numpy().item())
        frames.append(logits.numpy())
        comp_p.append(J.numpy().copy()) # Compliance with varying p
        real_comp_val =  model.loss(logits, True, t_args['conv_filter'], 3.0,
                                        t_args['den_proj'], cur_beta)
        true_comp.append(real_comp_val.numpy().item())
        if flag and i in indices:
              if conv_criteria and i > 10:
                  last_losses = np.array(losses[-10:])
                  per_change = -1*np.diff(last_losses)/ last_losses[:-1]*100
                  if np.all(per_change <= limit):
                      flag = False
                      indices = indices[:i+1]
                  weights_to_file(model,save_weights_path,filename+str(i))                                     
              else:
                  weights_to_file(model,save_weights_path,filename+str(i))                   
        if i < max_iterations:        
          optimizer.apply_gradients(zip(grads, tvars))   
        if stats_file is not None: 
           tb_save_grads_and_weights(train_summary_writer, grads,
                                     tvars, real_comp_val, i ,model)  

    betas = betas[1:] # first is repeated 
    if not t_args['den_proj']:
        betas = list(np.ones(len(frames)))
    designs = [model.env.render(x, volume_contraint=True, cone_filter = t_args['conv_filter'],
                                den_proj = t_args['den_proj'], beta=betas[b]) 
                               for b,x in enumerate(frames)]
    extra_details ={'c_loss':np.array(comp_p), 'compliance': np.array(true_comp),
                    'betas' : np.array(betas)}
    if t_args['cont_scheme']:
        p_code = 'vary'
    else:
        p_code = pval[0]
    return optimizer_result_dataset(np.array(losses), np.array(designs),
                    save_intermediate_designs, extra_details, p = p_code),indices

def train_tf_opt_soft(model, max_iterations, opt = 'adam',
      save_weights_path = '' , stats_file = None,
      n_saves = 1, save_intermediate_designs=True, 
      conv_criteria = False, limit = 0.1, t_args =None, **kwargs):
    """
      New!
      n_saves -- save weights of the model every n steps
      save_weights_path -- Path to folder to save the weight files
      conv_criteria = True => the weight saving is stopped early[based on 10 previous
                                                 weights]
      limit - 0.5%, if successive losses are less than this , stop saving
      weights
      """
    if opt == 'adam':
        optimizer = tf.keras.optimizers.Adam(0.01, amsgrad = True, 
                                     epsilon = 1e-8, global_clipnorm = 0.01)      
    else:
        raise ValueError("Wrong optimizer is chosen")  
    pval = [model.env.args['penal']]# Penalty values 
    if t_args['cont_scheme']:
       pval = np.arange(t_args['p_start'], t_args['p_end'], 
                           t_args['del_p']) 
    # Initial value for scaling compliance- as per paper
    pix_mdl = models.PixelModel(seed =0, args=model.env.args)
    pix_logits = pix_mdl(None)
    J0 = pix_mdl.loss(pix_logits, False, False, 3.0)
    model.J0 = J0.numpy().item()
    del pix_mdl
    
    alpha_val = np.arange(t_args['alpha_start'], t_args['alpha_end'], 
                          t_args['del_alpha'])       
    tvars = model.trainable_variables
    # Saving weights - TODO: Check this
    flag =  False
    indices =[]
    if save_weights_path != '':
        filename, indices = weight_saver(max_iterations, save_weights_path, n_saves)
        flag =  True        
    losses = []
    frames = []
    comp_p = []
    true_comp = []   
    den_p = []
    
    # for tensorboard    
    if stats_file is not None:
        train_summary_writer = tf.summary.create_file_writer(stats_file)     
    betas = [0.1]    
    for i in range(max_iterations + 1):
        if i >= len(pval):
          penal = pval[-1]
        else:
          penal = pval[i]  
        if i >= len(alpha_val):
            alpha = alpha_val[-1]
        else:
            alpha = alpha_val[i]            
        args = model.env.args    
        with tf.GradientTape() as t:
          t.watch(tvars)
          logits = model(None)   
          with t.stop_recording():
              if t_args['den_proj']:
                  if len(frames) == 0:
                      change =1
                      prev_beta = cur_beta = betas[0]
                  else:
                      change = np.max(np.abs(logits.numpy().ravel() - frames[-1].ravel()))                       
                      prev_beta = max(betas)
                      if prev_beta < 100 and (i%t_args['beta_change'] ==0 or change <= 0.01):
                          cur_beta =2 * prev_beta          
                          print("Beta has been changed to ", cur_beta)   
                      else:
                          cur_beta = prev_beta
                  betas.append(cur_beta)
              else:
                  cur_beta =1
          J = model.loss(logits, False, t_args['conv_filter'], penal,
                         t_args['den_proj'], cur_beta)     
          cur_density = mean_density(logits, args, t_args['conv_filter'],
                                     t_args['den_proj'], cur_beta)
          loss = tf.cast(alpha*((cur_density/args['volfrac']) - 1)**2, 
                               dtype=tf.float64) + J/model.J0         
        grads = t.gradient(loss, tvars)  
        # Log all details        
        losses.append(loss.numpy().item())      
        comp_p.append(J.numpy().copy()) # Compliance with varying p
        den_p.append(cur_density.numpy().item())
        real_comp_val =  model.loss(logits, False, t_args['conv_filter'], 3.0,
                                    t_args['den_proj'], cur_beta)
        frames.append(logits.numpy())
        true_comp.append(real_comp_val.numpy().item())
        # Save weights
        if stats_file is not None: 
            tb_save_grads_and_weights(train_summary_writer, grads, tvars, 
                                      real_comp_val, i, model)
        if flag and i in indices:
              if conv_criteria and i > 10:
                  last_losses = np.array(losses[-10:])
                  per_change = -1*np.diff(last_losses)/ last_losses[:-1]*100
                  if np.all(per_change <= limit):
                      flag = False
                      indices = indices[:i+1]
                  weights_to_file(model,save_weights_path,filename+str(i))                                      
              else:
                  weights_to_file(model,save_weights_path,filename+str(i))                
                    
        if i < max_iterations:
          optimizer.apply_gradients(zip(grads, tvars)) 
    designs = [model.env.render(x, volume_contraint=False, cone_filter = t_args['conv_filter']
                                ,den_proj=t_args['den_proj'], beta=betas[b]) 
                               for b,x in enumerate(frames)]
    
    extra_details ={'c_loss':np.array(comp_p), 'compliance': np.array(true_comp), 
                    'density':np.array(den_p)}
    if t_args['cont_scheme']:
        p_code = 'vary'
    else:
        p_code = pval[0]
    return optimizer_result_dataset(np.array(losses), np.array(designs),
                    save_intermediate_designs, extra_details, p = p_code, 
                    alpha = 'vary'),indices


def method_of_moving_asymptotes(
    model, max_iterations, save_intermediate_designs=True, init_model=None,
    save_weights_path = '', n_saves = 10, t_args = None, conv_criteria = False, 
    limit = 0.1
    ):
    
  indices =[]
  import nlopt  # pylint: disable=g-import-not-at-top

  if not isinstance(model, models.PixelModel):
    raise ValueError('MMA only defined for pixel models')

  env = model.env
  args = model.env.args
  
  if init_model is None:
    x0 = _get_variables(model.trainable_variables).astype(np.float64)
  # else:
  #   x0 = constrained_logits(init_model).ravel()
  
  def objective(x):      
      if t_args['den_proj']:
          # calculate beta to be used for this iteration
          i = len(losses)
          if i ==0 : # very first iteration starting
              change =1
              prev_beta = cur_beta = betas[0]
          else:
              change =  np.max(np.abs(x.ravel() - frames[-1].ravel()))          
              prev_beta = max(betas)#[i-1]
              if prev_beta < 100 and (i%t_args['beta_change'] ==0 or change <= 0.01):
                  cur_beta =2 * prev_beta          
                  print("Beta has been changed to ", cur_beta)   
              else:
                  cur_beta = prev_beta
              betas.append(cur_beta)
      else:
          cur_beta = 1
      return env.objective(x, volume_contraint=False, p=args['penal'], 
                         cone_filter = t_args['conv_filter'],
                         den_proj =t_args['den_proj'],
                         beta=cur_beta) 
  
  def constraint(x): # is called after teh objective
      if t_args['den_proj']:
          cur_beta = betas[-1]
      else:
          cur_beta = 1      
      return env.constraint(x, den_proj =t_args['den_proj'], beta=cur_beta)

  def wrap_autograd_func(func, losses=None, frames=None, den_proj = False):
    def wrapper(x, grad):
      # Call objective
      if grad.size > 0:
        value, grad[:] = autograd.value_and_grad(func)(x)
      else:
        value = func(x)        
      # Log the details of the current iteration  
      if losses is not None:
          losses.append(value)
          densities.append(mean_density(env.reshape(x).copy(), args, True))
      if frames is not None:
          frames.append(env.reshape(x).copy())           
      return value
    return wrapper

  losses = []
  frames = []
  densities = []
  betas = [0.1]
  opt = nlopt.opt(nlopt.LD_MMA, x0.size)
  #opt.set_param('verbosity', 1)
  opt.set_lower_bounds(0.0)
  opt.set_upper_bounds(1.0)
  opt.set_min_objective(wrap_autograd_func(objective, losses, frames))
  opt.add_inequality_constraint(wrap_autograd_func(constraint), 1e-8)
  opt.set_maxeval(max_iterations + 1)
  opt.set_xtol_rel(1e-5)
  opt.optimize(x0)
  if not t_args['den_proj']:
      betas = np.ones(len(losses))
  designs = [env.render(x, volume_contraint=False, 
                        cone_filter = t_args['conv_filter'],
                        den_proj=t_args['den_proj'], beta=betas[b])
                         for b,x in enumerate(frames)]
  
  extra_details ={'density':np.array(densities),
                  'betas': np.array(betas)}  
  return optimizer_result_dataset(np.array(losses), np.array(designs),
                                  save_intermediate_designs, extra_details,
                                  p = args['penal']), indices

################### restarted-LBFGS #############################
def train_lbfgs_restart(
    model, max_itr_run, save_weights_path = '' , n_saves = 1,
    conv_criteria = True, t_args = None, n_restarts = '',
    limit = 0.1, **kwargs):
    """
    L-BFGS with the ability to restart after 'max_itr_run' steps 
    It will be restarted  'n_restarts' no: of times    
    """   
    # Every restart runs for "max_itr_run" iterations
    if n_restarts == '':
        restart_vals = [0]
        tot_itrs = max_itr_run
    else:
        restart_vals = list(np.arange(0, n_restarts))     
        tot_itrs = max_itr_run * n_restarts
    
    tvars = model.trainable_variables  
    
    # Initial value for scaling compliance- as per paper
    pix_mdl = models.PixelModel(seed =0, args=model.env.args)
    pix_logits = pix_mdl(None)
    J0 = pix_mdl.loss(pix_logits, False, False, 3.0)
    model.J0 = J0.numpy().item()
    del pix_mdl
    
    # Saving weights 
    save_weights =  False
    indices =[]
    if save_weights_path != '':
        filename, indices = weight_saver(tot_itrs, save_weights_path, n_saves)
        save_weights =  True      
        weights_to_file(model,save_weights_path,filename+str(0))  
        
    def callback(x):
        _set_variables(tvars, x)
        nonlocal t_args
        nonlocal weight_count
        nonlocal save_weights # For saving weights
        
        if weight_count == 0 and len(losses_p)==0: # first time running 
            losses_p.append(itr_details['loss'][0])
            comp_p.append(itr_details['compliance'][0])
            frame_p.append(itr_details['designs'][0])
            true_comp.append(itr_details['real_comp'][0])            
            all_frames.append(frame_p[0])
            all_losses.append(losses_p[0])
            all_cal_comps.append(comp_p[0])
            all_real_comps.append(true_comp[0])
           
        losses_p.append(itr_details['loss'][-1])
        comp_p.append(itr_details['compliance'][-1])
        frame_p.append(itr_details['designs'][-1])
        true_comp.append(itr_details['real_comp'][-1])        
        logging.info("\n *Iteration %s" %(len(losses_p)-1))
        i = len(losses_p)-1 + weight_count # Check losses_p vs losses
        all_frames.append(frame_p[-1])
        all_losses.append(losses_p[-1])
        all_cal_comps.append(comp_p[-1])
        all_real_comps.append(true_comp[-1])
        # For density projection -> Count overall iterations to increase the beta
        # Currently-does not work with continuation scheme
        if t_args['den_proj']:
            change = np.max(np.abs(all_frames[-2].ravel() -
                                   all_frames[-1].ravel()))                       
            prev_beta = max(betas)
            if prev_beta < 100 and change <= 0.01:
                cur_beta =2 * prev_beta          
                print("Beta has been changed to ", cur_beta)   
            else:
                cur_beta = prev_beta
            betas.append(cur_beta)
        else:
            cur_beta =1                  
        # clearing itr details
        for k,v in itr_details.items():
            itr_details[k] = []          
        
        nonlocal indices          
        if save_weights and i in indices:#Check weight saving!!
            if len(restart_vals)==1: #--> Consider the convergence for weight saving
                if conv_criteria and i-1 > 10:
                    last_losses = np.array(losses_p[-10:])
                    per_change = -1*np.diff(last_losses)/ last_losses[:-1]*100
                    if np.all(per_change <= limit):
                        save_weights = False
                        indices = indices[:i]
                    weights_to_file(model,save_weights_path,filename+str(i))
                    #truncate indices                                        
                else:
                    weights_to_file(model,save_weights_path,filename+str(i))     
            else:
                weights_to_file(model,save_weights_path,filename+str(i))
        return None

    # Function returning the objective value and gradient        
    def value_and_grad(x):
      _set_variables(tvars, x)
      nonlocal t_args      
      with tf.GradientTape() as t:
        t.watch(tvars)
        logits = model(None)
        if t_args['den_proj']:
            J = model.loss(logits, True, t_args['conv_filter'], 3.0,
                           t_args['den_proj'], max(betas))
        else:
            J = model.loss(logits, True, t_args['conv_filter'], 3.0,
                           t_args['den_proj'], 1.0)
    
        if t_args['scale_loss']:
            loss = J/model.J0   
        else:
            loss = J
      grads = t.gradient(loss, tvars)
      logging.info("\n --Functioncall")
      # Log details of this function call
      itr_details['grads'].append(grads)
      itr_details['loss'].append(loss.numpy().item())
      itr_details['designs'].append(logits.numpy().copy())
      itr_details['compliance'].append(J.numpy().copy())
      if t_args['den_proj']:
          real_comp_val = model.loss(logits, True, t_args['conv_filter'], 3.0,
                                     t_args['den_proj'], max(betas))
      else:
          real_comp_val = model.loss(logits, True, t_args['conv_filter'], 3.0,
                                     t_args['den_proj'], 1)
              
      itr_details['real_comp'].append(real_comp_val.numpy().item())      
      
      return float(loss.numpy()), _get_variables(grads).astype(np.float64)
    
    # Optimization starts here
    all_frames = []
    all_losses = []
    all_real_comps =[]
    all_cal_comps = []
    
    ds = []  
    weight_count = 0
    betas = [0.1]
    itr_details = {'grads' :  [], 'loss':[],
                   'compliance': [], 'designs' :[],
                   'real_comp': []} 
    last_loss = 0
    for i in restart_vals:        
        if i==0:
            print('Starting optimization')
        else:
            print('Restarting optimization')
            model.J0 = last_loss # scale objective again for new iteration              
        losses_p =[]
        comp_p =[]
        frame_p = []
        true_comp = []        
        x0 = _get_variables(tvars).astype(np.float64)
        
        # rely upon the step limit instead of error tolerance for finishing.
        _, _, info = scipy.optimize.fmin_l_bfgs_b(
            value_and_grad, x0, maxfun=max_itr_run, maxiter =max_itr_run,
                            callback=callback,
                            factr=1, pgtol=1e-14,**kwargs)
        weight_count+=len(losses_p) 
        last_loss = comp_p[-1]    
        
    if save_weights:
        indices = indices[:weight_count]            
    if not t_args['den_proj']:
        betas = list(np.ones(len(all_frames)))

    designs = [model.env.render(x, volume_contraint=True,
                                cone_filter = t_args['conv_filter'],
                                den_proj = t_args['den_proj'], beta=betas[b]) 
                               for b,x in enumerate(all_frames)]
    extra_details ={'c_loss':np.array(all_cal_comps), 'compliance': np.array(all_real_comps),
                    'betas': np.array(betas)}
    ds = optimizer_result_dataset(np.array(all_losses), np.array(designs),
                            extra = extra_details)
    return ds, indices