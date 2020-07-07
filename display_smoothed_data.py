"""
display smoothed data from a single demonstration
"""
import numpy as np
import time
from scipy import signal
import pickle
import sys
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm

from get_3D_pose import HAND, BODY, get_arm_3D_coordinates


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
    


dict3_3_15_38 = {'start_cup_reach': 5, 
 'pour_end' : 20,
 'grab_spatula' : 22,
'replace_spatula' : 43,
'grab_ladel' : 43,
'replace_ladel' : 62,
'grab_metal_spatula_1' : 398,
'flip_start' : 401,
'flip_finish' : 476,
'replace_metal_spatula_1': 479,
'grab_metal_spatula_2' : 572,
'remove_start' : 573}



#Define limits of the values well plot in 3D

x_upper_limit = 1
x_lower_limit = 0

y_upper_limit = 0.75
y_lower_limit = -0.25

z_upper_limit = 0.5
z_lower_limit = -0.5


#Track start time
old_time = time.time()
#
#LOAD SAVED DATA

#file_name =  '1.23.17.49'
#file_name = '1.24.21.47'
#file_name = '1.24.22.0'
#file_name = '1.24.21.39'
#file_name = '1.24.21.52'
#file_name = '2.7.16.13'
#file_name = '2.7.16.27'
file_name = "mar.3.3.15.38"
TIMEDICT = dict3_3_15_38

wristdatafile = open("bin/filtered_data/wrist." + file_name + ".pickle", "rb")
wrist_list = pickle.load(wristdatafile)
datafile = open("bin/filtered_data/" + file_name + ".pickle", "rb")
results = pickle.load(datafile)


fig = plt.figure()
plt.close('all')

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

print(plot_list_x)
#Filter out spikes from the lists

for frame in range(len(plot_list_x)):
    limit = 0.2

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

#Plot x vs y with colour for the important sections
#plt.plot(plot_list_x,plot_list_y)
plt.title("x-y map")
plt.xlim(x_lower_limit,x_upper_limit)
plt.ylim(y_lower_limit,y_upper_limit)

timedictvallist = []
for val in sorted(TIMEDICT.values()):
        timedictvallist.append(val)
plt.plot(plot_list_x[timedictvallist[0]*10:timedictvallist[1]*10],plot_list_y[timedictvallist[0]*10:timedictvallist[1]*10], 'r')
plt.plot(plot_list_x[timedictvallist[2]*10:timedictvallist[3]*10],plot_list_y[timedictvallist[2]*10:timedictvallist[3]*10], 'g')
plt.plot(plot_list_x[timedictvallist[4]*10:timedictvallist[5]*10],plot_list_y[timedictvallist[4]*10:timedictvallist[5]*10], 'y')
plt.plot(plot_list_x[timedictvallist[6]*10:timedictvallist[9]*10],plot_list_y[timedictvallist[6]*10:timedictvallist[9]*10], 'c')
plt.plot(plot_list_x[timedictvallist[10]*10:],plot_list_y[timedictvallist[10]*10:], 'k')




#Plot x, y and x on their own
fig = plt.figure()
plt.plot(num_list, plot_list_x_old)
plt.plot(num_list, plot_list_x)
plt.title('X data')
plot_key_times(plt, 0.2, TIMEDICT)
plt.ylim(x_lower_limit,x_upper_limit)
fig = plt.figure()
plt.plot(num_list, plot_list_y_old)
plt.plot(num_list, plot_list_y)
plt.title('Y data')
plot_key_times(plt, 0.2, TIMEDICT)
plt.ylim(y_lower_limit,y_upper_limit)
fig = plt.figure()
plt.plot(num_list, plot_list_z_old)
plt.plot(num_list, plot_list_z)
plt.title('Z data')
plot_key_times(plt, 0.2, TIMEDICT)
plt.ylim(z_lower_limit,z_upper_limit)

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

"""
for frame in range(len(theta1_list)):
    limit = 30
    if frame >0:
        if abs(theta1_list_filtered[frame]-theta1_list_old[frame-1]) > limit:
            theta1_list_filtered[frame] = theta1_list_old[frame-1]
        if abs(theta2_list_filtered[frame]-theta2_list_old[frame-1]) > limit:
            theta2_list_filtered[frame] = theta2_list_old[frame-1]
            
            
"""
"""
for frame in range(len(theta1_list)):
    averaging_length = 5
    if frame>averaging_length+1 and frame<len(theta1_list) - averaging_length-1:
        #print( np.mean(theta1_list[frame-averaging_length:frame-averaging_length]))
        theta1_list_filtered[frame] = np.mean(theta1_list[frame-averaging_length:frame+averaging_length])
        theta2_list_filtered[frame] = np.mean(theta2_list[frame-averaging_length:frame+averaging_length])
     
   
"""
#Apply savgol filter to lists
window_length, polyorder = 81, 3

        
theta1_list_filtered = signal.savgol_filter(theta1_list_filtered, window_length, polyorder)
theta2_list_filtered = signal.savgol_filter(theta2_list_filtered, window_length, polyorder)


#Plot thet1, theta2, and theta1 vs theta2
fig = plt.figure()
plt.plot(num_list, theta1_list_old)
plt.plot(num_list, theta1_list_filtered)
plt.title('Theta 1')
plot_key_times(plt, -50, TIMEDICT, 20)
fig = plt.figure()
plt.plot(num_list, theta2_list_old)
plt.plot(num_list, theta2_list_filtered)

plt.title('Theta 2')
plot_key_times(plt, -50, TIMEDICT, 20)

fig = plt.figure()
#plt.plot(theta1_list_filtered, theta2_list_filtered)
plt.title('Theta 1 vs Theta 2')
#plot_key_times(plt, -50, 20)


#plt.plot(theta1_list_filtered[timedictvallist[0]*10:timedictvallist[1]*10],theta2_list_filtered[timedictvallist[0]*10:timedictvallist[1]*10], 'r')
#plt.plot(theta1_list_filtered[timedictvallist[2]*10:timedictvallist[3]*10],theta2_list_filtered[timedictvallist[2]*10:timedictvallist[3]*10], 'g')
#plt.plot(theta1_list_filtered[timedictvallist[4]*10:timedictvallist[5]*10],theta2_list_filtered[timedictvallist[4]*10:timedictvallist[5]*10], 'y')
#plt.plot(theta1_list_filtered[timedictvallist[6]*10:timedictvallist[9]*10],theta2_list_filtered[timedictvallist[6]*10:timedictvallist[9]*10], 'c')
#plt.plot(theta1_list_filtered[timedictvallist[10]*10:],theta2_list_filtered[timedictvallist[10]*10:], 'k')


print("Time taken is", time.time()-old_time)

"""
import mpl_toolkits.mplot3d.axes3d as p3
import mpl_toolkits.mplot3d as plt3d

fig = plt.figure()
ax = p3.Axes3D(fig)
for x,y,z in zip(plot_list_x, plot_list_y, plot_list_z):
    fig.plot(x,y,z)

"""