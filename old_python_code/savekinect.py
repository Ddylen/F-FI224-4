# -*- coding: utf-8 -*-
"""
Code to save kinect data at a certain frame rate

"""

from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import numpy as np
import cv2
import time

kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Depth)
j = 0
print("ans is", 424*512)
frameslist  = []
start_time = time.time()
oldtime = time.time() - start_time
i = 0
cap = cv2.VideoCapture(0)

"""
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (512, 424))
"""

while True:
    # --- Getting frames and drawing
    elapsed_time = time.time() - start_time
    
    time_lag = elapsed_time - oldtime
    #print("lag is", time_lag)
    if elapsed_time > i*(1/30): #TODO: This is a hacky way of getting 30 fps at the right time _+10%, should look in to improving this
        
        """
        ret, clframe = cap.read()
        print(len(clframe))
        if ret==True:
            clframe = cv2.flip(clframe,0)
            # write the flipped frame
            out.write(clframe)
        """
        print(1/(elapsed_time-oldtime))
        oldtime = time.time() - start_time

        frame = kinect.get_last_depth_frame()
        #if(np.count_nonzero(frame)
        frameD = kinect._depth_frame_data
        if j == 1000:
            print(type(frameD))
            print(frameD)
            print(frameD[1000])
        j = i+1
        frameslist.append(frameD)
        frame = frame.astype(np.uint8)
        frame = np.reshape(frame, (424, 512))
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        i = i+1
        
        def click_event(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                print("pos is ", x, y)
                Pixel_Depth = frameD[((y * 512) + x)] # we need to specify pixel number, not x,y coordinates
                print("depth is ", Pixel_Depth)
        
        ##output = cv2.bilateralFilter(output, 1, 150, 75)
        cv2.imshow('KINECT Video Stream', frame)
        cv2.setMouseCallback('KINECT Video Stream', click_event)
        output = None

    key = cv2.waitKey(1)
    if key == 27: break
cv2.destroyAllWindows()
cap.release()
out.release()
