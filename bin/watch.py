"""
Main file for recording data, NEEDS TO BE INSIDE THE SAME FOLDER AS THE OPENPOSE DEMO
"""
import numpy as np
import cv2
import pickle
import time 
import os
import datetime

from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime


def save_frames(FILE_NAME):
    """records and saves colour and depth frames from the Kinect"""
    
    print("Saving colour and depth frames")
    
    #Create files that we will save the colour and depth frames to
    depthfilename = "rawdata\DEPTH." + FILE_NAME +".pickle"
    colourfilename = "rawdata\COLOUR." + FILE_NAME +".pickle"
    depthfile = open(depthfilename, 'wb')
    colourfile = open(colourfilename, 'wb')
    
    #Initialise kinect recording
    kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Depth)
    
    #Initilaise some time variables for tracking the framerate of the recordings
    starttime = time.time()
    oldtime = 0
    i = 0
    fpsmax = 0
    fpsmin = 100
    
    # Actual recording loop, exit by pressing escape to close the pop-up window
    while True:
        
        #Initilaise elapsed time, used to maintain framerate later
        elapsedtime = time.time()- starttime
        
        #Used to have a check here that we had new data, dont think that actually helped, so have removed it- the check was: 
        #if kinect.has_new_depth_frame() and kinect.has_new_color_frame() :
        
        #If over 0.1s have passed since this loop was last run
        while(elapsedtime> i/10):
                            
            try:
                
                #Evaluate FPS
                fps =  1/(elapsedtime - oldtime)
                
                #Print FPS
                print(fps)
                
                #Update max and min FPS seen
                if fps> fpsmax:
                    fpsmax= fps
                if fps < fpsmin:
                    fpsmin = fps
            
            except ZeroDivisionError:
                print("Divide by zero error")
                pass
            
            #Define last time at which a frame was recorded
            oldtime = elapsedtime
            
            #read kinect colour and depth data (somehow the two formats below differ, think one is and one isnt ctypes)
            depthframe = kinect.get_last_depth_frame() #data for display
            depthframeD = kinect._depth_frame_data
            colourframe = kinect.get_last_color_frame()
            colourframeD = kinect._color_frame_data
            
            #convert depth frame from ctypes to an array so that I can save it
            depthframereadable = np.copy(np.ctypeslib.as_array(depthframeD, shape=(kinect._depth_frame_data_capacity.value,))) # TODO FIgure out how to solve intermittent up to 3cm differences
            pickle.dump(depthframereadable, depthfile)
            
            #reformat the other depth frame format for it to be displayed on screen
            depthframe = depthframe.astype(np.uint8)
            depthframe = np.reshape(depthframe, (424, 512))
            depthframe = cv2.cvtColor(depthframe, cv2.COLOR_GRAY2RGB)

            #Reslice to remove every 4th colour value, which is superfluous
            colourframe = np.reshape(colourframe, (2073600, 4))
            colourframe = colourframe[:,0:3] 
            
            #extract then combine the RBG data
            colourframeR = colourframe[:,0]
            colourframeR = np.reshape(colourframeR, (1080, 1920))
            colourframeG = colourframe[:,1]
            colourframeG = np.reshape(colourframeG, (1080, 1920))        
            colourframeB = colourframe[:,2]
            colourframeB = np.reshape(colourframeB, (1080, 1920))
            framefullcolour = cv2.merge([colourframeR, colourframeG, colourframeB])
            pickle.dump(framefullcolour, colourfile)
            
            #Show colour frames as they are recorded
            cv2.imshow('Recording KINECT Video Stream', framefullcolour)
            
            i = i+1
    
        #end recording if the escape key (key 27) is pressed
        key = cv2.waitKey(1)
        if key == 27: break
    
    #Close pop up window
    cv2.destroyAllWindows()

def frames_to_video(FILE_NAME):
    """Code to stitch a video based on frames saved in a pickle file"""
    
    print("stiching colour frames into video")
    
    #Load first colour frame, to get colour frame properties
    datafile = open("rawdata/COLOUR." + FILE_NAME + ".pickle", "rb")
    frame = pickle.load(datafile)
    height, width, channels = frame.shape
    
    #Define video properties
    out = cv2.VideoWriter('videos/' + FILE_NAME + '.avi', cv2.VideoWriter_fourcc(*'DIVX'), 10, (int(width), int(height))) 
    
    #Display first frame on a screen for progress (some duplication of later code as first frame needs to be loaded seperately to the rest so we can get the frame dimensions from it)
    out.write(frame)
    cv2.imshow('Stiching Video',frame)

    #Cycle through the rest of the colour frames, stiching them together
    while True:
        
        try:
            
            #Load a frame
            frame = pickle.load(datafile)
            
            #Save frame to video
            out.write(frame)
            
            #Show frame in the pop up window
            cv2.imshow('Stiching Video',frame)
            
            #Close process if q is pressed
            if (cv2.waitKey(1) & 0xFF) == ord('q'):
                
                break
            
        #End video processing when we reach the end of the file    
        except EOFError:
            
            print("Video Stiching Finished")
            
            break

    #Release video writer if job is finished
    out.release()
    
    #Close pop up video if job is finished
    cv2.destroyAllWindows()


def run_openpose(FILE_NAME):
    """Function to run openpose (which requires command line) from python"""
    
    print("running openpose")
    
    #Define terminal string required to carry out desired command
    command_string = command_string = 'OpenPoseDemo.exe --hand --video videos/' + FILE_NAME + '.avi --write_video videos/' + FILE_NAME + '.Tagged.avi --write_json JSON/' + FILE_NAME + '/ --keypoint_scale 3 --number_people_max 1'
    
    #Send terminal string to terminal
    os.system(command_string)
    
    print("OpenPose Finished Sucessfully")
    
    
def watch():
    """Main function, call to start recording data"""
    
    #Define file name from user input
    currentdate = datetime.datetime.now()
    custom_name = input("Enter a file name: ")
    file_name = custom_name+ "." + str(currentdate.day) + "." + str(currentdate.month) + "."+ str(currentdate.hour) + "."+ str(currentdate.minute)
    
    #Save colour and depth frames
    save_frames(file_name)
    
    #Stich colour frames into video
    frames_to_video(file_name)
    
    #Run openpose on colour video
    run_openpose(file_name)
    
    #Print file name for easier copying
    print("File Name is :", file_name)
    
    
if __name__ == "__main__":
    
    watch()
