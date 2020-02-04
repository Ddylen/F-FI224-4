import pickle
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import mpl_toolkits.mplot3d as plt3d
import matplotlib.animation as animation


def update_lines(frame_num, RESULTS_LIST, lines, time_text):
    #print(time.time())
    i = 0
    for line in lines:
        #print(results_list[frame_num][i])
        #print("I IS", i)
        #print(line)
        x = np.asarray(RESULTS_LIST[frame_num][i][0])
        #print('x', x)
        #print(type(x))
        #print(" ")
        y = np.asarray(RESULTS_LIST[frame_num][i][1])
        #print('y', y)
        #print(" ")
        z = np.asarray(RESULTS_LIST[frame_num][i][2])
        #print('z', z)
        #print(" ")
        
        #print(" ")
        
        if RESULTS_LIST[frame_num][i][3] == False:

            line.set_color('b')
  
        elif  RESULTS_LIST[frame_num][i][3] == True:
            #print(type(line))
            #pass
            line.set_color('r')
            #x = np.asarray([0,0])
            #y = np.asarray([0,0])
            #z = np.asarray([0,0])
        #if i == 47:
            #x = np.asarray([0,0])
            #y = np.asarray([0,0])
            #z = np.asarray([0,0])
            #print(frame_num, [results_list[frame_num][i]])
        line.set_data(x,y)
        line.set_3d_properties(z)
        i = i+1
    
    ax.set_xlim3d([x_lower_limit, x_upper_limit])
    ax.set_ylim3d([y_lower_limit, y_upper_limit])
    ax.set_zlim3d([z_lower_limit, z_upper_limit])
    ax.set_xlabel('X')
    
    ax.set_ylabel('Y')
    
    ax.set_zlabel('Z')
    time_text.set_text('Frame = %.1d' % frame_num)
    return lines


# Attaching 3D axis to the figure
fig = plt.figure()
ax = p3.Axes3D(fig)

file_name = '1.24.22.0'
readfile = open("bin/filtered_data/" + file_name + ".pickle", "rb")
loaded_results = pickle.load(readfile)



lines = [ax.plot(l[0], l[1], l[2])[0] for l in loaded_results[1]]


x_upper_limit = 0.75
x_lower_limit = -0.75

y_upper_limit = 0.75
y_lower_limit = -0.75

z_upper_limit = 0.5
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

def onClick(event):
    global pause
    pause ^= True
fig.canvas.mpl_connect('button_press_event', onClick)

# Creating the Animation object
#len(body_3D_pose[0])
ani = animation.FuncAnimation(fig, update_lines, len(BODY3DPOSE[0]), fargs = [loaded_results, lines, time_text],
                                   interval=100, blit=False, repeat = True)
Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
ani.save(file_name +'.mp4', writer=writer)

plt.show()
