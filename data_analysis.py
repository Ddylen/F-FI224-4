from multi_display_smoothed_data import get_smoothed_plotting_data
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

fig = plt.figure()
plt.close('all')

file_name_1 = '1.24.21.47'
file_name_2 = '1.24.21.52'
file_name_3 = '1.24.22.0'
file_name_4 = '2.7.16.13'
file_name_5 = '2.7.16.27'

plot_list_x_1, plot_list_y_1, plot_list_z_1, theta1_list_filtered_1, theta2_list_filtered_1, timedictvallist_1 = get_smoothed_plotting_data(file_name_1)
plot_list_x_2, plot_list_y_2, plot_list_z_2, theta1_list_filtered_2, theta2_list_filtered_2, timedictvallist_2 = get_smoothed_plotting_data(file_name_2)
plot_list_x_3, plot_list_y_3, plot_list_z_3, theta1_list_filtered_3, theta2_list_filtered_3, timedictvallist_3 = get_smoothed_plotting_data(file_name_3)
plot_list_x_4, plot_list_y_4, plot_list_z_4, theta1_list_filtered_4, theta2_list_filtered_4, timedictvallist_4 = get_smoothed_plotting_data(file_name_4)
plot_list_x_5, plot_list_y_5, plot_list_z_5, theta1_list_filtered_5, theta2_list_filtered_5, timedictvallist_5 = get_smoothed_plotting_data(file_name_5)


def plot_thetas(plot_list_x, plot_list_y, plot_list_z, theta1_list_filtered, theta2_list_filtered, timedictvallist):

    #plt.plot(theta1_list_filtered, theta2_list_filtered, 'b')
    plt.plot(theta1_list_filtered[timedictvallist[0]*10:timedictvallist[1]*10],theta2_list_filtered[timedictvallist[0]*10:timedictvallist[1]*10], 'r')
    plt.plot(theta1_list_filtered[timedictvallist[2]*10:timedictvallist[3]*10],theta2_list_filtered[timedictvallist[2]*10:timedictvallist[3]*10], 'g')
    plt.plot(theta1_list_filtered[timedictvallist[4]*10:timedictvallist[5]*10],theta2_list_filtered[timedictvallist[4]*10:timedictvallist[5]*10], 'y')
    plt.plot(theta1_list_filtered[timedictvallist[6]*10:timedictvallist[9]*10],theta2_list_filtered[timedictvallist[6]*10:timedictvallist[9]*10], 'c')
    plt.plot(theta1_list_filtered[timedictvallist[10]*10:],theta2_list_filtered[timedictvallist[10]*10:], 'k')


#plot_thetas(plot_list_x_1, plot_list_y_1, plot_list_z_1, theta1_list_filtered_1, theta2_list_filtered_1, timedictvallist_1)
#plot_thetas(plot_list_x_2, plot_list_y_2, plot_list_z_2, theta1_list_filtered_2, theta2_list_filtered_2, timedictvallist_2)
#plot_thetas(plot_list_x_3, plot_list_y_3, plot_list_z_3, theta1_list_filtered_3, theta2_list_filtered_3, timedictvallist_3)
#plot_thetas(plot_list_x_4, plot_list_y_4, plot_list_z_4, theta1_list_filtered_4, theta2_list_filtered_4, timedictvallist_4)
#plot_thetas(plot_list_x_5, plot_list_y_5, plot_list_z_5, theta1_list_filtered_5, theta2_list_filtered_5, timedictvallist_5)
    
def plot_linear(plot_list_x, plot_list_y, plot_list_z, theta1_list_filtered, theta2_list_filtered, timedictvallist):
    
    #plt.plot(plot_list_x,plot_list_y, 'b')
    plt.plot(plot_list_x[timedictvallist[0]*10:timedictvallist[1]*10],plot_list_y[timedictvallist[0]*10:timedictvallist[1]*10], 'r')
    plt.plot(plot_list_x[timedictvallist[2]*10:timedictvallist[3]*10],plot_list_y[timedictvallist[2]*10:timedictvallist[3]*10], 'g')
    plt.plot(plot_list_x[timedictvallist[4]*10:timedictvallist[5]*10],plot_list_y[timedictvallist[4]*10:timedictvallist[5]*10], 'y')
    plt.plot(plot_list_x[timedictvallist[6]*10:timedictvallist[9]*10],plot_list_y[timedictvallist[6]*10:timedictvallist[9]*10], 'c')
    plt.plot(plot_list_x[timedictvallist[10]*10:],plot_list_y[timedictvallist[10]*10:], 'k')
    

plot_linear(plot_list_x_1, plot_list_y_1, plot_list_z_1, theta1_list_filtered_1, theta2_list_filtered_1, timedictvallist_1)
fig = plt.figure()
plot_linear(plot_list_x_2, plot_list_y_2, plot_list_z_2, theta1_list_filtered_2, theta2_list_filtered_2, timedictvallist_2)
fig = plt.figure()
plot_linear(plot_list_x_3, plot_list_y_3, plot_list_z_3, theta1_list_filtered_3, theta2_list_filtered_3, timedictvallist_3)
fig = plt.figure()
plot_linear(plot_list_x_4, plot_list_y_4, plot_list_z_4, theta1_list_filtered_4, theta2_list_filtered_4, timedictvallist_4)
fig = plt.figure()
plot_linear(plot_list_x_5, plot_list_y_5, plot_list_z_5, theta1_list_filtered_5, theta2_list_filtered_5, timedictvallist_5)