# -*- coding: utf-8 -*-
"""

Attempt to save data at a defined frame rate, assume it also failed


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


starttime = time.time()
oldtime = time.time()
i = 0
framelist = []
colorframelist = []

clfrmstxt=open('colourframes.txt','w')
depthframestxt=open('depthframes.txt','w')


 
while(cap.isOpened()):
    ret, colorframe = cap.read()
    
    if ret==True:
        colorframe = cv2.flip(colorframe,0)

        # write the flipped frame
        clfrmstxt.write(colorframe)
        cv2.imshow('frame',colorframe)
        #print((time.time()-starttime)-oldtime)
        #print(time.time()-starttime)
        #oldtime = time.time() - starttime
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    """   
    while((time.time()-starttime)> i/10):
        pass
    """
    if kinect.has_new_depth_frame():
        print(1/((time.time()+0.0001-starttime)-oldtime))
        oldtime = time.time() - starttime
        frame = kinect.get_last_depth_frame()
        frameD = kinect._depth_frame_data
        frame = frame.astype(np.uint8)
        frame = np.reshape(frame, (424, 512))
        clfrmstxt.write(frameD)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        framelist.append(frameD)
        i = i+1
    
# Release everything if job is finished
cap.release()
out.release()
clfrmstxt.close()
cv2.destroyAllWindows()