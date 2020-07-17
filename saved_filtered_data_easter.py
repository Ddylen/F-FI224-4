"""
Code to filter and save the raw pose trajectories extracted from recordings in a format suitable for the animation code
"""
import numpy as np
import time
from scipy import signal
import pickle
import sys
import math

from get_3D_pose import HAND, BODY, get_arm_3D_coordinates
from animated_saved_data import animate


def savgol_filter(body_3D_pose, left_hand_3D_pose,right_hand_3D_pose, threshold = 0.2):
    """Code to apply a savgol filter to the recorded body pose"""
     
    #Define properties of the savgol filter
    window_length, polyorder = 11, 2
    
    #iterate over the hands
    for hand_pose in right_hand_3D_pose, left_hand_3D_pose:
        
        #iterate over the joints in each hand
        for joint in HAND:

            #Apply savgol filter to x, y and z position lists of that joint seperately
            x_filtered = signal.savgol_filter(list(zip(*hand_pose[joint.value]))[0], window_length, polyorder)
            y_filtered = signal.savgol_filter(list(zip(*hand_pose[joint.value]))[1], window_length, polyorder)
            z_filtered = signal.savgol_filter(list(zip(*hand_pose[joint.value]))[2], window_length, polyorder)
            
            #Define a list of whether the point we have found is believed to be valid, for use in the step below
            lost_track_list = list(zip(*hand_pose[joint.value]))[3]
            
            #Define a list of (x,y,z) points using the filtered list above
            smoothed_list = [list(elem) for elem in list(zip(x_filtered,y_filtered,z_filtered, lost_track_list))]
            
            #Update the hand_pose list for that joint with the new smoothed list of said joint's positions
            hand_pose[joint.value] = smoothed_list
           
    
    #iterate over the body's joints         
    for joint in BODY:

        #Apply savgol filter to x, y and z position lists of that joint seperately
        x_filtered = signal.savgol_filter(list(zip(*body_3D_pose[joint.value]))[0], window_length, polyorder)
        y_filtered = signal.savgol_filter(list(zip(*body_3D_pose[joint.value]))[1], window_length, polyorder)
        z_filtered = signal.savgol_filter(list(zip(*body_3D_pose[joint.value]))[2], window_length, polyorder)
        
        #Define a list of whether the point we have found is believed to be valid, for use in the step below
        lost_track_list = list(zip(*body_3D_pose[joint.value]))[3]
        
        #Define a list of (x,y,z) points using the filtered list above
        smoothed_list = [list(elem) for elem in list(zip(x_filtered,y_filtered,z_filtered, lost_track_list))]
        
        #Update the hand_pose list for that joint with the new smoothed list of said joint's positions
        body_3D_pose[joint.value] = smoothed_list

    return body_3D_pose, left_hand_3D_pose,right_hand_3D_pose


def find_last_good_pose(pose_list, frame_num, original_frame_num):
    """Function to replace an invalid point with a previously seen valid point"""
    
    #if previous point is valid
    if pose_list[frame_num-1][3] == False:
        
        #replace current point with previous position
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
  
    
def check_out_of_bounds(position, xmin = -1.5, xmax = 1.5, ymin = -1.5, ymax = 1.5, zmin = -0.5, zmax = 1.5):
    """Function to check a point is in the volume we have defined as valid"""
    
    #Define variable if point is invalid
    out_of_bounds = position[3]
    
    #Check if position is within the allowable bounds
    if position[0] > xmax or position[0] <xmin:
        out_of_bounds = True
        
    if position[1] > ymax or position[1] <ymin:
        out_of_bounds = True
        
    if position[2] > zmax or position[2] <zmin:
        out_of_bounds = True
        
    #Return if point is now invalid
    return out_of_bounds

  
def filter_out_jumps(body_3D_pose, left_hand_3D_pose,right_hand_3D_pose, threshold = 0.1):
    """Function to filter out spikes and invalid points from the raw data"""
    
    #remove first frame as its always -1,-1, -1
    for pose_list in body_3D_pose, left_hand_3D_pose, right_hand_3D_pose:
        for sublist in pose_list:
            sublist[0] = sublist[1]
            
    #DEL - single out a joint for further analysis/ processing
    tracked_joint = BODY.PELVIS
    tracked_joint_list = []
    
    #DEL - define a list of moving averages for each joint
    movingav = [[0,0,0,0]]*len(body_3D_pose[0])
    movingav = [movingav]*len(right_hand_3D_pose)
    
    #Create lists of the last good points seen for each joint
    last_good_point_list_right =  [[0,0,0,False]]*len(right_hand_3D_pose)
    last_good_point_list_left =  [[0,0,0,False]]*len(left_hand_3D_pose)    
    last_good_point_list_body =  [[0,0,0,False]]*len(body_3D_pose)
    
    #set a flag if we should track on join individually for debugging purposes
    special_joint = HAND.INDEX_KNUCKLE
    special_hand = "RIGHT"
    track_special_joint = True
    
    #Iterating over each frame
    for frame_num in range(len(body_3D_pose[0])):
        
       #Print progress update messages 
       if frame_num%100 == 0:
            print("Filtering frame", frame_num)
       
       #For each pose
       for hand_pose in right_hand_3D_pose, left_hand_3D_pose:
           
           #Declare which hand we are operating on
           if hand_pose == right_hand_3D_pose:
               hand = "RIGHT"   
           if hand_pose == left_hand_3D_pose:
               hand = "LEFT"
           
           #Iterate over each joint in the hands
           for joint in HAND:
               
               #Exclude the first frame as its always void of information
               if frame_num != 0:
                       
                       #Set wrist joint value and the last good hand pose
                       if hand == "RIGHT":
                           wristval = BODY.RIGHT_WRIST.value
                           last_good_hand_pose= last_good_point_list_right[joint.value]
                           last_good_point_list_right[joint.value][3] = False
                       if hand == "LEFT":
                           wristval = BODY.LEFT_WRIST.value
                           last_good_hand_pose= last_good_point_list_left[joint.value]
                           last_good_point_list_right[joint.value][3] = False
                       
                       #If wrist position is bad also set hand joint position as bad (as hand joint values will be stored in a relative-to-wrist position format)
                       if  body_3D_pose[wristval][frame_num][3] == True:
                           hand_pose[joint.value][frame_num][3] = True
                           
                       #If hand position is out the the expected box say hand position is bad
                       if check_out_of_bounds(hand_pose[joint.value][frame_num]) == True:
                           hand_pose[joint.value][frame_num][3] = True
                           
                       #Define hand joint positions relative to the wrist
                       hand_pose[joint.value][frame_num][0] = hand_pose[joint.value][frame_num][0] - body_3D_pose[wristval][frame_num][0]
                       hand_pose[joint.value][frame_num][1] = hand_pose[joint.value][frame_num][1] - body_3D_pose[wristval][frame_num][1]
                       hand_pose[joint.value][frame_num][2] = hand_pose[joint.value][frame_num][2] - body_3D_pose[wristval][frame_num][2]
                      
                       #Define distance from last good position    
                       move_distance = np.sqrt((hand_pose[joint.value][frame_num][0] - hand_pose[joint.value][frame_num-1][0])**2+(hand_pose[joint.value][frame_num][1]-hand_pose[joint.value][frame_num-1][1])**2 + (hand_pose[joint.value][frame_num][2]-hand_pose[joint.value][frame_num-1][2])**2)
                       
                       #Define distance from the moving average
                       #av_distance = np.sqrt((hand_pose[joint.value][frame_num][0] - movingav[joint.value][frame_num][0])**2+(hand_pose[joint.value][frame_num][1]-movingav[joint.value][frame_num][1])**2 + (hand_pose[joint.value][frame_num][2]-movingav[joint.value][frame_num][2])**2)
                       
                       #Define distance from wrist
                       wrist_distance = np.sqrt((hand_pose[joint.value][frame_num][0])**2+(hand_pose[joint.value][frame_num][1])**2 + (hand_pose[joint.value][frame_num][2])**2)
                       
                       #Debugging statements
                       if track_special_joint == True and joint == special_joint and hand == special_hand:
                           #print("Current:  ", hand_pose[joint.value][frame_num])
                           #print("Last Good:", last_good_point_list_right[joint.value])
                           pass
                           
                       #If hand moves too far or hand position is too far from wrist, replace position with last measured good position
                       if move_distance > 0.2:
                           
                           #Set hand pose to last good hand pose
                           hand_pose[joint.value][frame_num] = last_good_hand_pose
                           
                           #Set that position was bad so it comes up in red in the animation
                           hand_pose[joint.value][frame_num][3] = True  
                           
                           #Debugging statements
                           if track_special_joint == True and joint == special_joint and hand == special_hand:
                               #print("Point Bad/ Move")
                               pass
                       
                       #If hand joint is too far from the wrist, mark is as bad and replace it with the last good position
                       if wrist_distance > 0.2:
                           
                           #Set hand pose to last good hand pose
                           hand_pose[joint.value][frame_num] = last_good_hand_pose
                           
                           #Set that position was bad so it comes up in red in the animation
                           hand_pose[joint.value][frame_num][3] = True

                           #Debugging statment
                           if track_special_joint == True and joint == special_joint and hand == special_hand:
                               #print("Point Bad/ Wrist")   
                               pass
                               
                       #Debugging statement
                       if track_special_joint == True and joint == special_joint and hand == special_hand:
                           #print("PoseAfter :  ", hand_pose[joint.value][frame_num])
                           pass
                           
                       #Debugging statement
                       if track_special_joint == True and joint == special_joint and hand == special_hand:
                           #print(hand_pose[joint.value][frame_num][3], hand_pose[joint.value][frame_num][3] == False )
                           pass
                       
                       #Update last good right hand pose 
                       if hand == "RIGHT":
                           
                           #If current joint is good
                           if hand_pose[joint.value][frame_num][3] == False:
                               
                               #Update last good point with the current point
                               last_good_point_list_right[joint.value] = hand_pose[joint.value][frame_num]
                               
                               #Debugging statement
                               if joint == HAND.INDEX_KNUCKLE and hand == "RIGHT":
                                   #print("Update fired", hand_pose[joint.value][frame_num])
                                   pass
                                   
                       #Update last good left hand pose        
                       if hand == "LEFT":
                           
                           #If current joint is good
                           if hand_pose[joint.value][frame_num][3] == False:
                               
                               #Update last good point with the current point
                               last_good_point_list_left[joint.value] = hand_pose[joint.value][frame_num]
                       
                        #Debugging statement
                       if joint == HAND.INDEX_KNUCKLE and hand == "RIGHT":        
                           #print("")
                           pass
                      
       #Iterate over each joint in the body
       for joint in BODY:
           
           #Excluding the first frame, which contains no information
           if frame_num != 0:

               #Find last good pose
               last_good_body_pose, returned_frame, found_a_good_point = find_last_good_pose(body_3D_pose[joint.value], frame_num, frame_num) 
               
               #Define distance from current pose to last good pose
               move_distance = np.sqrt((body_3D_pose[joint.value][frame_num][0] - last_good_body_pose[0])**2+(body_3D_pose[joint.value][frame_num][1]-last_good_body_pose[1])**2 + (body_3D_pose[joint.value][frame_num][2]-last_good_body_pose[2])**2)
               
               #Update current point with last good hand pose
               body_3D_pose[joint.value][frame_num] = last_good_body_pose
               
    return body_3D_pose, left_hand_3D_pose,right_hand_3D_pose
 
    
def get_plot_list(body_3D_pose, left_hand_3D_pose,right_hand_3D_pose):
    """Turn tracked points into a series of lines to animate"""
    
    print("filter started")
    

    
    
    
    print("filter finished")
    
    #Define empty list to fill with lines to animate
    results_list = [ [] for i in range(len(body_3D_pose[0]))]
    
    #Iterate over each frame
    for frame_num in range(len(body_3D_pose[0])):
        
        #Iterate over each hand
        for hand_pose in right_hand_3D_pose, left_hand_3D_pose:
            
            #Define which hand we are operating on data points from
            if hand_pose == right_hand_3D_pose:
                hand = "RIGHT"
            if hand_pose ==left_hand_3D_pose:
                hand = "LEFT"
                
            #Iterate over each joint in the hand
            for joint in HAND:
                
                #Define which wrrist position
                if hand == "RIGHT":
                    wrist_offset =  body_3D_pose[BODY.RIGHT_WRIST.value][frame_num]
                elif hand == "LEFT":
                    wrist_offset = body_3D_pose[BODY.LEFT_WRIST.value][frame_num]
                    
                #Initialise points as valid
                lost_track = False
                
                #Dont draw a line for the palm of the hand
                if joint == HAND.PALM:
                    continue
                
                #If joint connects to the palm:
                elif joint.value%4 == 1:
                    
                    #Define a line from the joint to the palm
                    x1 = hand_pose[joint.value][frame_num][0] + wrist_offset[0]
                    x2 = hand_pose[HAND.PALM.value][frame_num][0] + wrist_offset[0]
                    
                    y1 = hand_pose[joint.value][frame_num][1] + wrist_offset[1]
                    y2 = hand_pose[HAND.PALM.value][frame_num][1] + wrist_offset[1]
                    
                    z1 = hand_pose[joint.value][frame_num][2] + wrist_offset[2]
                    z2 = hand_pose[HAND.PALM.value][frame_num][2]+wrist_offset[2]
                    
                    #Define whether the line is valid, using whether both ends of the line, and the wrist, are valid
                    if hand_pose[joint.value][frame_num][3] == True or hand_pose[HAND.PALM.value][frame_num][3] == True or wrist_offset[3] ==True:
                        
                        lost_track = True
                    
                    #Append line to the results list
                    results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2], lost_track])
                
                #For other joints
                else:
                    
                    #Draw a line from the joint to the previous joint
                    x1 = hand_pose[joint.value][frame_num][0]+wrist_offset[0]
                    x2 = hand_pose[joint.value-1][frame_num][0]+wrist_offset[0]
                    
                    y1 = hand_pose[joint.value][frame_num][1]+wrist_offset[1]
                    y2 = hand_pose[joint.value-1][frame_num][1]+wrist_offset[1]
                    
                    z1 = hand_pose[joint.value][frame_num][2]+wrist_offset[2]
                    z2 = hand_pose[joint.value-1][frame_num][2]+wrist_offset[2]
                    
                    #Define whether the line is valid, using whether both ends of the line, and the wrist, are valid
                    if hand_pose[joint.value][frame_num][3] == True or hand_pose[joint.value-1][frame_num][3] == True or wrist_offset[3] == True:
                        lost_track = True
                    
                    #Append line to the results list
                    results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2], lost_track])
        
        #For each joint in the body
        for joint in BODY:
            
            #Initialise lost track
            lost_track = False
            
            #For joints above the legs, excluding the facial features
            if joint.value < 9:
                
                #For joints that connect to the chest
                if joint == BODY.HEAD or joint== BODY.LEFT_SHOULDER or joint == BODY.RIGHT_SHOULDER or joint == BODY.PELVIS:
                    
                    #Define points in a line between the joint and the chest
                    x1 = body_3D_pose[joint.value][frame_num][0]
                    x2 = body_3D_pose[BODY.CHEST.value][frame_num][0]
                    
                    y1 = body_3D_pose[joint.value][frame_num][1]
                    y2 = body_3D_pose[BODY.CHEST.value][frame_num][1]
                    
                    z1 = body_3D_pose[joint.value][frame_num][2]
                    z2 = body_3D_pose[BODY.CHEST.value][frame_num][2]
                    
                    #If either end of the line is invalid, define the line as invalid
                    if body_3D_pose[joint.value][frame_num][3] == True or body_3D_pose[BODY.CHEST.value][frame_num][3] == True:
                        lost_track = True
                    
                    #Append line to the results list to be animated
                    results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2], lost_track])

                #For the arms
                else:
                    
                    #Define joints betwwen the joint and the previous joint
                    x1 = body_3D_pose[joint.value][frame_num][0]
                    x2 = body_3D_pose[joint.value -1 ][frame_num][0]
                    
                    y1 = body_3D_pose[joint.value][frame_num][1]
                    y2 = body_3D_pose[joint.value -1 ][frame_num][1]
                    
                    z1 = body_3D_pose[joint.value][frame_num][2]
                    z2 = body_3D_pose[joint.value -1 ][frame_num][2]

                    #If joint or previous joint have invalid position, mark the line as invalid
                    if body_3D_pose[joint.value][frame_num][3] == True or body_3D_pose[joint.value -1 ][frame_num][3] == True:

                        lost_track = True
                    
                    #Append line to the results list
                    results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2], lost_track])

            #For the eye 'joints'        
            elif joint == BODY.LEFT_EYE or joint == BODY.RIGHT_EYE:
                
                    #Define joints betwwen the eye 'joint' and the head 'joint'
                    x1 = body_3D_pose[joint.value][frame_num][0]
                    x2 = body_3D_pose[BODY.HEAD.value][frame_num][0]
                    
                    y1 = body_3D_pose[joint.value][frame_num][1]
                    y2 = body_3D_pose[BODY.HEAD.value][frame_num][1]
                    
                    z1 = body_3D_pose[joint.value][frame_num][2]
                    z2 = body_3D_pose[BODY.HEAD.value][frame_num][2]
                    
                    #If either joints have invalid position
                    if body_3D_pose[joint.value][frame_num][3] == True or body_3D_pose[BODY.HEAD.value][frame_num][3] == True:
                        
                        #Update results list with the line, mark it as invalid
                        results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2], True])
                    
                    #If points are good
                    else:
                        
                        #Update results list with the line, mark it as valid
                        results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2], False])

    return results_list


def crop(listtocrop, length):
    """Function to crop a pose list to a certain length""" 
    
    array = np.array(listtocrop)
    array = array[:,0:length]
    output = array.tolist()
    
    return output

if __name__ == '__main__': 
    
    #Set a recursion limit to avoid recusion length errors on long lists
    sys.setrecursionlimit(10**6)
    
    #Start a timer
    old_time = time.time()
    
    #Defimne the relevant file name
    
    #file_name =  '1.23.17.49'
    #file_name = '1.24.21.46'
    #file_name = '1.24.22.0'
    #file_name = '1.24.21.39'
    #file_name = 'mockcook.14.2.17.36'
    #file_name = 'trial6dylan.16.3.9.50'
    file_name = 'trial7thomas.16.3.10.24'
    
    #Find if file has already been processed to extract the pose lists
    try:
        readfile = open("bin/points_data/" + file_name + ".pickle", "rb")
        BODY3DPOSE = pickle.load(readfile)
        LEFTHAND3DPOSE = pickle.load(readfile)
        RIGHTHAND3DPOSE = pickle.load(readfile)
    
    #If not, process the file to extract the pose lists
    except FileNotFoundError:
        BODY3DPOSE, LEFTHAND3DPOSE,RIGHTHAND3DPOSE = get_arm_3D_coordinates(file_name, confidence_threshold = 0.05)
        
        #Save the extracted poselists
        pointsfile = open("bin/points_data/" + file_name + ".pickle", "wb")
        pickle.dump(BODY3DPOSE, pointsfile)
        pickle.dump(LEFTHAND3DPOSE, pointsfile)    
        pickle.dump(RIGHTHAND3DPOSE, pointsfile)
    
        #Then extract the poselists from the saved file for consistency with the prior method
        readfile = open("bin/points_data/" + file_name + ".pickle", "rb")
        BODY3DPOSE = pickle.load(readfile)
        LEFTHAND3DPOSE = pickle.load(readfile)
        RIGHTHAND3DPOSE = pickle.load(readfile)
    
    #Define the length that we want to crop the recording to
    croplength = 2700
    
    #Define an additional string to give this filtered cropped recording a unique file name
    extrastring = '10'
    
    #Crop the pose lists    
    body_3D_pose_cropped = crop(BODY3DPOSE, croplength)
    left_hand_3D_pose_cropped = crop(LEFTHAND3DPOSE, croplength)
    right_hand_3D_pose_cropped = crop(RIGHTHAND3DPOSE, croplength)    
    
    #Filter out jumps in the recorded trajectory
    body_3D_pose_filtered, left_hand_3D_pos_filtered,right_hand_3D_pose_filtered = filter_out_jumps(body_3D_pose_cropped, left_hand_3D_pose_cropped,right_hand_3D_pose_cropped)
    
    #Convert the pose trajectory into a set of lines to animate
    results_list = get_plot_list(body_3D_pose_filtered, left_hand_3D_pos_filtered,right_hand_3D_pose_filtered)
    
    #Save the set of lines to animate
    datafile = open("bin/filtered_data/FULL" + file_name + extrastring + ".pickle", "wb")
    pickle.dump(results_list, datafile)
    
    #Print the time required to carry out the above
    print("Time taken is", time.time()-old_time)
    
    #Display an animation of the processed joint trajectories
    animate(file_name)
    
    
