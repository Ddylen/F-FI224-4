# -*- coding: utf-8 -*-
"""
Code to convert a 3D camera coordinate vector to a 3D world coordinate vector
"""
import numpy as np
import math

def convert_2_world(camera_coords):
    #translation_vector = np.matrix([[-0.0162],    [0.5513],   [-1.4072]])
    xraw= 254
    yraw = 173
    
    x_normalised = xraw/424
    y_normalised = yraw/512
    
    x_scale_factor = 0.86*math.sin(math.radians(42.05)) # hand tunded value * value found Using FoV spec, this is the maximum object size that fits in half of FoV horizonally at 1m away
    y_scale_factor = 1.56*math.sin(math.radians(26.9)) # hand tunded value * value found Using FoV spec, this is the maximum object size that fits in half of FoV vertically at 1m away
    x_camera_coords = camera_coords.item(2)*2*(x_normalised-0.5)*x_scale_factor 
    
    y_camera_coords = camera_coords.item(2)*2*(y_normalised-0.5)*y_scale_factor
    #print("KEYVALS ARE", x_camera_coords, y_camera_coords)
    translation_vector = np.matrix([[x_camera_coords],    [y_camera_coords],   [1.414]]) #additions / subtarctions are by hand
    shifted_vector = camera_coords - translation_vector
    
    rotation_matrix = np.matrix([[0.9997, -0.0248, 0.0059],[0.0219, 0.9549, 0.2961],[-0.0130, -0.2959, 0.9551]])
    inv_rotation_matrix = rotation_matrix.getI()
    world_coords = inv_rotation_matrix*shifted_vector
    fine_tune = np.matrix([[-0.02], [-0.03], [0]])
    world_coords = world_coords -  fine_tune
    return world_coords