from __future__ import print_function
import sys
sys.path.insert(1,r'C:\Users\birl\Documents\updated_ur5_controller\Generic_ur5_controller')
import numpy as np
import math
import time
from math import pi
import pickle

import waypoints as wp


import kg_robot as kgr

from coordinate_transforms import convert_to_arm_coords


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import cv2

from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import ctypes

from get_3D_pose import BODY
from get_3D_pose import HAND
from get_3D_pose import get_arm_3D_coordinates


"""TODO UPDATE TO KEIRANS NEW UR5 LIBRARY TO FIGURE OUT THE JUMP DOWN THING"""
def main(filename):
    body_3D_pose, left_hand_3D_pose, right_hand_3D_pose = get_arm_3D_coordinates(filename, show_each_frame =  False)
    
    frame_rate = 10
    
    xlim = [-0.6,0.6] # x allowable range
    ylim = [-0.65, -0.16] # y allowable range
    zlim = [0.07, 1]
     
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

    burt = kgr.kg_robot(port=30010,db_host="169.254.150.100")

    print("----------------Hi Burt!-----------------\r\n\r\n")
    
    #burt.movej([np.radians(-90), np.radians(-70), np.radians(-135), np.radians(-60), np.radians(90), np.radians(45)], min_time = 5) #move to first position slowly
    #CHANGE TO MOVE TO CORRECT INITIONALISATION POSE
    
    burt.movej([np.radians(-90), np.radians(-65), np.radians(-115), np.radians(-85), np.radians(90), np.radians(45)], min_time = 3) #move to first position slowly
    
    print(burt.getl())
    
    #burt.movel(min_time)
    #burt.servoj([-0.110088, -0.313618, 0.701048, 1.156, 2.886, -0.15], lookahead_time = 10)
    
    #burt.servoj(burt.get_inverse_kin([-0.110088, -0.313618, 0.501048, 1.156, 2.886, -0.15], t=10))
    #burt.movel([-0.1980760896422284, -0.47090809213983564, 0.08714772882176902, 1.156, 2.886, -0.15], min_time = 10)
    #burt.servoj([-0.1980760896422284, -0.47090809213983564, 0.12714772882176902, 1.156, 2.886, -0.15])
    
   
    print("moved to start")
    first_round = 0
    count = 0

    for val in right_hand_3D_pose[HAND.INDEX_TIP.value]:
        
        val[2] = val[2]+0.09
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
            point_invalid = True
            
        elif first_round == 0 and point_invalid == False:

            first_round = 1
            print("Move to first pos")
            print("Go to ", val[0], val[1], val[2])
            burt.movel([val[0], val[1], val[2], 1.156, 2.886, -0.15], min_time = 5)
            count  = count + 1
        else:
            
            print("Go to ", val)
            #controll_time is the time per point (not blocking, it seems to just slow down the action)
            burt.servoj([val[0], val[1], val[2], 1.156, 2.886, -0.15], lookahead_time = 0.2, control_time = 0.1, gain = 100)
            count = count +1

    burt.close()
    print(count)


if __name__ == '__main__': 
    
    #main('1.23.17.49')
    main('upperrightdot.31.1.15.46')