"""
Program for carrying out cooking stages with the UR5
"""

import sys
sys.path.insert(1,r'C:\Users\birl\Documents\updated_ur5_controller\Generic_ur5_controller')
import numpy as np
import math
import time
from math import pi
import waypoints as wp

import kg_robot as kgr

from coordinate_transforms import convert_to_arm_coords


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import cv2


def grab_stirrer(robo):
    robo.open_hand()
    robo.movel([0.29,-0.52,0.26, 1.04, 2.50, 2.50], min_time = 5)
    robo.movel([0.29,-0.52,0.10, 1.04, 2.50, 2.50], min_time = 5)
    robo.close_hand()
    robo.translatel_rel([0,0,0.1, 0,0,0], min_time = 3)
    
    robo.movel([-0.11, -0.36, 0.28, 0.60,-1.5, -0.67], min_time = 5)
    pass

def grab_item(robo, location, orientation, move_time = 5):
    move_height_offset = 0.15
    robo.open_hand()
    robo.movel([location[0], location[1], location[2]+move_height_offset, orientation[0], orientation[1], orientation[2]], min_time = move_time)
    robo.movel([location[0], location[1], location[2], orientation[0], orientation[1], orientation[2]], min_time = move_time)
    robo.close_hand()
    robo.movel([location[0], location[1], location[2]+move_height_offset, orientation[0], orientation[1], orientation[2]], min_time = move_time)
    
def drop_item(robo, location, orientation, move_time = 5):
    move_height_offset = 0.4
    #robo.close_hand()
    robo.movel([location[0], location[1], location[2]+move_height_offset, orientation[0], orientation[1], orientation[2]], min_time = move_time)
    robo.movel([location[0], location[1], location[2]+0.03, orientation[0], orientation[1], orientation[2]], min_time = move_time)
    time.sleep(10)
    robo.open_hand()
    robo.movel([location[0], location[1], location[2]+move_height_offset, orientation[0], orientation[1], orientation[2]], min_time = move_time)


def stir(robo, total_time, time_per_rotation):
    #move_height_offset = 0.4
    #robo.close_hand()
    #robo.translatel_rel([0,0,0.2, 0,0,0], min_time = 3)
    #robo.movel([stirrer_location[0],stirrer_location[1],stirrer_location[2]+0.4,1.46, 0.68, -0.56], min_time = 5)
    circle_points = circle(total_time, time_per_rotation)
    print(circle_points[0])
    #robo.movel([circle_points[0][0],circle_points[0][1],circle_points[0][2], 1.46, 0.68, -0.42], min_time = 3)
    #robo.movel([circle_points[0][0],circle_points[0][1],circle_points[0][2], 1.52, 0.58, -0.62], min_time = 5)
    robo.movel([circle_points[0][0],circle_points[0][1],circle_points[0][2], 1.77, 3.90, -1.61], min_time = 5)

    
    for val in circle_points:
        #robo.movel([val[0], val[1], val[2], 1.52, 0.58, -0.62], min_time = 0.1)
        robo.servoj([val[0], val[1], val[2],1.77, 3.90, -1.61], lookahead_time = 0.2, control_time = 0.01, gain = 100)
    
    #time.sleep(total_time+5)
    #robo.open_hand()
    robo.translatel_rel([0,0,0.4, 0,0,0], min_time = 3)
    #robo.movel([stirrer_location[0],stirrer_location[1],stirrer_location[2]+0.4, 0.98, -2.42, -2.63], min_time = 5)
    #robo.movel([location[0], location[1], location[2]+move_height_offset, orientation[0], orientation[1], orientation[2]], min_time = move_time)
    #robo.movel([location[0], location[1], location[2], orientation[0], orientation[1], orientation[2]], min_time = move_time)
    #robo.open_hand()
    #robo.movel([location[0], location[1], location[2]+move_height_offset, orientation[0], orientation[1], orientation[2]], min_time = move_time)

def circle(total_time, time_per_rotation):
    #7cm radius, 30cm height worked well at getting the edges
    # also 4cm radius, 29.5cm height worked
    #centre= [0.3525, -0.2285]
    #centre= [0.3345, -0.2182]
    centre= [0.345, -0.19]
    #radius = 0.05
    #z_val = 0.302
    radius = 0.05
    z_val = 0.247
    num_rotations = total_time/time_per_rotation
    num_points = int(num_rotations*time_per_rotation*100)
    points = np.linspace(0,num_rotations*math.pi*2,num_points)
    x = np.sin(points)*radius + centre[0]
    y = np.cos(points)*radius + centre[1]
    z = [z_val]*num_points
    circle_points_list = list(zip(x,y,z))
    return circle_points_list


    
    
    
stirrer_location = [0.159, -0.53, 0.09]
ladel_location = [0.025,-0.528, 0.12]

spatula_location = [-0.12, -0.528, 0.12]
whisk_location = [0.16, -0.430, 0.1275]

cup_1_location = [0.312, -0.523, 0.16]
cup_2_location = [0.208, -0.512, 0.16]
x_orinetation = [1.04, 2.50, 2.50]
y_orientation = [0.60,-1.5, -0.67]
y_orientation_reverse = [1.78,0.52, 1.69]
vertical_orientation = [0.98, -2.42, -2.63]
cup_orientation = [1.34, -0.65, 0.65]

def get_cups(robo):
    robo.movej([np.radians(-45), np.radians(-110), np.radians(-90), np.radians(-161), np.radians(-45), np.radians(45)], min_time = 5)
    #time.sleep(20)
    
    grab_item(robo, cup_1_location, cup_orientation)
    robo.teach_mode.play("pour_cup_1.json")
    robo.open_hand()
    
    grab_item(robo, cup_2_location, cup_orientation)
    robo.teach_mode.play("pour_cup_2.json")
    robo.open_hand()
    time.sleep(10)
    robo.translatel_rel([0,0,0.1, 0,0,0], min_time = 3)



def main():

    print("------------Configuring Burt-------------\r\n")

    burt = 0

    burt = kgr.kg_robot(port=30010,db_host="169.254.150.100", ee_port = 'COM3')

    print("----------------Hi Burt!-----------------\r\n\r\n")
    #startpos is ([-0.11, -0.36, 0.28, 1.04, 2.50, 2.50])
    
    #burt.open_hand()
    #time.sleep(5)
    #burt.open_hand()
    """
    #STIR EXAMPLE
    
    #burt.movel([0.33, -0.4, 0.3, 1.72,-0.82,-1.76], min_time = 3)
    #stir(burt)
    """

    """
    #HAND OPEN EXAMPLE
    
    burt.open_hand()
    time.sleep(1)
    burt.close_hand()
    time.sleep(1)
    burt.open_hand()
    time.sleep(1)
    burt.close_hand()
    time.sleep(1)
    """
    
    """
    #POUR EXAMPLE
    
    #print(burt.getl())
    burt.movel([-0.11, -0.36, 0.4, 1.04, 2.50, 2.50], min_time = 3)
    print(burt.getl())
    #burt.set_tcp([0.0,0.07,0.06,0,0,-np.radians(225)])
    #burt.set_tcp([0.0,0.08,0.075,0,0,-np.radians(225)])
    burt.set_tcp([0.0565,-0.0565,0.075,0,0,-np.radians(225)])
    #time.sleep(2)
    print(burt.getl())
    #burt.movel([-0.159193 , -0.297381, 0.350267, 0.00330878, 2.22059+np.radians(180), 2.21666], min_time = 5)
    
    #MOVEL STILL WORKS NORMALLY
    
    #burt.movel([-0.20845, -0.297476, 0.187574, -1.21311 , -1.20947+ np.radians(90), -1.21248], min_time = 5)
    #burt.movel([0.26, -0.1, 0.4,0,0,0], min_time = 5)
    
    burt.movel_tool([0,0,0,0,0, np.radians(90)], min_time = 5)
    #burt.movel_tool([0,0,0,-np.radians(90),0,0], min_time = 5)
    #burt.movel_tool([0,0,0,np.radians(90),0,0], min_time = 5)
    #print(burt.getl())
    """
    
    """
    MOSTLY WORKS
    #STAGE 1___________________________________________________________________
    get_cups(burt)
    
    #get_cups(burt)
    burt.movej([np.radians(-55), np.radians(-120), np.radians(-81), np.radians(-160), np.radians(38), np.radians(43)], min_time = 3)

    #STAGE 2___________________________________________________________________
    grab_item(burt, whisk_location, y_orientation)
    burt.close_hand()
    burt.translatel_rel([0,0,0.1, 0,0,0], min_time = 3)

    burt.close_hand()
    burt.movel([0.33, -0.22, 0.5, 1.77, 3.90, -1.61], min_time = 3)
    stir(burt, total_time = 120, time_per_rotation =  1)
    """
    
    
    
    #burt.movej([np.radians(-90), np.radians(-90), np.radians(-100), np.radians(-73), np.radians(90), np.radians(45)], min_time = 3)
    
    
    
    #burt.open_hand()
    #time.sleep(10)
    #burt.close_hand()

    #Get Other Equiptment
    

    
    
    #burt.movel([-0.11, -0.36, 0.28, 1.04, 2.50, 2.50], min_time = 5)
    #grab_item(burt, ladel_location, y_orientation)
    #burt.movel([-0.11, -0.36, 0.28, 1.04, 2.50, 2.50], min_time = 5)
    #grab_item(burt, spatula_location, y_orientation_reverse)
    #burt.movel([-0.11, -0.36, 0.28, 1.04, 2.50, 2.50], min_time = 5)
    
    
    #burt.translatel_rel([0,0,0.2, 0,0,0], min_time = 3)
    #burt.movej([np.radians(-67), np.radians(-117), np.radians(-89), np.radians(-159), np.radians(30), np.radians(43)], min_time = 5)
    
    """
    #POURING
    grab_item(burt, ladel_location, y_orientation)

    burt.close_hand()
    #burt.movej([np.radians(-90), np.radians(-80), np.radians(-123), np.radians(-63), np.radians(90), np.radians(45)])

    burt.close_hand()
    burt.teach_mode.play("ladelvar2.json")
    """
    #drop_item(burt, ladel_location, y_orientation)
    burt.movej([np.radians(-82), np.radians(-110), np.radians(-96), np.radians(-142), np.radians(17), np.radians(35)])
    grab_item(burt, spatula_location, y_orientation)
    
    #burt.teach_mode.play("ladel_use1.json")

    #burt.close()
    burt.ee.close()


if __name__ == '__main__': 
    
    main()