"""
code to animate the recorded skeleton (assumes other files have already been run to process the data)
"""
import pickle
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import mpl_toolkits.mplot3d as plt3d
import matplotlib.animation as animation


def update_lines(frame_num, RESULTS_LIST, lines, time_text):
    """Function to update the drawn lines in the animation"""
    
    #Flag to state whether you should display data points flagged as false
    showfalse = True
    
    i = 0
    
    for line in lines:

        x = np.asarray(RESULTS_LIST[frame_num][i][0])

        y = np.asarray(RESULTS_LIST[frame_num][i][1])

        z = np.asarray(RESULTS_LIST[frame_num][i][2])
        
        if RESULTS_LIST[frame_num][i][3] == False:

            line.set_color('b')
  
        elif  RESULTS_LIST[frame_num][i][3] == True:

            line.set_color('r')
            
            if showfalse == True:
                x = np.asarray(RESULTS_LIST[frame_num][i][0])

                y = np.asarray(RESULTS_LIST[frame_num][i][1])

                z = np.asarray(RESULTS_LIST[frame_num][i][2])
            
            if showfalse == False:
                x = np.asarray([0,0])
                y = np.asarray([0,0])
                z = np.asarray([0,0])

        line.set_data(x,y)
        line.set_3d_properties(z)
        i = i+1
    
    

    time_text.set_text('Frame = %.1d' % frame_num)
    return lines


def animate(file_name):
    readfile = open("bin/filtered_data/" + file_name + ".pickle", "rb")
    loaded_results = pickle.load(readfile)
    
    # Attaching 3D axis to the figure
    fig = plt.figure()
    ax = p3.Axes3D(fig)
    
    x_upper_limit = 1
    x_lower_limit = 0
    
    y_upper_limit = 1
    y_lower_limit = 0
    
    z_upper_limit = 1
    z_lower_limit = 0
    ax.set_xlim3d([x_lower_limit, x_upper_limit])
    ax.set_ylim3d([y_lower_limit, y_upper_limit])
    ax.set_zlim3d([z_lower_limit, z_upper_limit])
    ax.set_xlabel('X')
    
    ax.set_ylabel('Y')
    
    ax.set_zlabel('Z')
    
    lines = [ax.plot(l[0], l[1], l[2])[0] for l in loaded_results[1]]
    
    # Setting the axes properties
    #ax.set_xlim3d([x_lower_limit, x_upper_limit])
    ax.set_xlabel('X')
    
    #ax.set_ylim3d([y_lower_limit, y_upper_limit])
    ax.set_ylabel('Y')
    
    #ax.set_zlim3d([z_lower_limit, z_upper_limit])
    ax.set_zlabel('Z')
    
    ax.set_title(file_name)
    time_text = ax.text(0,0.5,0,s= 'Frame = ',horizontalalignment='left',verticalalignment='top', transform=ax.transAxes)
    
    def onClick(event):
        global pause
        pause ^= True
    fig.canvas.mpl_connect('button_press_event', onClick)
    
    # Creating the Animation object
    #len(body_3D_pose[0])
    ani = animation.FuncAnimation(fig, update_lines, len(loaded_results), fargs = [loaded_results, lines, time_text],
                                       interval=100, blit=False, repeat = True)
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    ani.save(file_name +'.mp4', writer=writer)
    
    plt.show()

if __name__ == '__main__': 
    #file_name = '1.24.21.46'
    #file_name = '1.23.17.49'
    #file_name = '1.24.22.0'
    #file_name = 'stationaytrial5.17.3.9.44'
    file_name = 'trial7thomas.16.3.10.24'
    #file_name = 'trial6dylan.16.3.9.50'
    
    animate(file_name)