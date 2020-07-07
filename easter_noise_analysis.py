"""
Code for finding standard deviation of a trajectory useful for noise analysis if we know the tracked point is stationary
"""
import numpy as np
import pickle
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm


def find_stationary_standard_deviation(file_names, lengths):
    """Function to get standard deviation of position in files where the hand is held stationary"""
    
    #Create vectors for evaluating the average standard devitation between the differnt files above, either wieghted or unweighted by the length of the files
    std_store = [0,0,0,0]
    wheighted_std_store = [0,0,0,0]
    
    #create a counter for which file we are currently operating on
    filecounter = 0
    
    #Close all OpenCV windows
    plt.close('all')
        
    #For each file in our list of files
    for file_name in file_names:
        
        #Open file containing saved position of one point on the hand (the wrist)
        wristdatafile = open("bin/filtered_data/wrist." + file_name + ".pickle", "rb")
        wrist_list = pickle.load(wristdatafile)
        
        #Create a 3D plot
        fig = plt.figure()
        ax = Axes3D(fig)
        
        #Create a rainbow colourmap
        colors = cm.rainbow(np.linspace(0, 1, len(wrist_list)))
        
        #Assign different colours to each point, then ploy a scatter graph
        for val,c in zip (wrist_list, colors):
            ax.scatter(val[0], val[1], val[2], color = c)
    
        #Create empty list of points to create scatter plots of
        plot_list_x = []
        plot_list_y = []
        plot_list_z = []
        num_list = []
        
        #Create a counter to keep track of the length of data we record
        i = 0
        
        #For each entry in wrist_list (which tracks the wrist location), append the x, y and z values to their respective lists, 
        #and then create a list of integerrs counting upwards of equivalent length to help with he graphs later
        for val in wrist_list:
            plot_list_x.append(val[0])
            plot_list_y.append(val[1])
            plot_list_z.append(val[2])
            num_list.append(i)
            i = i+1
        
        #Plot the x, y and z data from each entry seperately
        fig = plt.figure()
        plt.plot(num_list, plot_list_x)
        plt.title('X data')
        
        fig = plt.figure()
        plt.plot(num_list, plot_list_y)
        plt.title('Y data')
        
        fig = plt.figure()
        plt.plot(num_list, plot_list_z)
        plt.title('Z data')
    
        #Calcualte the standard deviation in the x, y and z axes 
        x_std = np.std(plot_list_x)
        y_std = np.std(plot_list_y)
        z_std = np.std(plot_list_z)
        
        #Calculate the mean of the x,y and z axes
        x_mean = np.mean(plot_list_x)
        y_mean = np.mean(plot_list_y)
        z_mean = np.mean(plot_list_z)
        
        #Track the 3D distance of each point from the mean position
        distance_from_mean = []
        for i in range(len(plot_list_x)):
            distance_from_mean.append( np.sqrt((plot_list_x[i]-x_mean)**2 + (plot_list_y[i]-y_mean)**2+ (plot_list_z[i]-z_mean)**2))
        
        print("max distance from mean: ", max(distance_from_mean))
        print("min distance from mean: ", min(distance_from_mean))
        
        #Get standard deviation of the 3D distance from the mean
        std_3d = np.std(distance_from_mean)
        stdvec = [x_std, y_std, z_std, std_3d]
        print("Standard deviation vector: ", stdvec)
        print(" ")
        
        #Update the two vectors used to calculate an average standard deviation across trials
        for i in range(len(std_store)):
            std_store[i]+= stdvec[i]
            wheighted_std_store[i] += stdvec[i]*lengths[filecounter]
        filecounter += 1
    
    #Calculate average standard deviation across files
    std_store = np.divide(std_store, len(file_names))
    
    #Calcaulte average standard deviation across files wheighted by file length
    wheighted_std_store = np.divide(wheighted_std_store, np.sum(lengths))
    print("Average standard deviation across files: ", std_store)
    print("Weihted average standard deviation across files: ", wheighted_std_store)
    

if __name__ == '__main__': 
    
    find_stationary_standard_deviation(['stationarytrial1.17.3.9.38', 'stationarytrial2.17.3.9.41', 'stationarytrial3.17.3.9.43', 'stationaytrial4.17.3.9.43' , 'stationaytrial5.17.3.9.44' ], [36,65,4,38,50])

    #NOTE: These files are:
    
    #file_name = 'stationarytrial1.17.3.9.38'   #36s, hand on oil botle cap, nothing beneath it (dot on wrist close to shirt)
    #file_name = 'stationarytrial2.17.3.9.41'   #65s, hand on plate on salt tube (dot on shirt sleeve)
    #file_name = 'stationarytrial3.17.3.9.43'   #4s, very short, hand on salt shaker, dot on shirt
    #file_name = 'stationaytrial4.17.3.9.43'    #38s, hand on salt sharker (dot on shirt)
    #file_name = 'stationaytrial5.17.3.9.44'    #50s, hand on table (dot on shirt)


