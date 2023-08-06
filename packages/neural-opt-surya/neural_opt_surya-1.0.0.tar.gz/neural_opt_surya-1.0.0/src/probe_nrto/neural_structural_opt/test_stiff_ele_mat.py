#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 16:33:11 2022

@author: surya
testing the elemnet stiffnes matrix of hoyer vs that for mesh refinement
"""
import numpy as np
e = 5
nu = 0.5
H=1
W=1

knew =    e/(36*H*W*(1-nu**2))*np.array([12*H**2-6*W**2*nu+6*W**2,  4.5*H*W*(1+nu),  -12*H**2-3*W**2*nu+3*W**2,
                36*H*W*(-0.125+0.375*nu),  -6*H**2+3*W**2*nu-3*W**2,  -4.5*H*W*(1+nu),
                6*H**2+6*W**2*nu-6*W**2,  36*H*W*(0.125-0.375*nu)])

kh =  e/(1-nu**2)*np.array([1/2-nu/6, 1/8+nu/8, -1/4-nu/12, -1/8+3*nu/8,
              -1/4+nu/12, -1/8-nu/8, nu/6, 1/8-3*nu/8])

print(kh)
print(knew)