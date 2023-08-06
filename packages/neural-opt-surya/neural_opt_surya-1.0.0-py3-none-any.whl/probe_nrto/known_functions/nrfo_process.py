#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 14:34:10 2022

@author: surya
Process teh xarray  datasets from all NRFO experiments
1. Merge them all into one
"""
#%%
data_dir = data_dir =  '/media/surya/surya_2/phd1/data/NRFO_expts_opt/'
import os
import xarray
keyword = '.nc'
ds = []
os.chdir(data_dir)
exp_list = os.listdir()

for i in exp_list:
    os.chdir(data_dir+ i)# + '/'+i+'_results'+'/' + folder+ '/' )
    all_files = os.listdir()
    key_files = [fname for fname in all_files if keyword in fname]
    for file in key_files:
        print(file)
        ds.append(xarray.open_dataset(file))
#%%        
fds = xarray.merge(ds)
os.chdir(data_dir)
fds2 = fds.ffill(dim ='step')
fds.to_netcdf('merged_nrfo_dim2_lbfgs.nc')
fds2.to_netcdf('merged_nrfo_dim2_lbfgs_filled.nc')

#%%
# Change all nan values!


