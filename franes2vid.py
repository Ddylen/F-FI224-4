# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 14:17:15 2019

@author: birl
"""


import cv2
import argparse
import os
import pickle

# Construct the argument parser and parse the arguments

# Arguments


images = []
datafile = open("depthdata/COLOUR11.15.13.50.pickle", "rb")

frame = pickle.load(datafile)


out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'PIM1'), 10, (1920,1080))

#frame = cv2.imread(im0)
print(type(frame))
print(frame.shape)
out.write(frame)
cv2.imshow('video',frame)
height, width, channels = frame.shape

# Define the codec and create VideoWriter object

while True:
    try:
        frame = pickle.load(datafile)
        #frame = cv2.imread(im)
        out.write(frame)
        cv2.imshow('video',frame)
        if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
            break
    except:
        break
# Release everything if job is finished
out.release()
cv2.destroyAllWindows()
