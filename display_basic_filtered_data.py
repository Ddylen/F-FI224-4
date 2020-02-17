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

#print(len(results_list[5]))
#print(results_list[5])
sys.setrecursionlimit(10**6) # to stop a recursion error when looking back over 1000 places

old_time = time.time()

#file_name =  '1.23.17.49'
#file_name = '1.24.21.47'
file_name = '1.24.22.0'
#file_name = '1.24.21.39'
#file_name = '1.24.21.52'
wristdatafile = open("bin/filtered_data/wrist." + file_name + ".pickle", "rb")
wrist_list = pickle.load(wristdatafile)
datafile = open("bin/filtered_data/" + file_name + ".pickle", "rb")
results = pickle.load(datafile)

#print(wrist_list)

len_wrist_list = len(wrist_list)
x = np.arange(len_wrist_list)
ys = [i+x+(i*x)**2 for i in range(len_wrist_list)]

colors = cm.rainbow(np.linspace(0, 1, len(ys)))
i = 0
"""
ax = Axes3D(fig)
for val,c in zip (wrist_list, colors):
    #print(val)

    ax.scatter(val[0], val[1], val[2], color = c)
    i = i+1
"""

fig = plt.figure()
plt.close('all')

plot_list_x = []
plot_list_y = []
plot_list_z = []
num_list = []
for val in wrist_list:
    plot_list_x.append(val[0])
    plot_list_y.append(val[1])
    plot_list_z.append(val[2])
    num_list.append(i)
    i = i+1
    


x_upper_limit = 1
x_lower_limit = 0

y_upper_limit = 0.75
y_lower_limit = -0.25

z_upper_limit = 0.5
z_lower_limit = -0.5

#'1.24.22.0'
start_cup_reach = 2
pour_end = 17
grab_spatula = 17
replace_spatula = 55
grab_ladel = 59
replace_ladel = 92
grab_metal_spatula_1 = 311
flip_start = 316
flip_finish = 326
replace_metal_spatula_1= 338
grab_metal_spatula_2 = 433
remove_start = 436


def plot_vertical_line(plot, xval):
    plot.plot([xval*10, xval*10], [-180,180], linestyle = ':')

def plot_key_times(plot, ypos, yscale = 0.05):
    lines_list = []
    
    """
    #'1.24.22.0'
    start_cup_reach = 2
    pour_end = 17
    grab_spatula = 17
    replace_spatula = 55
    grab_ladel = 59
    replace_ladel = 92
    grab_metal_spatula_1 = 311
    flip_start = 316
    flip_finish = 326
    replace_metal_spatula_1= 338
    grab_metal_spatula_2 = 433
    remove_start = 436
    """
    
    """
    #'1.24.21.47'
    start_cup_reach = 3
    pour_end = 20
    grab_spatula = 22
    replace_spatula = 57
    grab_ladel = 61
    replace_ladel = 90
    grab_metal_spatula_1 = 131
    flip_start = 135
    flip_finish = 152
    replace_metal_spatula_1=156
    grab_metal_spatula_2 = 220
    remove_start = 224
    """
    """
    #'1.24.21.52'
    start_cup_reach = 2
    pour_end = 15
    grab_spatula = 20
    replace_spatula = 46
    grab_ladel = 51
    replace_ladel = 82
    grab_metal_spatula_1 = 209
    flip_start = 215
    flip_finish = 239
    replace_metal_spatula_1=244 #(camera then freezes for a bit)
    grab_metal_spatula_2 = 300
    remove_start = 305
    """
    


    
    lines_list.append(start_cup_reach)
    lines_list.append(pour_end)
    lines_list.append(grab_spatula)
    lines_list.append(replace_spatula)
    lines_list.append(grab_ladel)
    lines_list.append(replace_ladel)
    lines_list.append(grab_metal_spatula_1)
    lines_list.append(flip_start)
    lines_list.append(flip_finish)
    lines_list.append(replace_metal_spatula_1)
    lines_list.append(grab_metal_spatula_2)
    lines_list.append(remove_start)
    
    
    i = 0
    for val in lines_list:
        
        plot_vertical_line(plot, val)
        plot.annotate(i, (val*10, ypos - (i%5)*yscale))
        
        i = i+1
        
plot_list_x_old = plot_list_x *1
plot_list_y_old = plot_list_y *1
plot_list_z_old = plot_list_z *1

window_length, polyorder = 21, 2
for frame in range(len(plot_list_x)):
    limit = 0.2
    if frame >0:
        if abs(plot_list_x[frame]-plot_list_x[frame-1]) > limit:
            plot_list_x[frame] = plot_list_x[frame-1]
        if abs(plot_list_y[frame]-plot_list_y[frame-1]) > limit:
            plot_list_y[frame] = plot_list_y[frame-1]
        if abs(plot_list_z[frame]-plot_list_z[frame-1]) > limit:
            plot_list_z[frame] = plot_list_z[frame-1]

plot_list_x = signal.savgol_filter(plot_list_x, window_length, polyorder)
plot_list_y = signal.savgol_filter(plot_list_y, window_length, polyorder)
plot_list_z = signal.savgol_filter(plot_list_z, window_length, polyorder)


plt.plot(plot_list_x,plot_list_y)
plt.title("x-y map")
plt.xlim(x_lower_limit,x_upper_limit)
plt.ylim(y_lower_limit,y_upper_limit)

plt.plot(plot_list_x[start_cup_reach*10:pour_end*10],plot_list_y[start_cup_reach*10:pour_end*10], 'r')

plt.plot(plot_list_x[grab_spatula*10:replace_spatula*10],plot_list_y[grab_spatula*10:replace_spatula*10], 'g')

plt.plot(plot_list_x[grab_ladel*10:replace_ladel*10],plot_list_y[grab_ladel*10:replace_ladel*10], 'y')

plt.plot(plot_list_x[grab_metal_spatula_1*10:replace_metal_spatula_1*10],plot_list_y[grab_metal_spatula_1*10:replace_metal_spatula_1*10], 'c')

plt.plot(plot_list_x[grab_metal_spatula_2*10:],plot_list_y[grab_metal_spatula_2*10:], 'k')

#print(plot_list_x)
#plot_list_x = signal.savgol_filter(plot_list_x, window_length, polyorder)
#plot_list_y = signal.savgol_filter(plot_list_y, window_length, polyorder)
#plot_list_z = signal.savgol_filter(plot_list_z, window_length, polyorder)

fig = plt.figure()
plt.plot(num_list, plot_list_x_old)
plt.plot(num_list, plot_list_x)

plt.title('X data')
plot_key_times(plt, 0.2)
plt.ylim(x_lower_limit,x_upper_limit)
fig = plt.figure()
plt.plot(num_list, plot_list_y_old)
plt.plot(num_list, plot_list_y)
plt.title('Y data')
plot_key_times(plt, 0.2)
plt.ylim(y_lower_limit,y_upper_limit)
fig = plt.figure()
plt.plot(num_list, plot_list_z_old)
plt.plot(num_list, plot_list_z)
plt.title('Z data')
plot_key_times(plt, 0.2)
plt.ylim(z_lower_limit,z_upper_limit)


refernce_vector = [0,1]
theta1_list = []
theta2_list = []


#extra_list = []
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
"""
for frame in range(len(theta1_list)):
    averaging_length = 5
    if frame>averaging_length+1 and frame<len(theta1_list) - averaging_length-1:
        #print( np.mean(theta1_list[frame-averaging_length:frame-averaging_length]))
        theta1_list_filtered[frame] = np.mean(theta1_list[frame-averaging_length:frame+averaging_length])
        theta2_list_filtered[frame] = np.mean(theta2_list[frame-averaging_length:frame+averaging_length])
     
   
"""


theta1_list_filtered = signal.savgol_filter(theta1_list_filtered, window_length, polyorder)
theta2_list_filtered = signal.savgol_filter(theta2_list_filtered, window_length, polyorder)

"""
    allowable_deviation = 20
    if (abs(theta1_list[frame]-np.mean(theta1_list[frame-6:frame-1])))>allowable_deviation:
            if (abs(theta1_list[frame]-np.mean(theta1_list[frame+1:frame+6])))>allowable_deviation:
                theta1_list[frame]=np.mean(theta1_list[frame-4:frame-1])
                
    if (abs(theta2_list[frame]-np.mean(theta2_list[frame-6:frame-1])))>allowable_deviation:
        if (abs(theta2_list[frame]-np.mean(theta2_list[frame+1:frame+6])))>allowable_deviation:
            theta2_list[frame]=np.mean(theta2_list[frame-6:frame-1])
"""
"""
old_theta1_list = theta1_list
old_theta2_list = theta2_list
for frame in range(len(theta1_list)):
    allowable_deviation = 50
    if (abs(old_theta1_list[frame]-old_theta1_list[frame-1]))>allowable_deviation:
                theta1_list[frame]=old_theta1_list[frame-1]
                
    if (abs(old_theta2_list[frame]-old_theta2_list[frame-1]))>allowable_deviation:
            theta2_list[frame]=old_theta2_list[frame-1]
    
"""
    
fig = plt.figure()
#plt.plot(num_list, theta1_list)
plt.plot(num_list, theta1_list_filtered)
plt.title('Theta 1')
plot_key_times(plt, -50, 20)



    
    
    
fig = plt.figure()
#plt.plot(num_list, theta2_list)
plt.plot(num_list, theta2_list_filtered)

plt.title('Theta 2')
plot_key_times(plt, -50, 20)

fig = plt.figure()
plt.plot(theta1_list_filtered, theta2_list_filtered)
plt.title('Theta 1 vs Theta 2')
#plot_key_times(plt, -50, 20)
plt.plot(theta1_list_filtered[start_cup_reach*10:pour_end*10],theta2_list_filtered[start_cup_reach*10:pour_end*10], 'r')

plt.plot(theta1_list_filtered[grab_spatula*10:replace_spatula*10],theta2_list_filtered[grab_spatula*10:replace_spatula*10], 'g')

plt.plot(theta1_list_filtered[grab_ladel*10:replace_ladel*10],theta2_list_filtered[grab_ladel*10:replace_ladel*10], 'y')

plt.plot(theta1_list_filtered[grab_metal_spatula_1*10:replace_metal_spatula_1*10],theta2_list_filtered[grab_metal_spatula_1*10:replace_metal_spatula_1*10], 'c')

plt.plot(theta1_list_filtered[grab_metal_spatula_2*10:],theta2_list_filtered[grab_metal_spatula_2*10:], 'k')


#fig = plt.figure()
#plt.plot(num_list, extra_list)
#plt.title('Extra list')


#datafile = open("bin/filtered_data/" + file_name + ".pickle", "wb")
#pickle.dump(results_list, datafile)

print("Time taken is", time.time()-old_time)


