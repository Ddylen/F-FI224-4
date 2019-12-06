"""
Extract lists of points from the folder full of JSON files
"""

import json
import glob
import numpy as np

import matplotlib.pyplot as plt

import os
parentDirectory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))


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
        


if __name__ == "__main__":    
    import numpy as np
    palmpoints, closedpoints = interpret2D('vid0611HAND', 'hand')
    
    xL, yL, cL = zip(*palmpoints)
    print(xL)
    #plt.axis([0,1000,0,1000])
    #plt.scatter(xL, yL)
