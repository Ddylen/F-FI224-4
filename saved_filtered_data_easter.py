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
from efficient_load import efficient_load


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
    
    #Threshold, moving over this in a single frame marks a point as invalid
    move_distance_threshold = 0.1
    
    #Create lists of the last good points seen for each joint
    last_good_point_list_right =  [[0,0,0,False]]*len(right_hand_3D_pose)
    last_good_point_list_left =  [[0,0,0,False]]*len(left_hand_3D_pose)    
    last_good_point_list_body =  [[0,0,0,False]]*len(body_3D_pose)
    
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
                       
                       #If wrist position is bad also set hand joint position as bad
                       if  body_3D_pose[wristval][frame_num][3] == True:
                           hand_pose[joint.value][frame_num][3] = True
                           
                       #If hand position is out the the expected box say hand position is bad
                       if check_out_of_bounds(hand_pose[joint.value][frame_num]) == True:
                           hand_pose[joint.value][frame_num][3] = True
                       
                       #Define distance from last position    
                       move_distance = np.linalg.norm([hand_pose[joint.value][frame_num][0] - hand_pose[joint.value][frame_num-1][0], hand_pose[joint.value][frame_num][1]-hand_pose[joint.value][frame_num-1][1], hand_pose[joint.value][frame_num][2]-hand_pose[joint.value][frame_num-1][2]])
                       
                       #If hand moves too far or hand position is too far from wrist, replace position with last measured good position
                       if move_distance > move_distance_threshold:
                           
                           #Set that position was bad so it comes up in red in the animation
                           hand_pose[joint.value][frame_num][3] = True  

                       
                       #Update last good right hand pose 
                       if hand == "RIGHT":
                           
                           #If current joint is good
                           if hand_pose[joint.value][frame_num][3] == False:
                               
                               #Update last good point with the current point
                               last_good_point_list_right[joint.value] = hand_pose[joint.value][frame_num]
                             
                       #Update last good left hand pose        
                       if hand == "LEFT":
                           
                           #If current joint is good
                           if hand_pose[joint.value][frame_num][3] == False:
                               
                               #Update last good point with the current point
                               last_good_point_list_left[joint.value] = hand_pose[joint.value][frame_num]


       #Iterate over each joint in the body
       for joint in BODY:
           
           #Excluding the first frame, which contains no information
           if frame_num != 0:
               
               #Check joint lies within the allowable volume
               if check_out_of_bounds(body_3D_pose[joint.value][frame_num]) == True:
                           hand_pose[joint.value][frame_num][3] = True
                           
               #Define distance from current pose to last pose
               move_distance = np.linalg.norm([body_3D_pose[joint.value][frame_num][0] - body_3D_pose[joint.value][frame_num-1][0], body_3D_pose[joint.value][frame_num][1]-body_3D_pose[joint.value][frame_num-1][1], body_3D_pose[joint.value][frame_num][2]-body_3D_pose[joint.value][frame_num-1][2]])
               

               #If current joint is good
               if hand_pose[joint.value][frame_num][3] == False:
                   
                   #Update last good point with the current point
                   last_good_point_list_body[joint.value] = body_3D_pose[joint.value][frame_num]
                   
                   
    return body_3D_pose, left_hand_3D_pose,right_hand_3D_pose

    
def check_length_constraints(body_3D_pose, left_hand_3D_pose,right_hand_3D_pose):
    """Check the points correspond to a realistic skeleton"""
    
    #Define constraints on the size of the different parts of the skeleton
    palm_to_knuckles_max_length = 0.25 
    palm_to_knuckles_min_length = 0.03
    
    finger_interjoint_max_length = 0.07
    finger_interjoint_min_length = 0.01
    
    eye_head_max_length = 0.3
    eye_head_min_length = 0 
    
    max_arm_link_length = 0.35
    min_arm_link_length = 0.2 
    
    max_back_length = 0.8 
    min_back_length = 0.4 
    
    max_neck_length = 0.5
    min_neck_length = 0
    
    max_collar_length = 0.35
    min_collar_length = 0.15
    
    palm_to_wrist_max_length = 0.3 
    palm_to_wrist_min_length = 0 
    
    max_to_wrist_vector_length = 0.3
    
    #Iterate over each frame
    for frame_num in range(len(body_3D_pose[0])):
        
        #Iterate over each hand
        for hand_pose in right_hand_3D_pose, left_hand_3D_pose:
            
            #Define which hand we are operating on data points from
            if hand_pose == right_hand_3D_pose:
                hand = "RIGHT"
                wrist_joint = BODY.RIGHT_WRIST
                
            if hand_pose ==left_hand_3D_pose:
                hand = "LEFT"
                wrist_joint = BODY.LEFT_WRIST
                
            #Iterate over each joint in the hand
            for joint in HAND:
                
                #Define distance from the hand point to the wrist, to ensure it is not unrealisticaly far away
                x1 = body_3D_pose[wrist_joint.value][frame_num][0]
                x2 = hand_pose[joint.value][frame_num][0]
                
                y1 = body_3D_pose[wrist_joint.value][frame_num][1]
                y2 = hand_pose[joint.value][frame_num][1]
                
                z1 = body_3D_pose[wrist_joint.value][frame_num][2]
                z2 = hand_pose[joint.value][frame_num][2]
                    
                to_wrist_vector_length = np.linalg.norm([x1-x2, y1-y2, z1-z2])
                
                #If that line has unrealistic proprotions, mark this point as invalid
                if to_wrist_vector_length > max_to_wrist_vector_length:
                    
                    hand_pose[joint.value][frame_num][3] = True
                
                #If the palm is to far from the wrist, mark it as invalid
                if joint == HAND.PALM:
                    
                    if to_wrist_vector_length > palm_to_wrist_max_length or to_wrist_vector_length < palm_to_wrist_min_length:
                        
                        hand_pose[HAND.PALM.value][frame_num][3] = True
                
                #If joint connects to the palm:
                elif joint.value%4 == 1:
                    
                    #Define distance to the joint we draw a line to to make the skeleton (these are the lines from the palms to the knuckles)
                    x1 = hand_pose[joint.value][frame_num][0]
                    x2 = hand_pose[HAND.PALM.value][frame_num][0]
                    
                    y1 = hand_pose[joint.value][frame_num][1]
                    y2 = hand_pose[HAND.PALM.value][frame_num][1]
                    
                    z1 = hand_pose[joint.value][frame_num][2]
                    z2 = hand_pose[HAND.PALM.value][frame_num][2]
                    
                    vector_length = np.linalg.norm([x1-x2, y1-y2, z1-z2])
                    
                    #If the length of the line is unrealistic mark the two points at its ends as invalid
                    if vector_length > palm_to_knuckles_max_length or vector_length < palm_to_knuckles_min_length:
                        
                        hand_pose[joint.value][frame_num][3] = True
                        hand_pose[HAND.PALM.value][frame_num][3] = True
                    
                #For other joints
                else:
                    
                    #Define distance to the joint we draw a line to to make the skeleton (These are the lines in the fingers)
                    x1 = hand_pose[joint.value][frame_num][0]
                    x2 = hand_pose[joint.value-1][frame_num][0]
                    
                    y1 = hand_pose[joint.value][frame_num][1]
                    y2 = hand_pose[joint.value-1][frame_num][1]
                    
                    z1 = hand_pose[joint.value][frame_num][2]
                    z2 = hand_pose[joint.value-1][frame_num][2]
                    
                    vector_length = np.linalg.norm([x1-x2, y1-y2, z1-z2])
                    
                    #If the length of the line is unrealistic mark the two points at its ends as invalid
                    if vector_length > finger_interjoint_max_length or vector_length < finger_interjoint_min_length:

                        hand_pose[joint.value-1][frame_num][3] = True
                        hand_pose[joint.value][frame_num][3] = True
                        
        #For each joint in the body
        for joint in BODY:
            
            #For joints above the legs, excluding the facial features
            if joint.value < 9:
                
                #For joints that connect to the chest
                if joint == BODY.HEAD or joint== BODY.LEFT_SHOULDER or joint == BODY.RIGHT_SHOULDER or joint == BODY.PELVIS:
                    
                    #Define distance to the joint we draw a line to to make the skeleton  (these are the lines from the torso)
                    x1 = body_3D_pose[joint.value][frame_num][0]
                    x2 = body_3D_pose[BODY.CHEST.value][frame_num][0]
                    
                    y1 = body_3D_pose[joint.value][frame_num][1]
                    y2 = body_3D_pose[BODY.CHEST.value][frame_num][1]
                    
                    z1 = body_3D_pose[joint.value][frame_num][2]
                    z2 = body_3D_pose[BODY.CHEST.value][frame_num][2]
                    
                    vector_length = np.linalg.norm([x1-x2, y1-y2, z1-z2])
                    
                    #If the length of the line is unrealistic mark the two points at its ends as invalid
                    if joint == BODY.PELVIS:
                        if vector_length > max_back_length or vector_length < min_back_length:
                            body_3D_pose[joint.value][frame_num][3] = True
                    
                    if joint == BODY.HEAD:
                        if vector_length > max_neck_length or vector_length < min_neck_length:
                            body_3D_pose[joint.value][frame_num][3] = True
                            
                    if joint == BODY.LEFT_SHOULDER or joint == BODY.RIGHT_SHOULDER:
                         if vector_length > max_collar_length or vector_length < min_collar_length:
                             body_3D_pose[joint.value][frame_num][3] = True
                    
                #For the arms
                elif joint == BODY.RIGHT_ELBOW or joint== BODY.LEFT_ELBOW or joint == BODY.RIGHT_WRIST or joint == BODY.LEFT_WRIST:
                    
                    #Define distance to the joint we draw a line to to make the skeleton (these are the lines on the arms)
                    x1 = body_3D_pose[joint.value][frame_num][0]
                    x2 = body_3D_pose[joint.value -1 ][frame_num][0]
                    
                    y1 = body_3D_pose[joint.value][frame_num][1]
                    y2 = body_3D_pose[joint.value -1 ][frame_num][1]
                    
                    z1 = body_3D_pose[joint.value][frame_num][2]
                    z2 = body_3D_pose[joint.value -1 ][frame_num][2]
                    
                    vector_length = np.linalg.norm([x1-x2, y1-y2, z1-z2])
                    
                    #If the length of the line is unrealistic mark the two points at its ends as invalid
                    if vector_length > max_arm_link_length or vector_length < min_arm_link_length:
                             body_3D_pose[joint.value][frame_num][3] = True
                             
            
            #For the eye 'joints'        
            elif joint == BODY.LEFT_EYE or joint == BODY.RIGHT_EYE:
                
                    #Define distance to the joint we draw a line to to make the skeleton (these are the eye-head lines)
                    x1 = body_3D_pose[joint.value][frame_num][0]
                    x2 = body_3D_pose[BODY.HEAD.value][frame_num][0]
                    
                    y1 = body_3D_pose[joint.value][frame_num][1]
                    y2 = body_3D_pose[BODY.HEAD.value][frame_num][1]
                    
                    z1 = body_3D_pose[joint.value][frame_num][2]
                    z2 = body_3D_pose[BODY.HEAD.value][frame_num][2]
                    
                    vector_length = np.linalg.norm([x1-x2, y1-y2, z1-z2])
                    
                    #If the length of the line is unrealistic mark the two points at its ends as invalid
                    if vector_length > eye_head_max_length or vector_length < eye_head_min_length:
                        body_3D_pose[joint.value][frame_num][3] = True

                   
    return body_3D_pose, left_hand_3D_pose,right_hand_3D_pose


def overwrite_bad_values(body_3D_pose, left_hand_3D_pose,right_hand_3D_pose):
    """Overwrite invalid points in a list with the last valid point seen"""
    
    #Define empty list to fill with the last good points seen for each joint
    last_good_left_list = [ [] for i in HAND]
    last_good_right_list = [ [] for i in HAND]
    last_good_body_list = [ [] for i in BODY]
    
    #Iterate over each frame
    for frame_num in range(len(body_3D_pose[0])):
        
        #For each joint in the body
        for joint in BODY:
            
            #Define whether point is invalid
            point_bad = body_3D_pose[joint.value][frame_num][3]
            
            #For joints above the legs, excluding the facial features
            if joint.value < 9:
                
                #For joints that connect to the chest, offset position from current chest position
                if joint == BODY.HEAD or joint== BODY.LEFT_SHOULDER or joint == BODY.RIGHT_SHOULDER or joint == BODY.PELVIS:
                    
                    last_good_body_list, body_3D_pose = overwrite_position(joint, point_bad, frame_num, last_good_body_list, body_3D_pose, body_3D_pose, last_good_body_list, offset_joint = BODY.CHEST)
                       
                #For the arms, offset position from the current previous joint on the arm
                elif joint == BODY.RIGHT_ELBOW or joint== BODY.LEFT_ELBOW or joint == BODY.RIGHT_WRIST or joint == BODY.LEFT_WRIST:
                    
                    last_good_body_list, body_3D_pose = overwrite_position(joint, point_bad, frame_num, last_good_body_list, body_3D_pose, body_3D_pose, last_good_body_list, offset_joint = BODY(joint.value - 1))
                   
            #For the eye 'joints'    , offset position from the head    
            elif joint == BODY.LEFT_EYE or joint == BODY.RIGHT_EYE:
                
                last_good_body_list, body_3D_pose = overwrite_position(joint, point_bad, frame_num, last_good_body_list, body_3D_pose, body_3D_pose, last_good_body_list, offset_joint = BODY.HEAD)
                
        #Iterate over each hand
        for hand_pose in right_hand_3D_pose, left_hand_3D_pose:
            
            #Define which hand we are operating on data points from
            if hand_pose == right_hand_3D_pose:
                hand = "RIGHT"
                wrist_joint = BODY.RIGHT_WRIST
                last_good_hand_list = last_good_right_list
                
            if hand_pose ==left_hand_3D_pose:
                hand = "LEFT"
                wrist_joint = BODY.LEFT_WRIST
                last_good_hand_list = last_good_left_list
              
                
            #Iterate over each joint in the hand
            for joint in HAND:
                    
                #Define whether point is invalid
                point_bad = hand_pose[joint.value][frame_num][3]
                
                #For the palm, offset position from the wrist
                if joint == HAND.PALM:
                    
                    last_good_hand_list, hand_pose = overwrite_position(joint, point_bad, frame_num, last_good_hand_list, hand_pose, body_3D_pose, last_good_body_list, offset_joint = wrist_joint)
                    
                #If joint connects to the palm, offset position from the wrist
                elif joint.value%4 == 1:
                    
                    last_good_hand_list, hand_pose = overwrite_position(joint, point_bad, frame_num, last_good_hand_list, hand_pose, body_3D_pose, last_good_body_list, offset_joint = wrist_joint)

                #For other joints in the fingers, offset position from the wrist
                else:
                    
                    last_good_hand_list, hand_pose = overwrite_position(joint, point_bad, frame_num, last_good_hand_list, hand_pose, body_3D_pose, last_good_body_list, offset_joint = wrist_joint)
                   
    return body_3D_pose, left_hand_3D_pose,right_hand_3D_pose


def overwrite_position(joint, point_bad, frame_num, last_good_list, pose, body_3D_pose, last_good_body_list, offset_joint = False):
    """Function to overwrite a specific invalid point with its last good value, defining the last valid point, and the replacement point, from the corresponding offset joint"""
    
    #If the point is not invalid, just update the last good list
    if point_bad == False:
        
        last_good_list[joint.value] = [pose[joint.value][frame_num][0], pose[joint.value][frame_num][1], pose[joint.value][frame_num][2], pose[joint.value][frame_num][3], frame_num]
    
    #If the point is invalid and we have a previous valid point 
    elif point_bad == True and last_good_list[joint.value] != []:
        
        #Treat the offsets from the wrists seperately as they are stored on seperate lists to the 'pose' list if we call for them from the left or right hand pose lists
        if offset_joint == BODY.LEFT_WRIST or offset_joint == BODY.RIGHT_WRIST:
            
            #If we have a previous offset valid point
            if last_good_body_list[offset_joint.value] !=  []:
                
                #Define the frame that the previous valid point is from
                offset_original_frame = last_good_list[joint.value][4]
                
                #Find the previous valid offset point location
                offset_position = body_3D_pose[offset_joint.value][offset_original_frame]
                
                #Find said location in relation to the offset joint
                old_pos_from_offset = np.subtract(last_good_list[joint.value][0:3], offset_position[0:3])  
                
                #Use the current position of the offset joint to find the position to overwrite the invalid point with
                new_pos = np.add(old_pos_from_offset[0:3], last_good_body_list[offset_joint.value][0:3])  
                
                #Update the invalid point on the pose list with the valid point
                pose[joint.value][frame_num] = [new_pos[0], new_pos[1], new_pos[2], True]
            
            #If you have no previous valid point, do nothing
            else:
                pass
        
        #For any other offset joint
        elif offset_joint != False:
            if last_good_list[offset_joint.value] !=  []:
                
                #Define the frame that the previous valid point is from
                offset_original_frame = last_good_list[joint.value][4]
                
                #Find the previous valid offset point location
                offset_position = pose[offset_joint.value][offset_original_frame]
                
                #Find said location in relation to the offset joint
                old_pos_from_offset = np.subtract(last_good_list[joint.value][0:3], offset_position[0:3]) 
                
                #Use the current position of the offset joint to find the position to overwrite the invalid point with
                new_pos = np.add(old_pos_from_offset[0:3], last_good_list[offset_joint.value][0:3])  
                
                #Update the invalid point on the pose list with the valid point
                pose[joint.value][frame_num] = [new_pos[0], new_pos[1], new_pos[2], True]
                
            #If we do not have a previous valid point    
            else:
                
                pass
                
        #If we call this without an offset joint, just use the last good value
        elif offset_joint == False:
            pose[joint.value][frame_num] = last_good_list[joint.value]

    #If we do not have a previous valid point
    else:
        
        pass
    
    return last_good_list, pose

def get_plot_list(body_3D_pose, left_hand_3D_pose,right_hand_3D_pose):
    """Turn tracked points into a series of lines to animate"""
    
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
                    x1 = hand_pose[joint.value][frame_num][0]
                    x2 = hand_pose[HAND.PALM.value][frame_num][0] 
                    
                    y1 = hand_pose[joint.value][frame_num][1] 
                    y2 = hand_pose[HAND.PALM.value][frame_num][1] 
                    
                    z1 = hand_pose[joint.value][frame_num][2] 
                    z2 = hand_pose[HAND.PALM.value][frame_num][2]        

                    #Define whether the line is valid, using whether both ends of the line, and the wrist, are valid
                    if hand_pose[joint.value][frame_num][3] == True or hand_pose[HAND.PALM.value][frame_num][3] == True:
                        
                        lost_track = True
                    
                    #Append line to list of lines to draw
                    results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2], lost_track])
                    
                #For other joints
                else:
                    
                    #Define a line from the joint to the previous joint
                    x1 = hand_pose[joint.value][frame_num][0]
                    x2 = hand_pose[joint.value-1][frame_num][0]
                    
                    y1 = hand_pose[joint.value][frame_num][1]
                    y2 = hand_pose[joint.value-1][frame_num][1]
                    
                    z1 = hand_pose[joint.value][frame_num][2]
                    z2 = hand_pose[joint.value-1][frame_num][2]
                    
                    #Define whether the line is valid, using whether both ends of the line, and the wrist, are valid
                    if hand_pose[joint.value][frame_num][3] == True or hand_pose[joint.value-1][frame_num][3] == True or wrist_offset[3] == True:
                        lost_track = True
                    
                    #Append line to list of lines to draw
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
                    
                    #Append line to list of lines to draw
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
                    
                    #Append line to list of lines to draw
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
                        
                         lost_track = True
                         
                         #Append line to list of lines to draw
                         results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2], lost_track])

                    #If both points are good
                    else:
                         
                         #Append line to list of lines to draw
                         results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2], lost_track])
                                 
    return results_list
    

def crop(listtocrop, length, start = 0):
    """Function to crop a pose list to a certain length""" 
    croppedlist = []
    for row in listtocrop:
        croppedlist.append(row[start:length+start])
        
    
    return croppedlist

if __name__ == '__main__': 
    
    #Set a recursion limit to avoid recusion length errors on long lists
    sys.setrecursionlimit(10**6)
    
    #Start a timer
    old_time = time.time()
    
    #Defimne the relevant file name
    
    #file_name = 'stationaytrial5.17.3.9.44'
    #file_name = 'trial6dylan.16.3.9.50'
    file_name = 'trial7thomas.16.3.10.24'
    #file_name = 'test9keiran.17.3.11.40'
    #file_name = 'trial7josie.17.3.10.31'

    #Find if file has already been processed to extract the pose lists
    try:
        readfile = open("bin/points_data/" + file_name + ".pickle", "rb")
        BODY3DPOSE = pickle.load(readfile)
        LEFTHAND3DPOSE = pickle.load(readfile)
        RIGHTHAND3DPOSE = pickle.load(readfile)
        readfile.close()
    
    #If not, process the file to extract the pose lists
    except FileNotFoundError:
        BODY3DPOSE, LEFTHAND3DPOSE,RIGHTHAND3DPOSE = get_arm_3D_coordinates(file_name, confidence_threshold = 0.05)
        
        #Save the extracted poselists
        pointsfile = open("bin/points_data/" + file_name + ".pickle", "wb")
        pickle.dump(BODY3DPOSE, pointsfile)
        pickle.dump(LEFTHAND3DPOSE, pointsfile)    
        pickle.dump(RIGHTHAND3DPOSE, pointsfile)
        pointsfile.close()
    
        #Then extract the poselists from the saved file for consistency with the prior method
        readfile = open("bin/points_data/" + file_name + ".pickle", "rb")
        readbody3dpose = pickle.load(readfile)
        readlefthand3dpose = pickle.load(readfile)
        readrighthand3dpose = pickle.load(readfile)
        readfile.close()
    
    #Define the length that we want to crop the recording to
    croplength = 2735
    cropstart = 0
    
    #Define an additional string to give this filtered cropped recording a unique file name
    extrastring = 'Full'
    
    #Crop the pose lists    
    body_3D_pose_cropped = crop(readbody3dpose, croplength, start = cropstart)
    left_hand_3D_pose_cropped = crop(readlefthand3dpose, croplength, start = cropstart)
    right_hand_3D_pose_cropped = crop(readrighthand3dpose, croplength, start = cropstart)    
    
    #Filter out jumps in the recorded trajectory
    body_3D_pose_filtered, left_hand_3D_pose_filtered,right_hand_3D_pose_filtered = filter_out_jumps(body_3D_pose_cropped, left_hand_3D_pose_cropped,right_hand_3D_pose_cropped)
    
    #FIlter out limbs that are too long:
    body_3D_pose_lenthchecked, left_hand_3D_pose_lenthchecked,right_hand_3D_pose_lenthchecked = check_length_constraints(body_3D_pose_filtered, left_hand_3D_pose_filtered,right_hand_3D_pose_filtered)
    
    #Overwirte invalid points in the recording
    body_3D_pose_updated, left_hand_3D_pose_updated,right_hand_3D_pose_updated = overwrite_bad_values(body_3D_pose_lenthchecked, left_hand_3D_pose_lenthchecked,right_hand_3D_pose_lenthchecked )
    
    #Smooth the joint trajectories with a savgol filter
    body_3D_pose_smoothed, left_hand_3D_pose_smoothed,right_hand_3D_pose_smoothed = savgol_filter(body_3D_pose_updated, left_hand_3D_pose_updated,right_hand_3D_pose_updated)
    
    
    #Convert the pose trajectory into a set of lines to animate
    results_list = get_plot_list(body_3D_pose_smoothed, left_hand_3D_pose_smoothed,right_hand_3D_pose_smoothed)
    
    #Save the set of lines to animate
    datafile = open("bin/filtered_data/" + file_name + extrastring + ".pickle", "wb")
    pickle.dump(results_list, datafile)
    
    #Print the time required to carry out the above
    print("Time taken is", time.time()-old_time)
    
    #Display an animation of the processed joint trajectories
    animate(file_name + extrastring, True)

    
