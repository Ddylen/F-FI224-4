# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 16:58:09 2019

An old version of reader saved before signifcant changes were made
"""

# -*- coding: utf-8 -*-

import json
import glob
import matplotlib.pyplot as plt



def interpret2D():
    #path = 'outputs/*.json'
    path = 'referencevid/*.json'
    text_files = glob.glob(path)
    
    json_list = []
    wrist_list = []
    x_list = []
    y_list = []
    confidence_list = []
    

    for JSON in text_files:
        with open(JSON, "r") as json_data:
            json_list.append(json.load(json_data))
            
    #print(json_list[0])
    
    for json_dict in json_list:
        try:
            #print(json_list.index(json_dict))
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
        except:
            continue
        
    
        
    #print(type(json_list))
    #print(len(json_list))
    #print(x_list)
    return(x_list, y_list)
    
    #print(json_list)
    
    #plt.axis([0,1000,0,1000])
    #plt.scatter(x_list,y_list)
    #plt.plot(confidence_list)

interpret2D()