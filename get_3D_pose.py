"""Main file for reading openpose and using that to get 3D coordinates"""

import numpy as np
import time
import pickle
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cv2
import ctypes
import time
import json
import glob
import os
parentDirectory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
from enum import Enum
import math

from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

from coordinate_transforms import convert_to_arm_coords

"""
TODO
* Find appropriate joint confidence threshold
* Add some code to highlight on the 2D image which joint it is that you cant see
"""

class HAND(Enum):
    """Enum of what hand joint numbers /3 represent"""
    
    PALM = 0
    BELOW_THUMB = 1
    THUMB_KUNCKLE = 2
    THUMB_JOINT_1 = 3
    THUMB_TIP = 4
    INDEX_KNUCKLE = 5
    INDEX_JOINT_1 = 6
    INDEX_JOINT_2 = 7
    INDEX_TIP = 8
    MIDDLE_KNUCKLE = 9
    MIDDLE_JOINT_1= 10
    MIDDLE_JOINT_2 = 11
    MIDDLE_TIP =12
    RING_KNUCKLE = 13
    RING_JOINT_1 = 14
    RING_JOINT_2 = 15
    RING_TIP = 16
    PINKIE_KNUCKLE = 17
    PINKIE_JOINT_1 = 18
    PINKIE_JOINT_2 = 19
    PINKIE_TIP = 20
    
    
class BODY(Enum):
    """Enum of what body joint numbers /3 represent"""
    
    HEAD = 0
    CHEST = 1
    LEFT_SHOULDER = 2
    LEFT_ELBOW = 3
    LEFT_WRIST = 4
    RIGHT_SHOULDER = 5
    RIGHT_ELBOW = 6
    RIGHT_WRIST = 7
    PELVIS = 8
    LEFT_HIP = 9
    LEFT_KNEE = 10
    LEFT_FOOT = 11
    RIGHT_HIP = 12
    RIGHT_KNEE = 13
    RIGHT_FOOT = 14
    LEFT_EYE= 15
    RIGHT_EYE = 16
    LEFT_EAR = 17
    RIGHT_EAR = 18

    
def track_body(folder):
    """function for returning all tracked points on the human body, in normalised pixel coordinates in the colour image"""
    
    #define location of JSON file with the joint positions in normalised pixel coordinates
    path = 'bin/JSON/' + folder + '/*.json'
    text_files = glob.glob(path)
    
    print("Loading data")
    
    #Load JSONS into a local list
    json_list = []
    for JSON in text_files:
        with open(JSON, "r") as json_data:
            json_list.append(json.load(json_data))
            
    #Count the number of joints in the Enums BODY and HAND
    body_tracked_joints_num = 0
    for body_joint in BODY:
        body_tracked_joints_num += 1
        
    hand_tracked_joints_num = 0
    for hand_joint in HAND:
        hand_tracked_joints_num += 1
        
    print("Total number of frames is ", len(json_list))
    
    #define list of empty lists to store the joint locations in (in normalised pixel coordinates) 
    left_hand_2D_pose = [ [] for i in range(hand_tracked_joints_num)]
    right_hand_2D_pose = [ [] for i in range(hand_tracked_joints_num)]
    body_2D_pose = [ [] for i in range(body_tracked_joints_num)]
    
    #Iteraively store joint positions in appropriate lists, if there is an error append x= -1, y = -1, confidence = -1 to the list
    frame_num = 0
    for json_dict in json_list:
        if frame_num%200 == 0:
             print("Tracking frame", frame_num)
        try:
            for body_joint in BODY:
                body_2D_pose[body_joint.value].append([json_dict['people'][0].get('pose_keypoints_2d')[3*body_joint.value], json_dict['people'][0].get('pose_keypoints_2d')[3*body_joint.value+1], json_dict['people'][0].get('pose_keypoints_2d')[3*body_joint.value+2]])
            
            for hand_joint in HAND:
                right_hand_2D_pose[hand_joint.value].append([json_dict['people'][0].get('hand_left_keypoints_2d')[3*hand_joint.value], json_dict['people'][0].get('hand_left_keypoints_2d')[3*hand_joint.value+1], json_dict['people'][0].get('hand_left_keypoints_2d')[3*hand_joint.value+2]])
                left_hand_2D_pose[hand_joint.value].append([json_dict['people'][0].get('hand_right_keypoints_2d')[3*hand_joint.value], json_dict['people'][0].get('hand_right_keypoints_2d')[3*hand_joint.value+1], json_dict['people'][0].get('hand_right_keypoints_2d')[3*hand_joint.value+2]])
        
        except IndexError:
            for body_joint in BODY:
                body_2D_pose[body_joint.value].append([-1,-1,-1])
            
            for hand_joint in HAND:
                right_hand_2D_pose[hand_joint.value].append([-1,-1,-1])
                left_hand_2D_pose[hand_joint.value].append([-1,-1,-1])
        frame_num +=1
    return body_2D_pose, left_hand_2D_pose, right_hand_2D_pose
   
#REMEBER TO HAVE A KINECT CONNECTED WHEN RUNNING
def get_arm_3D_coordinates(filename, confidence_threshold = 0, show_each_frame = False):
    """Takes saved 2D arm coordinates from track_body and turns them into list of 3D arm coordinates"""
    
    
    convert_to_am_coords_bad_count = 0
    print("calculating 3D pose in arm coordinates")
    
    #Load lists of 2D arm coords, check they contain data
    body_2D_pose, left_hand_2D_pose, right_hand_2D_pose = track_body(filename)
    if len(body_2D_pose[BODY.CHEST.value]) == 0:
        print("JSON FILE NAME INVALID")
        raise ImportError
    
    #Start a kinect (required even if we are reading saved depth values)
    kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Depth)

    #Do a bunch of defines required for matching the colour coordinates to their depth later
    color2depth_points_type = _DepthSpacePoint* np.int(1920 * 1080)
    color2depth_points = ctypes.cast(color2depth_points_type(), ctypes.POINTER(_DepthSpacePoint))
    S = 1080*1920
    TYPE_CameraSpacePointArray = PyKinectV2._CameraSpacePoint * S
    csps1 = TYPE_CameraSpacePointArray()
    
    #Defined where aved depth data is stored
    depthdatafile = open("bin/rawdata/DEPTH." + filename + ".pickle", "rb")

    cv2.destroyAllWindows()
    
    #Check number of joints to track
    body_tracked_joints_num = 0
    for body_joint in BODY:
        body_tracked_joints_num += 1
        
    hand_tracked_joints_num = 0
    for hand_joint in HAND:
        hand_tracked_joints_num += 1
    
    #Define lists of lists to store 3D poses in
    left_hand_3D_pose = [ [] for i in range(hand_tracked_joints_num)]
    right_hand_3D_pose = [ [] for i in range(hand_tracked_joints_num)]
    body_3D_pose = [ [] for i in range(body_tracked_joints_num)]
    
    #print("Total number of frames is ", len(body_2D_pose[0]))
    #Iterate over each frame
    for framenum in range(len(body_2D_pose[0])):
        
        if framenum%100 == 0:
            print("Finding points in frame ", framenum)
        depthframe = pickle.load(depthdatafile) #need to do this once per frame
        
        #Carry out certain actions if you want an image of where all the tracked joints are (20x slower)
        if show_each_frame == True:
            frame = depthframe
            frame = frame.astype(np.uint8)
            frame = np.reshape(frame, (424, 512))
        
        #Defines to allow depth mapping to work correctly     
        ctypes_depth_frame = np.ctypeslib.as_ctypes(depthframe.flatten())
        L = depthframe.size
        kinect._mapper.MapColorFrameToDepthSpace(ctypes.c_uint(512 * 424), ctypes_depth_frame, ctypes.c_uint(1920 * 1080), color2depth_points)
        kinect._mapper.MapColorFrameToCameraSpace(L, ctypes_depth_frame, S, csps1)
        
        #Iterate over the lists of joint positions in the 2D colour image
        for raw_coords_list in body_2D_pose, left_hand_2D_pose, right_hand_2D_pose:
            
            #Define the type of list we are iterating over
            if raw_coords_list[5] == body_2D_pose[5]:
                tracked_class = BODY
                listtype = "BODY"
                
            elif raw_coords_list[5] == left_hand_2D_pose[5]:
                tracked_class = HAND
                listtype = "LEFTHAND"
                
            elif raw_coords_list[5] == right_hand_2D_pose[5]:
                tracked_class = HAND
                listtype = "RIGHTHAND"
            
            #Iterate over each joint
            for joint in tracked_class:
                
                position = raw_coords_list[joint.value][framenum]
                
                #Say we havent lost track if the confidence value in the joint position is over a certain threshold
                if position[2] > confidence_threshold:
                    lost_track = False
                    
                else:
                    lost_track = True
                    #print('a')
                    
                if position == [-1,-1,-1]:
                    lost_track = True
                    #print('b')
                if position == [0,0,0]: #what openpose returns if it cant see
                    lost_track = True
                    #print('c')
                
                #I think this filtering is all in the wrong place...
                if math.isinf(position[0]) == True: 
                    arm_coords = [0,0,0.1]
                    lost_track = True
                    #print('d')
                if math.isinf(position[1]) == True:  
                    arm_coords = [0,0,0.2]
                    lost_track = True
                    #print('e')
                if math.isinf(position[2]) == True:
                    arm_coords = [0,0,0.3]
                    lost_track = True
                    #print('f')
                if math.isnan(position[0]) == True:
                    arm_coords = [0,0,0.4]
                    lost_track = True
                    #print('g')
                if math.isnan(position[1]) == True:
                    arm_coords = [0,0,0.5]
                    lost_track = True
                    #print('h')
                if math.isnan(position[2]) == True:
                    arm_coords = [0,0,0.6]
                    lost_track = True
                    #print('i')
                if lost_track == False:

                    if position[0]>1 :
                        position[0] = 1-1/1920         
 
                    if position[0]<0 :
                        position[0] = 0    
                        
                    if position[1]>1 :
                        position[1] = 1-1/1920         
 
                    if position[1]<0 :
                        position[1] = 0  

                    #find x and y in pixel (not normalised pixel) position in the 2D image
                    x = int(position[0]*1920)
                    y = int(position[1]*1080)
                    
  

                    #Find 3D position of each pixel using Colour_to_camera method
                    x_3D = csps1[y*1920 + x].x
                    y_3D = csps1[y*1920 + x].y
                    z_3D = csps1[y*1920 + x].z

                   
                    arm_coords  = convert_to_arm_coords(x_3D, y_3D, z_3D)
                    if math.isnan(arm_coords[0]):
                        arm_coords = [-1,-1,-0.9]
                        lost_track = True
                        #print('j')
                        convert_to_am_coords_bad_count = convert_to_am_coords_bad_count + 1
                        #raise ImportError("Recieveing nan for 3D position, are you sure that kinect studio is running/ the kinect is connected?") 

                    if convert_to_am_coords_bad_count > 1000:
                        print("|||\\\___Lots of bad arm coords being returned, are you sure kinect studio is running or a Kinect is connected?___///|||")
                        
                        convert_to_am_coords_bad_count = 0
                    #if joint == BODY.RIGHT_ELBOW:
                       #print(framenum, lost_track)
                        #print(position)
                        #print(arm_coords) 
                    if show_each_frame == True:
                        try:
                        
                            #depth image 2D x and y in pixels, and deoth inage depth of a specific pixel using Colour_to_depth method - useful for displaying joint positions on a 2D image, NOT FOR FINDING 3D JOINT POSITIONS
                            read_pos = x+y*1920 -1
                            x_pixels = int(color2depth_points[read_pos].x)
                            y_pixels = int(color2depth_points[read_pos].y)
                            
                        except OverflowError:
                            
                            #Say joint is in the corner when you cant see it
                            x_pixels = 1
                            y_pixels = 1 
                    
                        #Display the 2D joint positions on the depth image if a flag is set (flag makes program run 20x slower)
                        if show_each_frame == True and lost_track == False:
                            cv2.circle(frame, (x_pixels,y_pixels), 5, (255, 0, 255), -1)

                if lost_track == True:
                    
                    #Set arm coords to -1 to show that they are in error
                    arm_coords = [-1,-1,-1]
                    
                    if show_each_frame == True:
                        
                        #draw a big circle if we cant see the joint (will probably end up in the corner of the image)
                        cv2.circle(frame, (0,0), 25, (200, 0, 200), -1)

                #Display annotated depth image if flag is set
                if show_each_frame == True:
                    cv2.imshow('KINECT Video Stream', frame)
                    key = cv2.waitKey(1)
                    if key == 27: 
                        pass
                
                #Add 3D joint positions, and whether we classify that joint as lost, in the approproate list
                if listtype == "BODY":
                    body_3D_pose[joint.value].append([arm_coords[0],arm_coords[1],arm_coords[2], lost_track])
                    
                elif listtype == "LEFTHAND":
                    left_hand_3D_pose[joint.value].append([arm_coords[0],arm_coords[1],arm_coords[2], lost_track])
                    
                elif listtype == "RIGHTHAND":
                    right_hand_3D_pose[joint.value].append([arm_coords[0],arm_coords[1],arm_coords[2], lost_track])
                    
    #Close Depth image window (if open), and return 3D joint position lists                
    cv2.destroyAllWindows()
    return body_3D_pose, left_hand_3D_pose, right_hand_3D_pose
     
    

if __name__ == '__main__': 

    #start_time = time.time()
    #body_3D_pose, left_hand_3D_pose, right_hand_3D_pose = get_arm_3D_coordinates('1.23.17.49', show_each_frame =  False)
    #body_3D_pose, left_hand_3D_pose, right_hand_3D_pose = get_arm_3D_coordinates('1.24.21.39', show_each_frame =  False)
    body_3D_pose, left_hand_3D_pose, right_hand_3D_pose = get_arm_3D_coordinates('feb3.3.3.15.30', show_each_frame =  False)
    print(body_3D_pose[BODY.RIGHT_ELBOW.value])
    """
    #print("Time taken is", time.time()-start_time)
    x_sec= []
    y_sec= []
    z_sec = []
    
    for pos in right_hand_3D_pose[HAND.PALM.value]:

        if pos[3] ==False:
            x_sec.append(pos[0])
            y_sec.append(pos[1])
            z_sec.append(pos[2])

    
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x_sec, y_sec, z_sec)
    plt.show()
    """

