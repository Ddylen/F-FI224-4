# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 10:13:08 2020

@author: birl
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 13:04:35 2019

@author: birl
"""

# -*- coding: utf-8 -*-
"""
Code for smoothly following a human demonstrator in 3D
TODO: NOT FINISED YET
TASKS:
   
    6) Review my coordinate trasnforms and check the paths I get out of some test code look sensible
    
COLOR AND DEPTH CAMERAS HAVE DIFFERENT FIELDS OF VIEW, FIGURE OUT HOW TO ACCOUNT FOR THAT!!!!!!!!!!!!!!!!!!!!
"""

import sys
sys.path.insert(1,r'C:\Users\birl\Documents\ur5_python_host\ur5_kg_robot')
import numpy as np
import math
import time
from math import pi
import pickle
import waypoints as wp
from kg_robot import kg_robot
from reader import interpret2D
from convert_2_world import convert_2_world
import specialised_kg_robot_example as kgrs 
from convert_to_arm_coords import convert_to_arm_coords

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import cv2
from convertcolourpixeltoIR import convertcolourpixeltoIR



from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import ctypes

"""
SOMETHING IS GOINT WRONG IN SCALING WITH HEIGHT
"""

    


def main():
    frame_rate = 0.1 
    #palm_list = interpret2D('staystill', 'wrist')
    palm_list = interpret2D('circle', 'wrist')
    if len(palm_list) == 0:
        print("JSON FILE NAME INVALID")
        raise ImportError
    #print(palm_list)
    #print(palm_list)
    arm_pos_list = []
    arm_x_list = []
    arm_y_list = []
    arm_z_list = []

    kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Depth | PyKinectV2.FrameSourceTypes_Infrared)
    color2depth_points_type = _DepthSpacePoint* np.int(1920 * 1080)
    color2depth_points = ctypes.cast(color2depth_points_type(), ctypes.POINTER(_DepthSpacePoint))
    
    #depthdatafile = open("depthdata/DEPTH12.3.14.50.pickle", "rb")
    depthdatafile = open("depthdata/DEPTH11.19.16.50.pickle", "rb")
    colourdatafile = open("depthdata/COLOUR11.19.16.50.pickle", "rb")
    x_scale_factor = math.sin(math.radians(42.05)) # Using FoV spec, this is the maximum object size that fits in half of FoV horizonally at 1m away
    y_scale_factor = math.sin(math.radians(26.9)) # Using FoV spec, this is the maximum object size that fits in half of FoV vertically at 1m away
    i = -1
    for val in palm_list:
        i = i+1
        x_normalised =val[0]
        y_normalised = val[1] # these are X and Y in terms of the normalised pixel value they are at
        #print(x_normalised, y_normalised)
        depthframe = pickle.load(depthdatafile) #need to do this once per frame
        colourframe = pickle.load(colourdatafile)
        ctypes_depth_frame = np.reshape(depthframe, 424*512)
        ctypes_depth_frame = np.ctypeslib.as_ctypes(ctypes_depth_frame)
        #print(depthframe[1001])
        #print(type(ctypes_depth_frame[1001]))
        #print(ctypes_depth_frame[1001])
        kinect._mapper.MapColorFrameToDepthSpace(ctypes.c_uint(512 * 424), ctypes_depth_frame, ctypes.c_uint(1920 * 1080), color2depth_points)
        x_pixels = color2depth_points[int(x_normalised)*1920+int(y_normalised)-1].x
        y_pixels = color2depth_points[int(x_normalised) * 1920+int(y_normalised)-1].y
        #x_pixels, y_pixels  = convertcolourpixeltoIR2(x_normalised, y_normalised, ctypes_depth_frame)
        #x_pixels, y_pixels  = convertcolourpixeltoIR2(x_normalised*1920, y_normalised*1080)
        #print(x_normalised, y_normalised)
        #x_normalised= x_pixels/512 
        #y_normalised = y_pixels/424
        #print(x_normalised)
        #plt.plot(x_normalised, y_normalised, 'ob')
        #print(x_normalised, y_normalised)
        """From one sample, normalised values look roughly correct"""
        
        #print(depthframe)
        
        #print(depthframe)
        #print(round(x_normalised*424))
        #print(round(y_normalised*512))
        #print(int(x_normalised*424), int(y_normalised*512))
        #print(x_normalised, y_normalised)
        frame = depthframe
        frame = frame.astype(np.uint8)
        frame = np.reshape(frame, (424, 512))
        cv2.circle(colourframe, (int(x_normalised*1920), int(y_normalised*1080)), 10, (255, 0, 255), -1)
        cv2.imshow('KINECT Video Stream', colourframe)
        time.sleep(0.1)
        key = cv2.waitKey(1)
        if key == 27: 
            pass
        
        arm_coords, depth = convert_to_arm_coords(x_normalised,y_normalised,depthframe, True)
        #print(arm_coords)
        
        arm_coords_list_form = [arm_coords.item(0), arm_coords.item(1), arm_coords.item(2)]
        if arm_coords.item(0) != -111:
            arm_x_list.append(arm_coords.item(0))
            arm_y_list.append(arm_coords.item(1))
            arm_z_list.append(arm_coords.item(2))
            
        #print(type(arm_coords_list_form))
        arm_pos_list.append(arm_coords_list_form)

    print("LAST VALE IS", arm_pos_list[-1])
    plt.plot(arm_x_list, arm_y_list)
    """
    depthframe = np.reshape(depthframe, (424, 512))
    depthfromcam = depthframe[round(x_normalised*424)][round(y_normalised*512)]/1000 #converted to m from mm # TODO: include some smoothing here
    
    x_camera_coords = depthfromcam* 0.86*2*(x_normalised-0.5)*x_scale_factor 
    y_camera_coords = depthfromcam* 1.56*2*(y_normalised-0.5)*y_scale_factor # i think my scaling method is off by a bit
    #print(x_camera_coords,y_camera_coords,depthfromcam)
    

    if depthfromcam != 0.0:

        board_coords = convert_2_world(np.matrix([[x_camera_coords], [y_camera_coords], [depthfromcam]])) #TODO: confirm that this transformation applies for normalised pixel coordinates
        #print(board_coords.item(0), board_coords.item(1), board_coords.item(2))
        
        board_to_arm_translation = np.matrix([[0.1],[0.39],[0.4]])#measured from board to arm 0,0,0 position
        arm_coords_twisted = board_coords + board_to_arm_translation
        arm_coords = np.matrix([[- arm_coords_twisted.item(0)], [-arm_coords_twisted.item(1)], [-arm_coords_twisted.item(2)]]) #axes for arm are other way round to that of checkerboard
        arm_pos_list.append(arm_coords)
    """

    #xlim = [-0.4,0.4] # x allowable range
    #ylim = [-0.22, -0.6] # y allowable range
    #zlim = [-0.32, 1]
    
            
    x_sec= []
    y_sec= []
    z_sec = []
    for pos in arm_pos_list:
        print(type(pos))
        if pos[0] != -111:
            x_sec.append(pos[0])
            y_sec.append(pos[1])
            z_sec.append(pos[2])
        print(pos[0],pos[1], pos[2])
    
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x_sec, y_sec, z_sec)
    plt.show()
    

    #fig = plt.figure()
    #ax = plt.axes(projection='3d')
    #ax.plot3D(x_sec, y_sec, z_sec, 'gray')
    #plt.show()
    
    #print(arm_pos_list)
    """
    print("------------Configuring Burt-------------\r\n")

    burt = 0

    burt = kgrs.specialised_kg_robot(port=30010,db_host="169.254.150.100")

    print("----------------Hi Burt!-----------------\r\n\r\n")
    
    "TODO: NEW FIRST POSITION"
    burt.movej([np.radians(-318), np.radians(-99), np.radians(156), np.radians(214), np.radians(-90), np.radians(45)], min_time = 5) #move to first position slowly
    #CHANGE TO MOVE TO CORRECT INITIONALISATION POSE
    first_round = 0
    print("moved to start")
    for val in arm_pos_list:
        if val.item(0)> xlim[1] or val.item(0) < xlim[0] or val.item(1)> ylim[1] or val.item(1) < ylim[0] or val.item(2)> zlim[1] or val.item(2) < zlim[0]:
            print(val.item(0),val.item(1),val.item(2))
            print("Invalid point, sleeping for a frame")
            time_min = 1 #TODO: This is hacky, find something better
            continue
        elif first_round == 0:
            time_min = 3
            first_round = 1
        else:
            time_min = frame_rate
    
        if(time_min == frame_rate):

            print("Go to ", val.item(0), val.item(1), val.item(2))
        
        burt.servoj([val._getitem(0), val._getitem(1), val._getitem(2), 1.156, 2.886, -0.15])
       
    
    burt.close()
    """
if __name__ == '__main__': main()
