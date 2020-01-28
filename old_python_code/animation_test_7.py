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
        #print("frame num is", frame_num, "_----------------------------------------------------------------")
        for hand_pose in right_hand_3D_pose, left_hand_3D_pose:
            for joint in HAND:
                if joint == HAND.PALM:
                    continue
                elif joint.value%4 == 1:
                    x1 = hand_pose[joint.value][frame_num][0]
                    x2 = hand_pose[HAND.PALM.value][frame_num][0]
                    
                    y1 = hand_pose[joint.value][frame_num][1]
                    y2 = hand_pose[HAND.PALM.value][frame_num][1]
                    
                    z1 = hand_pose[joint.value][frame_num][2]
                    z2 = hand_pose[HAND.PALM.value][frame_num][2]
                    
                    results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2], joint, 1])
                    #print(joint)
                    
                else:
                    x1 = hand_pose[joint.value][frame_num][0]
                    x2 = hand_pose[joint.value-1][frame_num][0]
                    
                    y1 = hand_pose[joint.value][frame_num][1]
                    y2 = hand_pose[joint.value-1][frame_num][1]
                    
                    z1 = hand_pose[joint.value][frame_num][2]
                    z2 = hand_pose[joint.value-1][frame_num][2]
                    
                    results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2], joint, 2])
                    #print(joint)

        for joint in BODY:
            if joint.value < 9:
                if joint == BODY.HEAD or joint== BODY.LEFT_SHOULDER or joint == BODY.RIGHT_SHOULDER or joint == BODY.PELVIS:
                    x1 = body_3D_pose[joint.value][frame_num][0]
                    x2 = body_3D_pose[BODY.CHEST.value][frame_num][0]
                    
                    y1 = body_3D_pose[joint.value][frame_num][1]
                    y2 = body_3D_pose[BODY.CHEST.value][frame_num][1]
                    
                    z1 = body_3D_pose[joint.value][frame_num][2]
                    z2 = body_3D_pose[BODY.CHEST.value][frame_num][2]
                    
                    results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2], joint, 3])
                    #print(joint)
                else:
                    x1 = body_3D_pose[joint.value][frame_num][0]
                    x2 = body_3D_pose[joint.value -1 ][frame_num][0]
                    
                    y1 = body_3D_pose[joint.value][frame_num][1]
                    y2 = body_3D_pose[joint.value -1 ][frame_num][1]
                    
                    z1 = body_3D_pose[joint.value][frame_num][2]
                    z2 = body_3D_pose[joint.value -1 ][frame_num][2]
                    
                    results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2], joint, 4])
                    #print(joint)
                    
            elif joint == BODY.LEFT_EYE or joint == BODY.RIGHT_EYE:
                    x1 = body_3D_pose[joint.value][frame_num][0]
                    x2 = body_3D_pose[BODY.HEAD.value][frame_num][0]
                    
                    y1 = body_3D_pose[joint.value][frame_num][1]
                    y2 = body_3D_pose[BODY.HEAD.value][frame_num][1]
                    
                    z1 = body_3D_pose[joint.value][frame_num][2]
                    z2 = body_3D_pose[BODY.HEAD.value][frame_num][2]
                    
                    results_list[frame_num].append([[x1,x2], [y1,y2], [z1,z2], joint, 5])
                    #print(joint)
    return results_list

results_list = get_plot_list()
print(len(results_list[5]))
print(results_list[5])


def update_lines(frame_num, results_list):
    print(time.time())
    ax.cla()
    for line in results_list[frame_num]:
        #print(line[0], line[1], line[2])
        lineB = ax.plot(line[0], line[1], line[2])
    
    ax.set_xlim3d([x_lower_limit, x_upper_limit])
    ax.set_ylim3d([y_lower_limit, y_upper_limit])
    ax.set_zlim3d([z_lower_limit, z_upper_limit])
    ax.set_xlabel('X')
    
    ax.set_ylabel('Y')
    
    ax.set_zlabel('Z')
    return lineB
    
    
# Attaching 3D axis to the figure
fig = plt.figure()
ax = p3.Axes3D(fig)




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
line_ani = animation.FuncAnimation(fig, update_lines, len(body_3D_pose[0]), fargs = ([results_list]),
                                   interval=100, blit=False, repeat = False)

plt.show()
