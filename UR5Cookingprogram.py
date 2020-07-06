"""
Final Program for carrying out pancake cooking with the UR5
"""
import sys
import numpy as np
import math
import time

import kg_robot as kgr
import waypoints as wp

sys.path.insert(1,r'C:\Users\birl\Documents\updated_ur5_controller\Generic_ur5_controller')


#Define tool locations
ladel_location = [0.04,-0.562, 0.113]
spatula_location = [-0.103, -0.507, 0.113]
whisk_location = [0.17, -0.422, 0.127]
cup_1_location = [0.340, -0.501, 0.156]
cup_2_location = [0.215, -0.501, 0.156]

#Define gripper orientations that work better/ worse with different types of tool
y_orientation = [0.60,-1.5, -0.67]
cup_orientation = [1.34, -0.65, 0.65]
spatula_orientation = [0.608,-1.455, -0.743]
drop_spatula_orientation = [0.659, -1.40, -0.905]
drop_spatula_location = [-0.104, -0.519, 0.11]
    
def grab_item(robo, location, orientation, move_time = 5, angle = 85, old = False):
    """Function to grab an item with the hand closed to a variety of angles"""
    
    #define offset to allow gripper to move above item without hitting it on the way there
    move_height_offset = 0.1
    
    #Check flag for if the older version of the gripping function on the arduino should be used
    if old == False:
        robo.open_hand()
    else:
        robo.open_hand_old()
        
    time.sleep(0.2)
    
    #Move to pick up tool
    robo.movel([location[0], location[1], location[2]+move_height_offset, orientation[0], orientation[1], orientation[2]], min_time = 1)
    robo.movel([location[0], location[1], location[2], orientation[0], orientation[1], orientation[2]], min_time = 3)
    
    #Close hand
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
    
    #Move gripper up with tool
    robo.movel([location[0], location[1], location[2]+move_height_offset, orientation[0], orientation[1], orientation[2]], min_time = 5)

    
def drop_item(robo, location, orientation,move_time = 5):
    """Funtion to drop a tool"""
    
    #define offset to allow gripper to move above tool holder without hitting it on the way there
    move_height_offset = 0.3
    
    #Move above tool holder
    robo.movejl([location[0], location[1], location[2]+move_height_offset, orientation[0], orientation[1], orientation[2]], min_time = move_time)
    
    #Move tool to holder
    robo.movejl([location[0], location[1], location[2]+0.02, orientation[0], orientation[1], orientation[2]], min_time = move_time, wait = True)
    
    #Open hand
    print("OPENING HAND")
    robo.open_hand()
    time.sleep(2)
    
    #Lift hand
    robo.movel([location[0], location[1], location[2]+move_height_offset, orientation[0], orientation[1], orientation[2]], min_time = move_time)


def stir(robo, total_time, time_per_rotation):
    """Function to stir the batter"""
    
    #define a trajectory for the stirring
    circle_points = circle(total_time, time_per_rotation)
    print(circle_points[0])
    
    #Move to first point on the stirring trajectory slowly
    robo.movel([circle_points[0][0],circle_points[0][1],circle_points[0][2], 1.77, 3.90, -1.61], min_time = 5)

    #move between each point on the stirring trajectory at a defined rate with a defined gripper pose
    for val in circle_points:
        robo.servoj([val[0], val[1], val[2],1.474, 4.212, -1.380], lookahead_time = 0.2, control_time = 0.01, gain = 100)
    
    #at end of stirring, move gripper up away from bowl
    robo.translatel_rel([0,0,0.05, 0,0,0], min_time = 1)


def circle(total_time, time_per_rotation):
    """Define a circular trajectory"""
    
    #define properties of the circle (centre, radius, height)
    centre= [0.355, -0.215]
    radius = 0.095
    z_val = 0.245
    
    #Define the number of points needed for the trajectory
    num_rotations = total_time/time_per_rotation
    num_points = int(num_rotations*time_per_rotation*100)
    points = np.linspace(0,num_rotations*math.pi*2,num_points)
    
    #Define x, y and z points for the circular trajectory
    x = np.sin(points)*radius + centre[0]
    y = np.cos(points)*radius + centre[1]
    z = [z_val]*num_points
    
    #Restructure the above lists into an (x,y,z) format
    circle_points_list = list(zip(x,y,z))
    
    return circle_points_list


def pour_ingredients(robo):
    """Function to pour water and pancake into into bowl"""
        
    #Go to home position
    robo.open_hand()
    robo.home(pose = wp.burt_homej, wait=False)
    
    #move above the cups
    robo.movej([np.radians(-45), np.radians(-110), np.radians(-90), np.radians(-161), np.radians(-45), np.radians(45)], min_time = 2)
    
    #grab cup 1, and pour it
    grab_item(robo, cup_1_location, cup_orientation, angle = 55)
    
    robo.teach_mode.play("pourcup1203201.json")
    
    #release cup one as the previous leaves it in roughly the correct position
    robo.open_hand()
    
    #Move gripper up to avoid collisions in the next instruction
    robo.translatel_rel([0,0,0.1, 0,0,0], min_time = 2)
    
    #grab cup 2 and pour it
    grab_item(robo, cup_2_location, cup_orientation, angle = 55)
    robo.teach_mode.play("pourcuptt9320.json")
  
    #release cup 2 as the previous leaves it in roughly the correct position
    robo.open_hand()
    
    #lift hand to ensure it doesnt hit cups when you move it
    robo.translatel_rel([0,0,0.1, 0,0,0], min_time = 2)
    
    
def whisk(robo, stirring_time, sit_time, startingtime):
    """Function to whisk the pancake mix"""
    
    #go above the whisk and grab it
    robo.movej([np.radians(-45), np.radians(-105), np.radians(-103), np.radians(-150), np.radians(45), np.radians(45)])
    grab_item(robo, whisk_location, y_orientation, angle = 85)
    
    #move up so the whisk wont hit the edge of the bowl in the next step
    robo.translatel_rel([0,0,0.1, 0,0,0], min_time = 2)
    
    #move above the bowl
    robo.movel([0.33, -0.22, 0.5, 1.77, 3.90, -1.61], min_time = 2)
    
    #stir
    stir(robo, total_time = stirring_time, time_per_rotation =  0.4)
    
    print(time.time()- startingtime, ": Batter Ready")
        
    #shake batter free from the whisk (not fully effective)
    robo.translatel_rel([0,0,0.07, 0,0,0], min_time = 0.25)
    robo.translatel_rel([0,0,-0.07, 0,0,0], min_time = 0.25)
    robo.translatel_rel([0,0,0.07, 0,0,0], min_time = 0.25)
    robo.translatel_rel([0,0,-0.07, 0,0,0], min_time = 0.25)
    robo.translatel_rel([0,0,0.07, 0,0,0], min_time = 0.25)
    robo.translatel_rel([0,0,-0.07, 0,0,0], min_time = 0.25)
    
    #move gripper up over the lip of the bowl
    robo.translatel_rel([0,0,0.15, 0,0,0], min_time = 2)
    
    #return the whisk
    drop_item(robo, whisk_location, y_orientation)
    
    #sleep so that the batter sits for the appropriate time
    sit_time_in_whisk = 27
    sit_time_in_pour = 44
    print(time.time()- startingtime, ": Letting Batter Sit")
    sleeptime1 = max(sit_time-sit_time_in_whisk-sit_time_in_pour,0)
    print("sleep for", sleeptime1)
    time.sleep(sleeptime1)
    
    
def pour_batter(robo, cookingtime1, startingtime):
    """Function to pour batter into the hotplate"""
    
    #move over the ladle and grab it
    robo.movej([np.radians(-67), np.radians(-112), np.radians(-87), np.radians(-161), np.radians(26), np.radians(43)], min_time = 2)
    robo.open_hand()
    grab_item(robo, ladel_location, y_orientation, angle = 80, old = True)
    
    #scoop the batter, leaving the ladle over the bowl
    robo.teach_mode.play_fast("scoop93201.json", speedup = 3)
    
    #pour the batter into the pan
    robo.teach_mode.play("pour93201.json")
    
    #return the ladle
    drop_item(robo, ladel_location, y_orientation)
    
    #sleep so that the pancake cooks for the appropriate amount of time
    cook1_time_in_pour = 52
    cook1_time_in_pick = 30
    print(time.time()- startingtime, ": Cooking Pancakes Side 1")
    sleeptime2 = max(cookingtime1-cook1_time_in_pour-cook1_time_in_pick,0)
    print("sleep for", sleeptime2)
    time.sleep(sleeptime2)
    

def flip_pancakes(robo, cookingtime2, startingtime):
    """Function to flip the pancakes"""
    
    #move above the spatula and grab it
    robo.movej([np.radians(-80), np.radians(-110), np.radians(-89), np.radians(-170), np.radians(14), np.radians(49)], min_time = 2)
    grab_item(robo, spatula_location, spatula_orientation)
    
    #Pick up the pancake and hold it above the pan
    robo.teach_mode.play("pick163201.json")
    
    #Move to a reference position slowly (nominally where the last action ends, then flip the pancake)
    robo.movej([np.radians(-20), np.radians(-111), np.radians(-93), np.radians(-87), np.radians(83), np.radians(99)], min_time = 2)
    robo.teach_mode.play("flip93202.json")    
    
    #Sleep so that the other side of the pancake cooks for an appropriate amount of time
    cook2_time_in_flip =13
    cook2_time_in_pickup = 0
    print(time.time()- startingtime, ": Cooking Pancakes Side 2")
    sleeptime3= max(cookingtime2-cook2_time_in_flip-cook2_time_in_pickup,0)
    print("sleep for", sleeptime3)
    time.sleep(sleeptime3)
    

def remove_pancakes(robo, startingtime):
    """Function to remove pancakes from the pan"""
    
    #Move to a reference position above the pan
    robo.movej([np.radians(-16), np.radians(-106), np.radians(-96), np.radians(-85), np.radians(86), np.radians(113)], min_time = 2)
    
    #Attempt to pick up and serve pancakes
    robo.teach_mode.play("pickup93202.json") 
    
    #Move spatula back to the tool holder location and replace it
    robo.movej([np.radians(-54), np.radians(-113), np.radians(-69), np.radians(-111), np.radians(93), np.radians(69)], min_time = 4)
    drop_item(robo, drop_spatula_location, drop_spatula_orientation)
 
    print(time.time()- startingtime, ": Pancakes Ready")
    
    
def cook(stir_time, batter_sit_time, cook1_time, cook2_time, use_gripper = True):
    """Main cooking program"""

    #STAGE 0: ROBOT INITIALISATION_____________________________________________
    print("----------------Initialising Robot-----------------\r\n")
    
    #TODO: Check with Keiran if this define from his code is redundant
    burt = 0
    
    #Initialise robot, deciding whether or not to talk to the gripper (initilaising the robot opens the gripper, so during debugging if we have something in the gripper we dont want released, use use_gripper == False)
    if use_gripper == True:
        burt = kgr.kg_robot(port=30010,db_host="169.254.150.100", ee_port="COM3")
    
    elif use_gripper == False:
        burt = kgr.kg_robot(port=30010,db_host="169.254.150.100")
        
    print("----------------Robot Initialised-----------------\r\n\r\n")

    start_time = time.time()
    
    #Define which cooking stages we want to execute
    stage1 = True
    stage2 = True
    stage3 = True
    stage4 = True
    stage5 = True
    
    #STAGE 1: POUR INGREDIENTS_________________________________________________
    if stage1 == True:
        pour_ingredients(burt)
    
    #STAGE 2: WHISK BOOGALOO___________________________________________________
    if stage2 == True:
        whisk(burt, stir_time, batter_sit_time, start_time)
        
    #STAGE 3: POUR BATTER______________________________________________________
    if stage3 == True:
        pour_batter(burt, cook1_time, start_time)
        
    #STAGE 4: FLIP PANCAKES____________________________________________________
    if stage4 == True:
       flip_pancakes(burt, cook2_time, start_time)
        
    #STAGE 5: REMOVE PANCAKES__________________________________________________
    if stage5 == True:
       remove_pancakes(burt, start_time)

    #Reset connection with UR5 to avoid issue where gripper does not accept commands when this code is run a second time
    burt.ee.reset_output_buffer()
    burt.ee.close()
    print("reset")
    burt.close()

if __name__ == '__main__': 

    cook(stir_time=21.4, batter_sit_time=0, cook1_time=95.7, cook2_time=133.6, use_gripper = True)