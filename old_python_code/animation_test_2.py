# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 13:53:04 2020

@author: birl
"""

import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import mpl_toolkits.mplot3d as plt3d
import matplotlib.animation as animation

# Fixing random state for reproducibility
np.random.seed(19680801)


from get_3D_pose import HAND, BODY, get_arm_3D_coordinates
body_3D_pose, left_hand_3D_pose, right_hand_3D_pose = get_arm_3D_coordinates('1.23.17.49')

x_plot_list= []
y_plot_list= []
z_plot_list = []



#for frame_num in range(len(body_3D_pose[0])):
frame_num = 15
for joints_list in body_3D_pose, left_hand_3D_pose, right_hand_3D_pose:
    for joint_positions in joints_list:
        print(joint_positions[frame_num])
        if joint_positions[frame_num][3] == False:
            x_plot_list.append(joint_positions[frame_num][0])
            y_plot_list.append(joint_positions[frame_num][1])
            z_plot_list.append(joint_positions[frame_num][2])




def update_lines(num, lineB):
    ax.cla()
    for val in range (6):
        lineB = ax.plot([val,val], [num,num], [0,val])
    return lineB

# Attaching 3D axis to the figure
fig = plt.figure()
ax = p3.Axes3D(fig)

# Fifty lines of random 3-D lines

for val in range (6):
    lineB = ax.plot([val,val], [0,0], [0,val])
    print(lineB)

"""
frame_num = 15
for joints in right_hand_3D_pose:
    for joint_positions in joints:
"""        
    
# Setting the axes properties
#ax.set_xlim3d([0.0, 1.0])
ax.set_xlabel('X')

#ax.set_ylim3d([0.0, 1.0])
ax.set_ylabel('Y')

#ax.set_zlim3d([0.0, 1.0])
ax.set_zlabel('Z')

ax.set_title('3D Test')

# Creating the Animation object
line_ani = animation.FuncAnimation(fig, update_lines, 50, fargs = (lineB),
                                   interval=50, blit=False, repeat = False)

plt.show()