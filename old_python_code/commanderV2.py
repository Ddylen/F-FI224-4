# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 12:13:11 2019

Early arm 'go to position in 2D code', for the X-Y plane. Not well synchonised with the actual motion
"""

import sys
sys.path.insert(1,r'C:\Users\birl\Documents\ur5_python_host\ur5_kg_robot')



import numpy as np

import time

import serial

import scipy.optimize

import socket

import math

from math import pi



import waypoints as wp

from kg_robot import kg_robot
from reader import interpret2D
import specialised_kg_robot_example as kgrs 


def main():
    move_scale_x = 0.75
    move_scale_y = 1 #scale the 0 to 1 move range into a range the arm can reach
    frame_rate = 1/5
    x_list, y_list = interpret2D()
    for val in x_list:
        x_list[x_list.index(val)] = (-val)* move_scale_x #add offset so the arm doesnt collide with itself
    
    for val in y_list:
        y_list[y_list.index(val)] = (val-1)*0.5* move_scale_y -0.2 #havent revesed y as negative is towards the bench
    
    print(x_list)
    print(y_list)
    print("------------Configuring Burt-------------\r\n")

    burt = 0

    burt = kgrs.specialised_kg_robot(port=30010,db_host="169.254.251.50")

    print("----------------Hi Burt!-----------------\r\n\r\n")
    
    
    burt.movel([x_list[0], y_list[0], 0.15, np.pi/2, 0, 0], min_time = 5) #move to first position slowly
    
    for val in x_list:
        index = x_list.index(val)
        #time.sleep(frame_rate)
        burt.movel([val, y_list[index], 0.15, np.pi/2, 0, 0], min_time = frame_rate)
    
    
    burt.close()

if __name__ == '__main__': main()