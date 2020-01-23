# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 16:47:39 2020

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
import pickle

#figure of 8 is 1.15.17.43
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
    
def std_3D(datalist):
    #print(datalist[0])
    mean_x = np.mean([x[0] for x in datalist])
    mean_y = np.mean([x[1] for x in datalist])
    mean_z = np.mean([x[2] for x in datalist])
    std = np.std([np.sqrt((x[0]-mean_x)**2+(x[1]-mean_y)**2+(x[2]-mean_z)**2) for x in datalist])
    return std
    
def main():
    """NEEDS A KINECT CONNECTED TO WORK"""
    #Open list of joint positions
    
    #palm_list = raw_interpret2D('circle', 'wrist')
    #filename = "1.14.11.40"
    #filename = "1.14.13.46"
    #filename = "1.14.18.4"
    #filename = "1.15.11.29"
    filename = "1.15.17.31"
    elbow_list, wrist_list = raw_interpret2D(filename, 'wrist')
    palm_list, thumb_list, index_end_list = raw_interpret2D(filename, 'hand')
    

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
    elbow_3D = []
    wrist_3D= []
    palm_3D = []
    thumb_3D = []
    index_3D = []
    for val in palm_list:
        i = i+1
        tracked_points= []
        tracked_points.append((elbow_list[i][0], elbow_list[i][1]))
        tracked_points.append((wrist_list[i][0], wrist_list[i][1]))
        tracked_points.append((palm_list[i][0], palm_list[i][1]))
        tracked_points.append((thumb_list[i][0], thumb_list[i][1]))
        tracked_points.append((index_end_list[i][0], index_end_list[i][1]))
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
        kinect._mapper.MapColorFrameToCameraSpace(L, ctypes_depth_frame, S, csps1)
        
        tracked_points_3D = []
        
        read_pos = int((x_normalised)*1920)+int((y_normalised)*1080)*1920 -1
        
        for val in tracked_points:
            
            x_3D = csps1[int(val[1]*1080)*1920 + int(val[0]*1920)].x
            y_3D = csps1[int(val[1]*1080)*1920 + int(val[0]*1920)].y
            z_3D = csps1[int(val[1]*1080)*1920 + int(val[0]*1920)].z
            
            #filter out infinite values and massive outliers
            if x_3D != (np.inf or -np.inf):
                #measured_pos_list.append((x_3D,y_3D, z_3D))
                tracked_points_3D.append((x_3D, y_3D, z_3D))
    
    
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
        
        """
        #Convert joints to arm coordinates
        arm_coords = convert_to_arm_coords(palm_x_3D,palm_y_3D,palm_z_3D, True)
        arm_coords_list_form = [arm_coords.item(0), arm_coords.item(1), arm_coords.item(2)]
        if arm_coords.item(0) != -111:
            arm_x_list.append(arm_coords.item(0))
            arm_y_list.append(arm_coords.item(1))
            arm_z_list.append(arm_coords.item(2))
    
        arm_pos_list.append(arm_coords_list_form)
        """
        elbow_3D.append(tracked_points_3D[0])
        wrist_3D.append(tracked_points_3D[1])
        palm_3D.append(tracked_points_3D[2])
        thumb_3D.append(tracked_points_3D[3])
        index_3D.append(tracked_points_3D[4])
    # Release everything if job is finished
    cv2.destroyAllWindows()
    
    elbowfile = open("elbow.pickle", 'wb')
    wristfile = open("wrist.pickle", 'wb')
    palmfile = open("palm.pickle", 'wb')
    thumbfile = open("thumb.pickle", 'wb')
    indexfile = open("index.pickle", 'wb')
    pickle.dump(elbow_3D, elbowfile)
    pickle.dump(wrist_3D, wristfile)
    pickle.dump(palm_3D, palmfile)
    pickle.dump(thumb_3D, thumbfile)
    pickle.dump(index_3D, indexfile)
    
    print
    print("elbow", std_3D(elbow_3D))
    print("wrist", std_3D(wrist_3D))
    print("palm", std_3D(palm_3D))
    print("thunb", std_3D(thumb_3D))
    print("index", std_3D(index_3D))
    
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
    #ax.scatter(camera_x_list, camera_y_list, camera_z_list)
    ax.scatter(arm_x_list, arm_y_list, arm_z_list)
    plt.draw()
    
    
if __name__ == '__main__': main()
