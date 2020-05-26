# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 16:42:32 2019

Code for smoothly following a human demonstrator in 2D
"""



import sys
sys.path.insert(1,r'C:\Users\birl\Documents\ur5_python_host\ur5_kg_robot')



import numpy as np

import math
import time

from math import pi



import waypoints as wp

from kg_robot import kg_robot
from reader import interpret2D
import specialised_kg_robot_example as kgrs 

"""
camera readings
upper left
0.3428944 0.5334604
low left
0.355475 0.297786
upper right
0.5972144 0.5274434
lower right
0.5954032 0.3027162
"""

def main():
    cam_x_max = 0.5972144
    cam_x_min= 0.3428944
    
    cam_x_range = cam_x_max - cam_x_min
    
    cam_y_max = 0.5334604
    cam_y_min= 0.297786
    
    cam_y_range = cam_y_max - cam_y_min
    
    move_scale_x = 1
    move_scale_y = 1 #scale the 0 to 1 move range into a range the arm can reach
    frame_rate = 0.2
    palm_list = interpret2D()
    normalised_pos_list = []
    out_of_bounds = "OUT OF BOUNDS"
    #HAND INITIALISATION 
    
    #this code used keypount scale 3
    
    
    """ ARM READINGS
    upper left
    352.5, -533.9
    
    low left
    364.5, -163.4
    
    upper right
    -288.5, -517.2
    
    lower right
    -295.5, -164.2
    
    """
    arm_x_min = -295.5/1000 #convert mm to m
    arm_x_max = 364.5/1000
    arm_x_range = arm_x_max - arm_x_min
    
    arm_y_min = -533.9/1000
    arm_y_max = -163.4/1000
    arm_y_range = arm_y_max - arm_y_min
    
    
    for val in palm_list:
        if (val[0] > cam_x_max) or (val[0] < cam_x_min) or (val[1] < cam_y_min) or (val[1] > cam_y_max):
            
            normalised_pos_list.append((out_of_bounds,out_of_bounds, -1))
        else:
            x_normalised = 1-(val[0]-cam_x_min)/cam_x_range #reflected so that more positive means more to the left
            y_normalised = 1-(val[1] - cam_y_min)/cam_y_range # 0,0 is now top right hand corner
            normalised_pos_list.append((x_normalised,y_normalised))#store normalised position + hand open/closed
    
    print(normalised_pos_list)
    print("------------Configuring Burt-------------\r\n")

    burt = 0

    burt = kgrs.specialised_kg_robot(port=30010,db_host="169.254.251.50")

    print("----------------Hi Burt!-----------------\r\n\r\n")
    #burt.movej([np.radians(-90), np.radians(-90), np.radians(-90), np.radians(-76), np.radians(0), np.radians(0)], min_time = 2)
    #burt.movej([np.radians(-72.4), np.radians(-99.8), np.radians(-136.8), np.radians(234.0), np.radians(-70.4), np.radians(161.5)], min_time = 5) #move to first position slowly
    burt.movej([np.radians(38), np.radians(-128), np.radians(150), np.radians(244), np.radians(-85), np.radians(-7)], min_time = 5) #move to first position slowly
    #CHANGE TO MOVE TO CORRECT INITIONALISATION POSE
    print("moved to start")
    for val in normalised_pos_list:
        if val == out_of_bounds:
            time.sleep(frame_rate)
            print("No data, sleeping for a frame")
            continue
        if(normalised_pos_list.index(val)==0):
            time_min = 3
        else:
            time_min = frame_rate
    
        if(val[0] != 'OUT OF BOUNDS'):
            move_to_x = val[0]*arm_x_range + arm_x_min
            move_to_y = val[1]*arm_y_range + arm_y_min
            print("Go to ", move_to_x, move_to_y)
        #time.sleep(frame_rate)
        #burt.movel([move_to_x, move_to_y, 0.2, 1.156, 2.886, -0.15], min_time = 0.3)
        #burt.servoj(burt.get_inverse_kin([move_to_x, move_to_y, 0.4, np.pi/2, 0, 0]), control_time = time_min,lookahead_time=0.008,gain=300)
        burt.servoj([move_to_x, move_to_y, 0.2, 1.156, 2.886, -0.15])
        """
        if val[2] ==1:
            print("hand closed")
        """
        #HAND CLOSE LINE
        
        #burt.servoj([-0.022, -0.386, 0.1, 0.31, -2.07, 1.97])
    
    burt.close()

if __name__ == '__main__': main()
