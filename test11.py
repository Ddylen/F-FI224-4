import numpy as np
import math
import matplotlib.pyplot as plt


centre= [2,7]
radius = 0.5
time_per_rotation = 5
points = np.linspace(0,math.pi*2,time_per_rotation*10)
x = np.sin(points)*radius + centre[0]
y = np.cos(points)*radius + centre[1]

plt.plot(x,y)
z = [1]*time_per_rotation*10
a = list(zip(x,y,z))
print(a)