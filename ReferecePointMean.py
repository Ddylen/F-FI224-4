# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 14:10:49 2019

File for extracting mean positions of reference points from a list of the last 5 measurements
"""

import numpy as np

up_left = [0.342293, 0.532481,
0.342279, 0.532374,
0.342299, 0.532434,
0.343795, 0.535004,
0.343806, 0.535009]

low_left = [0.354537, 0.2951,
0.35458, 0.297739,
0.356107, 0.300489,
0.356068, 0.297753,
0.356083, 0.297849
]

up_right = [0.5969, 0.524198,
0.596923, 0.526895,
0.59845, 0.532252,
0.596897, 0.526921,
0.596902, 0.526951
]

low_right = [
0.595377, 0.305947,
0.595407, 0.297849,
0.595425, 0.300538,
0.595412, 0.30329,
0.595395, 0.305957
]

def means(num_list):
    av_x = np.mean([num_list[0],num_list[2],num_list[4],num_list[6],num_list[8]])
    av_y = np.mean([num_list[1],num_list[3],num_list[5],num_list[7],num_list[9]])
    print(av_x, av_y)

print("upper left")
means(up_left)

print("low left")
means(low_left)

print("upper right")
means(up_right)

print("lower right")
means(low_right)