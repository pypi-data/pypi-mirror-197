# coding: utf-8
#import torch
"""
Functions necessary to make 2d visulaization plots

"""
import warnings
import numpy as np
from pathlib import Path
from tqdm import tqdm
from sklearn.decomposition import PCA

from scipy import sparse
from scipy.sparse import linalg
from . import matrix_vector_product as mvp

def vprint(*vargs, **kwargs):
    if vprint.verbosity >0:
        print(*vargs, **kwargs)
vprint.verbosity=0


def vectoriz(vector_orig,parameter):
    """
    Reshapes vector into model shape.

    Args:
        vector_orig: unstructured array
        parameter: python array of numpy arrays (target shape)
    Return:
        python array of numpy arrays, with data from vecotr_orig and shape like parameter
    """
    vector = []
    indic = 0
    for p in parameter:
        len_p = p.size
        p_size = p.shape
        #print(p_size)
        vec_it = vector_orig[indic:(indic+len_p)].reshape(p_size)
        vector.append(np.array(vec_it, dtype=np.float32))
        indic += len_p
    return vector


def get_params(parameter):
    """
    Concatenates a python array of numpy arrays into a single, flat numpy array.
    """
    return np.concatenate( [ar.flatten() for ar in parameter], axis=None)


def mask_layers(parameter,layername):
    new_pars = parameter.copy()
    i=0

    for key,val in new_pars.items():
        if layername in key:
            continue
        else:
            val*=0
        i+=1
    return new_pars



def get_pca_vec(model, filenames, layer_names, pca_direcs=None):
    """
    Calculates the principal components of the model parameters.

    Args:
        model: nn model, with nn_model.Base_NNModel interface
        filenames: filenames of the checkpoints which shall be included into the PCA.
        pca_direcs: array of PCA directions to be computed
    Return:
        Two vectors with highest variance
    """
    mats = []

    for file in filenames:
        testi = model.load_parameters(file)
        parlis = np.ndarray([0])
        for key in testi:
            if "moving" in key:
                testi[key] *= 0
            parlis = np.concatenate((parlis,testi[key]), axis=None)
        pas = parlis
        #pas = get_params(parlis)
        mats.append(pas)
    mats = np.vstack(mats) # Shape of (n_indice, n_pars)
    mats_new = mats[:-1]-mats[-1]
    data = mats_new
    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(data.T) # Why tranform it??-- to make the shape correct
    vprint("Principal",pca.explained_variance_ratio_)
    print("Explained ratio ",pca.explained_variance_ratio_)

    return np.array(principalComponents[:,0]),np.array(principalComponents[:,1]),pca.explained_variance_ratio_


def cont_loss(model,parameter,alph,bet,get_v,get_w):
    """
    Calculates the loss landscape based on vectors v and w (which can be principal components).
    Changes the internal state of model. Executes model.

    Args:
        model: nn model, with nn_model.Base_NNModel interface
        parameter: weights of the converged net, centered point of analysis
        alph: list of scalars for 1st direction/alpha in paper --grid coords
        bet: scalar for 2nd direction/beta in paper
        get_v: 1st direction
        get_w: 2nd direction
    Return:
        list of loss values
    """
    vals = []
    for al in alph:
        testi_clone = parameter.copy()
        ind = 0
        # calculate new parameters for model
        for key in parameter:           
            testi_clone[key] = testi_clone[key] + al*get_v[ind] + bet*get_w[ind]
            ind += 1
        # load parameters into model and calcualte loss
        model.set_parameters(testi_clone)
        loss = model.calc_loss()
        vals = np.append(vals,loss)
    return vals


def give_coefs(model, filenames, parameter, v, w,layername=None):
    """
    Calculates the scale factors for plotting points in the 2D space spanned by the vectors v and w.
    Note: Needs a converged model! --'pas' variable uses this implicitly
    Args:
        model: nn model, with nn_model.Base_NNModel interface
        filenames: checkpoint files, which define the trajectory.
        parameter: central point, to which the trajectory will be calculated.
        v: 1st vector spanning the 2D space
        w: 2nd vector spanning the 2D space
    Return:
        list of coefficients
    """
    #par_step = torch_params_to_numpy(torch.load(filename+str(i)))
    matris = [v,w]
    matris= np.vstack(matris)
    matris = matris.T# shape of (n_pars,2)
    parlis = parameter.values()
    pas = get_params(parlis)#single array
    coefs = []
    for file in filenames:
        par_step = model.load_parameters(file)
        parstep = par_step.values()
        st = get_params(parstep)

        b = st-pas
        coefs.append(np.hstack(np.linalg.lstsq(matris,b,rcond=None)[0]))
#coeff - matris @ x =  b solution - n_pars x 2 @ 2 x 1 = n_pars,1
    return(coefs)

def normalize(parameter,get_v,get_w):
    """
    Normalizes the vectors spanning the 2D space, to make trajectories comparable between each other.

    Args:
        parameter: the parameters to normalize to.(The point of interest)
        get_v, get_w: the vectors in the 2D space, which should be normalized to 'parameter'.
    Return:
        tuple of normalized vectors get_v, get_w
    """

    parlis = list(parameter.values())
    parnames = list(parameter.keys()) 
    
    for i in range(len(parlis)):
        if 'moving' in parnames[i]:# or 'bias' in parnames[i] :# don't consider batch norm parameters and biases
            get_v[i] = get_v[i]*0
            get_w[i] = get_w[i]*0
        else:
            if 'dense/kernel' in parnames[i]:
                for j in range(parlis[i].shape[1]):
                    factor_v = np.linalg.norm(parlis[i][:,j])/(np.linalg.norm(get_v[i][:,j]) + 1e-10)
                    factor_w = np.linalg.norm(parlis[i][:,j])/(np.linalg.norm(get_w[i][:,j]) + 1e-10)
                    get_v[i][:,j] = get_v[i][:, j] * factor_v
                    get_w[i][:, j] = get_w[i][:, j] * factor_w
            else:            
                factor_v = np.linalg.norm(parlis[i])/(np.linalg.norm(get_v[i])+ 1e-10)
                factor_w = np.linalg.norm(parlis[i])/(np.linalg.norm(get_w[i])+ 1e-10)
                #returns 2-norm
                get_v[i] = get_v[i]*factor_v
                get_w[i] = get_w[i]*factor_w
    return get_v,get_w

def cosine_similarity(vec_a, vec_b):
    a = get_params(vec_a)
    b = get_params(vec_b)
    costheta =  np.dot(a, b)/(np.linalg.norm(a) * np.linalg.norm(b))
    print("The angle between chosen directions is ", np.arccos(costheta)*180/np.pi)
    warn=False
    if np.abs(costheta - 0) >=1e-2:
        #warnings.warn("Warning...........Chosen vectors are not perpendicular")
        warn=True
    return warn

################################
### Main function
################################
def _visualize(model,filenames,N,random_dir=False,proz=0.5,v_vec=[],w_vec=[],verbose=False,
               layername=None,pca_dirs=None):
    """
    Main function to visualize trajectory in parameterspace.

    Args:
        model: nn model, with nn_model.Base_NNModel interface
        filenames: list of checkpoint names (files with parameters), 
                    orderered with the centerpoint last in list
        N: number of grid points for plotting (for 1 dim)
        random_dir (bool): if random directions should be used instead of PCA
        proz: margins for visualized space (in %)
        v_vec, w_vec: if defined, custom vectors will be used instead of PCA
        verbose: verbosity of prints
        pca_dirs: choose the pca directions to be plotted, if None the first two are chosen
    Return:
        Array containing loss values, path values, variance data and the two pca components. Also a flag value.
    """
    # verbosity level settings
    if verbose:
        vprint.verbosity=1
    progress_bar_wrapper = None
    if verbose:
        progress_bar_wrapper = lambda x : tqdm(x)
    else:
        progress_bar_wrapper = lambda x : x

    # load the parameters of the final step
    parameter = model.get_parameters()#S:dictioanry
    parlis = list(parameter.values()) # list of 'parameter' values

    if len(v_vec)!=0 and len(w_vec)!=0:
        v = v_vec
        w = w_vec
    elif random_dir:
        total_params = sum(np.size(p) for p in parlis)
        warn =False
        for i in range(51): # 50 tries to make it perpendicular!
            if i==0 or warn:
                # np.random.seed(i)
                v = np.random.normal(size=total_params)
                w = np.random.normal(size=total_params)
                get_v = vectoriz(v,parlis)#S:converts flattened vector to crct size of model--as list
                get_w = vectoriz(w,parlis)#
                get_v,get_w = normalize(parameter, get_v, get_w)
                warn = cosine_similarity(get_v, get_w)
        if warn:
            print("Unsuccessful orthogonality")
        else:
            print('Successfully normalized')
    else:
        v,w,pca_variance = get_pca_vec(model, filenames,layername,pca_direcs=pca_dirs)
        get_v = vectoriz(v,parlis)#S:converts flattened vector to crct size of model--as list
        get_w = vectoriz(w,parlis)#
    
    if not random_dir:# True:use this for plotting trajs on rand dirns
        vprint("Calculating coefficients...")
        v = get_params(get_v)
        w = get_params(get_w)
        #S:v,w are not in nested form -- np.array - 1d (n_pars,)
        coefs = give_coefs(model, filenames, parameter, v, w, layername)
        coefs = np.array(coefs)# 2 coeffs for each path point
        
        paths = []
        vprint("Calculating Z-values of paths...")
        for val in progress_bar_wrapper(range(len(coefs))):
            yo = cont_loss(model, parameter,[coefs[val][0]],coefs[val][1],get_v,get_w)
            paths.append(yo)#loss for a given coeff_x,coeff_y

        paths = np.array(paths)
        coefs_x = coefs[:,0][np.newaxis]
        coefs_y = coefs[:,1][np.newaxis]
        n = N
        proz = proz
        boundaries_x = max(coefs_x[0])-min(coefs_x[0])
        boundaries_y = max(coefs_y[0])-min(coefs_y[0])

        x = np.linspace(min(coefs_x[0])-proz*boundaries_x,
                        max(coefs_x[0])+proz*boundaries_x, n)
        y = np.linspace(min(coefs_y[0])-proz*boundaries_y, 
                        max(coefs_y[0])+proz*boundaries_y, n)
        # x = np.linspace(-proz*boundaries_x, proz*boundaries_x, n)
        # y = np.linspace(-proz*boundaries_y, proz*boundaries_y, n)
    else:
        n = N
        proz = proz
        boundaries_x = 1.
        boundaries_y = 1.

        x = np.linspace(-proz*boundaries_x, proz*boundaries_x, n)
        y = np.linspace(-proz*boundaries_y, proz*boundaries_y, n)

    X, Y = np.meshgrid(x, y)
    vprint("Calculating loss landscape...")
    Z = []

    for i in progress_bar_wrapper(range(len(y))):
        vals = cont_loss(model,parameter,X[i],Y[i][0],get_v,get_w)
        Z.append(vals)

    if not random_dir:
        if len(v_vec)!=0 and len(w_vec)!=0:
            return [(X,Y,np.vstack(Z)),(coefs_x[0],coefs_y[0],paths.T[0])],1
        else:
            cache = (pca_variance,v,w)
            return [(X,Y,np.vstack(Z)),(coefs_x[0],coefs_y[0],paths.T[0]),cache],2
    else:
        cache = (v,w)
        return [(X,Y,np.vstack(Z)),cache],3#,(coefs_x[0],coefs_y[0],paths.T[0]),cache],3
#S: has implemented paths for eigen,rand(commented out later) and pca dirns


def visualize(model, filenames, N, path_to_file, random_dir=False,proz=0.5,
              v_vec=[],w_vec=[],verbose=False,layername=None,pca_dirs=None):
    """
    Wrapper for _visualize function that saves results as npz (numpy_compressed) file

    Args:
        model: nn model, with nn_model.Base_NNModel interface
        filenames: list of checkpoint names (files with parameters), orderered with the centerpoint last in list
        N: number of grid points for plotting (for 1 dim)
        path_to_file: path and filename where the results are going to be saved at
        random_dir (bool): if random directions should be used instead of PCA
        proz: margins for visualized space (in %)
        v_vec, w_vec: if defined, custom vectors will be used instead of PCA
        verbose: verbosity of prints
        pca_dirs: choose the pca directions to be plotted, if None the first two are chosen
    """

    my_file = Path(path_to_file+".npz")

    if my_file.is_file():
        print("File {} already exists!".format(path_to_file+".npz"))
    else:
        outputs,flag = _visualize(model, filenames, N,
                                  random_dir=random_dir,proz=proz,v_vec=v_vec,w_vec=w_vec,
                                  verbose=verbose,layername=layername,pca_dirs=pca_dirs)
        np.savez_compressed(path_to_file, a=outputs, b=flag)



def visualize_eigendirs(model,filenames,N,path_to_file,criterion,proz=0.5,mode='LA',verbose=False):
    """
    Wrapper for _visualize function that saves results as npz (numpy_compressed) file

    Args:
        model: nn model, with nn_model.Base_NNModel interface
        filenames: list of checkpoint names (files with parameters), orderered with the centerpoint last in list
        N: number of grid points for plotting (for 1 dim)
        path_to_file: path and filename where the results are going to be saved at
        random_dir (bool): if random directions should be used instead of PCA
        proz: margins for visualized space (in %)
        v_vec, w_vec: if defined, custom vectors will be used instead of PCA
        verbose: verbosity of prints
        pca_dirs: choose the pca directions to be plotted, if None the first two are chosen
    """

    my_file = Path(path_to_file+".npz")
    eigenfile = Path("eigen_"+path_to_file+"_vecs.npy")

    if my_file.is_file():
        print("File {} already exists!".format(path_to_file+".npz"))
    else:
        if eigenfile.is_file():
            print("File {} already exists! Continuing with loss landscape calculation...".format("eigen_"+path_to_file+"_vecs.npy"))
            vecs = np.load("eigen_"+path_to_file+"_vecs.npy")
            outputs,flag = _visualize(model,filenames,N,proz=proz,v_vec=vecs[:,0],w_vec=vecs[:,0],verbose=verbose)
            np.savez_compressed(path_to_file, a=outputs, b=flag)
        else:
            get_eigenvector(model,criterion,filename="eigen_"+path_to_file,num_eigs=2,mode=mode)
            vecs = np.load("eigen_"+path_to_file+"_vecs.npy")
            outputs,flag = _visualize(model,filenames,N,proz=proz,v_vec=vecs[:,0],w_vec=vecs[:,0],verbose=verbose)
            np.savez_compressed(path_to_file, a=outputs, b=flag)#Vector indices for v_vec and w_vec have been interchanged
            #because of commenting out portions of get_eigenvector()

def get_eigenvector(model,criterion,filename,num_eigs=2, mode='LA'):
    """
    Compute Eigenvectors of the Hessian and save them to the hard drive

    Args:
        model: nn model, with nn_model.Base_NNModel interface
        dataloader: dataloader in Pytorch in order to get access to samples
        criterion: Loss function
        filename: path and filename where the resulting eigenvectors are going to be saved at
        num_eigs: Number of eigenvectors and eigenvalues to compute
        max_samples: Number of samples to choose
        use_gpu (bool): Mode to use the GPU for the calculations
        mode: Which eigenvalues to compute (Largest magnitude, etc..)
    """
    num_pars = Num_pars_origs(model)#S:number of parameters
    #opi = HessVec(model, dataloader, criterion, use_gpu=use_gpu, percentage=percentage,num_iters=num_iters)
    f = lambda v: mvp.model_hessian_vector_product(criterion, model, v)#S::
    #print("Has reached after f:lambda")    
    A = linalg.LinearOperator((num_pars, num_pars), matvec=f)
    # print("A has been calculated")
    vals, vecs = sparse.linalg.eigsh(A, k=num_eigs, which=mode)

    print("Eigenvalues are {:.2f} and {:.2f}".format(vals[0],vals[1]))
    np.save(filename+"_vecs",np.vstack(vecs))
    np.save(filename+"_vals",vals)

def Num_pars_origs(model):
    '''
    Returns the number of weights in a Neural Network

    Args:
        model: nn model, with nn_model.Base_NNModel interface
    '''
    num_pars = 0
    for param in model.get_parameters(all_params=False).values():#S:contains the parameters
        #shape = param.shape#returns the number of elements of a tensor
        p_len = param.size
        num_pars += p_len
    return num_pars