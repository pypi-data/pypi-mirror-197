#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 10:35:54 2020

@author: Surya
This is an interface for all the experiments i.e. for visualization and hessian analysis
Accepts a keras model - Provides easy access to the parameters
"""

#Modified tensorflow model from GradVis
from topopt.nso import models
from topopt.nso import train_new
import tensorflow as tf
import pickle

class Tensorflow_NNModel():
    """
    Provides an interface to the Tensorflow NN model.
    """
    def __init__(self, model, cone_filter = True, vol_const_hard = True,
                 pixelmodel_init = True, pvalue = 3.0, alphaval = 0.2):
        
        """        
        Parameters
        ----------
        model : TYPE
            Converged model --CNNmodel instance
        filename : String
            pickled dictionary of weights of converged model

        Returns
        -------
        None.

        """
        self.model = model  
        self.filter = cone_filter
        self.env = model.env
        
        self.penalty =pvalue
        self.alphaval = alphaval
        
        self.vol_const = vol_const_hard  
        self.pixelmodel_init = pixelmodel_init   
        self._calc_init_loss()
        
        # self.counter = 0
# if pixelmodel == True, the penalty used is 3.0, otehrwise the value specified is used
    def get_parameters(self, all_params= True):# Need to check whether this shud return only trainable ones
        """
        Returns the parameters of the current model attribute as a dictionary
        either all parameters or only the trainable variables        
        """    
        if all_params:
            return self._tf_params_to_dict(all_params = True)
        else:
            return self._tf_params_to_dict(all_params = False)
        
    def load_parameters(self, filename):
        """
        Load saved weights as a dictionary
        """
        lis_var_file = pickle.load(open(filename,'rb'))  
        #self.set_parameters(lis_var_file)          
        return lis_var_file
        
    def set_parameters(self, parameter_dict): # --> setting needs all variables
        """
            Sets the parameters to the model
        """
        if not isinstance(self.model, models.PixelModel):
            for i,layer in enumerate(self.model.core_model.layers):
                if layer.variables == []:
                    continue
                else:
                    wt_names = [wt.name for wt in layer.variables]
                    templst = [arr for k,arr in parameter_dict.items() if k in wt_names]
                    layer.set_weights(templst)
            if isinstance(self.model, models.CNNModel_c2dt_corr):
                self.model.z.assign(parameter_dict['z:0'])
        else:
            self.model.z.assign(parameter_dict['Variable:0'])
            
    def calc_loss(self, diffn =  False):        
        #S:calculate loss of model
        if self.vol_const:
            logits = self.model(None)
            J = self.model.loss(logits, vol_const_hard = self.vol_const,
                                   cone_filter=self.filter, p = self.penalty)  
            loss = J
        else:
            logits = self.model(None)
            J = self.model.loss(logits, vol_const_hard = self.vol_const,
                                   cone_filter=self.filter , p = self.penalty)  
            cur_density = train_new.mean_density(logits, self.env.args, self.filter)
            loss = tf.cast(self.alphaval*((cur_density/self.env.args['volfrac']) - 1)**2, 
                                 dtype=tf.float64) + J/self.model.J0
        if diffn:
            return loss
        else:            
            return loss.numpy().item()    
    
    def _calc_init_loss(self):
        if self.pixelmodel_init:
            pix_mdl = models.PixelModel(seed =0, args=self.model.env.args)
            pix_logits = pix_mdl(None)
            J0 = pix_mdl.loss(pix_logits, False, False, 3.0)
            self.model.J0 = J0.numpy().item()
        else:
            self.model.J0 = self.model.loss(self.model(None), self.vol_const,
                           self.filter, self.penalty).numpy().item()
    
            
    def _tf_params_to_dict(self, all_params = True):# Only trainable ones are stored here
        """ 
        Extracts the variables from a TF model into a dictionary
        """
        new_param = dict()
        if all_params:
            lis_tv = self.model.variables
        else:
            lis_tv = self.model.trainable_variables#returns a list of the trainable

        for i,var in enumerate(lis_tv):
            if all_params:
                key = self.model.variables[i].name
            else:
                key = self.model.trainable_variables[i].name
            new_param[key] = var.numpy()#can convert to numpy if needed
        return new_param
    
