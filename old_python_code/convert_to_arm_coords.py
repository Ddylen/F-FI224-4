# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 17:18:46 2019

@author: birl
"""

import math
from convert_2_world import convert_2_world
import numpy as np
def convert_to_arm_coords(x_input, y_input, depth_frame, return_depth = False):
    x_scale_factor = math.sin(math.radians(42.05)) # Using FoV spec, this is the maximum object size that fits in half of FoV horizonally at 1m away
    y_scale_factor = math.sin(math.radians(26.9)) # Using FoV spec, this is the maximum object size that fits in half of FoV vertically at 1m away



    x_normalised = x_input
    y_normalised = y_input
    depthfromcam = depth_frame[((int(y_input*512) * 512) + int(x_input*424))]/1000 # we need to specify pixel number, not x,y coordinates
    if depthfromcam == 0.0:
        outputmat =  np.matrix([[-111], [-111], [-111]])
    else:
        x_camera_coords = depthfromcam* 0.86*2*(x_normalised-0.5)*x_scale_factor 
        y_camera_coords = depthfromcam* 1.56*2*(y_normalised-0.5)*y_scale_factor # i think my scaling method is off by a bit
        board_coords = convert_2_world(np.matrix([[x_camera_coords], [y_camera_coords], [depthfromcam]])) #TODO: confirm that this transformation applies for normalised pixel coordinates
        #print(board_coords.item(0), board_coords.item(1), board_coords.item(2))
        #print("pos is ", x, y, "depth is ", Pixel_Depth)
        #print("board coords is",board_coords.item(0), board_coords.item(1), board_coords.item(2))
        
        board_to_arm_translation = np.matrix([[0.1],[0.39],[0.4]])#measured from board to arm 0,0,0 position
        arm_coords_twisted = board_coords + board_to_arm_translation
        arm_coords = np.matrix([[- arm_coords_twisted.item(0)], [-arm_coords_twisted.item(1)], [-arm_coords_twisted.item(2)]]) #axes for arm are other way round to that of checkerboard
        outputmat =  arm_coords
    if return_depth == False:
        return outputmat
    else:
        return outputmat, depthfromcam