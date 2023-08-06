#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 09:49:37 2022

@author: surya
Performance of optimal architecture
"""
#%%
import os
import sys
sys.path.insert(1, "..")
import xarray 
import tensorflow as tf
import benchmark_fns.obj_models as models
import benchmark_fns.obj_funcs as of
import benchmark_fns.obj_utilities as utils
import autograd.numpy as np
# import pickle
#%%
exp_name = 'optuna_2'
data_dir = '/home/surya/Desktop/PhD_work/Masters_extension/data_masters/' 

os.chdir(data_dir)
if not os.path.exists(str(exp_name)):
    os.makedirs(str(exp_name))
os.chdir( data_dir+str(exp_name))

def objective():
    # define search space
    depth = 9
    width = (40,40,130,70,100,40,20,80,80)
    activation = "leaky"
    if activation == 'leaky':
        activation = tf.nn.leaky_relu
        
    if activation in ['relu', 'leaky', 'swish']:    
        init = tf.keras.initializers.HeNormal # https://arxiv.org/pdf/1710.05941v2.pdf
    elif activation in ['selu']:
        init = tf.keras.initializers.LecunNormal # https://mlfromscratch.com/activation-functions-explained/#/
    else:
        init = tf.keras.initializers.GlorotNormal
        
    bias_val = 3.5
    #init_scale = # conditional on the initializtion -- maybe use default value
    args = {'dim':2}
    all_inits = []
    final_mdl = []
    final_pix = []
    max_iterations = 30
    func_obj = of.Rastrigin(seed = 0, dim = args['dim']) 
    func_obj.o = 0
    # glob_val = func_obj.global_minval 
    # limit = np.abs(0.02 * glob_val) # 2% of Global value
    hits = {'pix':0, 'mdl':0}
    n_seeds = 100
    hits['pix_comp'] = []
    hits['mdl_comp'] = []
    ds_all = []
    for i in range(n_seeds):
        tf.keras.backend.clear_session()
        model = models.FCNN_simple(seed=i, args = args, depth =depth, width= width,
                                   kernel_init = init, activation =activation, 
                                   bias_val =bias_val)
        logit = model(None)
        # make pixel model
        pixmdl = models.PixelModel(seed = 0, args = args)
        pixmdl.z = tf.Variable(logit, trainable= True, dtype = tf.float32)
        # store init
        all_inits.append(logit.numpy()[0,:])
        # train the models
        dsmdl,_ = utils.train_lbfgs(model, func_obj, max_iterations)
        dspix,_ = utils.train_lbfgs(pixmdl, func_obj, max_iterations)
        # Check the value w.r.t global min
        glob_mdl = dsmdl.min(dim = 'step').loss.values
        glob_pix = dspix.min(dim = 'step').loss.values
        # final_mdl.append(dsmdl.min(dim='step').output.values)
        # final_pix.append(dspix.min(dim='step').output.values)
        hits['pix_comp'].append(glob_pix)
        hits['mdl_comp'].append(glob_mdl)
        # Store the dataset
        dsmdl = dsmdl.expand_dims({'model': ['nn'], 'seed' : [i]})
        dspix = dspix.expand_dims({'model': ['pix'], 'seed' : [i]})
        ds_comb = xarray.merge([dsmdl, dspix])
        ds_all.append(ds_comb)
        # count the relative number of hits = (hits neural/ total hits)
        del model
        del pixmdl    
    # Use stored inits to make det(cov(init))/ det(uniform)   
    fds = xarray.merge(ds_all)
    # det = np.linalg.det(np.cov(np.array(np.array(all_inits).T))) # have to check
    # scale = np.linalg.det(np.cov(np.random.uniform(0, 1, size = (n_seeds,2)).T)) 
    # o1 = 0.9*(hits['mdl']/ totalhits)
    # o2 = 0.1*det/scale
    # print("=====================O1:{}, O2:{}==================".format(o1,o2))
    # obj_val = o1 + o2
    all_details ={'pixhits': hits['pix'], 'modelhits': hits['mdl'], 'mdl_comp': hits['mdl_comp']
                  , 'pix_comp': hits['pix_comp']}
    #pickle.dump(all_details, open("Performance.p"), 'wb')
    return all_details, all_inits, fds
#%%
detail, init, fds = objective() 
print("Median complaince for model -", np.median(detail['mdl_comp']))
print("Median complaince for pixel -", np.median(detail['pix_comp']))
#%%
import plot_dets
func_obj = of.Rastrigin(seed = 0, dim = 2) 
func_obj.o = 0
import matplotlib.pyplot as plt
g_min, X1, X2, Y = func_obj.find_global_min(px = 200, scale_y = False)

fig = plt.figure(num=None, figsize=(3.5, 2.16), dpi=300, facecolor='w', edgecolor='k',
                         frameon=False)
CS = plt.contourf(X1, X2, Y, 100, zorder=0) 
for c in CS.collections:
    c.set_edgecolor("face")       
cbar = plt.colorbar()
# cbar.set_ticks([])
plt.xticks([])
plt.yticks([])   
plt.scatter(
    g_min[0],
    g_min[1],
    color="white",
    edgecolors="black",
    marker="X",
    #s=150,
    label="Global optimum",
    alpha=0.8,
)  # 0.55*px

# xval = [x[0] for x in init][0]
# yval = [x[1] for x in init][0]
# plt.scatter(xval, yval, c ='k', label = 'Starting point')

plt.xlabel("X")#, fontsize=20)  # 20
plt.ylabel("Y")#, fontsize=20)
plt.legend(loc="lower right")
plt.tight_layout()
# plt.savefig("/home/surya/Desktop/Paper1_images/ras.eps", bbox_inches='tight')
# plt.savefig("/home/surya/Desktop/Paper1_images/ras.svg", bbox_inches='tight')
#%%
import numpy
fig = plt.figure(num=None, figsize=(3.5, 2.16), dpi=300, facecolor='w', edgecolor='k',
                         frameon=False)
y1 = numpy.minimum.accumulate(fds.ffill(dim ='step').sel(
                model = 'pix').median(dim ='seed').loss.values)
pix_min = np.nanmin(y1)
y2 =numpy.minimum.accumulate(fds.ffill(dim ='step').sel(model = 'nn').median(dim ='seed').loss.values)
nn_min = np.nanmin(y2)
x1 = np.arange(0, len(y1))
plt.plot(x1, y1, label ='Conventional')
x2 = np.arange(0, len(y2))
plt.plot(x2, y2, label ='With NR')

plt.scatter(x1[-1], pix_min, label = str(pix_min)[:5])
plt.scatter(x2[-1], nn_min, label = str(nn_min)[:5])
plt.xlabel('Steps')
plt.ylabel('Median function value')
plt.legend()
#%%
from mpl_toolkits import mplot3d
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(X1, X2, Y, cmap='viridis')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')