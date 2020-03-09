# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 13:34:05 2020

@author: birl
"""

import numpy as np
import matplotlib.pyplot as plt
from operator import add
from scipy import signal
def get_flip_positions():
    
    window_length, polyorder = 101, 3
    p_bool = False
    """
    point1 = [np.radians(2.8), np.radians(-113.4), np.radians(-103.8), np.radians(-41.7), np.radians(110.0), np.radians(229.3-360)]
    point2 = [np.radians(2.8), np.radians(-114.9), np.radians(-99.9), np.radians(-50.0), np.radians(110.0), np.radians(229.3-360)]
    point3 = [np.radians(2.8), np.radians(-116.5), np.radians(-96.1), np.radians(-58.0), np.radians(110.0), np.radians(229.3-360)]
    point4 = [np.radians(2.8), np.radians(-119.2), np.radians(-90.8), np.radians(-68.9), np.radians(110.0), np.radians(229.3-360)]
    point5 = [np.radians(2.8), np.radians(-122), np.radians(-85.8), np.radians(-78.4), np.radians(110.0), np.radians(229.3-360)]
    point6 = [np.radians(2.3), np.radians(-125.2), np.radians(-80.9), np.radians(-87.3), np.radians(110.0), np.radians(229.3-360)]
    point7 = [np.radians(2.3), np.radians(-129.2), np.radians(-75.5), np.radians(-96.9), np.radians(110.0), np.radians(229.3-360)]
    point8 = [np.radians(2.6), np.radians(-133.5), np.radians(-69.0), np.radians(-108.2), np.radians(109.9), np.radians(229.3-360)]
    point9 = [np.radians(2.3), np.radians(-139.2), np.radians(-61.2), np.radians(-121.6), np.radians(109.9), np.radians(229.3-360)]
    point10 = [np.radians(2.3), np.radians(-152.1), np.radians(-46.2), np.radians(-149.1), np.radians(109.9), np.radians(229.3-360)]

    point1 = [0.592, -0.054, -0.215+0.4, 3.11, 1.30, 0.497]
    point2 = [0.606, -0.053, -0.217+0.4, 3.17, 1.29, 0.339]
    point3 = [0.617, -0.053, -0.220+0.4, 3.22, 1.28, 0.175]
    point4 = [0.632, -0.052, -0.227+0.4, 3.29, 1.25, -0.0625]
    point5 = [0.645, -0.052, -0.237+0.4, 3.33, 1.23, -0.285]
    point6 = [0.656, -0.0568, -0.243+0.4, 3.36, 1.18, -0.491]
    point7 = [0.668, -0.056, -0.260+0.4, 3.37, 1.13, -0.746]
    point8 = [0.679, -0.052, -0.273+0.4, 3.36, 1.08, -1.04]
    point9 = [0.689, -0.055, -0.291+0.4, 3.32, 0.981, -1.39]
    point10 = [0.696, -0.055, -0.344+0.4, 3.05, 0.722, -2.17]
    """
    """
    point1 = [0.656, -0.248, -0.189+0.4, 1.33, 3.39, -0.082]
    point2 = [0.641, -0.285, -0.190+0.4, 1.16, 3.43, 0.382]
    point3 = [0.634, -0.317, -0.195+0.4, 1.01, 3.42, 0.714]
    point4 = [0.634, -0.336, -0.195+0.4, 0.917, 3.42, 0.946]
    point5 = [0.633, -0.358, -0.207+0.4, 0.775, 3.29, 1.332]
    point6 = [0.644, -0.376, -0.183+0.4, 0.790, 3.38, 1.46]
    """
    point1 = [0.731, -0.117, -0.197+0.4, 3.07, 1.41, 0.634]
    point2 = [0.767, -0.124, -0.199+0.4, 3.25, 1.33, 0.339]
    point3 = [0.785, -0.126, -0.203+0.4, 3.35, 1.31, 0.0736]
    point4 = [0.803, -0.120, -0.224+0.4, 3.41, 1.31,-0.472]
    point5 = [0.825, -0.122, -0.241+0.4, 3.44, 1.18, -0.693]

    #points_list = [point1, point2, point3, point4, point5]
    points_list = [point1, point2, point3, point4]
    interpolated_list= []
    for pos in range(len(points_list)-1):
        diff = [posnext - posnow for posnext, posnow in zip(points_list[pos+1], points_list[pos])]
        
        #print(diff)
        num_intern_points = 100
        step = [x / num_intern_points for x in diff]
        #print(step)
        for num in range(num_intern_points):
            increment_by = [x*num for x in step]
            interpolated_list.append(list( map(add, points_list[pos], increment_by) ))
            #print(points_list[pos]+increment_by)
    if p_bool == True:
        for i in range(6):
            plt.plot([point[i] for point in interpolated_list], color = 'k')
            
    #print([x[0] for x in interpolated_list])
    #list(zip(*hand_pose[joint.value]))[1]
    #x_filtered = signal.savgol_filter(list(interpolated_list))[0], window_length, polyorder)
    y_filtered = signal.savgol_filter([x[1] for x in interpolated_list], window_length, polyorder)
    #z_filtered = signal.savgol_filter(list(zip(*hand_pose[joint.value]))[2], window_length, polyorder)
    #plt.figure()
    filterlist1 = signal.savgol_filter([x[0] for x in interpolated_list], window_length, polyorder)
    filterlist2 = signal.savgol_filter([x[1] for x in interpolated_list], window_length, polyorder)
    filterlist3 = signal.savgol_filter([x[2] for x in interpolated_list], window_length, polyorder)
    filterlist4 = signal.savgol_filter([x[3] for x in interpolated_list], window_length, polyorder)
    filterlist5 = signal.savgol_filter([x[4] for x in interpolated_list], window_length, polyorder)
    filterlist6 = signal.savgol_filter([x[5] for x in interpolated_list], window_length, polyorder)
    
    if p_bool == True:
        for i in range(6):
            plt.plot(signal.savgol_filter([x[i] for x in interpolated_list], window_length, polyorder), color = 'b')
        
        
    filtered_positions = list(zip(filterlist1,filterlist2, filterlist3, filterlist4,filterlist5, filterlist6 ))
    #print(filtered_positions)
    return filtered_positions

get_flip_positions()