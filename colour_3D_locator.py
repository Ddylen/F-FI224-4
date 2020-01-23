# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 11:41:42 2020

@author: birl
"""

# -*- coding: utf-8 -*-
"""
Example code for recovering the depth of pixels and displaying it on a screen
"""

from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import numpy as np
import cv2
import ctypes

def convert_2_world(camera_coords):
    """Convert Camera coordinates to world coordinates"""  

    rotation_matrix = np.matrix([[-0.9976,    0.0043,   -0.0690],[   -0.0378,   -0.8696,    0.4923],[   -0.0579,    0.4938,    0.8677]])
    #rotation_matrix = np.matrix([[-0.0334, -0.8734, 0.4859],[0.9982, -0.0045, 0.0606],[-0.0508, 0.4870, 0.8719]])
    inv_rotation_matrix = rotation_matrix.getI()
    translation_vector = np.matrix([[0.0178517],	[0.1937653],	[0.7038045]])
    #translation_vector = np.matrix([[0],	[0],	[0]])
    shifted_vector = camera_coords - translation_vector
    world_coords = rotation_matrix*shifted_vector
    #fine_tune = np.matrix([[0.1748482], [0.0247562], [-0.0189254]])
    #fine_tune = translation_vector
    #world_coords = world_coords +  fine_tune
    return world_coords


def convert_to_arm_coords(x_input, y_input, z_input, return_depth = False):
    """Function to convert an x,y,z value into arm coordinates"""
    
    board_coords = convert_2_world(np.matrix([[x_input], [y_input], [z_input]])) #TODO: confirm that this transformation applies for normalised pixel coordinates
    #board_to_arm_translation = np.matrix([[0.1],[0.39],[0.4]])#measured from board to arm 0,0,0 position
    #arm_coords_twisted = board_coords + board_to_arm_translation
    arm_coords_twisted = board_coords
    arm_coords = np.matrix([[- arm_coords_twisted.item(0)], [-arm_coords_twisted.item(1)], [-arm_coords_twisted.item(2)]]) #axes for arm are other way round to that of checkerboard
    outputmat =  arm_coords
    if return_depth == False:
        return outputmat
    else:
        return outputmat




kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color |PyKinectV2.FrameSourceTypes_Depth)
frameslist = []

color2depth_points_type = _DepthSpacePoint* np.int(1920 * 1080)
color2depth_points = ctypes.cast(color2depth_points_type(), ctypes.POINTER(_DepthSpacePoint))


S = 1080*1920
TYPE_CameraSpacePointArray = PyKinectV2._CameraSpacePoint * S
csps1 = TYPE_CameraSpacePointArray()

while True:
    # --- Getting frames and drawing
    if kinect.has_new_depth_frame():
        frame = kinect.get_last_depth_frame()
        frameD = kinect._depth_frame_data
        
        colourframe = kinect.get_last_color_frame()
        colourframeD = kinect._color_frame_data
        
        
        frame = frame.astype(np.uint8)
        frame = np.reshape(frame, (424, 512))
        
        #Reslice to remove every 4th value, which is superfluous
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
            
        #Show colour frames as they are recorded

        
        def click_event(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                #Pixel_Depth = frameD[((y * 512) + x)] # we need to specify pixel number, not x,y coordinates
                
                L = frame.size
                ctypes_depth_frame = frameD
                kinect._mapper.MapColorFrameToDepthSpace(ctypes.c_uint(512 * 424), ctypes_depth_frame, ctypes.c_uint(1920 * 1080), color2depth_points)
                #read_pos = x+y*1920 -1
                
                kinect._mapper.MapColorFrameToCameraSpace(L, ctypes_depth_frame, S, csps1)
                x_3D = csps1[y*1920 + x].x
                y_3D = csps1[y*1920 + x].y
                z_3D = csps1[y*1920 + x].z

                arm_coords = convert_2_world(np.matrix([[z_3D], [y_3D], [x_3D]]))
                xaxis1 = [0,0,1]
                xaxis2 = [1,0,1]
                
                xaxisworld1 = convert_2_world(np.matrix([[0], [0], [1]]))
                xaxisworld2 = convert_2_world(np.matrix([[1], [0], [1]]))
                
                #print("pos is ", x_3D, y_3D, z_3D) 
                print("arm pos is", float(arm_coords[0]), float(arm_coords[1]), float(arm_coords[2]))
        ##output = cv2.bilateralFilter(output, 1, 150, 75)
        cv2.imshow('KINECT Video Stream', framefullcolour)
        cv2.setMouseCallback('KINECT Video Stream', click_event)
        output = None

    key = cv2.waitKey(1)
    if key == 27: break
cv2.destroyAllWindows()