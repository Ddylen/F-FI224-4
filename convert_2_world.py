# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 16:08:29 2019

@author: birl
"""
list1= [1,1,1]
list2 = [2,2,2]
list3 = list1-list2
print(list3)
import numpy as np


def convert_2_world(camera_coords):
    translation_vector = np.matrix([[-0.0162],    [0.5513],   [-1.4072]])

    shifted_vector = camera_coords - translation_vector
    
    rotation_matrix = np.matrix([[0.9997, -0.0248, 0.0059],[0.0219, 0.9549, 0.2961],[-0.0130, -0.2959, 0.9551]])
    inv_rotation_matrix = rotation_matrix.getI()
    world_coords = inv_rotation_matrix*shifted_vector
    return world_coords