# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 18:21:55 2020

@author: birl
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 18:13:27 2020

@author: birl
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 18:09:12 2020

@author: birl
"""

import sys
sys.path.insert(1,r'C:\Users\birl\Documents\ur5_python_host\ur5_kg_robot')
import numpy as np
import time
import pickle
from reader import raw_interpret2D
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import cv2
from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import ctypes
import math

def convert_2_world(camera_coords):
    """Convert Camera coordinates to world coordinates"""
    
    rotation_matrix = np.matrix([[-0.0060 , 1.0000, -0.0057],[-0.6635, 0.0002,  0.7481],[0.7481, 0.0083, 0.6635]])
    inv_rotation_matrix = rotation_matrix.getI()
    translation_vector = np.matrix([[-0.6859216],	[-0.1578426],	[-0.9921875]])
    shifted_vector = camera_coords - translation_vector
    world_coords = inv_rotation_matrix*shifted_vector
    fine_tune = np.matrix([[0],	[0],	[0]])
    world_coords = world_coords -  fine_tune
    return world_coords


def convert_to_arm_coords(x_input, y_input, z_input, return_depth = False):
    """Function to convert an x,y,z value into arm coordinates"""
    
    board_coords = convert_2_world(np.matrix([[x_input], [y_input], [z_input]])) #TODO: confirm that this transformation applies for normalised pixel coordinates
    #board_to_arm_translation = np.matrix([[0.1],[0.39],[0.4]])#measured from board to arm 0,0,0 position
    #arm_coords_twisted = board_coords + board_to_arm_translation
    arm_coords_twisted = board_coords
    arm_coords = np.matrix([[- arm_coords_twisted.item(0)], [-arm_coords_twisted.item(1)], [-arm_coords_twisted.item(2)]]) #axes for arm are other way round to that of checkerboard
    outputmat =  arm_coords
    if return_depth == False:
        return outputmat
    else:
        return outputmat
    
    
def main():
    """NEEDS A KINECT CONNECTED TO WORK"""
    #Open list of joint positions
    
    #palm_list = raw_interpret2D('circle', 'wrist')
    #filename = "1.14.11.40"
    #filename = "1.14.13.46"
    #filename = "1.14.18.4"
    filename = "1.15.18.20"
    elbow_list, palm_list = raw_interpret2D(filename, 'wrist')
    if len(palm_list) == 0:
        print("JSON FILE NAME INVALID")
        raise ImportError
        
    #Open corresponding list of depth frames
    
    #depthdatafile = open("depthdata/DEPTH11.19.16.50.pickle", "rb")
    depthdatafile = open("bin/rawdata/DEPTH."  + filename + ".pickle", "rb")
    #Lists for storing joint positions in arm coordinates
    arm_pos_list = []
    arm_x_list = []
    arm_y_list = []
    arm_z_list = []
    
    camera_x_list = []
    camera_y_list = []
    camera_z_list = []
    
    #code required to map the colour image coordinates of the joint to the depth coordinates
    kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Depth)
    color2depth_points_type = _DepthSpacePoint* np.int(1920 * 1080)
    color2depth_points = ctypes.cast(color2depth_points_type(), ctypes.POINTER(_DepthSpacePoint))
    

    S = 1080*1920
    TYPE_CameraSpacePointArray = PyKinectV2._CameraSpacePoint * S
    csps1 = TYPE_CameraSpacePointArray()



    i = -1
    for val in palm_list:
        i = i+1
        
        # Get normalised X and Y of the joint in the colour image
        x_normalised =val[0]
        y_normalised = val[1] 
        
        #Keep track of if openpose has lost track of the relevant joint
        lost_track = False
        if val[0] ==0 and val[1] ==0:
            lost_track = True

        #Load matching depth frame
        depthframe = pickle.load(depthdatafile) 
        
        #Code to find matching depth frame position for the colour frame position of the joints
        ctypes_depth_frame = np.ctypeslib.as_ctypes(depthframe.flatten())
        
        L = depthframe.size
        
        kinect._mapper.MapColorFrameToDepthSpace(ctypes.c_uint(512 * 424), ctypes_depth_frame, ctypes.c_uint(1920 * 1080), color2depth_points)
        read_pos = int((x_normalised)*1920)+int((y_normalised)*1080)*1920 -1
        
        kinect._mapper.MapColorFrameToCameraSpace(L, ctypes_depth_frame, S, csps1)
        x_3D = csps1[int(y_normalised*1080)*1920 + int(x_normalised*1920)].x
        y_3D = csps1[int(y_normalised*1080)*1920 + int(x_normalised*1920)].y
        z_3D = csps1[int(y_normalised*1080)*1920 + int(x_normalised*1920)].z
        
        #filter out infinite values and massive outliers
        if x_3D != (np.inf or -np.inf) and abs(x_3D)<10 and abs(y_3D)<10 and abs(z_3D)<10:
            if z_3D > 0.5 and z_3D< 2:
            #measured_pos_list.append((x_3D,y_3D, z_3D))
                camera_x_list.append(x_3D)
                camera_y_list.append(y_3D)
                camera_z_list.append(z_3D)
            
        print(x_3D,y_3D,z_3D)
        #Try except loop as we sometimes get back infinity from the function below causing knock-on errors
        try:
            x_pixels = int(color2depth_points[read_pos].x)
            y_pixels = int(color2depth_points[read_pos].y)
        except OverflowError:
            x_pixels = 1
            y_pixels = 1
        
        #Code to draw the depth frame as an image
        frame = depthframe
        frame = frame.astype(np.uint8)
        frame = np.reshape(frame, (424, 512))
        
        #extract the depth of the tracked joint
        #joint_depth = ctypes_depth_frame[int(x_pixels)+int(y_pixels)*512]
        #print(joint_depth)
        
        
        #Plot a small circle is joint seen, and a large circle at the last joint position OpenPose lost the joint
        try:
            if lost_track == False:
                pos_previous = (int(x_pixels), int(y_pixels))
                cv2.circle(frame, (int(x_pixels), int(y_pixels)), 5, (255, 0, 255), -1)
            else:
                cv2.circle(frame, pos_previous, 25, (200, 0, 200), -1)
        except:
            print("infinity seen")
            
        #display the frames, at roughly the speed they were filmed
        cv2.imshow('KINECT Depth Stream', frame)
        #time.sleep(0.1)
        
        #CLose Depth Data Screen if escape pressed
        key = cv2.waitKey(1)
        if key == 27: 
            pass
        
        #Convert joints to arm coordinates
        arm_coords = convert_to_arm_coords(x_3D,y_3D,z_3D, True)
        arm_coords_list_form = [arm_coords.item(0), arm_coords.item(1), arm_coords.item(2)]
        if arm_coords.item(0) != -111:
            arm_x_list.append(arm_coords.item(0))
            arm_y_list.append(arm_coords.item(1))
            arm_z_list.append(arm_coords.item(2))
    
        arm_pos_list.append(arm_coords_list_form)
        
    # Release everything if job is finished
    cv2.destroyAllWindows()

    #Lists to store the valid arm positions found
    x_sec= []
    y_sec= []
    z_sec = []
    
    #Filter out invalid arm positions
    for pos in arm_pos_list:
        if pos[0] != -111:
            x_sec.append(pos[0])
            y_sec.append(pos[1])
            z_sec.append(pos[2])
        
    #Plot a 3D diagram of arm positions
    #plt.plot(arm_z_list)
    
    
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(camera_x_list, camera_y_list, camera_z_list)
    #ax.scatter(arm_x_list, arm_y_list, arm_z_list)
    plt.draw()
    
    
if __name__ == '__main__': main()
