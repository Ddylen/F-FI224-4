# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 13:42:25 2019

Code to return hand exerts from the saved JSON files in real time
"""

# -*- coding: utf-8 -*-

import json
import glob
import matplotlib.pyplot as plt
import time
import numpy as np


def interpret2D():
    path = 'toutputs/*.json'
    text_files = glob.glob(path)
    
    json_list = []
    thumb_list = [("start", "start", "start")]
    index_joint2_list = [("start", "start", "start")]
    thumb_joint1_list = [("start", "start", "start")]
    palm_list = [("start", "start", "start")]
    closed_list = [0]

    JSON = text_files[-1]
    with open(JSON, "r") as json_data:
        json_list.append(json.load(json_data))
            
    #print(json_list[0])
    
    
    try:
        for json_dict in json_list:
            
            if (json_dict['people'][0].get('hand_right_keypoints_2d')[0] != 0) and (json_dict['people'][0].get('hand_right_keypoints_2d')[1] != 0):
                # dont store values where you cant see the hand
                palm_list.append((json_dict['people'][0].get('hand_right_keypoints_2d')[0],json_dict['people'][0].get('hand_right_keypoints_2d')[1], json_dict['people'][0].get('hand_right_keypoints_2d')[2]))
                thumb_list.append((json_dict['people'][0].get('hand_right_keypoints_2d')[12],json_dict['people'][0].get('hand_right_keypoints_2d')[13], json_dict['people'][0].get('hand_right_keypoints_2d')[14]))
                index_joint2_list.append((json_dict['people'][0].get('hand_right_keypoints_2d')[18],json_dict['people'][0].get('hand_right_keypoints_2d')[19], json_dict['people'][0].get('hand_right_keypoints_2d')[19]))
                thumb_joint1_list.append((json_dict['people'][0].get('hand_right_keypoints_2d')[6],json_dict['people'][0].get('hand_right_keypoints_2d')[7], json_dict['people'][0].get('hand_right_keypoints_2d')[8]))
            #json_dict['people'] removes the other useless category version
            #json_dict['people'][0] removes a useless single entry list which wraps the resired dict
            #json_dict['people'][0].get('pose_keypoints_2d') returns a list of all pose readings
            #pose readings are in a list of the form x1,y1,confidence1 etc
            
            
                #print("thumb is", thumb_list[-1], "joint is ", index_joint2_list[-1])
                grasp_dis = np.sqrt( (thumb_list[-1][0]- index_joint2_list[-1][0])**2 + (thumb_list[-1][1]- index_joint2_list[-1][1])**2)
                thumb_length = np.sqrt( (thumb_list[-1][0]- thumb_joint1_list[-1][0])**2 + (thumb_list[-1][1]- thumb_joint1_list[-1][1])**2)
                print(grasp_dis/thumb_length)
                if(grasp_dis < thumb_length/3): #to make determination invariant of distance
                    print("Hand closed")
                    closed_list.append(1)
                else:
                    closed_list.append(0)
    except(IndexError):
        print("Cant see hand")
    
    except(TypeError):
        print("stored value is not an int")
    
    print(palm_list[-1], closed_list[-1])
    return palm_list, closed_list
        
    
        
    #print(type(json_list))
    #print(len(json_list))
    #print(x_list)
    
    
    #print(json_list)
    
    #plt.axis([0,1000,0,1000])
    #plt.scatter(x_list,y_list)
    #plt.plot(confidence_list)

while(True):
    a,b = interpret2D()
    #print(a)
    #print(b)
    time.sleep(1)