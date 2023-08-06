#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 14:28:47 2022

@author: surya
"""

import tensorflow as tf
import pickle
import scipy.optimize
import autograd
import autograd.core
import autograd.numpy as np
from autograd import elementwise_grad as egrad
import xarray


def res_to_dataset(losses, frames, extras=None):
    if extras is None:
        ds = xarray.Dataset({
            'loss': (('step',), losses),
            'output': (('step', 'x'), frames),
        }, coords={'step': np.arange(len(losses))})
    else:
        loss_details =np.array(extras['loss_details'])
        obj = loss_details[:,0]
        c1 = loss_details[:,1]
        c2 = loss_details[:,2]
        ds = xarray.Dataset({
            'loss': (('step',), losses),
            'output': (('step', 'x'), frames),
            'obj':(('step',), obj),
            'c1':(('step',), c1),
            'c2':(('step',), c2)
        }, coords={'step': np.arange(len(losses))})    
    return ds

def weights_to_file(model,directory,filename):
    """ 
    Pickles the trainable weights into a file 
    For use of visualization of loss landscapes
    """
    new_param = dict()
    lis_tv = model.trainable_variables #returns a list of the trainable
    #variables of the CNN model
    for i,var in enumerate(lis_tv):
        key = model.trainable_variables[i].name
        new_param[key] = var.numpy()#can convert to numpy if needed    
    file_path = directory +'/'+filename+'.p'
    pickle.dump(new_param,open(file_path,'wb'))
    #return filename+'.p'

def convert_autograd_to_tensorflow(func):#S:func is completely written in numpy autograd
    @tf.custom_gradient
    def wrapper(x):
        vjp, ans = autograd.core.make_vjp(func, x.numpy())
        
        def first_grad(dy):                        
            @tf.custom_gradient
            def jacobian(a):
                vjp2, ans2 =  autograd.core.make_vjp(egrad(func), a.numpy())
                return ans2,vjp2 # hessian                    

            return dy* jacobian(x)  
        return ans, first_grad
    
    return wrapper


def convert_autograd_to_tensorflow_vector(func):#S:func is completely written in numpy autograd
    @tf.custom_gradient
    def wrapper(x):
        vjp, ans = autograd.core.make_vjp(func, x.numpy())              
        return ans, vjp    
    return wrapper


def _set_variables(variables, x):
  shapes = [v.shape.as_list() for v in variables]
  values = tf.split(x, [np.prod(s) for s in shapes])
  for var, value in zip(variables, values):
    var.assign(tf.reshape(tf.cast(value, var.dtype), var.shape))


def _get_variables(variables):
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

def train_lbfgs(model, func_obj, max_iterations, path ="", 
                n_saves =1, conv_criteria = False, limit = 0.01, **kwargs):
    """

            
    """
    func = convert_autograd_to_tensorflow(func_obj.ask) #So that gradients can flow to the models 
    tvars = model.trainable_variables
    
    save_weights =  False
    indices =[]
    if path != '':
        filename, indices = weight_saver(max_iterations, path, n_saves)
        save_weights =  True
    
    def callback(x):
        _set_variables(tvars, x)
        nonlocal save_weights # For saving weights
        nonlocal filename
        nonlocal path
        if len(fval)==0: # first timer running - saving initial weights
            fval.append(itr_details['fval'][0])
            outs.append(itr_details['outs'][0])
            if save_weights:
                weights_to_file(model,path,filename+str(0))   
             
        fval.append(itr_details['fval'][-1])
        outs.append(itr_details['outs'][-1])        
        #logging.info("\n *Iteration %s" %(len(losses_p)-1))
        i = len(fval)-1     
        # clearing itr details
        for k,v in itr_details.items():
            itr_details[k] = []          
        
        nonlocal indices          
        if save_weights and i in indices[1:]:#Check weight saving!!
            if conv_criteria and i-1 > 10:
                last_losses = np.array(fval[-10:])
                per_change = -1*np.diff(last_losses)/ last_losses[:-1]*100
                if np.all(per_change <= limit):
                    save_weights = False
                    indices = indices[:i]
                weights_to_file(model,path,filename+str(i))
                #truncate indices                                        
            else:
                weights_to_file(model,path,filename+str(i))    
        return None    
    
    
    def value_and_grad(z):
      _set_variables(tvars, z)      
      with tf.GradientTape() as t:
        t.watch(tvars)
        logits = 0.0 + tf.cast(model(None), tf.float64)           
        loss = func(tf.reshape(logits, (func_obj.dim)))
      grads = t.gradient(loss, tvars)
      #logging.info("\n --Functioncall")      
      # Log details of this function call
      itr_details['fval'].append(loss.numpy().item())
      itr_details['outs'].append(logits.numpy()[0])     
      return float(loss.numpy()), _get_variables(grads).astype(np.float64)
    
    itr_details = {'fval':[],
                   'outs': []} 
    fval = []   # To store the function values at each optimziation step   
    outs = []   #Storing teh outputs of the model (normalized!!)     
    x0 = _get_variables(tvars).astype(np.float64)    
    # rely upon the step limit instead of error tolerance for finishing.
    _, _, info = scipy.optimize.fmin_l_bfgs_b(
        value_and_grad, x0, maxfun=max_iterations, factr=1, pgtol=1e-14,callback=callback,
        **kwargs)    
    # Convert outs to xarray dataset            
    return res_to_dataset(fval, outs), indices


def train_tf_optimizer(model, func_obj, max_iterations, lr = 0.01, path ="",
                n_saves =1, conv_criteria = False, limit = 0.01,
                penalty_schedule = None,
                opt = 'default'):
    """
    penalty_schedule = (0.1, 0.01, 100) # (start, step, max)
    """
    if opt=='default':
        optimizer = tf.keras.optimizers.Adam()
    else:
        optimizer = tf.keras.optimizers.Adam(lr, amsgrad = True, 
                                 epsilon = 1e-8, global_clipnorm = 0.01) 
    model(None) # Build the model
    tvars = model.trainable_variables
    if penalty_schedule is not None:
        start, step, maxval = penalty_schedule
        pvalues = np.arange(start, maxval, step)
        if len(pvalues) < max_iterations+1:
            pvalues = np.concatenate((pvalues, 
                                      pvalues[-1]*np.ones(
                                          max_iterations+1-len(pvalues))) )
        func = convert_autograd_to_tensorflow(func_obj.ask)
        #So that gradients can flow to the models 
    else:
        func = convert_autograd_to_tensorflow(func_obj.ask)
    flag =  False
    indices =[]
    if path != '': # Routine to store the model's variables to Hard disk
        filename = 'weights_'
        print("Filename used: ",filename)
        i=0
        while i < max_iterations:
            if i == 0:
                indices.append(i)
            i+=n_saves
            if i < max_iterations:
                indices.append(i)
        indices.append(max_iterations)
        weights_to_file(model,path,filename+str(indices[0]))
        flag =  True
        
    fval = []   # To store the function values at each optimziation step   
    outs = []   #Storing teh outputs of the model (normalized!!) 
    extras = {'loss_details':[]}
    for i in range(max_iterations + 1):
        if penalty_schedule is not None:
            func_obj.lambdas = (pvalues[i], pvalues[i])
            
        with tf.GradientTape() as t:
            t.watch(tvars)
            logits = 0.0 + tf.cast(model(None), tf.float64)     
            loss = func(tf.reshape(logits, (func_obj.dim)))
            
        fval.append(loss.numpy().copy())
        outs.append(logits.numpy()[0].copy())
        if penalty_schedule is not None:
            extras['loss_details'].append(func_obj.loss_details)

      #Saving weight files to disk as pickled file: Applies convergence criterion as well
        if i == 0:#already saved initialization weight file
            pass
        else:
            if flag and i in indices[1:]:
                if conv_criteria and i > 10:
                    last_losses = np.array(fval[-10:])
                    per_change = -1*np.diff(last_losses)/ last_losses[:-1]*100
                    if np.all(per_change <= limit):
                        flag = False
                        indices = indices[:i+1]
                        weights_to_file(model,path,filename+str(i))                                     
                else:
                    weights_to_file(model,path,filename+str(i)) 

        if i < max_iterations:
            grads = t.gradient(loss, tvars)
            optimizer.apply_gradients(zip(grads, tvars))
    if penalty_schedule is not None:
        extras['lambdas'] = pvalues[:len(fval)]  
        ds = res_to_dataset(fval, outs, extras)
    else:
        ds=  res_to_dataset(fval, outs)
        
    return ds, indices

