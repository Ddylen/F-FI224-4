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
    open_gripper(robo)
    robo.movel([0.29,-0.52,0.26, 1.04, 2.50, 2.50], min_time = 5)
    robo.movel([0.29,-0.52,0.10, 1.04, 2.50, 2.50], min_time = 5)
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
    robo.close_hand()
    robo.movel([location[0], location[1], location[2]+move_height_offset, orientation[0], orientation[1], orientation[2]], min_time = move_time)
    robo.movel([location[0], location[1], location[2], orientation[0], orientation[1], orientation[2]], min_time = move_time)
    robo.open_hand()
    robo.movel([location[0], location[1], location[2]+move_height_offset, orientation[0], orientation[1], orientation[2]], min_time = move_time)


def stir(robo, move_time = 5):
    #move_height_offset = 0.4
    #robo.close_hand()
    #robo.translatel_rel([0,0,0.2, 0,0,0], min_time = 3)
    #robo.movel([stirrer_location[0],stirrer_location[1],stirrer_location[2]+0.4,1.46, 0.68, -0.56], min_time = 5)
    circle_points = circle(robo)
    print(circle_points[0])
    #robo.movel([circle_points[0][0],circle_points[0][1],circle_points[0][2], 1.46, 0.68, -0.42], min_time = 3)
    #robo.movel([circle_points[0][0],circle_points[0][1],circle_points[0][2], 1.52, 0.58, -0.62], min_time = 5)
    robo.movel([circle_points[0][0],circle_points[0][1],circle_points[0][2], 1.72,-0.82,-1.76], min_time = 5)

    for num in range(3):
        for val in circle_points:
            #robo.movel([val[0], val[1], val[2], 1.52, 0.58, -0.62], min_time = 0.1)
            robo.servoj([val[0], val[1], val[2],1.72,-0.82,-1.76], lookahead_time = 0.2, control_time = 0.01, gain = 100)

    #robo.movel([stirrer_location[0],stirrer_location[1],stirrer_location[2]+0.4, 0.98, -2.42, -2.63], min_time = 5)
    #robo.movel([location[0], location[1], location[2]+move_height_offset, orientation[0], orientation[1], orientation[2]], min_time = move_time)
    #robo.movel([location[0], location[1], location[2], orientation[0], orientation[1], orientation[2]], min_time = move_time)
    #robo.open_hand()
    #robo.movel([location[0], location[1], location[2]+move_height_offset, orientation[0], orientation[1], orientation[2]], min_time = move_time)

def circle(robo):
    centre= [0.33, -0.4]
    radius = 0.03
    time_per_rotation = 1
    z_val = 0.3
    points = np.linspace(0,math.pi*2,time_per_rotation*100)
    x = np.sin(points)*radius + centre[0]
    y = np.cos(points)*radius + centre[1]
    z = [z_val]*time_per_rotation*100
    circle_points_list = list(zip(x,y,z))
    return circle_points_list


    
    
    
stirrer_location = [0.308,-0.522, 0.07]
ladel_location = [0.085,-0.575, 0.10]
x_orinetation = [1.04, 2.50, 2.50]
y_orientation = [0.60,-1.5, -0.67]
vertical_orientation = [0.98, -2.42, -2.63]
def main():

    print("------------Configuring Burt-------------\r\n")

    burt = 0

    burt = kgr.kg_robot(port=30010,db_host="169.254.150.100", ee_port = 'COM3')

    print("----------------Hi Burt!-----------------\r\n\r\n")
    #startpos is ([-0.11, -0.36, 0.28, 1.04, 2.50, 2.50])
    #burt.open_hand()
    #time.sleep(5)
    #burt.close_hand()
    
    #grab_item(burt, stirrer_location, x_orinetation, 5)
    #stir(burt)
    
    #STIR EXAMPLE
    
    #burt.movel([0.33, -0.4, 0.3, 1.72,-0.82,-1.76], min_time = 3)
    #stir(burt)


    #HAND OPEN EXAMPLE
    
    #burt.open_hand()
    #time.sleep(5)
    #burt.close_hand()
    
    
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
    
    #grab_item(burt, ladel_location, y_orientation, 5)

    
    #burt.close_hand()
    #time.sleep(1)
    #burt.open_hand()
    #time.sleep(1)
    #burt.close_hand()
    #time.sleep(1)
    #burt.open_hand()
    #time.sleep(1)
    #burt.close_hand()
    #time.sleep(1)
    #burt.open_hand()
    #time.sleep(1)
    #burt.close_hand()
    #burt.movej([np.radians(-90), np.radians(-65), np.radians(-115), np.radians(-85), np.radians(90), np.radians(45)], min_time = 3) #move to first position slowly
    
    #print(burt.getl())
    
    #burt.movel(min_time)
    #burt.servoj([-0.110088, -0.313618, 0.701048, 1.156, 2.886, -0.15], lookahead_time = 10)
    
    #burt.servoj(burt.get_inverse_kin([-0.110088, -0.313618, 0.501048, 1.156, 2.886, -0.15], t=10))
    #
    #burt.servoj([-0.1980760896422284, -0.47090809213983564, 0.12714772882176902, 1.156, 2.886, -0.15])
    


    #burt.movel([val[0], val[1], val[2], 1.156, 2.886, -0.15], min_time = 5)
   
    #burt.servoj([val[0], val[1], val[2], 1.156, 2.886, -0.15], lookahead_time = 0.2, control_time = 0.1, gain = 100)

    burt.close()



if __name__ == '__main__': 
    
    main()