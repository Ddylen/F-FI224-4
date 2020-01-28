"""
Extract lists of points from the folder full of JSON files, DEPRECIATED
"""

import json
import glob
import numpy as np

import matplotlib.pyplot as plt

import os
parentDirectory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
from enum import Enum

def interpret2D(folder, mode):
    #path = 'outputs/*.json'
    path = 'JSON/' + folder + '/*.json'
    text_files = glob.glob(path)
    json_list = []
    wrist_list = []
    x_list = []
    y_list = []
    confidence_list = []
    
    #print(text_files)
    for JSON in text_files:
        with open(JSON, "r") as json_data:
            json_list.append(json.load(json_data))
    
    #print(json_list[])
    if (mode == 'wrist'):
        for json_dict in json_list:
            try:
                #print(json_list.index(json_dict))
                if (json_dict['people'][0].get('pose_keypoints_2d')[12] != 0) and (json_dict['people'][0].get('pose_keypoints_2d')[13] != 0):
                    # initial filter to remove missing values which are returned as 0, 0, 0
                    #print("run")
                    x= json_dict['people'][0].get('pose_keypoints_2d')[12]
                    y= json_dict['people'][0].get('pose_keypoints_2d')[13]
                    c= json_dict['people'][0].get('pose_keypoints_2d')[14]
                    
                    wrist_list.append((x, y, c))
                    x_list.append(x)
                    y_list.append(y)
                    confidence_list.append(c)
                #json_dict['people'] removes the other useless category version
                #json_dict['people'][0] removes a useless single entry list which wraps the resired dict
                #json_dict['people'][0].get('pose_keypoints_2d') returns a list of all pose readings
                #pose readings are in a list of the form x1,y1,confidence1 etc
            except:
                continue
            
        return(wrist_list)
            
    if (mode == 'hand'):
        thumb_list = []
        index_joint2_list = []
        thumb_joint1_list = []
        palm_list = []
        closed_list = [0]
        for json_dict in json_list:
            try:
                if (json_dict['people'][0].get('hand_right_keypoints_2d')[0] != 0) and (json_dict['people'][0].get('hand_right_keypoints_2d')[1] != 0):
                    # dont store values where you cant see the hand
                    palm_list.append((json_dict['people'][0].get('hand_right_keypoints_2d')[0],json_dict['people'][0].get('hand_right_keypoints_2d')[1], json_dict['people'][0].get('hand_right_keypoints_2d')[2]))
                    thumb_list.append((json_dict['people'][0].get('hand_right_keypoints_2d')[12],json_dict['people'][0].get('hand_right_keypoints_2d')[13], json_dict['people'][0].get('hand_right_keypoints_2d')[14]))
                    index_joint2_list.append((json_dict['people'][0].get('hand_right_keypoints_2d')[18],json_dict['people'][0].get('hand_right_keypoints_2d')[19], json_dict['people'][0].get('hand_right_keypoints_2d')[19]))
                    thumb_joint1_list.append((json_dict['people'][0].get('hand_right_keypoints_2d')[6],json_dict['people'][0].get('hand_right_keypoints_2d')[7], json_dict['people'][0].get('hand_right_keypoints_2d')[8]))
                    
            
            
                #print("thumb is", thumb_list[-1], "joint is ", index_joint2_list[-1])
                    grasp_dis = np.sqrt( (thumb_list[-1][0]- index_joint2_list[-1][0])**2 + (thumb_list[-1][1]- index_joint2_list[-1][1])**2)
                    thumb_length = np.sqrt( (thumb_list[-1][0]- thumb_joint1_list[-1][0])**2 + (thumb_list[-1][1]- thumb_joint1_list[-1][1])**2)
                    
                    if(grasp_dis < thumb_length/3): #to make determination invariant of distance
                        closed_list.append(1)
                    else:
                        closed_list.append(0)
                    
            except(IndexError):
                print("Cant see hand")
    
            except(TypeError):
                print("stored value is not an int")
            #print(palm_list)
        return palm_list, closed_list, index_joint2_list
        
def raw_interpret2D(folder, mode):
    #path = 'outputs/*.json'
    path = 'bin/JSON/' + folder + '/*.json'
    text_files = glob.glob(path)
    json_list = []
    wrist_list = []
    elbow_list = []
    x_list = []
    y_list = []
    confidence_list = []
    
    #print(text_files)
    for JSON in text_files:
        with open(JSON, "r") as json_data:
            json_list.append(json.load(json_data))
    
    #print(json_list[])
    if (mode == 'wrist'):
        for json_dict in json_list:
            try:
                #print(json_list.index(json_dict))
                if (json_dict['people'][0].get('pose_keypoints_2d')[21] != 0) and (json_dict['people'][0].get('pose_keypoints_2d')[22] != 0):
                    # initial filter to remove missing values which are returned as 0, 0, 0
                    #print("run")
                    x= json_dict['people'][0].get('pose_keypoints_2d')[21]
                    y= json_dict['people'][0].get('pose_keypoints_2d')[22]
                    c= json_dict['people'][0].get('pose_keypoints_2d')[23]
                    
                    elbow_list.append((json_dict['people'][0].get('pose_keypoints_2d')[9], json_dict['people'][0].get('pose_keypoints_2d')[10], json_dict['people'][0].get('pose_keypoints_2d')[11]))
                    wrist_list.append((x, y, c))
                    x_list.append(x)
                    y_list.append(y)
                    confidence_list.append(c)
                else:
                    wrist_list.append((0, 0, 0))
                    x_list.append(0)
                    y_list.append(o)
                    confidence_list.append(c)
                #json_dict['people'] removes the other useless category version
                #json_dict['people'][0] removes a useless single entry list which wraps the resired dict
                #json_dict['people'][0].get('pose_keypoints_2d') returns a list of all pose readings
                #pose readings are in a list of the form x1,y1,confidence1 etc
            except:
                continue
            
        return(elbow_list, wrist_list)
            
    if (mode == 'hand'):
        thumb_list = []
        index_joint2_list = []
        thumb_joint1_list = []
        palm_list = []
        index_end_list =[]
        closed_list = [0]
        for json_dict in json_list:
            try:
                if (json_dict['people'][0].get('hand_right_keypoints_2d')[0] != 0) and (json_dict['people'][0].get('hand_right_keypoints_2d')[1] != 0):
                    # dont store values where you cant see the hand
                    palm_list.append((json_dict['people'][0].get('hand_right_keypoints_2d')[0],json_dict['people'][0].get('hand_right_keypoints_2d')[1], json_dict['people'][0].get('hand_right_keypoints_2d')[2]))
                    thumb_list.append((json_dict['people'][0].get('hand_right_keypoints_2d')[12],json_dict['people'][0].get('hand_right_keypoints_2d')[13], json_dict['people'][0].get('hand_right_keypoints_2d')[14]))
                    index_joint2_list.append((json_dict['people'][0].get('hand_right_keypoints_2d')[18],json_dict['people'][0].get('hand_right_keypoints_2d')[19], json_dict['people'][0].get('hand_right_keypoints_2d')[19]))
                    thumb_joint1_list.append((json_dict['people'][0].get('hand_right_keypoints_2d')[6],json_dict['people'][0].get('hand_right_keypoints_2d')[7], json_dict['people'][0].get('hand_right_keypoints_2d')[8]))
                    index_end_list.append((json_dict['people'][0].get('hand_right_keypoints_2d')[24],json_dict['people'][0].get('hand_right_keypoints_2d')[25], json_dict['people'][0].get('hand_right_keypoints_2d')[26]))
            
            
                #print("thumb is", thumb_list[-1], "joint is ", index_joint2_list[-1])
                    grasp_dis = np.sqrt( (thumb_list[-1][0]- index_joint2_list[-1][0])**2 + (thumb_list[-1][1]- index_joint2_list[-1][1])**2)
                    thumb_length = np.sqrt( (thumb_list[-1][0]- thumb_joint1_list[-1][0])**2 + (thumb_list[-1][1]- thumb_joint1_list[-1][1])**2)
                    
                    if(grasp_dis < thumb_length/3): #to make determination invariant of distance
                        closed_list.append(1)
                    else:
                        closed_list.append(0)
                    
            except(IndexError):
                print("Cant see hand")
    
            except(TypeError):
                print("stored value is not an int")
            #print(palm_list)
        return palm_list, thumb_list, index_end_list


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
    LEFT_ARM = 2
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
    
    #define list of empty lists to store the joint locations in (in normalised pixel coordinates) 
    left_hand_2D_pose = [ [] for i in range(hand_tracked_joints_num)]
    right_hand_2D_pose = [ [] for i in range(hand_tracked_joints_num)]
    body_2D_pose = [ [] for i in range(body_tracked_joints_num)]
    
    #Iteraively store joint positions in appropriate lists, if there is an error append x= -1, y = -1, confidence = -1 to the list
    for json_dict in json_list:
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
        
    return body_2D_pose, left_hand_2D_pose, right_hand_2D_pose
   
    
if __name__ == "__main__":    
    #import numpy as np
    #palmpoints, closedpoints = interpret2D('vid0611HAND', 'hand')
    
    #xL, yL, cL = zip(*palmpoints)
    #print(xL)
    #plt.axis([0,1000,0,1000])
    #plt.scatter(xL, yL)
    
    track_body("1.24.22.0")