
"""Main file for recording data"""


from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import numpy as np
import cv2
import pickle
import datetime
import time 
import subprocess

""" 
TO DO
* get Openpose demo working, seem to recall I fixed it last time by reinstalling
* Get frame recording times to exactly 10FPS, not the 9.5-10.5 I see often currently
* Check recordings play back at the same speed as I record them
* Get simple/ rationalise/ documented noise collection/ imitation solution
"""


def save_frames(FILE_NAME):
    """records and saves colour and depth frames from the Kinect"""
    
    # define file names
    depthfilename = "rawdata\DEPTH." + FILE_NAME +".pickle"
    colourfilename = "rawdata\COLOUR." + FILE_NAME +".pickle"
    depthfile = open(depthfilename, 'wb')
    colourfile = open(colourfilename, 'wb')
    
    #initialise kinect recording, and some time varaivles for tracking the framerate of the recordings
    kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Depth)
    starttime = time.time()
    oldtime = 0
    i = 0
    fpsmax = 0
    fpsmin = 100
    
    # Actual recording loop, exit by pressing escape to close the pop-up window
    while True:
        elapsedtime = time.time()- starttime
        
        #Used to have a check here that we had new data, dont think that actually helped, so have removed it- the check was: 
        #if kinect.has_new_depth_frame() and kinect.has_new_color_frame() :
        
        
        while(elapsedtime> i/10): #TODO find better timing method
            
            #Only for high i try evalutaing FPS or else you get some divide by 0 errors
            if i >30:
                try:
                    fps =  1/(elapsedtime - oldtime)
                    print(fps)
                    if fps> fpsmax:
                        fpsmax= fps
                    if fps < fpsmin:
                        fpsmin = fps

                except ZeroDivisionError:
                    print("Divide by zero error")
                    pass
                
            oldtime = elapsedtime
            
            #read kinect colour and depth data (somehow the two formats below differ, think one is and one isnt ctypes)
            depthframe = kinect.get_last_depth_frame() #data for display
            depthframeD = kinect._depth_frame_data
            colourframe = kinect.get_last_color_frame()
            colourframeD = kinect._color_frame_data
            
            #convert depth frame from ctypes to an array so that I can save it
            depthframereadable = np.copy(np.ctypeslib.as_array(depthframeD, shape=(kinect._depth_frame_data_capacity.value,))) # TODO FIgure out how to solve intermittent up to 3cm differences
            pickle.dump(depthframereadable, depthfile)
            
            depthframe = depthframe.astype(np.uint8)
            depthframe = np.reshape(depthframe, (424, 512))
            depthframe = cv2.cvtColor(depthframe, cv2.COLOR_GRAY2RGB)

            
            #Reslice to remove every 4th value, which is superfluous
            colourframe = np.reshape(colourframe, (2073600, 4))
            colourframe = colourframe[:,0:3] #exclude superfluos values
            
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
    cv2.destroyAllWindows()

def frames_to_video(FILE_NAME):
    """Code to save a video based on frames saved in a pickle file"""
    
    #Load first colour frames, to get colour frame properties
    datafile = open("rawdata/COLOUR." + FILE_NAME + ".pickle", "rb")
    frame = pickle.load(datafile)
    height, width, channels = frame.shape
    
    #define video properties
    out = cv2.VideoWriter('videos/' + FILE_NAME + '.avi', cv2.VideoWriter_fourcc(*'DIVX'), 10, (int(width), int(height))) 
    
    #display first frame on a screen for progress (some duplication of later code as first frame needs to be loaded seperately to the rest so we can get the frame dimensions from it)
    out.write(frame)
    cv2.imshow('Stiching Video',frame)

    #Cycle through the rest of the colour frames, stiching them together
    while True:
        try:
            frame = pickle.load(datafile)
            out.write(frame)
            cv2.imshow('Stiching Video',frame)
            if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
                break
        except EOFError:
            print("Video Stiching Finished")
            break

    # Release everything if job is finished
    out.release()
    cv2.destroyAllWindows()

def run_openpose(FILE_NAME):
    #command_string = 'bin/OpenPoseDemo.exe --video videos/' + FILE_NAME + '.avi --write_video ' + FILE_NAME + '.Tagged.avi --write_json JSON/' + FILE_NAME + '/ --keypoint_scale 3'
    #os.system(command_string)

def watch():
    """Main function, call to start recording data"""
    currentdate = datetime.datetime.now()
    file_name = str(currentdate.month) + "." + str(currentdate.day) + "."+ str(currentdate.hour) + "."+ str(currentdate.minute)
    save_frames(file_name)
    frames_to_video(file_name)
    run_openpose(FILE_NAME)
    
if __name__ == "__main__":
    watch()
