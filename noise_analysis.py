# -*- coding: utf-8 -*-
"""
Created on Thu Nov 07 12:18:58 2019

SOme basic data nalaysis on the noise present in a recorded joint position (only works if joint was still!)
"""
import numpy as np
import matplotlib.pyplot as plt
from reader import interpret2D


#wristpoints = interpret2D('vid0611HAND', 'wrist')
palmpoints, closedpoints, thumbpoints = interpret2D('vid0611HAND', 'hand')

#print(palmpoints)
xL, yL, cL = zip(*thumbpoints) #extract individual lists from a list of tuples
#print(xL)
#plt.axis([0,1000,0,1000])

plt.scatter(xL, yL)

arrx = np.array([xL])
xstdev = np.std(arrx)
xmean = np.mean(arrx)

arry = np.array([yL])
ystdev = np.std(arry)
ymean = np.mean(arry)

print("X stdev is", xstdev, "and X mean is ", xmean)
print("Y stdev is", ystdev, " and Y mean is ", ymean)

