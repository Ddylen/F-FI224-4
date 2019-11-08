# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 14:45:57 2019

Early arm 'go to position in 2D code', for the Y-Z plane. Not well synchonised with the actual motion
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


def main():
    camera_x = 1280
    camera_y = 720
    
    x_list, y_list = interpret2D()
    for val in x_list:
        x_list[x_list.index(val)] = (val - 0.5*camera_x)/camera_x
    
    for val in y_list:
        y_list[y_list.index(val)] = (val)/(2*camera_y) + 0.5
    
    print(x_list)
    print(y_list)
    print("------------Configuring Burt-------------\r\n")

    burt = 0

    burt = kgrs.specialised_kg_robot(port=30010,db_host="169.254.251.50")

    print("----------------Hi Burt!-----------------\r\n\r\n")
    
    
    for val in x_list:
        index = x_list.index(val)
        time.sleep(1)
        burt.movejl([val, 0, y_list[index], -2.22769, 1.57521, -0.00545246])
    
    
    burt.close()

if __name__ == '__main__': main()