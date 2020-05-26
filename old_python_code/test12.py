import numpy as np
import math

def circle(total_time, time_per_rotation):
    centre= [0.35, -0.22]
    radius = 0.04
    z_val = 0.35
    num_rotations = total_time/time_per_rotation
    num_points = int(num_rotations*time_per_rotation*100)
    points = np.linspace(0,num_rotations*math.pi*2,num_points)
    x = np.sin(points)*radius + centre[0]
    y = np.cos(points)*radius + centre[1]
    z = [z_val]*num_points
    circle_points_list = list(zip(x,y,z))
    print(len(circle_points_list))
    return circle_points_list

circle(5,1)