#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 21:41:56 2021

@author: Surya
Utilities with function to make visualization plots and hessian spectra
"""
#%%
from . import Visualization as vis
from . import nn_model_v2
from . import tensor_list_util as tu
from . import trajectory_plots as tplot
from . import lanczos_algorithm as la
from . import jax_density as jd
from . import matrix_vector_product as mvp
from ..nso import pipeline_utils
from ..nso import models
from ..nso import train_new
import time
import datetime
import tensorflow as tf
import os
import xarray
import pickle as pik
import numpy as np
import scipy
import matplotlib.pyplot as plt


def grad_at(new_model):
    """
    Returns the gradients of the Loss w.r.t model.trainable_variables as a vector.
    Important: Sets the parameters as well!!
    Inputs:
        index: The index at which the gradient vector is required
    Outputs:
        grad_vec: Tensor- A tf tensor 
        loss: float- the loss at the specified index
    """
    with tf.GradientTape() as tape:
        tape.watch(new_model.model.trainable_variables)
        loss = new_model.calc_loss(diffn = True)
    grad = tape.gradient(loss, new_model.model.trainable_variables )
    grad_vec = tu.tensor_list_to_vector(grad)
    return grad_vec, loss

def B_v_product_fast(nn_mdl, alphavals, pvals, wt_steps,
                     indice, ind, v, m = 10):
    """
    This function should return the B-v product at a given iterate.
    Note that this function is sequential and always starts from iterate 0 in its internal
    processing. Also, The Bv returned corresponds to teh matrix approximation that was used to
    find the next iterate at the current iterate i.e. at the start of "ind"    
    
    """ 
    #taking care of the input vector v -For Linearoperator
    eps = 2.2e-16
    v = v.numpy()
    if v.ndim ==1:
        v = np.copy(v[:,np.newaxis])
    # Initialization
    nn_mdl.penalty = pvals[ind]
    nn_mdl.alphaval = alphavals[ind]
    nn_mdl.set_parameters(nn_mdl.load_parameters(wt_steps[ind]))  
    # The first point and gradient at that location
    x0 =  tu.tensor_list_to_vector(nn_mdl.model.trainable_variables).numpy()  
    
    #Number of model parameters/ Dimension of the problem
    n = x0.shape[0]                    
    # Starting matrix used for the first step from x0 to x1
    #B = np.copy(I) # Cannot store- Too large for memory
    if ind == 0:
        return tf.cast(v,tf.float32) #- The first entry I @ v      
    # Initializing the necessary matrices for storing the  "m" pairs
    S_k = np.zeros(shape = (n,1)) 
    Y_k = np.zeros(shape = (n,1))    
    # A temporary variable to store the diagonal values of D_k
    D_k_temp = []
    # if ind < m: run from start else run only last m ones
    if ind<m+1:
        indice = indice[:m]
        wt_steps_temp = wt_steps[:m+1]
    else:
        indice = indice[ind - m:ind]   
        wt_steps_temp =wt_steps[ind - m:ind+1]
    n_vec_pairs = 0
    for k,indi in enumerate(indice):          
        #1. Obtain the iterates as vectors by setting the model to the stored parameters         
        if k == 0:  
            nn_mdl.penalty = pvals[indi]
            nn_mdl.alphaval = alphavals[indi]
            nn_mdl.set_parameters(nn_mdl.load_parameters(wt_steps_temp[k])) 
            x_k = tu.tensor_list_to_vector(nn_mdl.model.trainable_variables).numpy()
            g_k = grad_at(nn_mdl)[0].numpy()# previous gradient  

        # Obtain the new iterate and gradient
        nn_mdl.penalty = pvals[indi+1]
        nn_mdl.alphaval = alphavals[indi+1]
        nn_mdl.set_parameters(nn_mdl.load_parameters(wt_steps_temp[k+1])) 
        x_k1 =  tu.tensor_list_to_vector(nn_mdl.model.trainable_variables).numpy()
        g_k1 =  grad_at(nn_mdl)[0].numpy()
        
        #2. Compute necessary values
        sk = x_k1 - x_k # Change in iterates
        yk = g_k1 - g_k # Change in gradients
        Dii = yk.T @ sk # the diagonal element of D_k
        theta = (yk.T @ yk)/Dii # positive scalar multiple
        
        #saving for next iteration  
        x_k = np.copy(x_k1)
        g_k = np.copy(g_k1)          
        if sk.T @ yk > eps * np.linalg.norm(yk)**2:
            pass
        else:
            print(f'The vector pair for indice %d is not saved' %(indi))         
            return 'stop'        
        #3. Update the B matrix            
        if n_vec_pairs < m : #Case 1: Less than "m" saved iterates
            # Scale the initial matrix
            #B0 = theta * I        
            #Update the necessary compact matrices that form the B matrix
            S_k = np.hstack([S_k, sk]) # n x k matrix
            Y_k = np.hstack([Y_k, yk]) # n x k matrix
            L_k = np.zeros(shape = (k+1,k+1)) # k x k matrix
            if k == 0 :
                S_k = np.delete(S_k, obj = 0,axis = 1)
                Y_k = np.delete(Y_k, obj = 0,axis = 1)
            #Calculate other matrices
            D_k_temp.append(Dii.item())
            D_k = np.diag(D_k_temp) # k x k matrix         
            for i in range(k+1):
                for j in range(k+1):
                    if i > j:
                        L_k[i,j] = S_k[:,i].T @ Y_k[:,j]
                    else:
                        L_k[i,j] = 0.0
            
            SS = S_k.T @ S_k # S_k^T S_k              
        else:# Case 2 : After the m iterations
            assert S_k.shape[1] == m 
            #Form the necessary matrices for B update
            S_k = np.hstack([S_k, sk]) # n x m matrix
            Y_k = np.hstack([Y_k, yk]) # n x m matrix
            L_k = np.zeros(shape = (m,m)) # m x m matrix
            D_k_temp.append(Dii.item())
            #Delete the oldest pair
            S_k = np.delete(S_k, obj = 0,axis = 1)
            Y_k = np.delete(Y_k, obj = 0,axis = 1)            
            #Calculate other matrices
            D_k_temp = D_k_temp[1:]        
            D_k = np.diag(D_k_temp) # m x m matrix         
            for i in range(m):
                for j in range(m):
                    if i > j:
                        L_k[i,j] = S_k[:,i].T @ Y_k[:,j]
                    else:
                        L_k[i,j] = 0.0
            
            SS = S_k.T @ S_k # S_k^T S_k     
    
        #4. Use the updated matrices to compute B-v
        # Perform Cholesky factorization
        Chol_mat = theta * SS + L_k @ np.linalg.inv(D_k) @ L_k.T
        J_k = np.linalg.cholesky(Chol_mat)    
        p = np.vstack([Y_k.T @ v, theta * S_k.T @ v])
        
        # Solve p := inv(U) inv(L) p 
        # assemble U and L     
        # Make the term in matrices that raises D_k to -0.5 
        D_k_np_sq = np.diag(np.array(D_k_temp)**-0.5)    
        U = np.vstack([np.hstack([-1*D_k**0.5, D_k_np_sq @ L_k.T ]),
                       np.hstack([ np.zeros(D_k.shape), J_k.T])])
        L = np.vstack([np.hstack([D_k**0.5, np.zeros(D_k.shape) ]),
                       np.hstack([-1*L_k @ D_k_np_sq , J_k])])    
        # Forward and Backward solves
        x = scipy.linalg.solve_triangular(L, p, overwrite_b =True, lower= True)
        p = scipy.linalg.solve_triangular(U, x, overwrite_b =True)   
        Bv = theta * v - np.hstack([Y_k, theta * S_k]) @ p # correction in paper   
        n_vec_pairs+=1
        if ind == indi+1:
            return tf.cast(Bv, tf.float32)
# Curvature info
    # Curv = d.T H d
def curv_info(new_model, d):
    """
    Important: Sets the parameters as well!!
    Returns the curvature of the model along  the given direction.
    Inputs:
        d: Tensor- of dim (npars,1) with float64 datatype
    Ouputs:
        Curvature: float- d^T.H.d 
    """
    d = tf.linalg.normalize(d)[0]
    hv = tf.cast(mvp.model_hessian_vector_product(new_model.calc_loss, 
                                              new_model,tf.cast(d, tf.float32)),tf.float64)
    #print(hv.shape)
    vHv = tf.tensordot(d,tf.transpose(hv),2)    
    return vHv.numpy().item()

def angle_between(vec_a, vec_b): # works
    vec_a_norm  = tf.linalg.normalize(vec_a)[0] 
    assert tf.norm(vec_a_norm) > 0.9999
    vec_b_norm = tf.linalg.normalize(vec_b)[0]
    assert tf.norm(vec_b_norm) > 0.9999 # Normalization is not exact ~0.9999994
    cos_g_dir = tf.tensordot(vec_a_norm, tf.transpose(vec_b_norm),2).numpy()
    if cos_g_dir > 1.0 or cos_g_dir < -1:
        print('WARNING: Cosine is >/< 1/-1 @ Index ')    
    return cos_g_dir

def eigen_info(pos, ind, top_eigs, g,  min_dir,step_dir, inc_curvature = False):
    """
    Finds:
        1. Curvature along the specified eigen vecs: Ideally, they should be the eigenvalues
        2. Angle with the step taken/ any vector
        3. Angle with the minima direction/ any vector
        4. Angle with the gradient/ any vector
    
    Inputs:
        pos: The current eigen vector's position [Continuous values] --
                Forms the index of the np array-- If eig_vecs were saved continuously, pos = ind
        ind: The current index (Step) in the optimizaion trajectory  
            Corresponds to the saved weights [Need not be continuous]

e.g.
If the eig_vecs were stored at indices [1,5,10],
    The pos would correspond to values 0, 1 or 2
    ind  would be 1, 5 or 10                    
        top_eigs: A numpy array of shape (n_indices,n_pars,n_eigs)
                This contains the eigen vectors
                n_indices = Number of indices
                n_pars = Number of model parameters
                n_eigs =  Number of eigen vectors
        g: Gradient vector at the current index of type TF of dims (n_pars,1)
        min_dir: The direction of the minima as a TF vector
        step_dir: TF Array 
        inc_curvature: Boolean -- Whether to include the curvature calculations
    Outputs:
        all_info: Dictionary with the necessary curvature information and angles
        np.nan is returned for any angle in which at least one of teh vecs is a zero vector
        
    """
    all_info = {}
    all_info['cos_min'] = []
    all_info['cos_step'] = []
    all_info['cos_grad'] = []
    if inc_curvature:
        all_info['curv'] = []
            
    for tp in range(top_eigs.shape[2]):
        e_top = top_eigs[pos]# becomes a matrix of shape (n_pars, no_eigen_top)
        e_vec = e_top[:,tp][..., np.newaxis] # the reqd eigen vec in np format- shape(n_pars,1)
        e_vec = tf.constant(e_vec, dtype = tf.float64) # tf float64 format -- norm ~ 1
        if inc_curvature:
            cur_eig = curv_info(new_model, e_vec , index = ind)
        
        #Angle with min_dir
        if tf.norm(min_dir) != 0:
            cos_min_dir = angle_between(e_vec, tf.cast(min_dir,tf.float64))
        else:
            cos_min_dir = np.nan
                     
        #Angle with grad
        if tf.norm(g) !=0:
            cos_grad = angle_between(e_vec, tf.cast(g,tf.float64))
        else:
            cos_grad = np.nan
                
        #Angle with step_dir
        if tf.norm(step_dir) !=0:
            cos_step = angle_between(e_vec, tf.cast(step_dir,tf.float64))
        else:
            cos_step = np.nan
        
        all_info['cos_min'].append(cos_min_dir)
        all_info['cos_step'].append(cos_step)
        all_info['cos_grad'].append(cos_grad)
        if inc_curvature:
            all_info['curv'].append(cur_eig) 
                
    return all_info























def plot(grids, density, filename, label=None):
    fig = plt.figure()
    plt.semilogy(grids, density, label=label)
    plt.ylim(1e-10, 1e2)
    plt.ylabel("Density")
    plt.xlabel("Eigenvalue")
    plt.legend()
    plt.savefig(filename, dpi=300, format='svg')
    pik.dump(fig,open(filename+'_interact','wb'))
    plt.clf()
    
        
def hessian_spectra(nn_mdl, indices, loss_func, path ,
                     k=10,sigma2 = 1e-4,m = 50,method = 'lbfgs'):
    """
    nn_mdl: Gradvis interface model
    indices: List of indices at whcih to compute the spectrum
    loss-func: Loss function of the Keras model
    path: path to the weights
    n: number of iterations for Hessian trace estimation
    
    """  
    
    # folder = 'Hessian_' + str(datetime.datetime.now().microsecond)
    # if not os.path.exists(folder):
    #     os.makedirs(folder)
    # os.chdir(folder)
    # cur_dir = os.getcwd()
    T_all = []
    tim_ind =[]
    for i,ind in enumerate(indices):
        #set the proper index using set_parameters
        set_parameters(nn_mdl.model, method, ind, path)
        os.chdir(cur_dir)

        T_ls =[]        
        ts = time.time()
        for itr in range(k):#k lanczos iterations
            V,T = la.approximate_hessian(nn_mdl, loss_fn, m ,
                                         random_seed=itr)
            T_ls.append(T)
        tfin = time.time()
        tim_ind.append((tfin-ts)/60)
        T_ls_np = [t.numpy() for t in T_ls]
        density, grids = jd.tridiag_to_density(
                            T_ls_np, grid_len=10000, sigma_squared=sigma2)
        filename = 'index_'+str(ind)+'_k_'+str(k)+ '_m_' + str(m) + \
                    '_sigma_' + str(sigma2)
        plot(grids, density,filename)
        T_all.append(T_ls_np)
        print(f'Iteration {i} has been completed')
    
    #Save all generated data
    pik.dump(tim_ind,open('Time_for_each_index','wb'))
    pik.dump(T_all,open('T_matrix_all_indices','wb'))
    #save V matrix?
    #Hessian trace plots
    #TODO: Check for rademacher and error with Tr(VTV)
    #trace_i,trace_all=la.hessian_trace(nn_mdl,loss_func,n = n)
    #return trace_i, trace_all,V,T
    #Norm of hessian plots
    #intrinsic dimension
        
    #TODO: USe hessian trace, top eigen values, bottom eigen vals,
    #save data generated(V,T), etc ...

def find_typical_seeds(ds, vf, search=20):
    dst = ds.ffill(dim ='step')
    comp =None
    # if dst.model.values == 'CNN':
    #     comp = None
    # else:
    #     search = 20 # last 'n' steps are to be searched
    #     density = dst.density.isel(opt=0,alpha=0,p=0,problem=0,model=0, 
    #                                step =slice(-search,None))
    #     compliance = dst.compliance.isel(opt=0,alpha=0,p=0,problem=0,
    #                                      model=0, step =slice(-search,None))
    #     del_den = np.abs(density - vf)
    #     min_den_ind = del_den.argmin(dim = 'step').values # minimum change from teh required value  
    #     comp = []
    #     den = []
    #     for i,seed in enumerate(del_den.model_seed.values):
    #         den.append(del_den.sel(model_seed = seed).isel(step = min_den_ind[i]).values.item() + vf)
    #         comp.append(compliance.sel(model_seed=seed).isel(step=min_den_ind[i]).values.item())

    #     real_comp = [x for i,x in enumerate(comp) if np.abs(den[i]-vf) <= 1e-3 ]
    #     fake_comp1 = [x if np.abs(den[i]-vf) <= 1e-3 else 1e9 for i,x in enumerate(comp) ]
    if comp is None:  # Use cnn
        real_comp = dst.isel(step=-1).compliance.values
        fake_comp1 = list(real_comp[:].ravel())
    tol = [2,5,8,10]
    typ_seeds = []
    temp = fake_comp1[:]    
    median_comp = np.median(real_comp)
    for i,tolerance in enumerate(tol):
        for j,val in enumerate(temp):
            if np.abs(val-median_comp)/median_comp <= tolerance/100:
                typ_seeds.append(fake_comp1.index(val)+1)
                del temp[j]
        if len(typ_seeds) > 2:
            return typ_seeds, real_comp, median_comp   
    return typ_seeds, real_comp, median_comp


def set_parameters(model,method,index,path):
    #Load the file and make parameter_dict
    """
    Sets the saved pickled parameters values to a model
    model: Keras model
    method: 'Adam'/ 'lbfgs'
    index: Index of the weight file to be loaded
    path: path to the weight file
    """
    
    os.chdir(path)
    wt_file_name = method+'_weights_'+str(index)+'.p' 
    parameter_dict = pik.load(open(wt_file_name,'rb'))
    if not isinstance(model,models.PixelModel):
        for i,layer in enumerate(model.core_model.layers):
            if layer.trainable_variables == []:
                continue
            else:
                wt_names = [wt.name for wt in layer.trainable_variables]
                templst = [arr for k,arr in parameter_dict.items() if k in wt_names]
                layer.set_weights(templst)
        model.z.assign(parameter_dict['z:0'])
    else:
        model.z.assign(parameter_dict['Variable:0'])
    
#For eigen directions
def loss_fn(nn_mdl):
    """
    Returns the loss of a Keras model(nn_mdl.model) as a tensor
    """
    logits = nn_mdl.model(None)
    J = nn_mdl.model.loss(logits, vol_const_hard = nn_mdl.vol_const,
                           cone_filter=nn_mdl.filter , p = nn_mdl.penalty)  
    cur_density = train_new.mean_density(logits, nn_mdl.env.args, nn_mdl.filter)
    loss = tf.cast(nn_mdl.alphaval*((cur_density/nn_mdl.env.args['volfrac']) - 1)**2, 
                         dtype=tf.float64) + J/nn_mdl.model.J0
    return loss

#PLOTTING IN 2D 
def proj_plots(model, loss_fn, ind, path_of_wts,
               filename ='visualization_2dproj_',only_last =True, N = 20, mode = 'LA', plot ='all',
               h = 40, d =150, proz = 0.8):  
    """
    model: Keras model
    loss_fn: A function taht takes in a keras model and 
            outputs the loss as a tensor
    filelist: List of filenames containing the  NN weights
    ind : List of indices at which the plots are to be made--will consider the
        weights at these indices as the converged weight
        Caution: All indices till the required point are to be included
        eg. if ind = [1,2,3,4,5]
        and you want to plot ind = 4
        you should provide ind as  [1,2,3,4] and select only_last = True
    filename: the base file name for saving the figures and data(.npz file)
    only_last: If True, will only make plots considering the last index of ind
    N: number of grid points
    plot: ['all','R','P','E'] to plot all plots  or to selectively plot
            R=random , P= PCA or E = Eigen directions
            
    """
    #Should be in results directory
    #generate plots
    folder = 'proj_plots_'+str(datetime.datetime.now().microsecond)
    if not os.path.exists(folder):
        os.makedirs(folder)
    os.chdir(folder)
    cur_dir = os.getcwd()# this will be inside the proj_plots_### folder
    local_ind = []
    for i in ind:
        #Prereqs
        #create new indices list and file list
        local_ind.append(i)
        if only_last:
            if i != ind[-1]:      
                continue
            else:
                pass
                
        index = local_ind[-1]# for plotting last weight file
        set_parameters(model,method,index,path_of_wts)
        os.chdir(cur_dir)
        file_list = [path_of_wts + '/' + method + 
                     '_weights_' +str(i)+'.p' for i in local_ind]
        nn_mdl = nn_model_v2.Tensorflow_NNModel(model,file_list[-1])
        
        #Make separate folders for each index
        os.mkdir('Index_'+str(index))
        os.chdir('Index_'+str(index))
        
        if plot == 'all':
            vis.visualize(nn_mdl,file_list,N,filename +'rndm',random_dir = True,
                      proz=proz,verbose=True)
            if i not in ind[0:3]:#PCA needs atleast 3 runs
                vis.visualize(nn_mdl,file_list,N,filename +'pca',
                              random_dir = False, proz=proz,verbose=True)  
            vis.visualize_eigendirs(nn_mdl,file_list,N,filename +'eigen',
                                criterion =loss_fn,proz=proz,mode=mode,verbose=True)
            
            if i not in ind[0:3]:
                for name in [filename +'rndm',filename +'pca',filename +'eigen']:
                    for log in [True,False]:
                        tplot.plot_loss_2D(name+'.npz',filename= name+'2D_log'+
                                           str(log),is_log = log)
                        tplot.plot_loss_3D(name+'.npz',filename= name+'3D_log'+
                                           str(log),height=h,degrees=d,is_log=log)
            else:
                for name in [filename +'rndm',filename +'eigen']:
                    for log in [True,False]:
                        tplot.plot_loss_2D(name+'.npz',filename= name+'2D_log'+
                                           str(log),is_log = log)
                        tplot.plot_loss_3D(name+'.npz',filename= name+'3D_log'+
                                           str(log),height=h,degrees=d,is_log=log)
                
        elif plot == 'R':
            vis.visualize(nn_mdl,file_list,N,filename +'rndm',random_dir = True,
                      proz=proz,verbose=True)
            for log in [True,False]:
                tplot.plot_loss_2D(filename +'rndm' + '.npz',
                                   filename= filename +'rndm_2D_log'+
                           str(log),is_log = log)
                tplot.plot_loss_3D(filename +'rndm'+'.npz',
                                   filename= filename +'rndm_3D_log'+
                           str(log),height=h,degrees=d,is_log=log)
        elif plot == 'P':
            vis.visualize(nn_mdl,file_list,N,filename +'pca',random_dir = False,
                      proz=proz,verbose=True)
            for log in [True,False]:
                tplot.plot_loss_2D(filename +'pca' + '.npz',
                           filename= filename +'pca_2D_log'+
                   str(log),is_log = log)
                tplot.plot_loss_3D(filename +'pca'+'.npz',
                           filename= filename +'pca_3D_log'+
                   str(log),height=h,degrees=d,is_log=log)
        else:
            vis.visualize_eigendirs(nn_mdl,file_list,N,filename +'eigen',
                                criterion =loss_fn,proz=proz,mode=mode,verbose=True)
            for log in [True,False]:
                tplot.plot_loss_2D(filename +'eigen' + '.npz',
                           filename= filename +'eigen_2D_log'+
                   str(log),is_log = log)
                tplot.plot_loss_3D(filename +'eigen'+'.npz',
                           filename= filename +'eigen_3D_log'+
                   str(log),height=h,degrees=d,is_log=log)
        if i!= ind[-1]:
            del nn_mdl
        
        print(f'Index {i} has finished')
            




def save_gif_movie(images, path, duration=200, loop=0, **kwargs):
    images[0].save(path, save_all=True, append_images=images[0:],
                   duration=duration, loop=loop, **kwargs)
    
def generate_designs(ds,problem,saveall= True,steps = (0,200)):
    """
    Generates the  design for the experiment
    ds- dataset containing the designs
    problem: Instance of Problem class
    saveall= True, for saving all the designs
    steps = tuple(starting step, final step) or integer: the design at the
            required step number(s) will be saved
            The design at the steps from steps[0] to steps[1](inc) will be saved.
    folder =  Folder to which the designs will be saved-- Should be in 
                data/exp/seed/folder
    """
    folder ='designs_' + str(datetime.datetime.now().microsecond)
    if not os.path.exists(folder):
        os.makedirs(folder)
    os.chdir(folder)
    
    if saveall:
        images = [pipeline_utils.image_from_design(design, problem)
                      for design in ds.design]
        stepnum =  ds.step.values
        for im,num in zip(images,stepnum):
            im.resize((5*200, 5*100)).save('Design_' + str(num) + '.png')
        
        save_gif_movie([im.resize((5*200, 5*100)) for im in images],'design.gif')
    else:
        if type(steps) ==  tuple:
            s,f = steps
            images = [pipeline_utils.image_from_design(design, problem)
                      for design in ds.design.sel(step = slice(s,f+1))]
            stepnum = np.arange(steps[0],steps[1],1)
            for im,num in zip(images,stepnum):
                im.resize((5*200, 5*100)).save('Design_' + str(num) + '.png')
                
            
            save_gif_movie([im.resize((5*200, 5*100)) for im in images],'design.gif')
        else:
            images = pipeline_utils.image_from_design(
            ds.design.sel(step = steps), problem)
            images.resize((5*200, 5*100)).save('Design_' + str(steps) + '.png')
    
def h_trace(new_model, loss_fn, n, indice ,seed, path, method):
    """
    Finds the Hessian Trace  for the given indices and the Radius of Initialization for the 
        first index. Saves as pickle file
        
    new_model: Gradvis interface model
    Loss_fn:  Function that returns teh model loss
    n: number of iterations of the algorithm--Expectation is calculated over n runs
    seed: The seed for which the computation is done!
    returns -1 for radius if index 0 was not included
    """
    
    folder ='Hessian_Trace_' + str(datetime.datetime.now().microsecond)
    if not os.path.exists(folder):
        os.makedirs(folder)
    os.chdir(folder)
    trace = []
    cwd =os.getcwd()
    radius = tf.constant(-1)
    for i in indice: 
        set_parameters(new_model.model,method,i,path)
        os.chdir(cwd)
        trace_i =la.hessian_trace(new_model,loss_fn,n = n)
        trace.append(trace_i)
        if i == 0:
            radius = tf.norm(tu.tensor_list_to_vector
                             (new_model.model.trainable_variables))
        print(f'Index {i} is done')
    plt.plot(indice,trace)
    plt.xlabel('Indices')
    plt.ylabel('Hessian Trace')
    plt.title('Seed: ' + str(seed))
    plt.savefig('Htrace_vs_indices.svg')
    trace_radius = {'trace':trace,'radius':radius.numpy()}
    pik.dump(trace_radius,open('trace_values','wb'))
    return trace, radius.numpy()
    
def remove_weights(exp_num,keep):
    """
    Removes all weight files from all the folders in the experiment directory
            and compiles the datasets into a single one having seed,steps,
            designs and loss
            
    exp_num: Integer= The experiment number [Main folder]
    keep: List = List of strings of format ['_x',...] where x is a number
                Denotes the seed folders to be exempted from teh purging.
    #Saves the final dataset as exp_num_all.nc in teh exp_num directory 
    """
  #TODO:Test this function
    path = '/home/surya/Desktop/Thesis/Data/'  
    exp_path = path + str(exp_num)        
    os.chdir(exp_path)
    all_folders =os.listdir()#list of all files and directories 
    folders = []# contains the folders to be purged
    
    keep_folders =[]
    for i in all_folders:
        flag = True
        if not os.path.isfile(i):
            for a in keep:# if the string is in folder name, dont keep it for purge
                if i.endswith(a): 
                    flag = False
                    keep_folders.append(i)
            if flag:
                folders.append(i)
    ds =[]
    for i,file in enumerate(folders):
        os.chdir(exp_path+'/'+file)
        inside_files = os.listdir()
        for f in inside_files:
            if 'weights' in f:
                if '_0' in f:
                    pass
                else:
                    os.remove(f)
        #[os.remove(f) for f in inside_files if 'weights' in f ]
#TODO: dont remove the first weights
        if 'results' not in file:
            d = xarray.open_dataset(str(file)+'.nc').load()
            seed = int(file.split('_')[1])
            ds.append(d.expand_dims(dim = {'seed':[seed]}))
    
    for file in keep_folders:
        os.chdir(exp_path+'/'+file)
        d = xarray.open_dataset(str(file)+'.nc').load()
        seed = int(file.split('_')[1])
        ds.append(d.expand_dims(dim = {'seed':[seed]}))#adding a dimension
    
    os.chdir(exp_path)
    fds = xarray.concat(ds,dim ='seed')    
    fds.to_netcdf(str(exp_num)+'_all.nc')
    print('Successfully deleted')

def filter_loss(loss):
  # Sometimes our optimization loss does not always monotonically decrease
  # (e.g., due to line-search in L-BFGS). This routine makes it monotonic, to
  # facilitate comparisons
  import xarray
  return (
      loss
      .T.stack(z=['seed', 'method_name', 'problem_name'])
      .to_pandas()
      .cummin()
      .ffill()
      .pipe(xarray.DataArray, dims=['step', 'z'])
      .unstack('z')
  )

def hist_hoyer(problem_name,exp_num):
    """
    Plots the Loss- seed Histogram for Hoyer's data for the first 50 seeds
    """
    import os
    import xarray
    import numpy as np
    import matplotlib.pyplot as plt
    
    path = '/home/surya/Desktop/Thesis/Data/'  
    os.chdir(path)
    ds = xarray.open_dataset('all_losses.nc').load()
    
    ds_filtered = (ds.assign(loss=filter_loss(ds.loss))
               .assign_coords(size=ds.width*ds.height)
               .assign_coords(problem_class=('problem_name', 
                 ['_'.join(k.split('_')[:-2]) for k in ds.problem_name.data]))
                   )
    data_req = ds_filtered.sel(method_name = 'cnn-lbfgs').isel(seed =slice(1,51))
    cur_prblm = problem_name
    loss_val = data_req.sel(problem_name = cur_prblm).isel(step = -1).loss.values
    loss_val = loss_val[~np.isnan(loss_val)]
    hloss = max(loss_val)
    lloss = min(loss_val)
    val = 0.01*lloss
    nbins = int((hloss - lloss)/val)
    fig,ax = plt.subplots(1,1,figsize = (20,10))
    ax.hist(loss_val,bins = nbins, )
    plt.xticks(np.arange(lloss,hloss,5*val))
    ax.set_title((problem_name,'low_loss '+
              str(round(lloss,2)),'high_loss '+str(round(hloss,2))))
    ax.set_ylim([0,30])
    os.chdir(str(exp_num))
    os.chdir(str(exp_num) +'_'+'results')
    plt.savefig('Seed-Loss_Histogram_HOYER.svg')

def replot(exp_num, seed, ind, dim = '3d', log = True, plot_type = 'proj'):


    #MOVE TO THE TRAJECTORY AND LIST THE FILES
    path = '/home/surya/Desktop/Thesis/Data/'+str(exp_num) + '/'+ \
            str(exp_num)+'_results'+ '/'+str(exp_num)+'_'+str(seed)+'_results'
    os.chdir(path)
    dirs = os.listdir()
    req_dirs = [f for f in dirs if plot_type in f]
    print(req_dirs)
    val = input('Select folder Index (Index starts with zero!): ')
    folder = req_dirs[int(val)]
    path = path + '/' + folder
    #To select index
    os.chdir(path)
    dirs = os.listdir()
    req_dirs = [f for f in dirs if '_'+str(ind) in f]
    folder = req_dirs[0]
    path = path + '/' + folder
    os.chdir(path)    
    
    #Time to replot
    if plot_type == 'Hess':
        print('Not yet implemented')
        pass
        #pik.load(open('T_matrix_all_indices','rb'))
    elif plot_type == 'proj':
        print('[R,P,E]')
        sel  = int(input('Select the type of plot: '))
        if sel  == 0:#Random plots
            if dim == '2d':
                tplot.plot_loss_2D('visualization_2dproj_rndm.npz',
                               filename= 'visualization_2dproj_rndm_2D_log'+
                            str(log),is_log = log)
            else:
                tplot.plot_loss_3D('visualization_2dproj_rndm.npz',
                               filename='visualization_rndm_3D_log'+
                            str(log),is_log = log)
        if sel  == 1 :#PCA plots
            if dim == '2d':
                tplot.plot_loss_2D('visualization_2dproj_pca.npz',
                               filename= 'visualization_2dproj_pca_2D_log'+
                            str(log),is_log = log)
            else:
                tplot.plot_loss_3D('visualization_2dproj_pca.npz',
                               filename='visualization_pca_3D_log'+
                            str(log),is_log = log)
        if sel  == 2 :#Eigen plots
            if dim == '2d':
                tplot.plot_loss_2D('visualization_2dproj_eigen.npz',
                               filename= 'visualization_2dproj_eigen_2D_log'+
                            str(log),is_log = log)
            else:
                tplot.plot_loss_3D('visualization_2dproj_eigen.npz',
                               filename='visualization_eigen_3D_log'+
                            str(log),is_log = log)                           
    elif plot_type == 'Trace':
        pass


def init_properties_calc(exp_num,seeds,args,method,n=20):
    """
    Calculates the radius, trace, Loss at initialization
    Caution: This function requires the creation of the 
        combined dataset(exp_num_all.nc) and the weight files for index 0
    #TODO: Test this function!!
    """
    path = '/home/surya/Desktop/Thesis/Data/'  
    exp_path = path + str(exp_num) 
    os.chdir(exp_path)
    details ={'Seed': [], 'InitLoss' :[], 'Radius' : [],'Trace':[], 'MinLoss':[] }
    cwd = os.getcwd()
    
    for i in seeds:
        os.chdir(str(exp_num)+'_'+str(i))
        tf.keras.backend.clear_session()
        model = models.CNNModel_c2dt(args = args, seed = i)
        logits = model(None)
        r = tf.norm(tu.tensor_list_to_vector(model.trainable_variables))
        details['Radius'].append(r.numpy())
        
        init_loss = model.loss(logits)
        details['InitLoss'].append(init_loss.numpy())
        
        details['Seed'].append(i)
        set_parameters(model,method,0,path_of_wts = os.getcwd())
        
        file_list = [os.getcwd() + '/' + method + '_weights_' +
                     str(0)+'.p']
        new_model = nn_model_v2.Tensorflow_NNModel(model,file_list[-1])
        
        trace_s = la.hessian_trace(new_model,loss_fn,n = n)
        details['Trace'].append(trace_s)

        
        os.chdir(cwd)
        ds = xarray.open_dataset(str(exp_num)+'_all.nc')
        details['MinLoss'].append(ds.sel(seed= i).dropna('step').isel
                     (step = -1 ).loss.values)
    pik.dump(details,open('Init_details','wb'))
    return details
        
    
        
    
       
    
#%%
#remove_weights(19,keep = ['_16','_23'])
# hist_hoyer('michell_centered_both_32x64_0.12',exp_num = 7)


        
