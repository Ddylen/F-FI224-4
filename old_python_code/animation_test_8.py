# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 13:56:46 2020

@author: birl
"""

import numpy as np
import time
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import mpl_toolkits.mplot3d as plt3d
import matplotlib.animation as animation

from get_3D_pose import HAND, BODY, get_arm_3D_coordinates

body_3D_pose, left_hand_3D_pose, right_hand_3D_pose = get_arm_3D_coordinates('1.23.17.49')

x_upper_limit = 1
x_lower_limit = -1

y_upper_limit = 1
y_lower_limit = -1

z_upper_limit = 0
z_lower_limit = -0.5

def get_plot_list():
    
    results_list = [ [] for i in range(len(body_3D_pose[0]))]
    
    for frame_num in range(len(body_3D_pose[0])):
        for hand_pose in right_hand_3D_pose, left_hand_3D_pose:

            for joint in HAND:
                if joint == HAND.PALM:
                    pass
                elif joint.value%4 == 1:
                    x1 = hand_pose[joint.value][frame_num][0]
                    x2 = hand_pose[HAND.PALM.value][frame_num][0]
                    
                    y1 = hand_pose[joint.value][frame_num][1]
                    y2 = hand_pose[HAND.PALM.value][frame_num][1]
                    
                    z1 = hand_pose[joint.value][frame_num][2]
                    z2 = hand_pose[HAND.PALM.value][frame_num][2]
                    
                    results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2]])
                    
                else:
                    x1 = hand_pose[joint.value][frame_num][0]
                    x2 = hand_pose[joint.value-1][frame_num][0]
                    
                    y1 = hand_pose[joint.value][frame_num][1]
                    y2 = hand_pose[joint.value-1][frame_num][1]
                    
                    z1 = hand_pose[joint.value][frame_num][2]
                    z2 = hand_pose[joint.value-1][frame_num][2]
                    
                    results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2]])
                        

        for joint in BODY:
            if joint.value < 9:
                if joint == BODY.HEAD or joint== BODY.LEFT_SHOULDER or joint == BODY.RIGHT_SHOULDER or joint == BODY.PELVIS:
                    x1 = body_3D_pose[joint.value][frame_num][0]
                    x2 = body_3D_pose[BODY.CHEST.value][frame_num][0]
                    
                    y1 = body_3D_pose[joint.value][frame_num][1]
                    y2 = body_3D_pose[BODY.CHEST.value][frame_num][1]
                    
                    z1 = body_3D_pose[joint.value][frame_num][2]
                    z2 = body_3D_pose[BODY.CHEST.value][frame_num][2]
                    
                    results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2]])
                else:
                    x1 = body_3D_pose[joint.value][frame_num][0]
                    x2 = body_3D_pose[joint.value -1 ][frame_num][0]
                    
                    y1 = body_3D_pose[joint.value][frame_num][1]
                    y2 = body_3D_pose[joint.value -1 ][frame_num][1]
                    
                    z1 = body_3D_pose[joint.value][frame_num][2]
                    z2 = body_3D_pose[joint.value -1 ][frame_num][2]
                    
                    results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2]])
                    
            elif joint == BODY.LEFT_EYE or joint == BODY.RIGHT_EYE:
                    x1 = body_3D_pose[joint.value][frame_num][0]
                    x2 = body_3D_pose[BODY.HEAD.value][frame_num][0]
                    
                    y1 = body_3D_pose[joint.value][frame_num][1]
                    y2 = body_3D_pose[BODY.HEAD.value][frame_num][1]
                    
                    z1 = body_3D_pose[joint.value][frame_num][2]
                    z2 = body_3D_pose[BODY.HEAD.value][frame_num][2]
                    
                    results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2]])
    return results_list



#print(len(results_list))
def update_lines(frame_num, results_list, lines):
    #print(time.time())
    #print(len(lines))
    i = 0
    
    this_frame = results_list[frame_num]
    #print(this_frame)
    print("this frame len", len(this_frame[0]))
    for line in lines:
        #print(line)
        #print(i)
        #print("len lines is", len(lines))
        #print(results_list[frame_num][i])
        new_data = results_list[frame_num][i]
        
        #print('newdata', new_data)
        print('lennewdata', len(new_data))
        x = new_data[0]
        print('x', x)
        y = new_data[1]
        print('y', y)
        z = new_data[2]
        print('z', z)
        line.set_data(x,y)
        line.set_3d_properties(z)
        i = i+  1
    
    ax.set_xlim3d([x_lower_limit, x_upper_limit])
    ax.set_ylim3d([y_lower_limit, y_upper_limit])
    ax.set_zlim3d([z_lower_limit, z_upper_limit])
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    ax.set_title('3D Test')

    return lines
    
# Attaching 3D axis to the figure
fig = plt.figure()
ax = p3.Axes3D(fig)
results_list = get_plot_list()

print("results list first frame is length ", len(results_list[0]))
print(results_list[0][0][0])

#print(results_list[1])
lines = [ax.plot(l[0], l[1], l[2])[0] for l in results_list[1]]
#print(lines[0])


# Creating the Animation object

line_ani = animation.FuncAnimation(fig, update_lines, len(body_3D_pose[0]), fargs = ([results_list], lines),
                                   interval=100, blit=False, repeat = False)

plt.show()
