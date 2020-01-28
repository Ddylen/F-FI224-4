import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from get_3D_pose import HAND, BODY, get_arm_3D_coordinates


def render_points(filename):
    """Render the 3D points tracked by OpenPose"""
    """
    #start_time = time.time()
    body_3D_pose, left_hand_3D_pose, right_hand_3D_pose = get_arm_3D_coordinates('1.23.17.49', show_each_frame =  False)
    #print("Time taken is", time.time()-start_time)
    x_plot_list= []
    y_plot_list= []
    z_plot_list = []
    
    x_sec= []
    y_sec= []
    z_sec = []

    #for frame_num in range(len(body_3D_pose[0])):
    frame_num = 0
    for joints_list in body_3D_pose, left_hand_3D_pose, right_hand_3D_pose:
        for joint_positions in joints_list:
            print(joint_positions[frame_num])
            if joint_positions[frame_num][3] == False:
                x_plot_list.append(joint_positions[frame_num][0])
                y_plot_list.append(joint_positions[frame_num][1])
                z_plot_list.append(joint_positions[frame_num][2])

    for pos in right_hand_3D_pose[HAND.PALM.value]:

        if pos[3] ==False:
            x_sec.append(pos[0])
            y_sec.append(pos[1])
            z_sec.append(pos[2])

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x_plot_list, y_plot_list, z_plot_list)
    print(x_plot_list)
    plt.show()
    """
        #start_time = time.time()
    body_3D_pose, left_hand_3D_pose, right_hand_3D_pose = get_arm_3D_coordinates(filename, 0.4, False)
    #print("Time taken is", time.time()-start_time)
    x_sec= []
    y_sec= []
    z_sec = []
    """
    for pos in right_hand_3D_pose[HAND.PALM.value]:

        if pos[3] ==False:
            x_sec.append(pos[0])
            y_sec.append(pos[1])
            z_sec.append(pos[2])
    """
    x_plot_list= []
    y_plot_list= []
    z_plot_list = []
    

    #for frame_num in range(len(body_3D_pose[0])):
    frame_num = 1
    for joints_list in body_3D_pose, left_hand_3D_pose, right_hand_3D_pose:
        for joint_positions in joints_list:
            print(joint_positions[frame_num])
            if joint_positions[frame_num][3] == False:
                x_plot_list.append(joint_positions[frame_num][0])
                y_plot_list.append(joint_positions[frame_num][1])
                z_plot_list.append(joint_positions[frame_num][2])
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x_plot_list, y_plot_list, z_plot_list)
    plt.show()
    
if __name__ == '__main__': 
    
    #file_name = '1.23.17.49'
    file_name ="1.24.22.0"
    render_points(file_name)

