"""
Functions for reading openpose data and using that to get 3D coordinates of the joints
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pickle
import cv2
import ctypes
import json
import glob
import os
from enum import Enum
import math

from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

from coordinate_transforms import convert_to_arm_coords

parentDirectory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))


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
    
    #Initialse frame tracking variable
    frame_num = 0
    
    #Iteraively store joint positions in appropriate lists, if there is an error append x= -1, y = -1, confidence = -1 to the list
    for json_dict in json_list:
        
        #Print progress messages to avoid long pauses with no output when processing long recordings
        if frame_num%200 == 0:
             print("Tracking frame", frame_num)
             
        #try to extact the 2D recorded positions of each joint from openpose
        try:
            for body_joint in BODY:
                body_2D_pose[body_joint.value].append([json_dict['people'][0].get('pose_keypoints_2d')[3*body_joint.value], json_dict['people'][0].get('pose_keypoints_2d')[3*body_joint.value+1], json_dict['people'][0].get('pose_keypoints_2d')[3*body_joint.value+2]])
            
            for hand_joint in HAND:
                right_hand_2D_pose[hand_joint.value].append([json_dict['people'][0].get('hand_left_keypoints_2d')[3*hand_joint.value], json_dict['people'][0].get('hand_left_keypoints_2d')[3*hand_joint.value+1], json_dict['people'][0].get('hand_left_keypoints_2d')[3*hand_joint.value+2]])
                left_hand_2D_pose[hand_joint.value].append([json_dict['people'][0].get('hand_right_keypoints_2d')[3*hand_joint.value], json_dict['people'][0].get('hand_right_keypoints_2d')[3*hand_joint.value+1], json_dict['people'][0].get('hand_right_keypoints_2d')[3*hand_joint.value+2]])
        
        #exception for if openpose lost track of the human skeleton, leading the lists measured above to be empty
        except IndexError:
            for body_joint in BODY:
                body_2D_pose[body_joint.value].append([-1,-1,-1])
            
            for hand_joint in HAND:
                right_hand_2D_pose[hand_joint.value].append([-1,-1,-1])
                left_hand_2D_pose[hand_joint.value].append([-1,-1,-1])
        frame_num +=1
    return body_2D_pose, left_hand_2D_pose, right_hand_2D_pose
   

def filter_out_invalid(pos, threshold):
    """Function to mark clealy invalid points as bad"""
    
    #initialise armpos (will be overwritten later if point is good)
    armpos = [-3,-3,-3]
    
    #Say we havent lost track if the confidence value in the joint position is over a certain threshold
    if pos[2] > threshold:
        lost = False
        
    else:
        lost = True
      
    #Catch the joint position we returned when openpose cant see a skeleton
    if pos == [-1,-1,-1]:
        lost = True

    #Catch the position openpose sometimes fills its first JSON message with
    if pos == [0,0,0]: 
        lost = True
    
    #Catch any other invalid points - this may be redundant given previous filtering stages, but the effect of removing this has not been extensively tested
    if math.isinf(pos[0]) == True: 
        armpos = [0,0,0.1]
        lost = True

    if math.isinf(pos[1]) == True:  
        armpos = [0,0,0.2]
        lost = True

    if math.isinf(pos[2]) == True:
        armpos = [0,0,0.3]
        lost = True

    if math.isnan(pos[0]) == True:
        armpos = [0,0,0.4]
        lost = True

    if math.isnan(pos[1]) == True:
        armpos = [0,0,0.5]
        lost = True

    if math.isnan(pos[2]) == True:
        armpos = [0,0,0.6]
        lost = True
    
    return armpos, lost
    
def display_joints(x,y, lost_track, color2depth_points, frame):
    """Function to display the position of the tracked joints"""
    
    try:
                            
        #depth image 2D x and y in pixels, and deoth inage depth of a specific pixel using Colour_to_depth method - useful for displaying joint positions on a 2D image, NOT FOR FINDING 3D JOINT POSITIONS
        read_pos = x+y*1920 -1
        x_pixels = int(color2depth_points[read_pos].x)
        y_pixels = int(color2depth_points[read_pos].y)
        
    except OverflowError:
        
        #Say joint is in the corner when you cant see it
        x_pixels = 1
        y_pixels = 1 
    
    #Highlight the 2D joint positions on the depth image 
    if lost_track == False:
        cv2.circle(frame, (x_pixels,y_pixels), 5, (255, 0, 255), -1)    
    
    else:
        #Draw a joint in the corner of the screen if its recorded as bad
        cv2.circle(frame, (0,0), 25, (200, 0, 200), -1)
    
    #Display annotated depth image 
    cv2.imshow('KINECT Video Stream', frame)
    key = cv2.waitKey(1)
    if key == 27: 
        pass
    
def get_tracked_class(raw_coords_sample, body_2D_sample, left_hand_2D_sample, right_hand_2D_sample):
    """Function to define what kind of list we are iterating over in get_arm_3D_coordinates"""
    
    if raw_coords_sample == body_2D_sample:
        tracked_class = BODY
        listtype = "BODY"
        
    elif raw_coords_sample == left_hand_2D_sample:
        tracked_class = HAND
        listtype = "LEFTHAND"
        
    elif raw_coords_sample == right_hand_2D_sample:
        tracked_class = HAND
        listtype = "RIGHTHAND"
        
    return tracked_class, listtype
    

def get_arm_3D_coordinates(filename, confidence_threshold = 0, show_each_frame = False):
    """Takes saved 2D arm coordinates from track_body and turns them into list of 3D arm coordinates
    NEEDS TO HAVE A KINECT OR RUNNING KINECT STUDIO RECORDING CONNECTED WHEN THIS PROGRAM IS RUN, because of requirements from PyKinect2"""
    
    print("calculating 3D pose in arm coordinates")
    
    #keep a could of how many conversion fail - a high number could suggest that no kinect/ running kinectstudio recording is present
    convert_to_am_coords_bad_count = 0
    
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
    
    #Iterate over each frame
    for framenum in range(len(body_2D_pose[0])):
        
        #Print progress messages
        if framenum%100 == 0:
            print("Finding points in frame ", framenum)
            
        #Load the single relevant (to this iteration) depth frame from pickle
        depthframe = pickle.load(depthdatafile) 
        
        #Carry out certain actions if you want an image of where all the tracked joints are (this makes the program run 20x slower)
        if show_each_frame == True:
            frame = depthframe
            frame = frame.astype(np.uint8)
            frame = np.reshape(frame, (424, 512))
        
        #More defines to allow depth mapping to work correctly     
        ctypes_depth_frame = np.ctypeslib.as_ctypes(depthframe.flatten())
        L = depthframe.size
        kinect._mapper.MapColorFrameToDepthSpace(ctypes.c_uint(512 * 424), ctypes_depth_frame, ctypes.c_uint(1920 * 1080), color2depth_points)
        kinect._mapper.MapColorFrameToCameraSpace(L, ctypes_depth_frame, S, csps1)
        
        #Iterate over the lists of joint positions in the 2D colour image
        for raw_coords_list in body_2D_pose, left_hand_2D_pose, right_hand_2D_pose:
            
            #Define the type of list we are iterating over
            tracked_class, listtype = get_tracked_class(raw_coords_list[5], body_2D_pose[5], left_hand_2D_pose[5], right_hand_2D_pose[5])
            
            #Iterate over each joint
            for joint in tracked_class:
                
                #Read 2D joint position
                position = raw_coords_list[joint.value][framenum]
                
                #Filter out invalid points
                arm_coords, lost_track = filter_out_invalid(position, confidence_threshold)
                
                if lost_track == False:
                    
                    #find x and y in pixel (not normalised pixel) position in the 2D image
                    x = int(position[0]*1920)
                    y = int(position[1]*1080)
                    
                    #Find 3D position of each pixel using Colour_to_camera method
                    x_3D = csps1[y*1920 + x].x
                    y_3D = csps1[y*1920 + x].y
                    z_3D = csps1[y*1920 + x].z

                    #find joint position in the robot arm coordinate frame
                    arm_coords  = convert_to_arm_coords(x_3D, y_3D, z_3D)
                    
                    #Warning message if errors like what occur if no Kinect is connected to the computer are seen
                    if convert_to_am_coords_bad_count > 1000:
                        print("|||\\\___WARNING: Lots of bad arm coords being returned, are you sure kinect studio is running or a Kinect is connected?___///|||")
                        
                        #only print the above for every 1000 missed joints
                        convert_to_am_coords_bad_count = 0
                    
                    #Code for visualising where the tracked joints are in the depth image
                    if show_each_frame == True:
                        
                        display_joints(x,y, lost_track, color2depth_points, frame)

                if lost_track == True:
                    #Set arm coords to -1 to show that they are in error
                    arm_coords = [-1,-1,-1]
                
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

    #Load an example file
    body_3D_pose, left_hand_3D_pose, right_hand_3D_pose = get_arm_3D_coordinates('stationarytrial3.17.3.9.43', show_each_frame =  False)
    
    #Print some values from it
    print(body_3D_pose[BODY.RIGHT_ELBOW.value])
    
    #Convert the right palms trajectory into a form for 3D plotting
    x_sec= []
    y_sec= []
    z_sec = []
    
    for pos in right_hand_3D_pose[HAND.PALM.value]:

        if pos[3] ==False:
            x_sec.append(pos[0])
            y_sec.append(pos[1])
            z_sec.append(pos[2])
    
    #Plot the right palms trajectory in 3D
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x_sec, y_sec, z_sec)
    plt.show()


