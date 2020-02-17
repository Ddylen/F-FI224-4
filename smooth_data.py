# -*- coding: utf-8 -*-
"""
Get the smoothed trajectory data from multiple plots
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

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def plot_vertical_line(plot, xval):
    """draw a vertical line on plot at xval"""
    plot.plot([xval*10, xval*10], [-180,180], linestyle = ':')

def plot_key_times(plot, ypos, times_dict, yscale = 0.05):
    """Plot vertical lines at the defined key time points"""
    lines_list = []
    
    for val in sorted(times_dict.values()):
        lines_list.append(val)
    
    
    i = 0
    for val in lines_list:
        
        plot_vertical_line(plot, val)
        plot.annotate(i, (val*10, ypos - (i%5)*yscale))
        
        i = i+1
 
#define dictionaries of key times
        
#'1.24.22.0'
dict1_24_22_0 = {'start_cup_reach': 2, 
 'pour_end' : 17,
 'grab_spatula' : 18,
'replace_spatula' : 55,
'grab_ladel' : 59,
'replace_ladel' : 92,
'grab_metal_spatula_1' : 311,
'flip_start' : 316,
'flip_finish' : 326,
'replace_metal_spatula_1': 338,
'grab_metal_spatula_2' : 433,
'remove_start' : 436}

#'1.24.21.47'
dict1_24_21_47 = {'start_cup_reach': 3, 
 'pour_end' : 20,
 'grab_spatula' : 22,
'replace_spatula' : 57,
'grab_ladel' : 61,
'replace_ladel' : 90,
'grab_metal_spatula_1' : 131,
'flip_start' : 135,
'flip_finish' : 152,
'replace_metal_spatula_1': 156,
'grab_metal_spatula_2' : 220,
'remove_start' : 224}

#'1.24.21.52'
dict1_24_21_52 = {'start_cup_reach': 2, 
 'pour_end' : 15,
 'grab_spatula' : 20,
'replace_spatula' : 46,
'grab_ladel' : 51,
'replace_ladel' : 82,
'grab_metal_spatula_1' : 209,
'flip_start' : 215,
'flip_finish' : 239,
'replace_metal_spatula_1': 244,
'grab_metal_spatula_2' : 300,
'remove_start' : 305}
#(camera then freezes for a bit after 244)

#'2.7.16.13'
dict2_7_16_13 = {'start_cup_reach': 8, 
 'pour_end' : 21,
 'grab_spatula' : 25,
'replace_spatula' : 76,
'grab_ladel' : 77,
'replace_ladel' : 96,
'grab_metal_spatula_1' : 152,
'flip_start' : 157,
'flip_finish' : 194,
'replace_metal_spatula_1': 199,
'grab_metal_spatula_2' : 284,
'remove_start' : 286}
#two attempts needed to remove

#'2.7.16.27'
dict2_7_16_27 = {'start_cup_reach': 6, 
 'pour_end' : 17,
 'grab_spatula' : 20,
'replace_spatula' : 46,
'grab_ladel' : 47,
'replace_ladel' : 64,
'grab_metal_spatula_1' : 398,
'flip_start' : 401,
'flip_finish' : 476,
'replace_metal_spatula_1': 479,
'grab_metal_spatula_2' : 572,
'remove_start' : 573}
#grab_metal_spatula_1 = 284 (abandoned attempt)
#flip_start = 287 (abandoned attempt)

dictmockcook_14_2_17_36 = {'start_cup_reach': 7, 
 'pour_end' : 17,
 'grab_spatula' : 19,
'replace_spatula' : 44,
'grab_ladel' : 45,
'replace_ladel' : 57,
'grab_metal_spatula_1' : 68,
'flip_start' : 71,
'flip_finish' : 76,
'replace_metal_spatula_1': 86,
'grab_metal_spatula_2' : 101,
'remove_start' : 104
        }



def get_smoothed_plotting_data(file_name):
    
    if file_name == 'middle2.7.16.27':
        TIMEDICT = dict2_7_16_27
    if file_name == 'middle2.7.16.13':
        TIMEDICT = dict2_7_16_13    
    if file_name == 'middle1.24.21.47':
        TIMEDICT = dict1_24_21_47
    if file_name == 'middle1.24.21.52':
        TIMEDICT = dict1_24_21_52
    if file_name == 'middle1.24.22.0':
        TIMEDICT = dict1_24_22_0   
    if file_name == 'mockcook.14.2.17.36':
        TIMEDICT = dictmockcook_14_2_17_36   
    wristdatafile = open("bin/filtered_data/wrist." + file_name + ".pickle", "rb")
    wrist_list = pickle.load(wristdatafile)
    datafile = open("bin/filtered_data/" + file_name + ".pickle", "rb")
    results = pickle.load(datafile)


    #Define x, y and z values of the wrist
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
        
    #filter nans from data
    for num in range(len(plot_list_x)):
        if math.isnan(plot_list_x[num]) == True:
            plot_list_x[num] = 0
    for num in range(len(plot_list_y)):
        if math.isnan(plot_list_y[num]) == True:
            plot_list_y[num] = 0
    for num in range(len(plot_list_z)):
        if math.isnan(plot_list_z[num]) == True:
            plot_list_z[num] = 0
        

    #save what the unfiltered lists looked like       
    plot_list_x_old = plot_list_x *1
    plot_list_y_old = plot_list_y *1
    plot_list_z_old = plot_list_z *1


    # filter out spikes
    for frame in range(len(plot_list_x)):
        limit = 0.2
        if plot_list_x[frame]>1 or plot_list_x[frame]<-1:
            plot_list_x[frame] = 0
        if plot_list_y[frame]>1 or plot_list_y[frame]<-1:
            plot_list_y[frame] = 0
        if plot_list_z[frame]>1 or plot_list_z[frame]<-1:
            plot_list_z[frame] = 0
        if frame >0:
            if abs(plot_list_x[frame]-plot_list_x[frame-1]) > limit and plot_list_x[frame] != -1 and plot_list_x[frame-1] != -1:
                plot_list_x[frame] = plot_list_x[frame-1]
            if abs(plot_list_y[frame]-plot_list_y[frame-1]) > limit and plot_list_y[frame] != -1 and plot_list_y[frame-1] != -1:
                plot_list_y[frame] = plot_list_y[frame-1]
            if abs(plot_list_z[frame]-plot_list_z[frame-1]) > limit and plot_list_z[frame] != -1 and plot_list_z[frame-1] != -1:
                plot_list_z[frame] = plot_list_z[frame-1]

    #Apply savgol filter for smoothing of x,y,z values
    window_length, polyorder = 21, 2
    plot_list_x = signal.savgol_filter(plot_list_x, window_length, polyorder)
    plot_list_y = signal.savgol_filter(plot_list_y, window_length, polyorder)
    plot_list_z = signal.savgol_filter(plot_list_z, window_length, polyorder)


    #track important times
    timedictvallist = []
    for val in sorted(TIMEDICT.values()):
            timedictvallist.append(val)


    #Define theta1 and theta2 space (space in turn of arm 2D angles)
    refernce_vector = [0,1]
    theta1_list = []
    theta2_list = []
    
    for frame_num in range(len(results)):
        shoulder_2D = [results[frame_num][21][0][0], results[frame_num][21][1][0]]
        elbow_2D = [results[frame_num][22][0][0], results[frame_num][22][1][0]]
        wrist_2D = [results[frame_num][23][0][0], results[frame_num][23][1][0]]
        shoulder_to_elbow = [elbow_2D[0]- shoulder_2D[0], elbow_2D[1]- shoulder_2D[1]]
        elbow_to_wrist = [wrist_2D[0]-elbow_2D[0], wrist_2D[1]- shoulder_2D[1]]
        theta1 = angle_between(refernce_vector, shoulder_to_elbow)*180/np.pi
        theta2 = angle_between(shoulder_to_elbow, elbow_to_wrist)*180/np.pi
        theta1_list.append(theta1)
        theta2_list.append(theta2)
        #extra_list.append(wrist_2D)


    theta1_list_filtered = theta1_list
    theta2_list_filtered = theta2_list
    
    theta1_list_old = theta1_list*1
    theta2_list_old = theta2_list*1 

    for num in range(len(theta1_list_filtered)):
        if math.isnan(theta1_list_filtered[num]) == True:
            theta1_list_filtered[num] = 0
    for num in range(len(theta2_list_filtered)):
        if math.isnan(theta2_list_filtered[num]) == True:
            theta2_list_filtered[num] = 0



    #Apply savgol filter to lists
    window_length, polyorder = 81, 3    
    theta1_list_filtered = signal.savgol_filter(theta1_list_filtered, window_length, polyorder)
    theta2_list_filtered = signal.savgol_filter(theta2_list_filtered, window_length, polyorder)
    
    return plot_list_x, plot_list_y, plot_list_z, theta1_list_filtered, theta2_list_filtered, timedictvallist




