"""OLD File to save the JSON data in vector format suitable for animation"""

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


def savgol_filter(body_3D_pose, left_hand_3D_pose,right_hand_3D_pose, threshold = 0.2):
     #print(range(len(body_3D_pose[0])))
     
     window_length, polyorder = 11, 2
     
     
     too_big_distance_list = []
     for hand_pose in right_hand_3D_pose, left_hand_3D_pose:
         for joint in HAND:
             #print(list(zip(*hand_pose[joint.value])), window_length, polyorder)
             #try:
             x_filtered = signal.savgol_filter(list(zip(*hand_pose[joint.value]))[0], window_length, polyorder)
             y_filtered = signal.savgol_filter(list(zip(*hand_pose[joint.value]))[1], window_length, polyorder)
             z_filtered = signal.savgol_filter(list(zip(*hand_pose[joint.value]))[2], window_length, polyorder)
             lost_track_list = list(zip(*hand_pose[joint.value]))[3]
             smoothed_list = [list(elem) for elem in list(zip(x_filtered,y_filtered,z_filtered, lost_track_list))]
             #print(smoothed_list[0])
             hand_pose[joint.value] = smoothed_list
             #except np.linalg.LinAlgError:
                 #print("Linalg error rasied")
                 #print(joint)
                 #print(hand_pose[joint.value][0][0])
                 #print(type(hand_pose[joint.value][0][0]))
                 #print(math.isnan(hand_pose[joint.value][0][0]))
                 #print(hand_pose[joint.value])

             
     for joint in BODY:
         #try:
         x_filtered = signal.savgol_filter(list(zip(*body_3D_pose[joint.value]))[0], window_length, polyorder)
         y_filtered = signal.savgol_filter(list(zip(*body_3D_pose[joint.value]))[1], window_length, polyorder)
         z_filtered = signal.savgol_filter(list(zip(*body_3D_pose[joint.value]))[2], window_length, polyorder)
         lost_track_list = list(zip(*body_3D_pose[joint.value]))[3]
         smoothed_list = [list(elem) for elem in list(zip(x_filtered,y_filtered,z_filtered, lost_track_list))]
         body_3D_pose[joint.value] = smoothed_list
         #except np.linalg.LinAlgError:
             #print("Linalg error rasied")
             #print(joint)
             #print(hand_pose[joint.value][0][0])
             #print(type(hand_pose[joint.value][0][0]))
             #print(math.isnan(hand_pose[joint.value][0][0]))
             #print(hand_pose[joint.value])
        
    
     print("Total number of filtered points is", len(too_big_distance_list))
     return body_3D_pose, left_hand_3D_pose,right_hand_3D_pose

def find_last_good_pose(pose_list, frame_num, original_frame_num):
    # pose_list is pose[joint.value][frame_num-1]

    if pose_list[frame_num-1][3] == False:
        returned_frame = frame_num-1
        found_a_good_point = True
        last_good_pose = pose_list[returned_frame]
    else:
        if frame_num == 0:
            #print("Found no good past points")
            last_good_pose = pose_list[original_frame_num]
            found_a_good_point = False
            returned_frame = original_frame_num
            return last_good_pose, returned_frame, found_a_good_point
        else:

            last_good_pose, returned_frame, found_a_good_point = find_last_good_pose(pose_list, frame_num -1, original_frame_num)
    return last_good_pose, returned_frame, found_a_good_point
    
    
def filter_out_jumps(body_3D_pose, left_hand_3D_pose,right_hand_3D_pose, threshold = 0.1):
     count= 0
     tracked_joint = BODY.PELVIS
     right_wrist_list = []
     #print(range(len(body_3D_pose[0])))
     too_big_distance_list = []
     for frame_num in range(len(body_3D_pose[0])):
        if frame_num%100 == 0:
             print("Filtering frame", frame_num)
        for hand_pose in right_hand_3D_pose, left_hand_3D_pose:
            if hand_pose == right_hand_3D_pose:
                hand = "RIGHT"
            if hand_pose == left_hand_3D_pose:
                hand = "LEFT"
            for joint in HAND:
                if frame_num != 0:
                    if hand == "RIGHT":
                        hand_pose[joint.value][frame_num][0] = hand_pose[joint.value][frame_num][0]
                        hand_pose[joint.value][frame_num][1] = hand_pose[joint.value][frame_num][1]
                        hand_pose[joint.value][frame_num][2] = hand_pose[joint.value][frame_num][2]
                        if  body_3D_pose[BODY.RIGHT_WRIST.value][frame_num][3] ==True:
                            hand_pose[joint.value][frame_num][3] = True
                    if hand == "LEFT":
                        hand_pose[joint.value][frame_num][0] = hand_pose[joint.value][frame_num][0]
                        hand_pose[joint.value][frame_num][1] = hand_pose[joint.value][frame_num][1]
                        hand_pose[joint.value][frame_num][2] = hand_pose[joint.value][frame_num][2]
                        if  body_3D_pose[BODY.LEFT_WRIST.value][frame_num][3] ==True:
                            hand_pose[joint.value][frame_num][3] = True
                        
                    last_good_hand_pose, returned_frame, found_a_good_point = find_last_good_pose(hand_pose[joint.value], frame_num, frame_num)
                    move_distance = np.sqrt((hand_pose[joint.value][frame_num][0] - last_good_hand_pose[0])**2+(hand_pose[joint.value][frame_num][1]-last_good_hand_pose[1])**2 + (hand_pose[joint.value][frame_num][2]-last_good_hand_pose[2])**2)
                    if move_distance > threshold:
                        hand_pose[joint.value][frame_num] = [last_good_hand_pose[0],last_good_hand_pose[1], last_good_hand_pose[2], True]
                        #hand_pose[joint.value][frame_num] = last_good_hand_pose
                        #hand_pose[joint.value][frame_num][3] = True
                        
                        too_big_distance_list.append(move_distance)
                        #print("hand fired ", count)
                        count  +=1
                    

                    
    
        for joint in BODY:
            if frame_num != 0:
                #print(body_3D_pose)
                last_good_body_pose, returned_frame, found_a_good_point = find_last_good_pose(body_3D_pose[joint.value], frame_num, frame_num) 
                move_distance = np.sqrt((body_3D_pose[joint.value][frame_num][0] - last_good_body_pose[0])**2+(body_3D_pose[joint.value][frame_num][1]-last_good_body_pose[1])**2 + (body_3D_pose[joint.value][frame_num][2]-last_good_body_pose[2])**2)
                if joint == tracked_joint:
                    if frame_num ==8 or frame_num == 7 or frame_num == 4  or frame_num == 5:
                        last_good_body_pose, returned_frame, found_a_good_point = find_last_good_pose(body_3D_pose[joint.value], frame_num, frame_num
                                                                                                      ) 
                        move_distance = np.sqrt((body_3D_pose[joint.value][frame_num][0] - last_good_body_pose[0])**2+(body_3D_pose[joint.value][frame_num][1]-last_good_body_pose[1])**2 + (body_3D_pose[joint.value][frame_num][2]-last_good_body_pose[2])**2)
                    #print(frame_num, last_good_body_pose, move_distance)
                    #print(body_3D_pose[joint.value][frame_num])
                if move_distance >= threshold:
                    #if frame_num < 10 and joint == tracked_joint:
                        #print("threshold exceeded on", frame_num)
                    body_3D_pose[joint.value][frame_num] = [last_good_body_pose[0],last_good_body_pose[1], last_good_body_pose[2], True]
                    
                    
                    #body_3D_pose[joint.value][frame_num-1][3] = True
                    too_big_distance_list.append(move_distance)
                    #print("body fired ", count)
                    count +=1 
                    #print(joint)
                #if joint == tracked_joint:
                    #right_wrist_list.append([[frame_num, move_distance, body_3D_pose[joint.value][returned_frame][0],body_3D_pose[joint.value][returned_frame][1], body_3D_pose[joint.value][returned_frame][2] ]])
                    #print(body_3D_pose[joint.value][frame_num])
                right_wrist_list.append([[move_distance,frame_num, body_3D_pose[joint.value][returned_frame][3],body_3D_pose[joint.value-1][returned_frame][3]]])
    
     #print(sorted(too_big_distance_list))
     print("Total number of filtered out points is", len(too_big_distance_list))
     #print(body_3D_pose)
     return body_3D_pose, left_hand_3D_pose,right_hand_3D_pose
    
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

file_name =  'mockcook.14.2.17.36'
#file_name = '1.24.21.47'
#file_name = "2.7.16.13"
#file_name = '1.24.22.0'
#file_name = '1.24.21.39'
#file_name = '1.24.21.47'
#file_name = '1.24.21.52'
#file_name = '1.24.22.0'
#file_name = '2.7.16.13'
#file_name = '2.7.16.27'


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

