

import numpy as np
import cv2
import pickle
import time 
import datetime
import ctypes

from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime


filename = 'trial7thomas.16.3.10.24'
#Start a kinect (required even if we are reading saved depth values)
kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Depth)

#Do a bunch of defines required for matching the colour coordinates to their depth later
color2depth_points_type = _DepthSpacePoint* np.int(1920 * 1080)
color2depth_points = ctypes.cast(color2depth_points_type(), ctypes.POINTER(_DepthSpacePoint))
S = 1080*1920
TYPE_CameraSpacePointArray = PyKinectV2._CameraSpacePoint * S
csps1 = TYPE_CameraSpacePointArray()

#Defined where aved depth data is stored
depthdatafile = open("bin/rawdata/DEPTH." + filename + ".pickle", "rb")

depthmax = 0
count = 0 
while True:
    try:
        depthframe = pickle.load(depthdatafile)
        localdepthmax = max(depthframe)
        if localdepthmax > depthmax:
            depthmax= localdepthmax
        
        depthframe[depthframe > 4000] = 3999
        
        depthframe = np.divide(depthframe,4000/256)
        depthframe = np.reshape(depthframe, (424, 512))
    
        depthframe = depthframe.astype(np.uint8)
        depthframe = cv2.flip(depthframe, 1)
        depthframe = cv2.cvtColor(depthframe, cv2.COLOR_GRAY2RGB)
        depthframe = cv2.applyColorMap(depthframe, cv2.COLORMAP_JET)
    

        #print(depthframe)
        cv2.imshow('Recording KINECT Video Stream', depthframe)
        if count%20==0:
            cv2.imwrite("depthimages/frame%d.jpg" % count, depthframe)
        #time.sleep(0.1)
        count = count + 1
        
    
    
    

        key = cv2.waitKey(1)
        if key == 27: 
            break

    except(EOFError):
        break
cv2.destroyAllWindows()





    