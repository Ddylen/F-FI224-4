# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 13:40:02 2019

@author: birl
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 12:48:54 2019

@author: birl
"""

# -*- coding: utf-8 -*-
"""
TODO- SOLVE MEMORY ERROR
"""

from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import numpy as np
import cv2
import pickle
import datetime
import time 

currentdate = datetime.datetime.now()
timestring = str(currentdate.month) + "." + str(currentdate.day) + "."+ str(currentdate.hour) + "."+ str(currentdate.minute)
depthfilename = "depthdata\DEPTH" + timestring +".pickle"
colourfilename = "depthdata\COLOUR" + timestring +".pickle"
depthfile = open(depthfilename, 'wb')
colourfile = open(colourfilename, 'wb')

kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Depth)
starttime = time.time()
oldtime = 0
t1 = time.time()
t2 = time.time()
i = 0
fpsmax = 0
fpsmin = 100
while True:
    # --- Getting frames and drawing
    elapsedtime = time.time()- starttime
    
    if kinect.has_new_depth_frame() and kinect.has_new_color_frame() :
        while(elapsedtime> i/10): #TODO find better timing method
            if i >100:
                try:
                    fps =  1/(elapsedtime - oldtime)
                    print(fps)
                    if fps> fpsmax:
                        fpsmax= fps
                    if fps < fpsmin:
                        fpsmin = fps
                    print(fpsmax - fpsmin)
                except ZeroDivisionError:
                    pass
            oldtime = elapsedtime
        #if True:
            #t1 = time.time()
            depthframe = kinect.get_last_depth_frame() #data for display
            depthframeD = kinect._depth_frame_data
            
            colourframe = kinect.get_last_color_frame()
            colourframeD = kinect._color_frame_data
            #t2 = time.time()
            
            
            
            depthframereadable = np.copy(np.ctypeslib.as_array(depthframeD, shape=(kinect._depth_frame_data_capacity.value,))) # TODO FIgure out how to solve intermittent up to 3cm differences
            depthframe = depthframe.astype(np.uint8)
            depthframe = np.reshape(depthframe, (424, 512))
            depthframe = cv2.cvtColor(depthframe, cv2.COLOR_GRAY2RGB)
           
            pickle.dump(depthframereadable, depthfile)
            
            #print(depthframereadable[424*200+250] - depthframeD[424*200+250])
            #print(frame)
    
    
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
            pickle.dump(framefullcolour, colourfile)
    
            #print(t2-t1)
            cv2.imshow('KINECT Video Stream', framefullcolour)
            
            i = i+1
        

        

    key = cv2.waitKey(1)
    if key == 27: break
cv2.destroyAllWindows()


#filehandler = open(my_data_file, 'wb') 


#print(depthframeslist)
