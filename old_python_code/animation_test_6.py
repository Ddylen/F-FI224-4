# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 15:27:06 2020

@author: birl
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 14:55:23 2020

@author: birl
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 13:53:04 2020

@author: birl
"""

import numpy as np
import time
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import mpl_toolkits.mplot3d as plt3d
import matplotlib.animation as animation

# Fixing random state for reproducibility
np.random.seed(19680801)


from get_3D_pose import HAND, BODY, get_arm_3D_coordinates
body_3D_pose, left_hand_3D_pose, right_hand_3D_pose = get_arm_3D_coordinates('1.23.17.49')
#body_3D_pose, left_hand_3D_pose, right_hand_3D_pose = get_arm_3D_coordinates('1.24.22.0')

x_plot_list= []
y_plot_list= []
z_plot_list = []



#for frame_num in range(len(body_3D_pose[0])):
frame_num = 15
for joints_list in body_3D_pose, left_hand_3D_pose, right_hand_3D_pose:
    for joint_positions in joints_list:
        #print(joint_positions[frame_num])
        if joint_positions[frame_num][3] == False:
            x_plot_list.append(joint_positions[frame_num][0])
            y_plot_list.append(joint_positions[frame_num][1])
            z_plot_list.append(joint_positions[frame_num][2])



x_upper_limit = 1
x_lower_limit = -1

y_upper_limit = 1
y_lower_limit = -1

z_upper_limit = 0
z_lower_limit = -0.5


def update_lines(frame_num):
    
    ax.cla()
    print(time.time())

    for hand_pose in right_hand_3D_pose, left_hand_3D_pose:
        for joint_positions in hand_pose:
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
                    
                    ax.plot([x1,x2], [y1,y2], [z1,z2])
                    
                else:
                    x1 = hand_pose[joint.value][frame_num][0]
                    x2 = hand_pose[joint.value-1][frame_num][0]
                    
                    y1 = hand_pose[joint.value][frame_num][1]
                    y2 = hand_pose[joint.value-1][frame_num][1]
                    
                    z1 = hand_pose[joint.value][frame_num][2]
                    z2 = hand_pose[joint.value-1][frame_num][2]
                    
                    ax.plot([x1,x2], [y1,y2], [z1,z2])
                    
    for joint_positions in body_3D_pose:
        for joint in BODY:
            if joint.value < 9:
                if joint == BODY.HEAD or joint== BODY.LEFT_SHOULDER or joint == BODY.RIGHT_SHOULDER or joint == BODY.PELVIS:
                    x1 = body_3D_pose[joint.value][frame_num][0]
                    x2 = body_3D_pose[BODY.CHEST.value][frame_num][0]
                    
                    y1 = body_3D_pose[joint.value][frame_num][1]
                    y2 = body_3D_pose[BODY.CHEST.value][frame_num][1]
                    
                    z1 = body_3D_pose[joint.value][frame_num][2]
                    z2 = body_3D_pose[BODY.CHEST.value][frame_num][2]
                    
                    ax.plot([x1,x2], [y1,y2], [z1,z2])
                else:
                    x1 = body_3D_pose[joint.value][frame_num][0]
                    x2 = body_3D_pose[joint.value -1 ][frame_num][0]
                    
                    y1 = body_3D_pose[joint.value][frame_num][1]
                    y2 = body_3D_pose[joint.value -1 ][frame_num][1]
                    
                    z1 = body_3D_pose[joint.value][frame_num][2]
                    z2 = body_3D_pose[joint.value -1 ][frame_num][2]
                    
                    ax.plot([x1,x2], [y1,y2], [z1,z2])
            elif joint == BODY.LEFT_EYE or joint == BODY.RIGHT_EYE:
                    x1 = body_3D_pose[joint.value][frame_num][0]
                    x2 = body_3D_pose[BODY.HEAD.value][frame_num][0]
                    
                    y1 = body_3D_pose[joint.value][frame_num][1]
                    y2 = body_3D_pose[BODY.HEAD.value][frame_num][1]
                    
                    z1 = body_3D_pose[joint.value][frame_num][2]
                    z2 = body_3D_pose[BODY.HEAD.value][frame_num][2]
                    
                    ax.plot([x1,x2], [y1,y2], [z1,z2])
    ax.set_xlim3d([x_lower_limit, x_upper_limit])
    ax.set_ylim3d([y_lower_limit, y_upper_limit])
    ax.set_zlim3d([z_lower_limit, z_upper_limit])
    ax.set_xlabel('X')
    
    ax.set_ylabel('Y')
    
    ax.set_zlabel('Z')
    
# Attaching 3D axis to the figure
fig = plt.figure()
ax = p3.Axes3D(fig)

"""
# Fifty lines of random 3-D lines
frame_num = 0
for hand_pose in right_hand_3D_pose, left_hand_3D_pose:
    for joint_positions in hand_pose:
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
                
                lineB = ax.plot([x1,x2], [y1,y2], [z1,z2])
                
            else:
                x1 = hand_pose[joint.value][frame_num][0]
                x2 = hand_pose[joint.value-1][frame_num][0]
                
                y1 = hand_pose[joint.value][frame_num][1]
                y2 = hand_pose[joint.value-1][frame_num][1]
                
                z1 = hand_pose[joint.value][frame_num][2]
                z2 = hand_pose[joint.value-1][frame_num][2]
                
                lineB = ax.plot([x1,x2], [y1,y2], [z1,z2])
            
for joint_positions in body_3D_pose:
    for joint in BODY:
        if joint.value < 9:
            if joint == BODY.HEAD or joint== BODY.LEFT_SHOULDER or joint == BODY.RIGHT_SHOULDER or joint == BODY.PELVIS:
                x1 = body_3D_pose[joint.value][frame_num][0]
                x2 = body_3D_pose[BODY.CHEST.value][frame_num][0]
                
                y1 = body_3D_pose[joint.value][frame_num][1]
                y2 = body_3D_pose[BODY.CHEST.value][frame_num][1]
                
                z1 = body_3D_pose[joint.value][frame_num][2]
                z2 = body_3D_pose[BODY.CHEST.value][frame_num][2]
                
                lineB = ax.plot([x1,x2], [y1,y2], [z1,z2])
            else:
                x1 = body_3D_pose[joint.value][frame_num][0]
                x2 = body_3D_pose[joint.value -1 ][frame_num][0]
                
                y1 = body_3D_pose[joint.value][frame_num][1]
                y2 = body_3D_pose[joint.value -1 ][frame_num][1]
                
                z1 = body_3D_pose[joint.value][frame_num][2]
                z2 = body_3D_pose[joint.value -1 ][frame_num][2]
                
                lineB = ax.plot([x1,x2], [y1,y2], [z1,z2])
        elif joint == BODY.LEFT_EYE or joint == BODY.RIGHT_EYE:
                x1 = body_3D_pose[joint.value][frame_num][0]
                x2 = body_3D_pose[BODY.HEAD.value][frame_num][0]
                
                y1 = body_3D_pose[joint.value][frame_num][1]
                y2 = body_3D_pose[BODY.HEAD.value][frame_num][1]
                
                z1 = body_3D_pose[joint.value][frame_num][2]
                z2 = body_3D_pose[BODY.HEAD.value][frame_num][2]
                
                lineB = ax.plot([x1,x2], [y1,y2], [z1,z2])

"""
"""
frame_num = 20
x1 = right_hand_3D_pose[frame_num][1][0]
x2 = right_hand_3D_pose[frame_num][0][0]

y1 = right_hand_3D_pose[frame_num][1][1]
y2 = right_hand_3D_pose[frame_num][0][1]

z1 = right_hand_3D_pose[frame_num][1][2]
z2 = right_hand_3D_pose[frame_num][0][2]
print([x1,x2], [y1,y2], [z1,z2])
lineB = ax.plot([x1,x2], [y1,y2], [z1,z2])

"""
"""
frame_num = 15
for joints in right_hand_3D_pose:
    for joint_positions in joints:
"""        
    
# Setting the axes properties
ax.set_xlim3d([x_lower_limit, x_upper_limit])
ax.set_xlabel('X')

ax.set_ylim3d([y_lower_limit, y_upper_limit])
ax.set_ylabel('Y')

ax.set_zlim3d([z_lower_limit, z_upper_limit])
ax.set_zlabel('Z')

ax.set_title('3D Test')

# Creating the Animation object
line_ani = animation.FuncAnimation(fig, update_lines, len(body_3D_pose[0]),
                                   interval=100, blit=False, repeat = False)

plt.show()