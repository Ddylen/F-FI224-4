"""
Example code for recovering the depth of cicked on pixels and displaying it on a screen
"""
from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import numpy as np
import cv2
from coordinate_transforms import convert_to_arm_coords


def click_event(event, x, y, flags, param):
    """Function to print the 3D position of the location you click"""
    
    # on left click
    if event == cv2.EVENT_LBUTTONDOWN: 
        
        #Carry out defines required to use MapColorFrameToCameraSpace 
        L = frame.size
        ctypes_depth_frame = frameD
        
        #Define mapping from 2D colour image to 3D position in space
        kinect._mapper.MapColorFrameToCameraSpace(L, ctypes_depth_frame, S, csps1)
        
        #Read 3D position of 2D point clicked on
        x_3D = csps1[y*1920 + x].x
        y_3D = csps1[y*1920 + x].y
        z_3D = csps1[y*1920 + x].z
        
        #Convert 3D position to world coordinates (also referred to as 'arm coordinates', as they are defined to match the UR5's coordinate system)
        arm_coords = convert_to_arm_coords(x_3D,y_3D,z_3D)
                
        print("clicked pos is", arm_coords)


#Initialise kinect to track colour and depth data                 
kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color |PyKinectV2.FrameSourceTypes_Depth) 

#Carry out a bunch of defines required to use MapColorFrameToCameraSpace 
S = 1080*1920
TYPE_CameraSpacePointArray = PyKinectV2._CameraSpacePoint * S
csps1 = TYPE_CameraSpacePointArray()

while True:
    
    # If you've recieved a new depth frame:
    if kinect.has_new_depth_frame():
        
        #Collect depth frane data in python and cython formats
        frame = kinect.get_last_depth_frame()
        frameD = kinect._depth_frame_data
        
        #Collect colour frame data in two formats
        colourframe = kinect.get_last_color_frame()
        colourframeD = kinect._color_frame_data
        
        #convert depth frame data to a data type that opencv can display
        frame = frame.astype(np.uint8)
        
        #reshape depth frame to form an image
        frame = np.reshape(frame, (424, 512))
        
        #Reslice to remove every 4th value, which is superfluous
        colourframe = np.reshape(colourframe, (2073600, 4))
        colourframe = colourframe[:,0:3]
        
        #extract RGB data from colour frame, then combine into a colour image
        colourframeR = colourframe[:,0]
        colourframeR = np.reshape(colourframeR, (1080, 1920))
        colourframeG = colourframe[:,1]
        colourframeG = np.reshape(colourframeG, (1080, 1920))        
        colourframeB = colourframe[:,2]
        colourframeB = np.reshape(colourframeB, (1080, 1920))
        framefullcolour = cv2.merge([colourframeR, colourframeG, colourframeB])
            
        #Display colour image
        cv2.imshow('KINECT Video Stream', framefullcolour)
        
        #Define behaviour on click
        cv2.setMouseCallback('KINECT Video Stream', click_event)
        output = None
    
    #Exit loop if 'esc' is pressed
    key = cv2.waitKey(1)
    if key == 27: break

#Close window with image
cv2.destroyAllWindows()