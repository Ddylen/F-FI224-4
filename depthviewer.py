"""
code to display the depth data current read by the kinect
"""
import numpy as np
import cv2
import pickle
import time 
import datetime
import ctypes

from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime


#define file to operate on
filename = 'trial7thomas.16.3.10.24'

#Start a kinect (required even if we are reading saved depth values)
kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Depth)

#Do a bunch of defines required for matching the colour coordinates to their depth later
color2depth_points_type = _DepthSpacePoint* np.int(1920 * 1080)
color2depth_points = ctypes.cast(color2depth_points_type(), ctypes.POINTER(_DepthSpacePoint))
S = 1080*1920
TYPE_CameraSpacePointArray = PyKinectV2._CameraSpacePoint * S
csps1 = TYPE_CameraSpacePointArray()

#Defined where saved depth data is stored
depthdatafile = open("bin/rawdata/DEPTH." + filename + ".pickle", "rb")

#initialise deepest depth seen
depthmaxseen = 0

#initialise frame counter
count = 0 

#define video saving
height= 424
width = 512
out = cv2.VideoWriter('bin/videos/DEPTHVIDFLIPPED' + filename + '.avi', cv2.VideoWriter_fourcc(*'DIVX'), 10, (int(width), int(height))) 

# all depths after maxdepth distance artificially set to same colour to increase forground contrast in saved video
maxdepth = 2000

while True:
    
    try:
        
        #load a frame of saved depth data
        depthframe = pickle.load(depthdatafile)
        
        #keep a record of largest depth seen in case you want to fine tune maxdepth
        localdepthmax = max(depthframe)
        if localdepthmax > depthmaxseen:
            depthmaxseen= localdepthmax
        
        #Set all depth values over a threshold to just under it to increase colour contrast in the important depth ranges
        depthframe[depthframe > maxdepth] = maxdepth - 1
        
        #Reformat depth frame into a format OpenCV can display
        depthframe = np.divide(depthframe,maxdepth/256)
        depthframe = np.reshape(depthframe, (424, 512))
        depthframe = depthframe.astype(np.uint8)
        
        #Set false colour settings
        depthframe = cv2.cvtColor(depthframe, cv2.COLOR_GRAY2RGB)
        depthframe = cv2.applyColorMap(depthframe, cv2.COLORMAP_JET)
        
        #Flip data horizontally to correct for a horizontal flip
        depthframe = cv2.flip(depthframe, 1)
        
        #show depth data
        cv2.imshow('Recording KINECT Video Stream', depthframe)
        
        #save depth data
        out.write(depthframe)
        
        #Update frame count
        count = count + 1
        
        #Kill image if 'esc' is pressed
        key = cv2.waitKey(1)
        if key == 27: 
            break
    
    #When save data file ends, end program
    except(EOFError):
        print("Video Stiching Finished")
        break
    
#Finish saving video
out.release()

#Close the pop up window
cv2.destroyAllWindows()





    

    