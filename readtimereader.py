# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 13:33:32 2019

Code to return wrist exerts from the saved JSON files in real time
"""

# -*- coding: utf-8 -*-

import json
import glob
import matplotlib.pyplot as plt
import time


def interpret2D():
    path = 'outputdemo/*.json'
    text_files = glob.glob(path)
    
    json_list = []
    wrist_list = []
    x_list = [0]
    y_list = [0]
    confidence_list = []
    

    JSON = text_files[-1]
    with open(JSON, "r") as json_data:
        json_list.append(json.load(json_data))
            
    #print(json_list[0])
    
    
    try:
        for json_dict in json_list:
            if (json_dict['people'][0].get('pose_keypoints_2d')[12] != 0) and (json_dict['people'][0].get('pose_keypoints_2d')[13] != 0) and (json_dict['people'][0].get('pose_keypoints_2d')[14] > 0.1 ):
                # initial filter to remove missing values which are returned as 0, 0, 0
                wrist_list.append(json_dict['people'][0].get('pose_keypoints_2d')[12:15])
                x_list.append(json_dict['people'][0].get('pose_keypoints_2d')[12])
                y_list.append(json_dict['people'][0].get('pose_keypoints_2d')[13])
                confidence_list.append(json_dict['people'][0].get('pose_keypoints_2d')[14])
            #json_dict['people'] removes the other useless category version
            #json_dict['people'][0] removes a useless single entry list which wraps the resired dict
            #json_dict['people'][0].get('pose_keypoints_2d') returns a list of all pose readings
            #pose readings are in a list of the form x1,y1,confidence1 etc
            print(x_list[-1], y_list[-1])
    except(IndexError):
        print("Cant see hand")
    
        
    
        
    #print(type(json_list))
    #print(len(json_list))
    #print(x_list)
    
    
    #print(json_list)
    
    #plt.axis([0,1000,0,1000])
    #plt.scatter(x_list,y_list)
    #plt.plot(confidence_list)

while(True):
    interpret2D()
    time.sleep(1)