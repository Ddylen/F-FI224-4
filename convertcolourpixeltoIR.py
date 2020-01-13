# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 14:24:06 2019

@author: birl
"""
import numpy as np
from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import ctypes

def convertcolourpixeltoIR(x,y):
    
    T = np.matrix([[0.3584, 0.0089, 0], [0.0031, 0.3531, 0.0001], [-101.5934, 13.6311, 0.9914]])
    homogeneouscolourvec = np.matrix([[x], [y], [1]])
    homogeneousIR = T *homogeneouscolourvec
    print(homogeneousIR.item(0), homogeneousIR.item(1), homogeneousIR.item(2))
    return homogeneousIR.item(0), homogeneousIR.item(1)
    
