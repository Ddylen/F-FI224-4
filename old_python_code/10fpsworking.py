# -*- coding: utf-8 -*-
"""
I mean, the title suggests that this worked at saving data at 10fps, BUT I DONT THINK THAT IT DID
"""

import numpy as np
import cv2

from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import time


kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Depth)
frameslist = []

cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
#fourcc = cv2.cv.CV_FOURCC(*'DIVX')
#out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
print("check1")
out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'PIM1'), 10, (1920,1080))
print("check2")

starttime = time.time()
oldtime = time.time()
i = 0
framelist = []
while(cap.isOpened()):
    ret, colorframe = cap.read()
    
    if ret==True:
        colorframe = cv2.flip(colorframe,0)

        # write the flipped frame
        out.write(colorframe)

        cv2.imshow('frame',colorframe)
        #print((time.time()-starttime)-oldtime)
        #print(time.time()-starttime)
        #oldtime = time.time() - starttime
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        
    if (time.time()-starttime)> i/10:
        print(1/((time.time()-starttime)-oldtime))
        oldtime = time.time() - starttime
        frame = kinect.get_last_depth_frame()
        frameD = kinect._depth_frame_data
        frame = frame.astype(np.uint8)
        frame = np.reshape(frame, (424, 512))
        
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        framelist.append
        i = i+1
    
# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()