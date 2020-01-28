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


kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Depth)
frameslist = []

while True:
    # --- Getting frames and drawing
    if kinect.has_new_depth_frame():
        frame = kinect.get_last_depth_frame()
        frameD = kinect._depth_frame_data
        frame = frame.astype(np.uint8)
        frame = np.reshape(frame, (424, 512))
        
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        def click_event(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                Pixel_Depth = frameD[((y * 512) + x)] # we need to specify pixel number, not x,y coordinates
                print("pos is ", x, y, "depth is ", Pixel_Depth)
        ##output = cv2.bilateralFilter(output, 1, 150, 75)
        cv2.imshow('KINECT Video Stream', frame)
        cv2.setMouseCallback('KINECT Video Stream', click_event)
        output = None
        

    key = cv2.waitKey(1)
    if key == 27: break
cv2.destroyAllWindows()