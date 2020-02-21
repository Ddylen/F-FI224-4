"""Code to save a video based on frames saved in a pickle file"""

import cv2
import pickle
import time


images = []
datafile = open("depthdata/COLOUR12.3.14.50.pickle", "rb")

frame = pickle.load(datafile)
height, width, channels = frame.shape
#print(height)
#print(width)
out = cv2.VideoWriter('videos/staystill.avi', cv2.VideoWriter_fourcc(*'DIVX'), 10, (int(width), int(height))) #TODO: look in to why I have to say 30fs or else it goes to slow

#frame = cv2.imread(im0)
#print(type(frame))
#print(frame.shape)
#frame = cv2.flip(frame,0)
out.write(frame)
cv2.imshow('video',frame)


# Define the codec and create VideoWriter object
while True:
    try:
        frame = pickle.load(datafile)
        #frame = cv2.imread(im)
        #frame = cv2.flip(frame,0)
        #print(frame.shape)
        out.write(frame)
        cv2.imshow('video',frame)
        time.sleep(0.1)
        if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
            break
    except EOFError:
        print("end")
        break
print("done")
# Release everything if job is finished
out.release()
cv2.destroyAllWindows()