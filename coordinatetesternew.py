"""
Example code for recovering the depth of pixels and displaying it on a screen
"""

from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import numpy as np
import cv2
import ctypes

def convert_2_world(x,y,z):
    """Convert Camera coordinates to world coordinates"""  
   
    input_coords = np.matrix([[x,y,z]])
    
    #horizontal board attempt
    rotation_matrix = np.matrix([[-0.9978,   -0.0316,   -0.0577],[-0.0007,   -0.8722,    0.4891],[-0.0658,    0.4881,    0.8703]])
    
    a = np.radians(-57.6)
    roty = np.matrix([[np.cos(a),   0,   np.sin(a)],[0,   1,    0],[-np.sin(a),    0,    np.cos(a)]])
    rotx = np.matrix([[1,0,0],[0,   np.cos(a),    -np.sin(a)],[0, np.sin(a), np.cos(a)]])
    inv_rotation_matrix = rotation_matrix.getI()
    
    #horizontal board attempt
    translation_vector = np.matrix([[0.2566,   -0.4042,   -1.1052]])
    
    #translation_vector = np.matrix([[0],	[0],	[0]])
    shifted_vector = input_coords - translation_vector
    world_coords = shifted_vector*inv_rotation_matrix
    world_coords = world_coords*rotx
    fine_tune = np.matrix([[0.31608206594757293, -1.1510445103398879, 1.8711518386598227]])
    world_coords = world_coords - fine_tune
    world_coords = np.matrix([[world_coords.item(0),-world_coords.item(1), -world_coords.item(2)]])
    return world_coords


def convert_to_arm_coords(x_input, y_input, z_input):
    """Convert from world coordinates to arm coordinates"""
    
    board_coords = convert_2_world(x_input, y_input, z_input) #TODO: confirm that this transformation applies for normalised pixel coordinates
    board_to_arm_translation = np.matrix([[0.09,-0.475,-0.418]])#measured from board to arm 0,0,0 position
    fine_tune_2 = np.matrix([[-0.035, -0.015, 0.018]])
    arm_coords_twisted = board_coords + board_to_arm_translation + fine_tune_2
    arm_coords = np.matrix([[arm_coords_twisted.item(0),arm_coords_twisted.item(1),arm_coords_twisted.item(2)]]) #axes for arm are other way round to that of checkerboard
    return arm_coords
    

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
                
                L = frame.size
                ctypes_depth_frame = frameD
                kinect._mapper.MapColorFrameToDepthSpace(ctypes.c_uint(512 * 424), ctypes_depth_frame, ctypes.c_uint(1920 * 1080), color2depth_points)
                
                kinect._mapper.MapColorFrameToCameraSpace(L, ctypes_depth_frame, S, csps1)
                x_3D = csps1[y*1920 + x].x
                y_3D = csps1[y*1920 + x].y
                z_3D = csps1[y*1920 + x].z
                
                arm_coords = convert_to_arm_coords(x_3D, y_3D, z_3D)

                print("arm pos is", float(arm_coords.item(0)), float(arm_coords.item(1)), float(arm_coords.item(2)))
        
        cv2.imshow('KINECT Video Stream', framefullcolour)
        cv2.setMouseCallback('KINECT Video Stream', click_event)
        output = None

    key = cv2.waitKey(1)
    if key == 27: break
cv2.destroyAllWindows()