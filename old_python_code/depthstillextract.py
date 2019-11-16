# -*- coding: utf-8 -*-
"""
Recover a still from the saved depth data
"""
import cv2
import pickle
import time
import numpy as np


datafile = open("depthdata/DEPTH11.15.13.49.pickle", "rb")
depthframe = pickle.load(datafile)
depthframe = np.reshape(depthframe, (424, 512))

depthframe = depthframe.astype(np.uint8)
"""
depthframe = depthframe.astype(np.uint8)
depthframe = np.reshape(depthframe, (424, 512))
cv2.imshow('video',depthframe)
time.sleep(5)
cv2.destroyAllWindows()
"""

while True:

   
    
    
    #frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
    cv2.imshow('KINECT Video Stream', depthframe)
    if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
        break
cv2.destroyAllWindows()