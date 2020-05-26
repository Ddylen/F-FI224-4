# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 07:53:30 2020

@author: birl
"""

#'1.24.22.0'
dict1_24_22_0 = {'start_cup_reach': 2, 
 'pour_end' : 17,
 'grab_spatula' : 18,
'replace_spatula' : 55,
'grab_ladel' : 59,
'replace_ladel' : 92,
'grab_metal_spatula_1' : 311,
'flip_start' : 316,
'flip_finish' : 326,
'replace_metal_spatula_1': 338,
'grab_metal_spatula_2' : 433,
'remove_start' : 436}

for val in sorted(dict1_24_22_0.values()):
    print(val)