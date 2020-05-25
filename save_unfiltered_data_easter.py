# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 18:41:47 2020

@author: birl
"""

"""File to save the JSON data in vector format suitable for animation"""

import numpy as np
import time
from scipy import signal
import pickle
import sys
import math
from get_3D_pose import HAND, BODY, get_arm_3D_coordinates
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm



def get_plot_list(body_3D_pose, left_hand_3D_pose,right_hand_3D_pose):
    
    print("filter started")
    wrist_list = []
    #remove first fame as its always -1,-1, -1
    for pose_list in body_3D_pose, left_hand_3D_pose, right_hand_3D_pose:
        for sublist in pose_list:
            sublist[0] = sublist[1]
    
    print("filter finished")
    
    results_list = [ [] for i in range(len(body_3D_pose[0]))]
    

    for frame_num in range(len(body_3D_pose[0])):
        hand_pose = right_hand_3D_pose
        for joint in HAND:
            
            lost_track = False
            if joint == HAND.PALM:
                continue
            elif joint.value%4 == 1:
                

                
                x1 = hand_pose[joint.value][frame_num][0]
                x2 = hand_pose[HAND.PALM.value][frame_num][0]
                
                y1 = hand_pose[joint.value][frame_num][1]
                y2 = hand_pose[HAND.PALM.value][frame_num][1]
                
                z1 = hand_pose[joint.value][frame_num][2]
                z2 = hand_pose[HAND.PALM.value][frame_num][2]
                
                if hand_pose[joint.value][frame_num][3] == True or hand_pose[HAND.PALM.value][frame_num][3] == True:
                    lost_track = True

                results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2], lost_track])
                
            else:
                if joint ==HAND.THUMB_JOINT_1:
                    wrist_list.append(hand_pose[joint.value][frame_num])
                x1 = hand_pose[joint.value][frame_num][0]
                x2 = hand_pose[joint.value-1][frame_num][0]
                
                y1 = hand_pose[joint.value][frame_num][1]
                y2 = hand_pose[joint.value-1][frame_num][1]
                
                z1 = hand_pose[joint.value][frame_num][2]
                z2 = hand_pose[joint.value-1][frame_num][2]
                
                if hand_pose[joint.value][frame_num][3] == True or hand_pose[joint.value-1][frame_num][3] == True:
                    lost_track = True
                    
                results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2], lost_track])
        
        for joint in BODY:
            lost_track = False
            if joint.value < 9:
                if joint == BODY.HEAD or joint == BODY.RIGHT_SHOULDER:
                    x1 = body_3D_pose[joint.value][frame_num][0]
                    x2 = body_3D_pose[BODY.CHEST.value][frame_num][0]
                    
                    y1 = body_3D_pose[joint.value][frame_num][1]
                    y2 = body_3D_pose[BODY.CHEST.value][frame_num][1]
                    
                    z1 = body_3D_pose[joint.value][frame_num][2]
                    z2 = body_3D_pose[BODY.CHEST.value][frame_num][2]

                    if body_3D_pose[joint.value][frame_num][3] == True or body_3D_pose[BODY.CHEST.value][frame_num][3] == True:
                        lost_track = True
                    if joint != BODY.PELVIS:
                        results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2], lost_track])
                    else:
                        results_list[frame_num].append([[0,0], [0,0], [0,0], True])

                elif joint ==BODY.RIGHT_ELBOW or joint == BODY.RIGHT_WRIST:
                    x1 = body_3D_pose[joint.value][frame_num][0]
                    x2 = body_3D_pose[joint.value -1 ][frame_num][0]
                    
                    y1 = body_3D_pose[joint.value][frame_num][1]
                    y2 = body_3D_pose[joint.value -1 ][frame_num][1]
                    
                    z1 = body_3D_pose[joint.value][frame_num][2]
                    z2 = body_3D_pose[joint.value -1 ][frame_num][2]
                        
                    if body_3D_pose[joint.value][frame_num][3] == True:

                        lost_track = True
                    if body_3D_pose[joint.value -1 ][frame_num][3] == True:

                        lost_track = True

                    results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2], lost_track])
                    #if joint ==BODY.RIGHT_WRIST:
                        #wrist_list.append(body_3D_pose[joint.value][frame_num])
                    
         
    return results_list, wrist_list


old_time = time.time()

#file_name =  'mockcook.14.2.17.36'
#file_name = '1.24.21.47'
#file_name = "2.7.16.13"
#file_name = '1.24.22.0'
#file_name = '1.24.21.39'
#file_name = '1.24.21.47'
#file_name = '1.24.21.52'
#file_name = '1.24.22.0'
#file_name = '2.7.16.13'
#file_name = '2.7.16.27'

#file_name = 'stationarytrial1.17.3.9.38'   #36s, hand on oil botle cap, nothing beneath it (dot on wrist close to shirt)
#file_name = 'stationarytrial2.17.3.9.41'   #65s, hand on plate on salt tube (dot on shirt sleeve)
file_name = 'stationarytrial3.17.3.9.43'   #4s, very short, hand on salt shaker, dot on shirt
#file_name = 'stationaytrial4.17.3.9.43'    #38s, hand on salt sharker (dot on shirt)
#file_name = 'stationaytrial5.17.3.9.44'    #50s, hand on table (dot on shirt)


BODY3DPOSE, LEFTHAND3DPOSE,RIGHTHAND3DPOSE = get_arm_3D_coordinates(file_name, confidence_threshold = 0)

results_list, wrist_list = get_plot_list(BODY3DPOSE, LEFTHAND3DPOSE,RIGHTHAND3DPOSE)

"""
len_wrist_list = len(wrist_list)
x = np.arange(len_wrist_list)
ys = [i+x+(i*x)**2 for i in range(len_wrist_list)]

colors = cm.rainbow(np.linspace(0, 1, len(ys)))
i = 0

for val,c in zip (wrist_list, colors):
    #print(val)
    if i%10 ==0:
        ax.scatter(val[0], val[1], val[2], color = c)
    i = i+1
"""
    
datafile = open("bin/filtered_data/" + file_name + ".pickle", "wb")
pickle.dump(results_list, datafile)
wristdatafile = open("bin/filtered_data/wrist." + file_name + ".pickle", "wb")
pickle.dump(wrist_list, wristdatafile)

print("Time taken is", time.time()-old_time)

