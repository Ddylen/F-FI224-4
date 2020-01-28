# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 12:18:09 2019

@author: birl
"""

# -*- coding: utf-8 -*-
"""
Example code for recovering the depth of pixels and displaying it on a screen
"""

from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import math
import numpy as np
import cv2
from convert_2_world import convert_2_world
from convert_to_arm_coords import convert_to_arm_coords

kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Depth)
frameslist = []


"""
for baord coords
x axis is to sink
y axis isto camera
z axis is positive down
"""

"""
wooden block length 45cm:
    in x axis:  board coords is -0.19478164678260376 -0.11625986217754267 -0.04704581156581377
board coords is 0.4529602298722016 -0.12347530905602884 -0.0645459752500683

board coords is -0.19027850681296357 -0.08191963294265536 -0.06356783580389518
board coords is 0.44392617363279313 -0.08052721090476701 -0.08382050198879079

in y axis:
    board coords is 0.12998420058235488 0.1066823888909349 -0.06673948960276592
board coords is 0.13729491397297738 -0.3219523249140604 -0.06646514402724506
board coords is 0.17658049663712108 0.10242929430125686 -0.06846992499212165
board coords is 0.18267185659672147 -0.3220552223132248 -0.06797341236176926

in z axis:
    
board coords is 0.11528363832952573 -0.10514044298338746 -0.47389003222751597
board coords is 0.16629652582298574 -0.08780003530330693 -0.03854902691922271
board coords is 0.0992321480280357 -0.09358478313285154 -0.4778575221491428
board coords is 0.1394970369744109 -0.08679289481362172 -0.02917867877152479

Checkboard length: 28.6 in the  x axis, 19.1cm in y axis
x axis:
    board coords is 0.011178739953937575 -0.09760158639526681 -0.024850786090417912
board coords is 0.41518484218727525 -0.09396621463920694 -0.03707172020030013

board coords is 0.012748530063610774 -0.026264731342684658 -0.024715739831926986
board coords is 0.4112499807092446 -0.024046195200277846 -0.03535652749507074
    
y axis:
    board coords is 0.07244273313575528 -0.13094457414592578 -0.025970834424682746
board coords is 0.2041013495832043 0.05024352801468711 -0.025630428767534547


board coords is 0.3519997670007216 -0.13441445651867692 -0.03266384746400075
board coords is 0.3214834836263925 0.049455140608980395 -0.0326530610477012

-0.30956989988473455

"""

x_scale_factor = math.sin(math.radians(42.05)) # Using FoV spec, this is the maximum object size that fits in half of FoV horizonally at 1m away
y_scale_factor = math.sin(math.radians(26.9)) # Using FoV spec, this is the maximum object size that fits in half of FoV vertically at 1m away

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
                """
                x_normalised = x/424
                y_normalised = y/512
                depthfromcam = frameD[((y * 512) + x)]/1000 # we need to specify pixel number, not x,y coordinates
                x_camera_coords = depthfromcam* 0.86*2*(x_normalised-0.5)*x_scale_factor 
                y_camera_coords = depthfromcam* 1.56*2*(y_normalised-0.5)*y_scale_factor # i think my scaling method is off by a bit
                board_coords = convert_2_world(np.matrix([[x_camera_coords], [y_camera_coords], [depthfromcam]])) #TODO: confirm that this transformation applies for normalised pixel coordinates
                #print(board_coords.item(0), board_coords.item(1), board_coords.item(2))
                #print("pos is ", x, y, "depth is ", Pixel_Depth)
                #print("board coords is",board_coords.item(0), board_coords.item(1), board_coords.item(2))
                
                board_to_arm_translation = np.matrix([[0.1],[0.39],[0.4]])#measured from board to arm 0,0,0 position
                arm_coords_twisted = board_coords + board_to_arm_translation
                arm_coords = np.matrix([[- arm_coords_twisted.item(0)], [-arm_coords_twisted.item(1)], [-arm_coords_twisted.item(2)]]) #axes for arm are other way round to that of checkerboard
                print("arm coords is",arm_coords.item(0), arm_coords.item(1), arm_coords.item(2))
                
                """
                xnorm = x/424
                ynorm = y/512
                arm_coords = convert_to_arm_coords(xnorm, ynorm, frameD)
                print(arm_coords.item(0), arm_coords.item(1), arm_coords.item(2))
                
        ##output = cv2.bilateralFilter(output, 1, 150, 75)
        cv2.imshow('KINECT Video Stream', frame)
        cv2.setMouseCallback('KINECT Video Stream', click_event)
        output = None

    key = cv2.waitKey(1)
    if key == 27: break
cv2.destroyAllWindows()