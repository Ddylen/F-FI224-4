from __future__ import print_function
import sys
sys.path.insert(1,r'C:\Users\birl\Documents\ur5_python_host\ur5_kg_robot')
import numpy as np
import math
import time
from math import pi
import pickle
import waypoints as wp
from kg_robot import kg_robot
from reader import track_body
import specialised_kg_robot_example as kgrs 
from coordinatetesternew import convert_2_world
from coordinatetesternew import convert_to_arm_coords


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import cv2

from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import ctypes

from reader import BODY
from reader import HAND

from get_3D_pose import get_arm_3D_coordinates


"""TODO UPDATE TO KEIRANS NEW UR5 LIBRARY TO FIGURE OUT THE JUMP DOWN THING"""
def main(filename):
    body_3D_pose, left_hand_3D_pose, right_hand_3D_pose = get_arm_3D_coordinates(filename, show_each_frame =  False)
    
    frame_rate = 10
    
    xlim = [-0.6,0.6] # x allowable range
    ylim = [-0.6, -0.22] # y allowable range
    zlim = [-0.33, 1]
     
    x_sec= []
    y_sec= []
    z_sec = []
    for pos in right_hand_3D_pose[HAND.PALM.value]:
        #print(type(pos))
        if pos[3] ==False:
            x_sec.append(pos[0])
            y_sec.append(pos[1])
            z_sec.append(pos[2])
        #print(pos[0],pos[1], pos[2])
    #print(right_hand_3D_pose[HAND.PALM.value])
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x_sec, y_sec, z_sec)
    plt.show()

    print("------------Configuring Burt-------------\r\n")

    burt = 0

    burt = kgrs.specialised_kg_robot(port=30010,db_host="169.254.150.100")

    print("----------------Hi Burt!-----------------\r\n\r\n")
    
    "TODO: NEW FIRST POSITION"
    burt.movej([np.radians(52), np.radians(-88), np.radians(85), np.radians(267), np.radians(-88), np.radians(26)], min_time = 5) #move to first position slowly
    #CHANGE TO MOVE TO CORRECT INITIONALISATION POSE

    print("moved to start")
    first_round = 0

    for val in right_hand_3D_pose[HAND.PALM.value]:
        point_invalid = False
        if val[3] == True:
            print("Lost track of point", end = '')
            point_invalid = True
        if val[0]> xlim[1] or val[0] < xlim[0]:
            point_invalid = True
            print("x out of limits", end = '')
        if val[1]> ylim[1] or val[1] < ylim[0]:
            point_invalid = True 
            print("y out of limits", end = '')
        if val[2]> zlim[1] or val[2] < zlim[0]:
            point_invalid = True   
            print("z out of limits", end = '')
            
        if point_invalid == True:
            print(' ', val[0],val[1],val[2])
            print("Invalid point, sleeping for a frame")
            time_min = 10 #TODO: This is hacky, find something better
            point_invalid = True
        elif first_round == 0:
            time_min = 10
            first_round = 1
        else:
            time_min = frame_rate
    
        if(point_invalid == False):

            print("Go to ", val[0], val[1], val[2])
            #Arm still has issue where it shoots down rapidly when I call servoj, might need to update my code to the new library
            #burt.servoj([val[0], val[1], val[2]+0.6, 1.156, 2.886, -0.15], control_time = time_min)
    
    burt.close()


if __name__ == '__main__': 
    
    main('1.23.17.49')
