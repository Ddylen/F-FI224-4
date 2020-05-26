# -*- coding: utf-8 -*-
"""
Code for generating plots of x,y,z, theta 1, theta 2 etc
"""

import numpy as np
import time
from scipy import signal
import pickle
import sys
import math
from get_3D_pose import HAND, BODY, get_arm_3D_coordinates
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm

from scipy import signal
import numpy as np




#file_name = 'stationarytrial1.17.3.9.38'   #36s, hand on oil botle cap, nothing beneath it (dot on wrist close to shirt)
#file_name = 'stationarytrial2.17.3.9.41'   #65s, hand on plate on salt tube (dot on shirt sleeve)
#file_name = 'stationarytrial3.17.3.9.43'   #4s, very short, hand on salt shaker, dot on shirt
#file_name = 'stationaytrial4.17.3.9.43'    #38s, hand on salt sharker (dot on shirt)
file_name = 'stationaytrial5.17.3.9.44'    #50s, hand on table (dot on shirt)
lengths = [36,65,4,38,50]
file_names = ['stationarytrial1.17.3.9.38', 'stationarytrial2.17.3.9.41', 'stationarytrial3.17.3.9.43', 'stationaytrial4.17.3.9.43' , 'stationaytrial5.17.3.9.44' ]
std_store = [0,0,0,0]
wheighted_std_store = [0,0,0,0]
it = 0
for file_name in file_names:

    wristdatafile = open("bin/filtered_data/wrist." + file_name + ".pickle", "rb")
    wrist_list = pickle.load(wristdatafile)
    datafile = open("bin/filtered_data/" + file_name + ".pickle", "rb")
    results = pickle.load(datafile)
    
    
    
    len_wrist_list = len(wrist_list)
    x = np.arange(len_wrist_list)
    ys = [i+x+(i*x)**2 for i in range(len_wrist_list)]
    
    
    """
    colors = cm.rainbow(np.linspace(0, 1, len(ys)))
    i = 0
    ax = Axes3D(fig)
    for val,c in zip (wrist_list, colors):
        #print(val)
    
        ax.scatter(val[0], val[1], val[2], color = c)
        i = i+1
    """
    
    fig = plt.figure()
    #plt.close('all')
    
    plot_list_x = []
    plot_list_y = []
    plot_list_z = []
    num_list = []
    i = 0
    for val in wrist_list:
        plot_list_x.append(val[0])
        plot_list_y.append(val[1])
        plot_list_z.append(val[2])
        num_list.append(i)
        i = i+1
        
    
    
    
    
    
    
    
            
    
    #plot_list_x = signal.savgol_filter(plot_list_x, window_length, polyorder)
    #plot_list_y = signal.savgol_filter(plot_list_y, window_length, polyorder)
    #plot_list_z = signal.savgol_filter(plot_list_z, window_length, polyorder)
    
    
    plt.scatter(plot_list_x,plot_list_y)
    plt.title("x-y map")
    
    
    """
    fig = plt.figure()
    plt.plot(num_list, plot_list_x)
    plt.title('X data')
    
    
    fig = plt.figure()
    plt.plot(num_list, plot_list_y)
    plt.title('Y data')
    
    
    fig = plt.figure()
    plt.plot(num_list, plot_list_z)
    plt.title('Z data')
    """
    
    x_std = np.std(plot_list_x)
    y_std = np.std(plot_list_y)
    z_std = np.std(plot_list_z)
    
    x_mean = np.mean(plot_list_x)
    y_mean = np.mean(plot_list_y)
    z_mean = np.mean(plot_list_z)
    
    distance_from_mean = []
    for i in range(len(plot_list_x)):
        distance_from_mean.append( np.sqrt((plot_list_x[i]-x_mean)**2 + (plot_list_y[i]-y_mean)**2+ (plot_list_z[i]-z_mean)**2))
    
    print("max", max(distance_from_mean))
    print("min", min(distance_from_mean))
    std_3d = np.std(distance_from_mean)
    ans = [x_std, y_std, z_std, std_3d]
    print(ans)
    for i in range(len(std_store)):
        std_store[i]+= ans[i]
        wheighted_std_store[i] += ans[i]*lengths[it]
    it += 1

std_store = np.divide(std_store, len(file_names))
wheighted_std_store = np.divide(wheighted_std_store, np.sum(lengths))
print(std_store)
print(wheighted_std_store)





#datafile = open("bin/filtered_data/" + file_name + ".pickle", "wb")
#pickle.dump(results_list, datafile)




