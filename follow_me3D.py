# -*- coding: utf-8 -*-
"""
Code for smoothly following a human demonstrator in 3D
TODO: NOT FINISED YET
TASKS:
    1) figure out how to get a vector position from the camera (the x and y are in pixels but z is in depth, how do I convert?)- ask toby
    2) Find the board to arm translation
    3) Find new initilaisation pose
    4) Video claims to be at 30fps but is actually at 10 fps, could cuase issues - I THINK THE VIDEO WAS ACTUALLY TAKEN AT 30 NOT 10 FPS, TRY A NEW VIDEO
    5) Change time between values on the arm to 0.1s
    6) Review my coordinate trasnforms and check the paths I get out of some test code look sensible
"""

import sys
sys.path.insert(1,r'C:\Users\birl\Documents\ur5_python_host\ur5_kg_robot')
import numpy as np
import math
import time
from math import pi
import pickle
import waypoints as wp
from kg_robot import kg_robot
from reader import interpret2D
from convert_2_world import convert_2_world
import specialised_kg_robot_example as kgrs 

"""
SOMETHING IS GOINT WRONG IN SCALING WITH HEIGHT
"""
def main():
    
    frame_rate = 0.1 
    palm_list = interpret2D('circle', 'wrist')
    #print(palm_list)
    arm_pos_list = []

    
    
    depthdatafile = open("depthdata/DEPTH11.19.16.50.pickle", "rb")
    x_scale_factor = math.sin(math.radians(42.05)) # Using FoV spec, this is the maximum object size that fits in half of FoV horizonally at 1m away
    y_scale_factor = math.sin(math.radians(26.9)) # Using FoV spec, this is the maximum object size that fits in half of FoV vertically at 1m away
    
    for val in palm_list:
        x_normalised = val[0]
        y_normalised = 1-val[1] # these are X and Y in terms of the normalised pixel value they are at
        #print(x_normalised, y_normalised)
        """From one sample, normalised values look roughly correct"""
        depthframe = pickle.load(depthdatafile) #need to do this once per frame
        #print(depthframe)
        depthframe = np.reshape(depthframe, (424, 512))
        #print(depthframe)
        #print(round(x_normalised*424))
        #print(round(y_normalised*512))
        depthfromcam = depthframe[round(x_normalised*424)][round(y_normalised*512)]/1000 #converted to m from mm # TODO: include some smoothing here
        
        x_camera_coords = depthfromcam* 0.86*2*(x_normalised-0.5)*x_scale_factor 
        y_camera_coords = depthfromcam* 1.56*2*(y_normalised-0.5)*y_scale_factor # i think my scaling method is off by a bit
        #print(x_camera_coords,y_camera_coords,depthfromcam)
        
        """From one sample, camera coordinates look roughly correct (but the place i checked was near the origin, should check somewhere off it"""
        if depthfromcam != 0.0:

            board_coords = convert_2_world(np.matrix([[x_camera_coords], [y_camera_coords], [depthfromcam]])) #TODO: confirm that this transformation applies for normalised pixel coordinates
            print(board_coords.item(0), board_coords.item(1), board_coords.item(2))
            
            board_to_arm_translation = np.matrix([[0.1],[0.39],[0.4]])#measured from board to arm 0,0,0 position
            arm_coords_twisted = board_coords + board_to_arm_translation
            arm_coords = np.matrix([[- arm_coords_twisted.item(0)], [-arm_coords_twisted.item(1)], [-arm_coords_twisted.item(2)]]) #axes for arm are other way round to that of checkerboard
            arm_pos_list.append(arm_coords)
    
    
    """TODO: MEASURE THESE LIMITS !!!!!!!"""
    xlim = [-0.4,0.4] # x allowable range
    ylim = [-0.22, -0.6] # y allowable range
    zlim = [-0.32, 1]
    
            
    
    
    #print(arm_pos_list)

    print("------------Configuring Burt-------------\r\n")

    burt = 0

    burt = kgrs.specialised_kg_robot(port=30010,db_host="169.254.150.100")

    print("----------------Hi Burt!-----------------\r\n\r\n")
    
    "TODO: NEW FIRST POSITION"
    burt.movej([np.radians(-318), np.radians(-99), np.radians(156), np.radians(214), np.radians(-90), np.radians(45)], min_time = 5) #move to first position slowly
    #CHANGE TO MOVE TO CORRECT INITIONALISATION POSE
    first_round = 0
    print("moved to start")
    for val in arm_pos_list:
        if time.sleep(val._getitem(0)> xlim[1] or val._getitem(0) < xlim[0] or val._getitem(1)> ylim[1] or val._getitem(1) < ylim[0] or val._getitem(2)> zlim[1] or val._getitem(2) < zlim[0]):
            print("Invalid point, sleeping for a frame")
            time_min = 1 #TODO: This is hacky, find something better
            continue
        elif first_round == 0:
            time_min = 3
            first_round = 1
        else:
            time_min = frame_rate
    
        if(time_min == frame_rate):

            print("Go to ", val._getitem(0), val._getitem(1), val._getitem(2))
        
        burt.servoj([val._getitem(0), val._getitem(1), val._getitem(2), 1.156, 2.886, -0.15])
       
    
    burt.close()

if __name__ == '__main__': main()
