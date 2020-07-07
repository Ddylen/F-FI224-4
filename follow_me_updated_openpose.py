"""
Code for imitating recorded arm positions in 3D using the UR5
"""
from __future__ import print_function
import sys
import numpy as np
import math
import time
from math import pi
import pickle
import waypoints as wp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import cv2
from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import ctypes

import kg_robot as kgr
from coordinate_transforms import convert_to_arm_coords
from get_3D_pose import BODY
from get_3D_pose import HAND
from get_3D_pose import get_arm_3D_coordinates

sys.path.insert(1,r'C:\Users\birl\Documents\updated_ur5_controller\Generic_ur5_controller')


def follow(filename):
    """Function to get UR5 to follow a recorded trajectory"""
    
    #extract 3D pose
    body_3D_pose, left_hand_3D_pose, right_hand_3D_pose = get_arm_3D_coordinates(filename, show_each_frame =  False)
    
    #define allowable range of x,y and z values
    xlim = [-0.6,0.6]
    ylim = [-0.65, -0.16]
    zlim = [0.07, 1]
    
    #define empty lists to fill with palm values
    x_sec= []
    y_sec= []
    z_sec = []
    
    #For all palm values
    for pos in right_hand_3D_pose[HAND.PALM.value]:
        
        #If they are not recorded as bad
        if pos[3] ==False:
            
            #Add x,y and z values to list of values to plot
            x_sec.append(pos[0])
            y_sec.append(pos[1])
            z_sec.append(pos[2])

    #create 3D scatter plot of palm values
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x_sec, y_sec, z_sec)
    plt.show()

    #Initialise connection with robot
    print("------------Configuring Burt-------------\r\n")
    burt = 0
    burt = kgr.kg_robot(port=30010,db_host="169.254.150.100")
    print("----------------Hi Burt!-----------------\r\n\r\n")
    
    #Move UR5 arm to a starting position slowly
    burt.movej([np.radians(-90), np.radians(-65), np.radians(-115), np.radians(-85), np.radians(90), np.radians(45)], min_time = 3)
    print("moved to start")
    
    #Flag for if this is the first position on the trajectory
    first_round = True
    
    #Counter for number of the current waypoint on the trajectory
    count = 0
    
    #define a height offset to ensure that the gripper does not hit the table trying to follow the route that the palm took
    height_offset = 0.09
    
    #For every palm value
    for val in right_hand_3D_pose[HAND.PALM.value]:
        
        #offset z axis value to minimise risk of collision with table
        val[2] = val[2]+height_offset
        
        #Initialise our invalid point tracker
        point_invalid = False
        
        #Catch if point is already declared to be invalid
        if val[3] == True:
            print("Lost track of point", end = '')
            point_invalid = True
          
        #Set point to invalid if it lies outside our allowable 3D bounds
        if val[0]> xlim[1] or val[0] < xlim[0]:
            point_invalid = True
            print("x out of limits", end = '')
        if val[1]> ylim[1] or val[1] < ylim[0]:
            point_invalid = True 
            print("y out of limits", end = '')
        if val[2]> zlim[1] or val[2] < zlim[0]:
            point_invalid = True   
            print("z out of limits", end = '')
            
        #Seperate catch for if out of bounds code leads point to be declared invalid
        if point_invalid == True:
            
            print(' ', val[0],val[1],val[2])
            print("Invalid point, sleeping for a frame")
            point_invalid = True
            
        #If this is the trajectory position that is valid, move to it slowly
        elif first_round == True and point_invalid == False:

            first_round = False
            print("Move to first pos")
            print("Go to ", val[0], val[1], val[2])
            burt.movel([val[0], val[1], val[2], 1.156, 2.886, -0.15], min_time = 5)
            count  = count + 1
            
        #Otherwise go to that trajectory in real time
        else:
            
            print("Go to ", val)
            
            #Note controll_time is the time per point (not blocking, it seems to just slow down the action)
            burt.servoj([val[0], val[1], val[2], 1.156, 2.886, -0.15], lookahead_time = 0.2, control_time = 0.1, gain = 100)
            count = count +1

    #Close connection to burt
    burt.close()
    print(count)


if __name__ == '__main__': 
    
    #follow('1.23.17.49')
    follow('emo2.6.2.15.12')
    #follow('upperrightdot.31.1.15.46')