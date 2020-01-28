# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 14:26:02 2020

@author: birl
"""

import numpy as np
#Jan22 second value
rotation_matrix1 = np.matrix([[0.0310,   -0.9971,   -0.0695],[0.8756,   -0.0065,    0.4831],[-0.4821,   -0.0759,    0.8728]])

rotation_matrix2 = np.matrix([[-0.9976,    0.0043,   -0.0690],[   -0.0378,   -0.8696,    0.4923],[   -0.0579,    0.4938,    0.8677]])

#Jan21
rotation_matrix3 = np.matrix([[-0.0334, -0.8734, 0.4859],[0.9982, -0.0045, 0.0606],[-0.0508, 0.4870, 0.8719]])

#Jan22 first value
rotation_matrix4 = np.matrix([[0.0310,    0.8756,   -0.4821],[-0.9971,   -0.0065,   -0.0759],[-0.0695,    0.4831,    0.8728]])

inv_rotation_matrix1 = rotation_matrix1.getI()
inv_rotation_matrix2 = rotation_matrix2.getI()
inv_rotation_matrix3 = rotation_matrix3.getI()
inv_rotation_matrix4 = rotation_matrix4.getI()

transpose_matrix1 = rotation_matrix1.transpose()
transpose_matrix2 = rotation_matrix2.transpose()
transpose_matrix3 = rotation_matrix3.transpose()
transpose_matrix4 = rotation_matrix4.transpose()

subtraction1 = inv_rotation_matrix1 - transpose_matrix1
subtraction2 = inv_rotation_matrix2 - transpose_matrix2
subtraction3 = inv_rotation_matrix3 - transpose_matrix3
subtraction4 = inv_rotation_matrix4 - transpose_matrix4

print(subtraction1)
print(subtraction2)
print(subtraction3)
print(subtraction4)

#Jan22 value
#translation_vector = np.matrix([[0.5695,   -0.1760,   -1.1065]])

#Jan21
#translation_vector = np.matrix([[0.0178517,0.1937653,0.7038045]])

#Jan22 first value
translation_vector = np.matrix([[-0.2700,    0.0347,    1.2269]])

det_rot1 = np.linalg.det(rotation_matrix1)
det_rot2 = np.linalg.det(rotation_matrix2)
det_rot3 = np.linalg.det(rotation_matrix3)
det_rot4 = np.linalg.det(rotation_matrix4)

print(det_rot1)
print(det_rot2)
print(det_rot3)
print(det_rot4)