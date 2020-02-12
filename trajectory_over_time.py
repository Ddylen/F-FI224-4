# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 15:28:23 2020

@author: birl
"""

import pickle
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import mpl_toolkits.mplot3d as plt3d
import matplotlib.animation as animation



# Attaching 3D axis to the figure
fig = plt.figure()
ax = p3.Axes3D(fig)

#file_name = '1.24.21.46'
file_name = '1.23.17.49'
#file_name = '1.24.22.0'
readfile = open("bin/filtered_data/" + file_name + ".pickle", "rb")
loaded_results = pickle.load(readfile)



ax.scatter(x_sec, y_sec, z_sec)

x_upper_limit = 1
x_lower_limit = -1

y_upper_limit = 1
y_lower_limit = -1

z_upper_limit = 1
z_lower_limit = -1

# Setting the axes properties
ax.set_xlim3d([x_lower_limit, x_upper_limit])
ax.set_xlabel('X')

ax.set_ylim3d([y_lower_limit, y_upper_limit])
ax.set_ylabel('Y')

ax.set_zlim3d([z_lower_limit, z_upper_limit])
ax.set_zlabel('Z')

ax.set_title(file_name)
time_text = ax.text(0,0.5,0,s= 'Frame = ',horizontalalignment='left',verticalalignment='top', transform=ax.transAxes)
"""
def onClick(event):
    global pause
    pause ^= True
fig.canvas.mpl_connect('button_press_event', onClick)
"""
# Creating the Animation object
#len(body_3D_pose[0])
#ani = animation.FuncAnimation(fig, update_lines, len(loaded_results), fargs = [loaded_results, lines, time_text],interval=100, blit=False, repeat = True)
#Writer = animation.writers['ffmpeg']
#writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
#ani.save(file_name +'.mp4', writer=writer)

plt.show()
