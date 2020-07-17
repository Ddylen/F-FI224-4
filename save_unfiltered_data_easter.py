"""
Code to save the unfiltered raw pose trajectory from huamn recordings in a format suitable for the animation code
This file ignores the left half of the body as the noise from it can obscure the more important events with the right side of the body
"""
import numpy as np
import time
from scipy import signal
import pickle
import sys
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm

from get_3D_pose import HAND, BODY, get_arm_3D_coordinates


def get_unfiltered_data(body_3D_pose, left_hand_3D_pose,right_hand_3D_pose):
    """Code to save the unfiltered raw pose trajectory from huamn recordings in a format suitable for the animation code
    This file ignores the left half of the body as the noise from it can obscure the more important events with the right side of the body"""
    
    #remove first frame as its always -1,-1, -1
    for pose_list in body_3D_pose, left_hand_3D_pose, right_hand_3D_pose:
        for sublist in pose_list:
            sublist[0] = sublist[1]
    
    #Create empty list of lists to store our data in
    results_list = [ [] for i in range(len(body_3D_pose[0]))]
    
    #Create a seperate list for the position of the right wrist, which is used in standard deviation analysis later
    wrist_list = []
    
    #Iterate over each frame
    for frame_num in range(len(body_3D_pose[0])):
        
        #only consider right hand
        for hand_pose in [right_hand_3D_pose]:
            
            #iterate over each hand joint
            for joint in HAND:
                
                #Intialise a vairable to keep track if points are good are not
                lost_track = False
                
                #If you are looking at the right hand palm, explictly record that seperately
                if joint == HAND.PALM:
                    if hand_pose == right_hand_3D_pose:
                        wrist_list.append(hand_pose[joint.value][frame_num])
                
                #For all tracked points that branch of the palm in the skeleton provided by OpenPose
                elif joint.value%4 == 1:
                    
                    #Record the position of the tracked point and the palm
                    x1 = hand_pose[joint.value][frame_num][0]
                    x2 = hand_pose[HAND.PALM.value][frame_num][0]
                    
                    y1 = hand_pose[joint.value][frame_num][1]
                    y2 = hand_pose[HAND.PALM.value][frame_num][1]
                    
                    z1 = hand_pose[joint.value][frame_num][2]
                    z2 = hand_pose[HAND.PALM.value][frame_num][2]
                    
                    #Record if both tracked point and palm are believed to be valid points
                    if hand_pose[joint.value][frame_num][3] == True or hand_pose[HAND.PALM.value][frame_num][3] == True:
                        lost_track = True
                    
                    #Save a line between the tracked point and the palm to be animated
                    results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2], lost_track])
                    
                #for all parts of the hand skeleton that dont branch of the palm
                else:
                    
                    #record the tracked point, and the tracked point next to it that preceeds it in the tracked point ordering provided by OpenPose
                    x1 = hand_pose[joint.value][frame_num][0]
                    x2 = hand_pose[joint.value-1][frame_num][0]
                    
                    y1 = hand_pose[joint.value][frame_num][1]
                    y2 = hand_pose[joint.value-1][frame_num][1]
                    
                    z1 = hand_pose[joint.value][frame_num][2]
                    z2 = hand_pose[joint.value-1][frame_num][2]
                    
                    #Record if both tracked points are believed to be valid points
                    if hand_pose[joint.value][frame_num][3] == True or hand_pose[joint.value-1][frame_num][3] == True:
                        lost_track = True
                    
                    #Save a line between the two tracked points to be animated
                    results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2], lost_track])
        
        #iterate over each point in the body
        for joint in BODY:
            
            #Intialise a vairable to keep track if points are good are not
            lost_track = False
            
            #Iterate over all body tracked points above and including the knees
            if joint.value < 9:
                
                if joint == BODY.HEAD or joint == BODY.RIGHT_SHOULDER:
                    
                    #Get positions of head/right shoulder and chest
                    x1 = body_3D_pose[joint.value][frame_num][0]
                    x2 = body_3D_pose[BODY.CHEST.value][frame_num][0]
                    
                    y1 = body_3D_pose[joint.value][frame_num][1]
                    y2 = body_3D_pose[BODY.CHEST.value][frame_num][1]
                    
                    z1 = body_3D_pose[joint.value][frame_num][2]
                    z2 = body_3D_pose[BODY.CHEST.value][frame_num][2]
                    
                    #If either of the chest and the joint above are invalid, mark the line as invalid
                    if body_3D_pose[joint.value][frame_num][3] == True or body_3D_pose[BODY.CHEST.value][frame_num][3] == True:
                        lost_track = True
                    
                    #Save a line between the head/ right shoulder and the chest
                    results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2], lost_track])

                elif joint ==BODY.RIGHT_ELBOW or joint == BODY.RIGHT_WRIST:
                    
                    #Get positions of the elbow/ wrist and the wrist/shoulder
                    x1 = body_3D_pose[joint.value][frame_num][0]
                    x2 = body_3D_pose[joint.value -1 ][frame_num][0]
                    
                    y1 = body_3D_pose[joint.value][frame_num][1]
                    y2 = body_3D_pose[joint.value -1 ][frame_num][1]
                    
                    z1 = body_3D_pose[joint.value][frame_num][2]
                    z2 = body_3D_pose[joint.value -1 ][frame_num][2]
                        
                    #If either of the positions above are invalid, mark the line as invalid
                    if body_3D_pose[joint.value][frame_num][3] == True:
                        lost_track = True
                    if body_3D_pose[joint.value -1 ][frame_num][3] == True:
                        lost_track = True
                    
                    #Save a line between the elbow/ wrist and the wrist/shoulder
                    results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2], lost_track])
             
    return results_list, wrist_list


if __name__ == '__main__': 
    
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
    #file_name = 'stationarytrial3.17.3.9.43'   #4s, very short, hand on salt shaker, dot on shirt
    #file_name = 'stationaytrial4.17.3.9.43'    #38s, hand on salt sharker (dot on shirt)
    #file_name = 'stationaytrial5.17.3.9.44'    #50s, hand on table (dot on shirt)
    
    file_name = 'trial1dylan.12.3.16.31'
    
    #Get trajectory in arm coordinates
    BODY3DPOSE, LEFTHAND3DPOSE,RIGHTHAND3DPOSE = get_arm_3D_coordinates(file_name, confidence_threshold = 0)
    
    #Get unfiltered trajectory
    results_list, wrist_list = get_unfiltered_data(BODY3DPOSE, LEFTHAND3DPOSE,RIGHTHAND3DPOSE)
    
    #Save unfiltered data 
    datafile = open("bin/filtered_data/" + file_name + ".pickle", "wb")
    pickle.dump(results_list, datafile)
    
    #Save unfiltered wrist data
    wristdatafile = open("bin/filtered_data/wrist." + file_name + ".pickle", "wb")
    pickle.dump(wrist_list, wristdatafile)
    
    print("Time taken is", time.time()-old_time)
    
