"""
Program to convert camera coords to word coords in the new camera position from 14/02/20, hand tuned as precise as possible
"""
import numpy as np


def convert_2_world(x,y,z):
    """Convert Camera coordinates to world coordinates (i.e. x, y and z aligned to the work surface)
    Note that this functiono built off the output of the matlab camera calibration tool which turned out to be inaccurate, 
    hence the two seperate definitions of the rotations and translations required"""  
    
    #Convert input coords to numpy matrix
    input_coords = np.matrix([[x,y,z]])
    
    #Rotation matrix obtained from matlab camera calibration tool (one axis is way off because the tool isnt working correctly - I suspect my A3 calibration grids are too small)
    rotation_matrix = np.matrix([[-0.9978,   -0.0316,   -0.0577],[-0.0007,   -0.8722,    0.4891],[-0.0658,    0.4881,    0.8703]])
    inv_rotation_matrix = rotation_matrix.getI()
    
    #Define hand tunded rotations in each axis to correct the error in the matlab camera calibration tool's output
    a = np.radians(-77.85-0.2)
    rotx = np.matrix([[1,0,0],[0,   np.cos(a),    -np.sin(a)],[0, np.sin(a), np.cos(a)]])
    
    b = np.radians(-1)
    roty = np.matrix([[np.cos(b), 0, np.sin(b)],[0,1,0],[-np.sin(b), 0, np.cos(b)]])
    
    c = np.radians(-3.9)
    rotz = np.matrix([[np.cos(c),-np.sin(c),0],[np.sin(c), np.cos(c),0],[0,0,1]])
    
    #Translation vector from matlab (also contains error)
    translation_vector = np.matrix([[0.2566,   -0.4042,   -1.1052]])
    
    #Carry out the coordinate transform the way matlab suggests
    shifted_vector = input_coords - translation_vector
    world_coords = shifted_vector*inv_rotation_matrix
    
    #Apply my manual rotation about the x,, y and z axes to correct the errors from the matlab camera calibration tool
    world_coords = world_coords*rotx
    world_coords = world_coords*roty
    world_coords = world_coords*rotz
    
    #Hand tune a new vector to correct for errors in the matlab translation vector
    fine_tune = np.matrix([[0.31608206594757293, -1.1510445103398879, 1.8711518386598227]])
    world_coords = world_coords - fine_tune
    
    #Reverse the orientation of some axes so that they are aligned in the correct direction
    world_coords = np.matrix([[world_coords.item(0),-world_coords.item(1), -world_coords.item(2)]])
    
    return world_coords


def convert_to_arm_coords(x_input, y_input, z_input):
    """Convert from camera coordinates to arm coordinates (the coordinate system of the UR5)"""
    
    #Change input from camera coordates to the world coordinate system
    board_coords = convert_2_world(x_input, y_input, z_input)
    
    #define distance from checkboard (i.e. world) origin to arm origin
    board_to_arm_translation = np.matrix([[0.09,-0.475,-0.018]])
    
    #Add an additional fine tuning translation vector
    fine_tune = np.matrix([[-0.055, 0.01, 0.018]])
    
    #Move origin to the arm's origin
    arm_coords = board_coords + board_to_arm_translation + fine_tune

    return [arm_coords.item(0), arm_coords.item(1), arm_coords.item(2)]