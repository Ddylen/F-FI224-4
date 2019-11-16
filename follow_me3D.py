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


def main():
    
    frame_rate = 0.1 #"""TO DO: SORT OUT IF I NEED TO ONLY USE CERTAIN JSON MESSAGES TO GET ARROUND THIS FRAME RATE THING"""
    palm_list = interpret2D('TRIAL_JSONS', 'wrist')
    arm_pos_list = []

    
    
    depthdatafile = open("depthdata/DEPTH11.15.13.49.pickle", "rb")
    
    
    for val in palm_list:
        x_normalised = val[0]
        y_normalised = 1-val[1] # these are X and Y in terms of the normalised pixel value they are at
        depthframe = pickle.load(depthdatafile) #need to do this once per frame
        depthfromcam = depthframe[round(x_normalised*424)][round(y_normalised*512)] # TODO: include some smoothing here
    """-- keypoint_scale 3 gives top left as (0,0) and bottom right as (1,1), then reflects y"""
    
    """!!!! CHECK THE LINE BELOW!!!"""
        board_coords = convert_2_world(np.matrix([x_normalised], [y_normalised], [depthfromcam])) #TODO: confirm that this transformation applies for normalised pixel coordinates
    """!!!! CHECK THE LINE ABOVE!!!"""
        board_to_arm_translation = np.matrix([0],[0],[0])#TODO: MEASURE THIS, in arm coords , from board to arm I think
        arm_coords_twisted = board_coords + board_to_arm_translation
        arm_coords = np.matrix(- arm_coords_twisted._getitem(0), - arm_coords_twisted._getitem(1), arm_coords_twisted._getitem(2)) #axes for arm are other way round to that of checkerboard
        arm_pos_list.append(arm_coords)
    
    
    """TODO: MEASURE THESE LIMITS !!!!!!!"""
    xlim = [-1,1] # x allowable range
    ylim = [-0.2, -1] # y allowable range
    zlim = [0, 1]
    

    for val in arm_pos_list:
        if 
            
    
    
    print(arm_pos_list)
    print("------------Configuring Burt-------------\r\n")

    burt = 0

    burt = kgrs.specialised_kg_robot(port=30010,db_host="169.254.251.50")

    print("----------------Hi Burt!-----------------\r\n\r\n")
    
    "TODO: NEW FIRST POSITION"
    burt.movej([np.radians(38), np.radians(-128), np.radians(150), np.radians(244), np.radians(-85), np.radians(-7)], min_time = 5) #move to first position slowly
    #CHANGE TO MOVE TO CORRECT INITIONALISATION POSE
    
    print("moved to start")
    for val in arm_pos_list:
        if time.sleep(val._getitem(0)> xlim[1] or val._getitem(0) < xlim[0] or val._getitem(1)> ylim[1] or val._getitem(1) < ylim[0] or val._getitem(2)> zlim[1] or val._getitem(2) < zlim[0]):
            print("Invalid point, sleeping for a frame")
            time_min = 1 #TODO: This is hacky, find something better
            continue
        else:
            time_min = frame_rate
    
        if(time_min = frame_rate):

            print("Go to ", val._getitem(0), val._getitem(1), val._getitem(2))
        
        burt.servoj([val._getitem(0), val._getitem(1), val._getitem(2), 1.156, 2.886, -0.15])
       
    
    burt.close()

if __name__ == '__main__': main()
