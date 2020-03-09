# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 18:02:58 2020

@author: birl
"""

"""
Program for carrying out cooking stages with the UR5
"""

import sys
sys.path.insert(1,r'C:\Users\birl\Documents\updated_ur5_controller\Generic_ur5_controller')
import numpy as np
import math
import time

import kg_robot as kgr
import waypoints as wp

stirrer_location = [0.159, -0.53, 0.09]
ladel_location = [0.04,-0.562, 0.113]

spatula_location = [-0.103, -0.507, 0.116]
whisk_location = [0.17, -0.425, 0.127]

cup_1_location = [0.340, -0.504, 0.156]
cup_2_location = [0.215, -0.504, 0.156]
x_orinetation = [1.04, 2.50, 2.50]
y_orientation = [0.60,-1.5, -0.67]
y_orientation_reverse = [1.78,0.52, 1.69]
vertical_orientation = [0.98, -2.42, -2.63]
cup_orientation = [1.34, -0.65, 0.65]
spatula_orientation = [0.608,-1.455, -0.743]

drop_spatula_orientation = [0.659, -1.40, -0.905]
drop_spatula_location = [-0.106, -0.519, 0.11]

def grab_stirrer(robo):
    robo.open_hand()
    robo.movel([0.29,-0.52,0.26, 1.04, 2.50, 2.50], min_time = 5, wait = True)
    robo.movel([0.29,-0.52,0.10, 1.04, 2.50, 2.50], min_time = 5, wait = True)
    robo.close_hand()
    robo.translatel_rel([0,0,0.1, 0,0,0], min_time = 3, wait = True)
    
    robo.movel([-0.11, -0.36, 0.28, 0.60,-1.5, -0.67], min_time = 5, wait = True)
    pass

def grab_item(robo, location, orientation, move_time = 5):
    move_height_offset = 0.1

    robo.open_hand()

    time.sleep(0.2)
    robo.movel([location[0], location[1], location[2]+move_height_offset, orientation[0], orientation[1], orientation[2]], min_time = 2)
    robo.movel([location[0], location[1], location[2], orientation[0], orientation[1], orientation[2]], min_time = 5)
    print("start grab")
    robo.close_hand()
    #time.sleep(1)
    #robo.close_hand()
    #input("Press enter")
    #time.sleep(5)
    #robo.close_hand()

    robo.movel([location[0], location[1], location[2]+move_height_offset, orientation[0], orientation[1], orientation[2]], min_time = 5)

    #robo.close_hand()
    
def grab_big_item(robo, location, orientation, move_time = 5, angle = 85, old = False):
    move_height_offset = 0.1
    if old == False:
        robo.open_hand()
    else:
        robo.open_hand_old()
    time.sleep(0.2)
    robo.movel([location[0], location[1], location[2]+move_height_offset, orientation[0], orientation[1], orientation[2]], min_time = 2)
    robo.movel([location[0], location[1], location[2], orientation[0], orientation[1], orientation[2]], min_time = 5)
    print("start grab")
    #robo.fat_close_hand()
    if angle == 55:
        robo.close_hand()
    if angle == 85:
        robo.close_hand_85()
    if angle == 90:
        robo.close_hand_90()
    if angle == 95:
        robo.close_hand_95()
    if angle == 100:
        robo.close_hand_100()
    if angle == 110:
        robo.close_hand_110()
    if angle == 80:
        robo.fat_close_hand()
    robo.movel([location[0], location[1], location[2]+move_height_offset, orientation[0], orientation[1], orientation[2]], min_time = 5)

    #robo.close_hand()
    
def drop_item(robo, location, orientation,move_time = 5):
    move_height_offset = 0.3
    #robo.close_hand()
    robo.movejl([location[0], location[1], location[2]+move_height_offset, orientation[0], orientation[1], orientation[2]], min_time = move_time)
    robo.movejl([location[0], location[1], location[2]+0.02, orientation[0], orientation[1], orientation[2]], min_time = move_time, wait = True)

    time.sleep(2)
    print("OPENING HAND")
    robo.open_hand()
    time.sleep(2)
    robo.open_hand()
    time.sleep(2)
    """
    robo.translatel_rel([0,0,0.09, 0,0,0], min_time = 0.3)
    robo.translatel_rel([0,0,-0.09, 0,0,0], min_time = 0.3)
    robo.translatel_rel([0,0,0.09, 0,0,0], min_time = 0.3)
    robo.open_hand()
    robo.translatel_rel([0,0,-0.09, 0,0,0], min_time = 0.3)
    robo.translatel_rel([0,0,0.09, 0,0,0], min_time = 0.3)
    robo.translatel_rel([0,0,-0.09, 0,0,0], min_time = 0.3)
    
    robo.translatel_rel([0,0,0.09, 0,0,0], min_time = 0.3)
    robo.translatel_rel([0,0,-0.09, 0,0,0], min_time = 0.3)
    robo.translatel_rel([0,0,0.09, 0,0,0], min_time = 0.3)
    """
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
    robo.translatel_rel([0,0,0.05, 0,0,0], min_time = 1)
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
    centre= [0.355, -0.19]
    #radius = 0.05
    #z_val = 0.302
    radius = 0.065
    z_val = 0.247
    num_rotations = total_time/time_per_rotation
    num_points = int(num_rotations*time_per_rotation*100)
    points = np.linspace(0,num_rotations*math.pi*2,num_points)
    x = np.sin(points)*radius + centre[0]
    y = np.cos(points)*radius + centre[1]
    z = [z_val]*num_points
    circle_points_list = list(zip(x,y,z))
    return circle_points_list


    
    
    


def get_cups(robo):

    robo.movej([np.radians(-45), np.radians(-110), np.radians(-90), np.radians(-161), np.radians(-45), np.radians(45)], min_time = 2.5)
    #time.sleep(20)
    
    grab_item(robo, cup_1_location, cup_orientation)
    robo.teach_mode.play("pour_cup_1.json")
    robo.open_hand()

    grab_item(robo, cup_2_location, cup_orientation)
    robo.teach_mode.play("pour_cup_2.json")
    robo.open_hand()
    time.sleep(10)
    robo.translatel_rel([0,0,0.1, 0,0,0], min_time = 3)

def whisk_actions(robo):
    robo.movej([np.radians(-45), np.radians(-105), np.radians(-103), np.radians(-150), np.radians(45), np.radians(45)])
    grab_big_item(robo, whisk_location, y_orientation, angle = 85)
    
    robo.translatel_rel([0,0,0.1, 0,0,0], min_time = 3)
    
    robo.movel([0.33, -0.22, 0.5, 1.77, 3.90, -1.61], min_time = 3)
    


    stir(robo, total_time = 20, time_per_rotation =  0.5)
    
    robo.translatel_rel([0,0,0.07, 0,0,0], min_time = 0.5)
    robo.translatel_rel([0,0,-0.07, 0,0,0], min_time = 0.5)
    robo.translatel_rel([0,0,0.07, 0,0,0], min_time = 0.5)
    robo.translatel_rel([0,0,-0.07, 0,0,0], min_time = 0.5)
    robo.translatel_rel([0,0,0.07, 0,0,0], min_time = 0.5)
    robo.translatel_rel([0,0,-0.07, 0,0,0], min_time = 0.5)
    
    robo.translatel_rel([0,0,0.15, 0,0,0], min_time = 2)
    drop_item(robo, whisk_location, y_orientation)

def main():

    print("------------Configuring Burt-------------\r\n")

    burt = 0

    #burt = kgr.kg_robot(port=30010,db_host="169.254.150.100", ee_port="COM3")
    burt = kgr.kg_robot(port=30010,db_host="169.254.150.100")
    print("----------------Hi Burt!-----------------\r\n\r\n")



    """
    #STAGE 1___________________________________________________________________
    burt.open_hand()
    burt.home(pose = wp.burt_homej, wait=False)
    get_cups(burt)


    #STAGE 2___________________________________________________________________
    whisk_actions(burt)

 
    #STAGE 3___________________________________________________________________
    burt.movej([np.radians(-67), np.radians(-112), np.radians(-87), np.radians(-161), np.radians(26), np.radians(43)], min_time = 3)
    burt.open_hand()
    grab_big_item(burt, ladel_location, y_orientation, angle = 80, old = True)
    
    burt.teach_mode.play("scoop93201.json")

    burt.teach_mode.play("pour93201.json") #works
    drop_item(burt, ladel_location, y_orientation)

    time.sleep(180)
    """   
    #STAGE 4___________________________________________________________________
    """
    burt.movej([np.radians(-80), np.radians(-110), np.radians(-89), np.radians(-170), np.radians(14), np.radians(49)], min_time = 4)
    grab_big_item(burt, spatula_location, spatula_orientation)
    burt.teach_mode.play("pick93201.json")    #picks up pancake
    """
    """
    burt.movej([np.radians(-20), np.radians(-111), np.radians(-93), np.radians(-87), np.radians(83), np.radians(99)], min_time = 4)
    burt.teach_mode.play("flip93202.json")    #picks up pancake
    
    
    #burt.movej([np.radians(-54), np.radians(-113), np.radians(-69), np.radians(-111), np.radians(93), np.radians(69)], min_time = 8)
    
    time.sleep(180)
    #STAGE 5___________________________________________________________________
    """
    burt.movej([np.radians(-16), np.radians(-106), np.radians(-96), np.radians(-85), np.radians(86), np.radians(113)], min_time = 4)
    burt.teach_mode.play("pickup93202.json")    #picks up pancake
 
    burt.movej([np.radians(-54), np.radians(-113), np.radians(-69), np.radians(-111), np.radians(93), np.radians(69)], min_time = 4)
    drop_item(burt, drop_spatula_location, drop_spatula_orientation)
 



    burt.ee.reset_output_buffer()
    burt.ee.close()
    print("reset")
    burt.close()



if __name__ == '__main__': 
    
    main()