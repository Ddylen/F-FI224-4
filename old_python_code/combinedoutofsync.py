# -*- coding: utf-8 -*-
"""
Save colour and depth data, but with the frames not synced
"""

from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import numpy as np
import cv2
import pickle
import datetime
import time

"""
currentdate = datetime.datetime.now()
filename = "depthdata\DATA" + str(currentdate.month) + "." + str(currentdate.day) + "."+ str(currentdate.hour) + "."+ str(currentdate.minute) +".pickle"
my_data_file = open(filename, 'wb')
"""
kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Depth)
depthframeslist = []
colourframeslist = []
"""
starttime = time.time()
oldtime = starttime
"""
while True:
    # --- Getting frames and drawing
    elapsedtime = time.time() - starttime
    if kinect.has_new_depth_frame():
        print(elapsedtime-oldtime)
        oldtime = elapsedtime
    #if True:
        depthframe = kinect.get_last_depth_frame() #data for display
        depthframeD = kinect._depth_frame_data
        depthframereadable = np.copy(np.ctypeslib.as_array(depthframeD, shape=(kinect._depth_frame_data_capacity.value,))) # TODO FIgure out how to solve intermittent up to 3cm differences
        depthframe = depthframe.astype(np.uint8)
        depthframe = np.reshape(depthframe, (424, 512))
        depthframe = cv2.cvtColor(depthframe, cv2.COLOR_GRAY2RGB)
        depthframeslist.append(depthframereadable)
        #print(depthframereadable[424*200+250] - depthframeD[424*200+250])
    if kinect.has_new_color_frame():
        #print(frame)
        colourframe = kinect.get_last_color_frame()
        colourframeD = kinect._color_frame_data

        #Reslice to remove every 4th value, which is superfluous
        colourframe = np.reshape(colourframe, (2073600, 4))
        colourframe = colourframe[:,0:3] #exclude superfluos values
        colourframeR = colourframe[:,0]
        colourframeR = np.reshape(colourframeR, (1080, 1920))
        colourframeG = colourframe[:,1]
        colourframeG = np.reshape(colourframeG, (1080, 1920))        
        colourframeB = colourframe[:,2]
        colourframeB = np.reshape(colourframeB, (1080, 1920))
        framefullcolour = cv2.merge([colourframeR, colourframeG, colourframeB])
        colourframeslist.append(framefullcolour)
        cv2.imshow('KINECT Video Stream', framefullcolour)
        

        

    key = cv2.waitKey(1)
    if key == 27: break
cv2.destroyAllWindows()

"""
#filehandler = open(my_data_file, 'wb') 
pickle.dump(depthframeslist, my_data_file)
pickle.dump(colourframeslist, my_data_file)

#print(depthframeslist)
"""