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

#spatula_location = [-0.103, -0.507, 0.116]
spatula_location = [-0.103, -0.507, 0.113]
whisk_location = [0.17, -0.425, 0.127]

cup_1_location = [0.340, -0.501, 0.156]
cup_2_location = [0.215, -0.501, 0.156]
x_orinetation = [1.04, 2.50, 2.50]
y_orientation = [0.60,-1.5, -0.67]
y_orientation_reverse = [1.78,0.52, 1.69]
vertical_orientation = [0.98, -2.42, -2.63]
cup_orientation = [1.34, -0.65, 0.65]
spatula_orientation = [0.608,-1.455, -0.743]

drop_spatula_orientation = [0.659, -1.40, -0.905]
drop_spatula_location = [-0.106, -0.519, 0.11]

    
def grab_item(robo, location, orientation, move_time = 5, angle = 85, old = False):
    move_height_offset = 0.1
    if old == False:
        robo.open_hand()
    else:
        robo.open_hand_old()
    time.sleep(0.2)
    robo.movel([location[0], location[1], location[2]+move_height_offset, orientation[0], orientation[1], orientation[2]], min_time = 1)
    robo.movel([location[0], location[1], location[2], orientation[0], orientation[1], orientation[2]], min_time = 3)
    print("CLOSING HAND")
    if angle == 55:
        robo.close_hand()
    elif angle == 85:
        robo.close_hand_85()
    elif angle == 90:
        robo.close_hand_90()
    elif angle == 95:
        robo.close_hand_95()
    elif angle == 100:
        robo.close_hand_100()
    elif angle == 110:
        robo.close_hand_110()
    elif angle == 80:
        robo.fat_close_hand()
    else:
        raise ValueError
        
    robo.movel([location[0], location[1], location[2]+move_height_offset, orientation[0], orientation[1], orientation[2]], min_time = 5)


    
def drop_item(robo, location, orientation,move_time = 5):
    move_height_offset = 0.3
    robo.movejl([location[0], location[1], location[2]+move_height_offset, orientation[0], orientation[1], orientation[2]], min_time = move_time)
    robo.movejl([location[0], location[1], location[2]+0.02, orientation[0], orientation[1], orientation[2]], min_time = move_time, wait = True)

    print("OPENING HAND")
    robo.open_hand()
    time.sleep(2)

    robo.movel([location[0], location[1], location[2]+move_height_offset, orientation[0], orientation[1], orientation[2]], min_time = move_time)


def stir(robo, total_time, time_per_rotation):

    circle_points = circle(total_time, time_per_rotation)
    print(circle_points[0])

    robo.movel([circle_points[0][0],circle_points[0][1],circle_points[0][2], 1.77, 3.90, -1.61], min_time = 5)

    
    for val in circle_points:

        robo.servoj([val[0], val[1], val[2],1.77, 3.90, -1.61], lookahead_time = 0.2, control_time = 0.01, gain = 100)
    

    robo.translatel_rel([0,0,0.05, 0,0,0], min_time = 1)


def circle(total_time, time_per_rotation):

    centre= [0.355, -0.19]

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




def main(stir_time, batter_sit_time, cook1_time, cook2_time, use_gripper = True):

    #STAGE 0: ROBOT INITIALISATION_____________________________________________
    print("----------------Initialising Robot-----------------\r\n")

    burt = 0
    
    #Initialise robot, deciding whether or not to talk to the gripper (initilaising the robot opens the gripper, so during debugging if we have something in the gripper we dont want released, use, use_gripper == False)
    if use_gripper == True:
        burt = kgr.kg_robot(port=30010,db_host="169.254.150.100", ee_port="COM3")
    
    elif use_gripper == False:
        burt = kgr.kg_robot(port=30010,db_host="169.254.150.100")
        
    print("----------------Robot Initialised-----------------\r\n\r\n")

    start_time = time.time()
    
    for i in range(10):
        burt.movej([np.radians(-67), np.radians(-112), np.radians(-87), np.radians(-161), np.radians(26), np.radians(43)], min_time = 2)
        burt.open_hand()
        grab_item(burt, ladel_location, y_orientation, angle = 80, old = True)
        burt.translatel_rel([0,0,0.1, 0,0,0], min_time = 2)
        time.sleep(3)
        #scoop the batter, leaving the ladel over the bowl
        burt.teach_mode.play("scoop93201.json")
        
        #pour the batter into the pan
        #burt.teach_mode.play("pour93201.json")
        
        #return the ladel
        drop_item(burt, ladel_location, y_orientation)
        time.sleep(15)
    
    
    
    stage1 = False
    stage2 = False
    stage3 = False
    stage4 = False
    stage5 = False
    
    
    #STAGE 1: POUR INGREDIENTS_________________________________________________
    if stage1 == True:
        #Go to home position
        burt.open_hand()
        burt.home(pose = wp.burt_homej, wait=False)
        
        #move above the cups
        burt.movej([np.radians(-45), np.radians(-110), np.radians(-90), np.radians(-161), np.radians(-45), np.radians(45)], min_time = 2)
        
        #grab cup 1, and pour it
        grab_item(burt, cup_1_location, cup_orientation, angle = 55)
        
        
        burt.teach_mode.play("pourcup93201.json") #cup 1
  
        #burt.teach_mode.play("pour_cup_1.json")
        
        #release cup one as the previous leaves it in roughly the correct position
        burt.open_hand()
        
        burt.translatel_rel([0,0,0.1, 0,0,0], min_time = 2)
        
        #grab cup 2 and pour it
        grab_item(burt, cup_2_location, cup_orientation, angle = 55)
        
        burt.teach_mode.play("pourcuptt9320.json") # cup 2
      
        #release cup 2 as the previous leaves it in roughly the correct position
        burt.open_hand()
        
        #lift hand to ensure it doesnt hit cups when you move it
        burt.translatel_rel([0,0,0.1, 0,0,0], min_time = 2)

        
    #STAGE 2: WHISK BOOGALOO___________________________________________________
    if stage2 == True:
        #go above the whisk and grab it
        burt.movej([np.radians(-45), np.radians(-105), np.radians(-103), np.radians(-150), np.radians(45), np.radians(45)])
        grab_item(burt, whisk_location, y_orientation, angle = 85)
        
        #move up so the whisk wont hit the edge of the bowl in the next step
        burt.translatel_rel([0,0,0.1, 0,0,0], min_time = 2)
        
        #move above the bowl
        burt.movel([0.33, -0.22, 0.5, 1.77, 3.90, -1.61], min_time = 2)
        
        #stir
        stir(burt, total_time = stir_time, time_per_rotation =  0.44)
        
        print(time.time()- start_time, ": Batter Ready")
            
        #shake battery free from the whisk (no very effective)
        burt.translatel_rel([0,0,0.07, 0,0,0], min_time = 0.25)
        burt.translatel_rel([0,0,-0.07, 0,0,0], min_time = 0.25)
        burt.translatel_rel([0,0,0.07, 0,0,0], min_time = 0.25)
        burt.translatel_rel([0,0,-0.07, 0,0,0], min_time = 0.25)
        burt.translatel_rel([0,0,0.07, 0,0,0], min_time = 0.25)
        burt.translatel_rel([0,0,-0.07, 0,0,0], min_time = 0.25)
        
        #move over lip of the bowl
        burt.translatel_rel([0,0,0.15, 0,0,0], min_time = 2)
        
        #return the whisk
        drop_item(burt, whisk_location, y_orientation)
        
        #sleep so that the batter sits for the appropriate time
        batter_sit_time_in_whisk = 27
        batter_sit_time_in_pour = 44
        print(time.time()- start_time, ": Letting Batter Sit")
        time.sleep(min(batter_sit_time-batter_sit_time_in_whisk-batter_sit_time_in_pour, 0))
    
    
    #STAGE 3: POUR BATTER______________________________________________________
    if stage3 == True:
        #move over the ladel and grab it
        burt.movej([np.radians(-67), np.radians(-112), np.radians(-87), np.radians(-161), np.radians(26), np.radians(43)], min_time = 2)
        burt.open_hand()
        grab_item(burt, ladel_location, y_orientation, angle = 80, old = True)
        
        #scoop the batter, leaving the ladel over the bowl
        burt.teach_mode.play("scoop93201.json")
        
        #pour the batter into the pan
        burt.teach_mode.play("pour93201.json")
        
        #return the ladel
        drop_item(burt, ladel_location, y_orientation)
        
        #sleep so that the pancake cooks for the appropriate amount of time
        cook1_time_in_pour = 52
        cook1_time_in_pick = 40
        print(time.time()- start_time, ": Cooking Pancakes Side 1")
        time.sleep(min(cook1_time-cook1_time_in_pour-cook1_time_in_pick,0))
 
    
    #STAGE 4: FLIP PANCAKES____________________________________________________
    if stage4 == True:
        #move above the spatula and grab it
        burt.movej([np.radians(-80), np.radians(-110), np.radians(-89), np.radians(-170), np.radians(14), np.radians(49)], min_time = 2)
        grab_item(burt, spatula_location, spatula_orientation)
        
        #Pick up the pancake and hold it above the pan
        burt.teach_mode.play("pick93201.json") 
        
        #Move to a reference position slowly (nominally where the last action ends, then flip the pancake)
        burt.movej([np.radians(-20), np.radians(-111), np.radians(-93), np.radians(-87), np.radians(83), np.radians(99)], min_time = 2)
        burt.teach_mode.play("flip93202.json")    
        
        #Sleep so that the other side of the pancake cooks for an appropriate amount of time
        cook2_time_in_flip =20
        cook2_time_in_pickup = 0
        print(time.time()- start_time, ": Cooking Pancakes Side 2")
        time.sleep(min(cook2_time-cook2_time_in_flip-cook2_time_in_pickup,0))
        
    
    #STAGE 5: REMOVE PANCAKES___________________________________________________
    if stage5 == True:
        #Move to a reference position above the pan
        burt.movej([np.radians(-16), np.radians(-106), np.radians(-96), np.radians(-85), np.radians(86), np.radians(113)], min_time = 2)
        
        #Attempt to pick up pancakes (and probably fail)
        burt.teach_mode.play("pickup93202.json") 
        
        #Move spatula back to the appropriate location and release it
        burt.movej([np.radians(-54), np.radians(-113), np.radians(-69), np.radians(-111), np.radians(93), np.radians(69)], min_time = 4)
        drop_item(burt, drop_spatula_location, drop_spatula_orientation)
     
    
        print(time.time()- start_time, ": Pancakes Ready")


    burt.ee.reset_output_buffer()
    burt.ee.close()
    print("reset")
    burt.close()



if __name__ == '__main__': 
    
    main(stir_time=15, batter_sit_time=0, cook1_time=210, cook2_time=210, use_gripper = True)