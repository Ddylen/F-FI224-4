"""old code to save filtered data in a format suitabel for animation"""

import numpy as np
import time
from scipy import signal
import pickle
import sys
import math
from get_3D_pose import HAND, BODY, get_arm_3D_coordinates

"""TODO:
    *error could be memoery or could nbe infs/nans, try a memory based fix or inf/ nan based fixe still doesnt work
    """

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
                        hand_pose[joint.value][frame_num][0] = hand_pose[joint.value][frame_num][0] - body_3D_pose[BODY.RIGHT_WRIST.value][frame_num][0]
                        hand_pose[joint.value][frame_num][1] = hand_pose[joint.value][frame_num][1] - body_3D_pose[BODY.RIGHT_WRIST.value][frame_num][1]
                        hand_pose[joint.value][frame_num][2] = hand_pose[joint.value][frame_num][2] - body_3D_pose[BODY.RIGHT_WRIST.value][frame_num][2]
                        if  body_3D_pose[BODY.RIGHT_WRIST.value][frame_num][3] ==True:
                            hand_pose[joint.value][frame_num][3] = True
                    if hand == "LEFT":
                        hand_pose[joint.value][frame_num][0] = hand_pose[joint.value][frame_num][0] - body_3D_pose[BODY.LEFT_WRIST.value][frame_num][0]
                        hand_pose[joint.value][frame_num][1] = hand_pose[joint.value][frame_num][1] - body_3D_pose[BODY.LEFT_WRIST.value][frame_num][1]
                        hand_pose[joint.value][frame_num][2] = hand_pose[joint.value][frame_num][2] - body_3D_pose[BODY.LEFT_WRIST.value][frame_num][2]
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
    
    #remove first fame as its always -1,-1, -1
    for pose_list in body_3D_pose, left_hand_3D_pose, right_hand_3D_pose:
        for sublist in pose_list:
            sublist[0] = sublist[1]
    

    #print("LENGTH IS -----------------------------------------------", len(body_3D_pose[0]))
    #print(body_3D_pose[0])
    #for i in range(20):
        #print("new pose ",i,  body_3D_pose[i][0])
    #print("new pose 1", body_3D_pose[1])
    
    body_3D_pose, left_hand_3D_pose,right_hand_3D_pose = filter_out_jumps(body_3D_pose, left_hand_3D_pose,right_hand_3D_pose)
    
    #body_3D_pose, left_hand_3D_pose,right_hand_3D_pose = savgol_filter(body_3D_pose, left_hand_3D_pose,right_hand_3D_pose)

    #print(body_3D_pose)
    
    print("filter finished")
    
    results_list = [ [] for i in range(len(body_3D_pose[0]))]
    
    #print(body_3D_pose)
    
    for frame_num in range(len(body_3D_pose[0])):
        for hand_pose in right_hand_3D_pose, left_hand_3D_pose:
            #print(hand_pose)
            if hand_pose == right_hand_3D_pose:
                hand = "RIGHT"
            if hand_pose ==left_hand_3D_pose:
                hand = "LEFT"
            for joint in HAND:
                if hand == "RIGHT":
                    wrist_offset =  body_3D_pose[BODY.RIGHT_WRIST.value][frame_num]
                elif hand == "LEFT":
                    wrist_offset = body_3D_pose[BODY.LEFT_WRIST.value][frame_num]
                lost_track = False
                if joint == HAND.PALM:
                    continue
                elif joint.value%4 == 1:

                    
                    x1 = hand_pose[joint.value][frame_num][0] + wrist_offset[0]
                    x2 = hand_pose[HAND.PALM.value][frame_num][0] + wrist_offset[0]
                    
                    y1 = hand_pose[joint.value][frame_num][1] + wrist_offset[1]
                    y2 = hand_pose[HAND.PALM.value][frame_num][1] + wrist_offset[1]
                    
                    z1 = hand_pose[joint.value][frame_num][2] + wrist_offset[2]
                    z2 = hand_pose[HAND.PALM.value][frame_num][2]+wrist_offset[2]
                    
                    if hand_pose[joint.value][frame_num][3] == True or hand_pose[HAND.PALM.value][frame_num][3] == True or wrist_offset[3] ==True:
                        #print("LOST TRACK")
                        lost_track = True

                    results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2], lost_track])
                    #print(joint)
                    
                else:
                    x1 = hand_pose[joint.value][frame_num][0]+wrist_offset[0]
                    x2 = hand_pose[joint.value-1][frame_num][0]+wrist_offset[0]
                    
                    y1 = hand_pose[joint.value][frame_num][1]+wrist_offset[1]
                    y2 = hand_pose[joint.value-1][frame_num][1]+wrist_offset[1]
                    
                    z1 = hand_pose[joint.value][frame_num][2]+wrist_offset[2]
                    z2 = hand_pose[joint.value-1][frame_num][2]+wrist_offset[2]
                    
                    if hand_pose[joint.value][frame_num][3] == True or hand_pose[joint.value-1][frame_num][3] == True or wrist_offset[3] == True:
                        lost_track = True
                        
                    results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2], lost_track])
                    #print(joint)

        for joint in BODY:
            lost_track = False
            if joint.value < 9:
                if joint == BODY.HEAD or joint== BODY.LEFT_SHOULDER or joint == BODY.RIGHT_SHOULDER or joint == BODY.PELVIS:
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
                    #print(joint)
                else:
                    x1 = body_3D_pose[joint.value][frame_num][0]
                    x2 = body_3D_pose[joint.value -1 ][frame_num][0]
                    
                    y1 = body_3D_pose[joint.value][frame_num][1]
                    y2 = body_3D_pose[joint.value -1 ][frame_num][1]
                    
                    z1 = body_3D_pose[joint.value][frame_num][2]
                    z2 = body_3D_pose[joint.value -1 ][frame_num][2]
                    #if joint.value == 7:
                        #print("Looking at wrist")
                        
                    if body_3D_pose[joint.value][frame_num][3] == True:
                        #if joint.value == 7:
                            #print("case 1")
                        lost_track = True
                    if body_3D_pose[joint.value -1 ][frame_num][3] == True:
                        #if joint.value == 7:
                            #print("case 2")
                        lost_track = True
                    #if joint.value == 7:
                            #print(lost_track)
                    results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2], lost_track])
                    #print(joint)
                    
            elif joint == BODY.LEFT_EYE or joint == BODY.RIGHT_EYE:
                    x1 = body_3D_pose[joint.value][frame_num][0]
                    x2 = body_3D_pose[BODY.HEAD.value][frame_num][0]
                    
                    y1 = body_3D_pose[joint.value][frame_num][1]
                    y2 = body_3D_pose[BODY.HEAD.value][frame_num][1]
                    
                    z1 = body_3D_pose[joint.value][frame_num][2]
                    z2 = body_3D_pose[BODY.HEAD.value][frame_num][2]
                    
                    if body_3D_pose[joint.value][frame_num][3] == True or body_3D_pose[BODY.HEAD.value][frame_num][3] == True:
                        lost_track = True
                    
                        results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2], True])
                    else:
                        results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2], False])
                    #print(joint)
                    #print(results_list)
    #print(results_list)            
    return results_list



#print(len(results_list[5]))
#print(results_list[5])
sys.setrecursionlimit(10**6) # to stop a recursion error when looking back over 1000 places

old_time = time.time()

#file_name =  '1.23.17.49'
#file_name = '1.24.21.46'
#file_name = '1.24.22.0'
#file_name = '1.24.21.39'
#file_name = "mar.3.3.15.38"
#file_name = 'trial6dylan.16.3.9.50'
file_name = 'trial7thomas.16.3.10.24'
BODY3DPOSE, LEFTHAND3DPOSE,RIGHTHAND3DPOSE = get_arm_3D_coordinates(file_name, confidence_threshold = 0.05)
#BODY3DPOSE, LEFTHAND3DPOSE,RIGHTHAND3DPOSE = get_arm_3D_coordinates('1.24.21.39', confidence_threshold = 0)

results_list = get_plot_list(BODY3DPOSE, LEFTHAND3DPOSE,RIGHTHAND3DPOSE)

datafile = open("bin/filtered_data/" + file_name + ".pickle", "wb")
pickle.dump(results_list, datafile)

print("Time taken is", time.time()-old_time)

