# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 15:06:32 2020

@author: birl
"""

import numpy as np
import time
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import mpl_toolkits.mplot3d as plt3d
import matplotlib.animation as animation

from get_3D_pose import HAND, BODY, get_arm_3D_coordinates

#'1.24.21.47'
BODY3DPOSE, LEFTHAND3DPOSE,RIGHTHAND3DPOSE = get_arm_3D_coordinates('1.23.17.49', confidence_threshold = 0)
#BODY3DPOSE, LEFTHAND3DPOSE,RIGHTHAND3DPOSE = get_arm_3D_coordinates('1.24.21.39', confidence_threshold = 0)

x_upper_limit = 0.75
x_lower_limit = -0.75

y_upper_limit = 0.75
y_lower_limit = -0.75

z_upper_limit = 0.5
z_lower_limit = -1

def find_last_good_pose(pose_list, frame_num, original_frame_num):
    # pose_list is pose[joint.value][frame_num-1]
    if pose_list[frame_num-1][3] == False:
        returned_frame = frame_num-1
    else:
        if frame_num == 0:
            returned_frame = original_frame_num
        else:
            last_good_pose, returned_frame = find_last_good_pose(pose_list, frame_num -1, original_frame_num)
    
    last_good_pose = pose_list[returned_frame]
    return last_good_pose, returned_frame
    
def filter_out_jumps(body_3D_pose, left_hand_3D_pose,right_hand_3D_pose, threshold = 0.1):
     count= 0
     right_wrist_list = []
     #print(range(len(body_3D_pose[0])))
     too_big_distance_list = []
     for frame_num in range(len(body_3D_pose[0])):
        #print(frame_num)
        for hand_pose in right_hand_3D_pose, left_hand_3D_pose:
            for joint in HAND:
                if frame_num != 0:
                    last_good_hand_pose, returned_frame = find_last_good_pose(hand_pose[joint.value], frame_num, frame_num)
                    move_distance = np.sqrt((hand_pose[joint.value][frame_num][0] - last_good_hand_pose[0])**2+(hand_pose[joint.value][frame_num][1]-last_good_hand_pose[1])**2 + (hand_pose[joint.value][frame_num][2]-last_good_hand_pose[2])**2)
                    if move_distance >= threshold:
                        
                        
                        hand_pose[joint.value][returned_frame][3] = True
                        
                        too_big_distance_list.append(move_distance)
                        #print("hand fired ", count)
                        count  +=1
    
        for joint in BODY:
            if frame_num != 0:
                last_good_body_pose, returned_frame = find_last_good_pose(body_3D_pose[joint.value], frame_num, frame_num)
                move_distance = np.sqrt((body_3D_pose[joint.value][frame_num][0] - last_good_body_pose[0])**2+(body_3D_pose[joint.value][frame_num][1]-last_good_body_pose[1])**2 + (body_3D_pose[joint.value][frame_num][2]-last_good_body_pose[2])**2)
                if move_distance >= threshold:
                    
                    
                    body_3D_pose[joint.value][returned_frame][3] = True
                    
                    
                    #body_3D_pose[joint.value][frame_num-1][3] = True
                    too_big_distance_list.append(move_distance)
                    #print("body fired ", count)
                    count +=1 
                    #print(joint)
                if joint.value == 7:
                    #right_wrist_list.append([[frame_num, move_distance, body_3D_pose[joint.value][returned_frame][0],body_3D_pose[joint.value][returned_frame][1], body_3D_pose[joint.value][returned_frame][2] ]])
                    right_wrist_list.append([[move_distance,frame_num, body_3D_pose[joint.value][returned_frame][3],body_3D_pose[joint.value-1][returned_frame][3]]])
    
     #print(sorted(too_big_distance_list))
     print("Total number of filtered points is", len(too_big_distance_list))
     #print(right_wrist_list)
     return body_3D_pose, left_hand_3D_pose,right_hand_3D_pose
    
def get_plot_list(body_3D_pose, left_hand_3D_pose,right_hand_3D_pose):
    
    print("filter started")
    
    body_3D_pose, left_hand_3D_pose,right_hand_3D_pose = filter_out_jumps(body_3D_pose, left_hand_3D_pose,right_hand_3D_pose)
    
    print("filter finished")
    
    results_list = [ [] for i in range(len(body_3D_pose[0]))]
    
    for frame_num in range(len(body_3D_pose[0])):
        for hand_pose in right_hand_3D_pose, left_hand_3D_pose:
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
                    #print(joint)
                    
                else:
                    x1 = hand_pose[joint.value][frame_num][0]
                    x2 = hand_pose[joint.value-1][frame_num][0]
                    
                    y1 = hand_pose[joint.value][frame_num][1]
                    y2 = hand_pose[joint.value-1][frame_num][1]
                    
                    z1 = hand_pose[joint.value][frame_num][2]
                    z2 = hand_pose[joint.value-1][frame_num][2]
                    
                    if hand_pose[joint.value][frame_num][3] == True or hand_pose[joint.value-1][frame_num][3] == True:
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
                    
                    results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2], lost_track])
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
                    
                    results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2], lost_track])
                    #print(joint)
                    #print(results_list)
    return results_list


#print(len(results_list[5]))
#print(results_list[5])
old_time = time.time()

def update_lines(frame_num, lines, time_text):
    #print(time.time())
    i = 0
    for line in lines:
        #print(results_list[frame_num][i])
        #print("I IS", i)
        #print(line)
        x = np.asarray(results_list[frame_num][i][0])
        #print('x', x)
        #print(type(x))
        #print(" ")
        y = np.asarray(results_list[frame_num][i][1])
        #print('y', y)
        #print(" ")
        z = np.asarray(results_list[frame_num][i][2])
        #print('z', z)
        #print(" ")

        #print(" ")

        if results_list[frame_num][i][3] == False:

            pass
  
        elif  results_list[frame_num][i][3] == True:
            #print(type(line))
            #line.set_color = 'none'
            x = np.asarray([0,0])
            y = np.asarray([0,0])
            z = np.asarray([0,0])
        #if i == 47:
            #x = np.asarray([0,0])
            #y = np.asarray([0,0])
            #z = np.asarray([0,0])
            #print(frame_num, [results_list[frame_num][i]])
        line.set_data(x,y)
        line.set_3d_properties(z)
        i = i+1
    
    ax.set_xlim3d([x_lower_limit, x_upper_limit])
    ax.set_ylim3d([y_lower_limit, y_upper_limit])
    ax.set_zlim3d([z_lower_limit, z_upper_limit])
    ax.set_xlabel('X')
    
    ax.set_ylabel('Y')
    
    ax.set_zlabel('Z')
    time_text.set_text('Frame = %.1d' % frame_num)
    return lines
    
    
# Attaching 3D axis to the figure
fig = plt.figure()
ax = p3.Axes3D(fig)

results_list = get_plot_list(BODY3DPOSE, LEFTHAND3DPOSE,RIGHTHAND3DPOSE)
print()
lines = [ax.plot(l[0], l[1], l[2])[0] for l in results_list[1]]

  
# Setting the axes properties
ax.set_xlim3d([x_lower_limit, x_upper_limit])
ax.set_xlabel('X')

ax.set_ylim3d([y_lower_limit, y_upper_limit])
ax.set_ylabel('Y')

ax.set_zlim3d([z_lower_limit, z_upper_limit])
ax.set_zlabel('Z')

ax.set_title('Skeleton Tracking')
time_text = ax.text(0,0.5,0,s= 'Frame = ',horizontalalignment='left',verticalalignment='top', transform=ax.transAxes)

# Creating the Animation object
#len(body_3D_pose[0])
ani = animation.FuncAnimation(fig, update_lines, len(BODY3DPOSE[0]), fargs = [lines, time_text],
                                   interval=100, blit=False, repeat = True)
Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
ani.save('ani.mp4', writer=writer)

plt.show()