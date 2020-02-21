# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 18:02:41 2020

@author: birl
"""

"""File to save the JSON data in vector format suitable for animation"""

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
import csv
from scipy import signal


old_time = time.time()

#file_name =  'mockcook.14.2.17.36'
#file_name = '1.24.21.47'
#file_name = "2.7.16.13"
#file_name = '1.24.22.0'
#file_name = "smallpantry1.17.2.16.58"
#file_name = "smallpantry2heat7.17.2.17.6"
file_name = "thomastest.17.2.17.28"
#file_name = '1.24.21.47'
#file_name = '1.24.21.52'
#file_name = '1.24.22.0'
#file_name = '2.7.16.13'
#file_name = '2.7.16.27'


BODY3DPOSE, LEFTHAND3DPOSE,RIGHTHAND3DPOSE = get_arm_3D_coordinates(file_name, confidence_threshold = 0)
"""
for jointslist in BODY3DPOSE, LEFTHAND3DPOSE,RIGHTHAND3DPOSE:
    for jointlist in jointslist:
        if BODY3DPOSE[1][0] == [-1,-1,-1, True] and BODY3DPOSE[7][0] == [-1,-1,-1, True] and BODY3DPOSE[6][0] == [-1,-1,-1, True] and RIGHTHAND3DPOSE[0][0] == [-1,-1,-1, True]:
            jointlist = jointlist[1:]
"""   
body_raw = BODY3DPOSE
left_hadn_raw = LEFTHAND3DPOSE
right_hand_raw = RIGHTHAND3DPOSE

i = 0

"""
for row in BODY3DPOSE:
    if i%9 ==0:
        plt.plot(row[0])
        plt.figure()
    i = i + 1
"""

with open(file_name + "filtered" + '.csv', 'w', newline='') as file:
    filteredwriter = csv.writer(file)
    for pose_list in BODY3DPOSE, LEFTHAND3DPOSE,RIGHTHAND3DPOSE:
        i = 0
        for joint in pose_list:
            joint = joint[1:]
            plot_list_x = [entry[0] for entry in joint]
            plot_list_y = [entry[1] for entry in joint]
            plot_list_z = [entry[2] for entry in joint]
            invalid_list = [entry[3] for entry in joint]
            plot_list_x_old = plot_list_x *1
            plot_list_y_old = plot_list_y *1
            plot_list_z_old = plot_list_z *1
    
            window_length, polyorder = 21, 2
            for frame in range(len(plot_list_x)):
                limit = 0.2
                if frame >0 and plot_list_x[frame-1] != -1:
                    if abs(plot_list_x[frame]-plot_list_x[frame-1]) > limit:
                        plot_list_x[frame] = plot_list_x[frame-1]
                    if abs(plot_list_y[frame]-plot_list_y[frame-1]) > limit:
                        plot_list_y[frame] = plot_list_y[frame-1]
                    if abs(plot_list_z[frame]-plot_list_z[frame-1]) > limit:
                        plot_list_z[frame] = plot_list_z[frame-1]
            if i < 19:
                ident_string = BODY(i).name
            elif i>=19 and i<40:
                ident_string = "Left" + HAND(i).name
            elif i>=40:
                ident_string = "Right" + HAND(i).name
    
            savgol_plot_list_x = signal.savgol_filter(plot_list_x, window_length, polyorder)
            savgol_plot_list_y = signal.savgol_filter(plot_list_y, window_length, polyorder)
            savgol_plot_list_z = signal.savgol_filter(plot_list_z, window_length, polyorder)
            
            savgol_plot_list_x = savgol_plot_list_x.tolist()
            savgol_plot_list_y = savgol_plot_list_y.tolist()
            savgol_plot_list_z = savgol_plot_list_z.tolist()
            
            savgol_plot_list_x.insert(0,ident_string + " X Value")
            savgol_plot_list_y.insert(0,ident_string+ " Y Value")
            savgol_plot_list_z.insert(0,ident_string + " Z Value")
            invalid_list.insert(0, ident_string + " Invalid?")
            filteredwriter.writerow(savgol_plot_list_x)
            filteredwriter.writerow(savgol_plot_list_y)
            filteredwriter.writerow(savgol_plot_list_z)
            filteredwriter.writerow(invalid_list)


#results_list, wrist_list = get_plot_list(BODY3DPOSE, LEFTHAND3DPOSE,RIGHTHAND3DPOSE)
with open(file_name + '.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    i_body = 0
    i_left = 0
    i_right = 0
    for row in BODY3DPOSE:
            rowcopy = row[1:]
            rowcopy.insert(0, [BODY(i_body).name + " X Value", BODY(i_body).name +" Y Value", BODY(i_body).name +" Z Value", BODY(i_body).name +" Invaid?"])
            writer.writerow([entry[0] for entry in rowcopy])
            writer.writerow([entry[1] for entry in rowcopy])
            writer.writerow([entry[2] for entry in rowcopy])
            writer.writerow([entry[3] for entry in rowcopy])
            i_body +=1 
            
    for row in LEFTHAND3DPOSE:
            rowcopy = row[1:]
            rowcopy.insert(0, ["Left "+ HAND(i_left).name + " X Value", "Left "+ HAND(i_left).name + " Y Value", "Left "+ HAND(i_left).name + " Z Value", "Left "+ HAND(i_left).name + " Invalid?"])
            writer.writerow([entry[0] for entry in rowcopy])
            writer.writerow([entry[1] for entry in rowcopy])
            writer.writerow([entry[2] for entry in rowcopy])
            writer.writerow([entry[3] for entry in rowcopy])    
            i_left +=1 
            
    for row in RIGHTHAND3DPOSE:
            rowcopy = row[1:]
            rowcopy.insert(0, ["Right "+ HAND(i_right).name+ " X Value", "Right "+ HAND(i_right).name + " Y Value", "Right "+ HAND(i_right).name + " Z Value", "Right "+ HAND(i_right).name + " Invalid?"])
            writer.writerow([entry[0] for entry in rowcopy])
            writer.writerow([entry[1] for entry in rowcopy])
            writer.writerow([entry[2] for entry in rowcopy])
            writer.writerow([entry[3] for entry in rowcopy])
            i_right +=1 