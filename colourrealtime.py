# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 17:14:55 2019

@author: birl
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 16:50:08 2019

@author: birl
"""

from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import numpy as np
import cv2

kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color)
frameslist = []

while True:
    # --- Getting frames and drawing
    if kinect.has_new_color_frame():
        print(frame)
        frame = kinect.get_last_color_frame()
        frameD = kinect._color_frame_data

        #print(type(frameD))
        """
        i = 0
        for val in frameD:
            i = i+1
            print(i)
            if ((i)%4 == 0):
                pass
            else:
                frameslist.append(val)
        """
        frame = np.reshape(frame, (2073600, 4))
        
        frame = frame[:,0:3] #exclude superfluos values
        #print(frame[1][0])
        #print(frame.shape)
        frameR = frame[:,0]
        frameR = np.reshape(frameR, (1080, 1920))
        frameG = frame[:,1]
        frameG = np.reshape(frameG, (1080, 1920))        
        frameB = frame[:,2]
        frameB = np.reshape(frameB, (1080, 1920))
        framefullcolour = cv2.merge([frameR, frameG, frameB])
        #print(len(frame))
        #frame = cv2.cvtColor(framefullcolour, cv2.COLOR_GRAY2RGB)
        cv2.imshow('KINECT Video Stream', framefullcolour)
        print("color fires")
        

        

    key = cv2.waitKey(1)
    if key == 27: break
cv2.destroyAllWindows()