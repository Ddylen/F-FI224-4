"""
The coorinate transforms from camera to arm coordinates
"""

import numpy as np
import cv2
import ctypes

from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime


def convert_2_world(x,y,z):
    """Convert Camera coordinates to world coordinates"""  
    
    #Convert to matrix
    input_coords = np.matrix([[x,y,z]])
    
    #Rotation matrix obtained from matlab camera claibration tool (one axis is way off for some reason)
    rotation_matrix = np.matrix([[-0.9978,   -0.0316,   -0.0577],[-0.0007,   -0.8722,    0.4891],[-0.0658,    0.4881,    0.8703]])
    
    #Define an x axis rotation to get the x and y axes in the correct directions, because matlab got them wrong for some reason (hand tuned)
    a = np.radians(-57.6)
    rotx = np.matrix([[1,0,0],[0,   np.cos(a),    -np.sin(a)],[0, np.sin(a), np.cos(a)]])
    inv_rotation_matrix = rotation_matrix.getI()
    
    #Translation vector from matlab (also to wrong position, included just because)
    translation_vector = np.matrix([[0.2566,   -0.4042,   -1.1052]])
    
    #Carry out the coordinate transform the way matlab suggests
    shifted_vector = input_coords - translation_vector
    world_coords = shifted_vector*inv_rotation_matrix
    
    #Apply my manual rotation about the x axis to correct the bad y and z axis direction in matlab
    world_coords = world_coords*rotx
    
    #Define a new vector to get us to where we want the origin to be
    fine_tune = np.matrix([[0.31608206594757293, -1.1510445103398879, 1.8711518386598227]])
    world_coords = world_coords - fine_tune
    world_coords = np.matrix([[world_coords.item(0),-world_coords.item(1), -world_coords.item(2)]])
    return world_coords


def convert_to_arm_coords(x_input, y_input, z_input):
    """Convert from world coordinates to arm coordinates"""
    
    board_coords = convert_2_world(x_input, y_input, z_input)
    
    #measure distance from checkboard origin to arm origin
    board_to_arm_translation = np.matrix([[0.09,-0.475,-0.418]])
    
    #Add some adition fine tuning parameters
    fine_tune_2 = np.matrix([[-0.035, -0.015, 0.018]])
    
    #Move origin to the arm's origin
    arm_coords = board_coords + board_to_arm_translation + fine_tune_2

    return [arm_coords.item(0), arm_coords.item(1), arm_coords.item(2)]
    

if __name__ == '__main__': 
    """Code to check that the functions above return axes in the correct locations"""
    
    #Defins required to extract depth
    kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color |PyKinectV2.FrameSourceTypes_Depth)
    color2depth_points_type = _DepthSpacePoint* np.int(1920 * 1080)
    color2depth_points = ctypes.cast(color2depth_points_type(), ctypes.POINTER(_DepthSpacePoint))
    S = 1080*1920
    TYPE_CameraSpacePointArray = PyKinectV2._CameraSpacePoint * S
    csps1 = TYPE_CameraSpacePointArray()
    
    while True:
        # --- Getting frames and drawing
        if kinect.has_new_depth_frame():
            
            #Collect live colour and depth data
            frame = kinect.get_last_depth_frame()
            frameD = kinect._depth_frame_data        
            frame = frame.astype(np.uint8)
            frame = np.reshape(frame, (424, 512))
            
            colourframe = kinect.get_last_color_frame()
            colourframeD = kinect._color_frame_data
            
            #Reslice the colour frame to remove every 4th value, which is superfluous
            colourframe = np.reshape(colourframe, (2073600, 4))
            colourframe = colourframe[:,0:3] #exclude superfluos values
            
            #extract then combine the RBG data
            colourframeR = colourframe[:,0]
            colourframeR = np.reshape(colourframeR, (1080, 1920))
            colourframeG = colourframe[:,1]
            colourframeG = np.reshape(colourframeG, (1080, 1920))        
            colourframeB = colourframe[:,2]
            colourframeB = np.reshape(colourframeB, (1080, 1920))
            framefullcolour = cv2.merge([colourframeR, colourframeG, colourframeB])
                
            #Show colour frames as they are recorded, left click to get the 3D location of a colour pixel in world coords
            def click_event(event, x, y, flags, param):
                if event == cv2.EVENT_LBUTTONDOWN:
                    
                    #Defines to do colour to camera coords transformation
                    L = frame.size
                    ctypes_depth_frame = frameD
                    kinect._mapper.MapColorFrameToDepthSpace(ctypes.c_uint(512 * 424), ctypes_depth_frame, ctypes.c_uint(1920 * 1080), color2depth_points)
                    kinect._mapper.MapColorFrameToCameraSpace(L, ctypes_depth_frame, S, csps1)
                    
                    #Get position in camera coords
                    x_3D = csps1[y*1920 + x].x
                    y_3D = csps1[y*1920 + x].y
                    z_3D = csps1[y*1920 + x].z
                    
                    #Convert to arm coords
                    arm_coords = convert_to_arm_coords(x_3D, y_3D, z_3D)
    
                    print("arm pos is", float(arm_coords.item(0)), float(arm_coords.item(1)), float(arm_coords.item(2)))
            
            #Display imagem define what a click means
            cv2.imshow('KINECT Video Stream', framefullcolour)
            cv2.setMouseCallback('KINECT Video Stream', click_event)
            output = None
            
        #Close withdow if escape is pressed
        key = cv2.waitKey(1)
        if key == 27: break
    cv2.destroyAllWindows()

