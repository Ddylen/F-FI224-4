"""
File to save unfiltered data in a CSV file, the data format that is used as the input for the MATLAB code of this project
"""
import numpy as np
import time
from scipy import signal
import pickle
import sys
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import csv
from scipy import signal

from get_3D_pose import HAND, BODY, get_arm_3D_coordinates


def save_CSV(file_name):
    """Save filtered trajectory to CSV"""
    
    #Get 3D pose in arm coordinates
    BODY3DPOSE, LEFTHAND3DPOSE,RIGHTHAND3DPOSE = get_arm_3D_coordinates(file_name, confidence_threshold = 0)
    
    #define a custom string for the CSV file names
    extrastring = "REDO"
    
    #Save file name
    with open(file_name + "filtered" + extrastring + ".csv", 'w', newline='') as file:
        
        #Open CSV writer
        filteredwriter = csv.writer(file)
        
        #Iterate over lists of body and hand poses
        for pose_list in BODY3DPOSE, LEFTHAND3DPOSE,RIGHTHAND3DPOSE:
            
            #Define a tracking varaible to allow us to keep track of which joint we are talking about
            i = 0
        
            #Iterate over each tracked point on the list
            for joint in pose_list:
                
                #remove first value from JSON, which contains no information
                joint = joint[1:]
                
                #extract x, y, z and lost_track lists
                plot_list_x = [entry[0] for entry in joint]
                plot_list_y = [entry[1] for entry in joint]
                plot_list_z = [entry[2] for entry in joint]
                invalid_list = [entry[3] for entry in joint]
                
                #Define an empty list that will be filled with tha above lists with the invalid points replaced by their last good value
                new_plot_list_x = []
                new_plot_list_y = []
                new_plot_list_z = []
                new_invalid_list = []
                
                #initialis a list of the last good x, y and z value seen (used to overwrite bad values)
                lastgoodvallist = [1,1,1]
                
                #define region of interest, outside of which points are bad
                xlim = [-1, 1]
                ylim = [-0.5, 2]
                zlim = [-2,2]
                
                #define properties of the savgol filter
                window_length, polyorder = 21, 2
                
                #iterate over each frame
                for frame in range(len(plot_list_x)):
                    
                    #intialise variable to keep trak of whether points are invalid
                    valgood = True
                    
                    #Assign points as ivalid if they are set to the error value of -99, or are outside the region of interest
                    if plot_list_x[frame] == -99 or plot_list_x[frame] < xlim[0] or plot_list_x[frame] > xlim[1]:
                        valgood = False
                    if plot_list_y[frame] == -99 or plot_list_y[frame] < ylim[0] or plot_list_y[frame] > ylim[1]:
                        valgood = False
                    if plot_list_z[frame] == -99 or plot_list_z[frame] < zlim[0] or plot_list_z[frame] > zlim[1]:
                        valgood = False
                    
                    #Append last good value to the new list of values if the current value is bad
                    if valgood == False:
                        new_plot_list_x.append(lastgoodvallist[0])
                        new_plot_list_y.append(lastgoodvallist[1])
                        new_plot_list_z.append(lastgoodvallist[2])
                    
                    else:
                        
                        #Update last good val list
                        lastgoodvallist = [plot_list_x[frame], plot_list_y[frame], plot_list_z[frame]]
                        
                        #Append current value to the new list
                        new_plot_list_x.append(plot_list_x[frame])
                        new_plot_list_y.append(plot_list_y[frame])
                        new_plot_list_z.append(plot_list_z[frame])
                
                #Track which joint we are urrently tracking
                if pose_list == BODY3DPOSE:
                    ident_string = BODY(i).name
                elif pose_list == LEFTHAND3DPOSE:
                    ident_string = "Left" + HAND(i).name
                elif pose_list == RIGHTHAND3DPOSE:
                    ident_string = "Right" + HAND(i).name
                
                #Apply savgol filter to our new filtered x, y and z list
                savgol_plot_list_x = signal.savgol_filter(new_plot_list_x, window_length, polyorder)
                savgol_plot_list_y = signal.savgol_filter(new_plot_list_y, window_length, polyorder)
                savgol_plot_list_z = signal.savgol_filter(new_plot_list_z, window_length, polyorder)
                
                #Convert format to list
                savgol_plot_list_x = savgol_plot_list_x.tolist()
                savgol_plot_list_y = savgol_plot_list_y.tolist()
                savgol_plot_list_z = savgol_plot_list_z.tolist()
                
                #Add the name of the joint being tracked to the the start of the list (and so CSV file)
                savgol_plot_list_x.insert(0,ident_string + " X Value")
                savgol_plot_list_y.insert(0,ident_string+ " Y Value")
                savgol_plot_list_z.insert(0,ident_string + " Z Value")
                invalid_list.insert(0, ident_string + " Invalid?")
                
                #Write filtered values to CSV
                filteredwriter.writerow(savgol_plot_list_x)
                filteredwriter.writerow(savgol_plot_list_y)
                filteredwriter.writerow(savgol_plot_list_z)
                filteredwriter.writerow(invalid_list)
                
                #Update which joint we are referring to
                i = i+1
    
    #Seperately, save the unfiltered raw input to a CSV file for reference
    with open(file_name + extrastring + '.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        
        #define varaibles to keep track of which joint we are referring to in each block of rows
        i_body = 0
        i_left = 0
        i_right = 0
        
        #Write unfiltered body data to a new CS file
        for row in BODY3DPOSE:
                rowcopy = row[1:]
                rowcopy.insert(0, [BODY(i_body).name + " X Value", BODY(i_body).name +" Y Value", BODY(i_body).name +" Z Value", BODY(i_body).name +" Invaid?"])
                writer.writerow([entry[0] for entry in rowcopy])
                writer.writerow([entry[1] for entry in rowcopy])
                writer.writerow([entry[2] for entry in rowcopy])
                writer.writerow([entry[3] for entry in rowcopy])
                i_body +=1 
        
        #Write unfiltered left hand data to a new CS file        
        for row in LEFTHAND3DPOSE:
                rowcopy = row[1:]
                rowcopy.insert(0, ["Left "+ HAND(i_left).name + " X Value", "Left "+ HAND(i_left).name + " Y Value", "Left "+ HAND(i_left).name + " Z Value", "Left "+ HAND(i_left).name + " Invalid?"])
                writer.writerow([entry[0] for entry in rowcopy])
                writer.writerow([entry[1] for entry in rowcopy])
                writer.writerow([entry[2] for entry in rowcopy])
                writer.writerow([entry[3] for entry in rowcopy])    
                i_left +=1 
                
        #Write unfiltered right hand data to a new CS file        
        for row in RIGHTHAND3DPOSE:
                rowcopy = row[1:]
                rowcopy.insert(0, ["Right "+ HAND(i_right).name+ " X Value", "Right "+ HAND(i_right).name + " Y Value", "Right "+ HAND(i_right).name + " Z Value", "Right "+ HAND(i_right).name + " Invalid?"])
                writer.writerow([entry[0] for entry in rowcopy])
                writer.writerow([entry[1] for entry in rowcopy])
                writer.writerow([entry[2] for entry in rowcopy])
                writer.writerow([entry[3] for entry in rowcopy])
                i_right +=1 

    
if __name__ == "__main__":

    #file_name = 'mockcook.14.2.17.36'
    #file_name = '1.24.21.47'
    #file_name = "2.7.16.13"
    #file_name = '1.24.22.0'
    #file_name = "smallpantry1.17.2.16.58"
    #file_name = "smallpantry2heat7.17.2.17.6"
    #file_name = "march10.10.3.15.1"
    #file_name = "firstcomparison.11.3.14.18"
    #file_name = "trial1dylan.12.3.16.31"
    #file_name = "trial3josie.13.3.13.11"
    #file_name = "trial6dylan.16.3.9.50"
    #file_name = "trial7thomas.16.3.10.24"
    #file_name = "trial7josie.17.3.10.31"
    #file_name = "testtrial8luca.17.3.11.12"
    file_name = "test9keiran.17.3.11.40"
    #file_name = 'stationarytrial3.17.3.9.43'
    #file_name = '1.24.21.47'
    #file_name = '1.24.21.52'
    #file_name = '1.24.22.0'
    #file_name = '2.7.16.13'
    #file_name = '2.7.16.27'
    
    save_CSV(file_name)
    