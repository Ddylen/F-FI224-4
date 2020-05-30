# F-FI224-4: Robotic cooking through pose extraction from human natural cooking using OpenPose

<img src=githubgraphics/humangif.gif width="450" height="254" /> <img src=githubgraphics/robotgif.gif width="450" height="254" />

This GitHub repository contains all the code used during the F-FI224-4 masters project, carried out from 2019-2020 in the BIRL lab

## Prerequisites

### OpenPose

This project has relied heavy on to OpenPose pretrained neural network to localise joint positions in 2D colour video. This was chosen both because it track fingers, and because it has a compilation free demo. The main OpenPose repository can be [found here](https://github.com/CMU-Perceptual-Computing-Lab/openpose)

#### OpenPose Windows Portable Demo Installation Instructions

1) Download latest version of the demo from [this link](https://github.com/CMU-Perceptual-Computing-Lab/openpose/releases). Each version has multiple files attached to it, I’m unsure as to the exact difference between these. This project has been using 'openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended', but a more recent version has been released since then. To reiterate, you only need ONE of the cluster of files listed in the most recent version

2) Extract downloaded zip file

3) Follow the instructions in the file 'Instructions.txt'. For clarity, these are

    a) Open folder 'models'

    b) Double click 'getModels.bat' to download what I believe is additional information to do with foot and hand tracking (this may take a few minutes)

#### Using the OpenPose Windows Portable Demo

With the above completed, the demo can be run by executing the file 'bin/OpenPoseDemo', either by double clicking it or through the command line.

Using the command line allows a number of additional parameters to be specified, like which camera to use (if there are multiple), the maximum number of people to track in an image, whether to save the resulting joint positions and in what format they would be saved, and whether to save the video of the human skeletons superimposed on the input video, etc. 

The way the output of the demo is/can be structures is [described here](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/output.md)

#### Issues with the OpenPose Windows Portable Demo

At least twice during this project windows defender on the labs Windows 10 dell PC has (apparently spontaneously) started declaring an error message that 'this file cannot be run on this pc' when attempting to run the demo. Uninstalling (i.e. deleting the OpenPose folder) and reinstalling OpenPose a described above fixes this issue when it comes up

### PyKinect2

This project also heavily relied on the PyKinect2 library to communicate with the Kinect 2 colour and depth camera used. This can be found at the following [link](https://github.com/Kinect/PyKinect2).

#### Installation Instructions

The package is available through pip, so can be installed with 

````bash
pip install pykinect2
````

#### Issues with PyKinect2 - PLEASE READ

Before deciding to use this library, please note that it is both undocumented and unsupported, which will increase your development time (took me about a month to figure out how to get it to do what I wanted for this project). While it is based on a well documented C++ library ([source](https://www.microsoft.com/en-gb/download/details.aspx?id=44561), [documentation](https://docs.microsoft.com/en-us/previous-versions/windows/kinect/dn782033(v=ieb.10)) ), using the C++ documentation to get anything more than what functions exist in the python code proved difficult in my experience. I have written some demonstration programs to better explain to how to use the PyKinect V2 library ([linked here](https://github.com/Kinect/PyKinect2/issues/79)), so hopefully future students wont struggle as much as I did when first using the library. In summary, please note that finding out how to do new commands with this library cans be difficult - even I don’t understand what all the defines required to get my code to work mean. 

### Generic UR5 Controller

To command the UR5, this project used the [generic UR5 controller](https://github.com/kg398/Generic_ur5_controller) library

#### Setting up the UR5

Setting up the UR5 to accept commands via this library requires changing some settings on the UR5 itself, via its touch screen interface. A guide to how to do this is laid out below

1)	Connect your computer to the UR5 (this requires an ethernet cable, if your computer lacks such a port use a USB to ethernet converter). The robots ethernet port is (I believe) on its black control box

2) Ensure that the robot is on

3) On your computer, use ````ipconfig````  in command line to get your ethernet IP address (you want the top IP address listed in the ethernet IP block of text)

4) On your computer, open the 'kg_robot' file

5) Update self.host (line 27 in the version I am using) with the ethernet IP you recorded in step 3

6) Go to the file Generic_ur5_controller.py (or whichever file you intend to use to command the robot from python). You will see a line along the lines of ````burt = kgr.kg_robot(port=30010,db_host="192.168.1.10")````, which initiates communication between your computer and the robot. Change the ````db_host```` variable to an IP address similar to your ethernet IP from step 3, but with the last number changes. You will need to use an address like your IP but with the last number changed in ANY file from which you want to command the robot

7) Swap to the UR5 touch screen

8) load program 'kg client' on the UR5 touch screen

9)	Press the 'robot program' button to open a list of variables. Open var1 (socket) (it should be open by default) and change to the IP address you recorded in step 3

10) Press 'Setup robot' on the touchscreen

11) Press 'network' on the touchscreen

12) Enter the dashboard IP you used in step 6 in the 'dashboard' section

13) Press apply

### Kinect Studio
This software allows you toe record and replay colour and depth video from the Kinect. Some parts of my code require the computer to be connect to a Kinect, said programs also work if the computer as Kinect Studio open and playing a recorded video (note that such videos can be played on loop so a long recording isn’t necessary, which is beneficial as Kinect studio recordings take up a lot of memory)

Kinect studio can be downloaded from [here](https://www.microsoft.com/en-us/download/details.aspx?id=44561)

### MATLAB Camera Calibration Tool

The MATLAB camera calibration tool was used to assist in locating the pose of the camera in world coordinates. While it did occasionally work in my case, it often returned axes that were significantly out from the actual world coordinate system I was trying to find (I had to correct such errors manually). I suspect this was because my A3 checkerboards did not take up 20% of the images when laid on the kitchen worksurface, so if using this tool for calibration make sure your checkboards are large enough to take up 20% of the image from the Kinect. 


I believe that the tool comes with the standard MATLAB install.

<img src=githubgraphics/cameracalibrator.PNG  width="450" height="254"/>

Documentation of the tool can be found [here](https://uk.mathworks.com/help/vision/ref/cameracalibrator-app.html)


## Description of Repository Structure

The main folder of the repository contains both the majority of the relevant python files, as well as the UR5's used kinaesthetic trajectories as JSON files. 

### Files

#### Kinect Output Viewer Files
###### colur_3D_locator
Allows you to click on a pixel from the Kinect colour stream and read its depth

###### depthviewer
Allows you to view the current connect depth stream

###### bin/watch
Main file for recording data from the Kinect, stitching it into videos and then calling OpenPose to run on it. Must be located in the bin folder to call OpenPose correctly (as in, I couldn’t figure out how to get python to call a terminal command in another folder)


#### Pose Transform Files
###### coordinate_transforms
Provides functions to transform from camera centric coordinates to world coordinates (i.e. z is up), and from world coordinates to the UR5 arm's coordinate system

###### get_3D_pose
Takes the values recorded by OpenPose in a JSON file, converts them to a more understandable format, then converts the to UR5 arm centric coordinates. Due to quirks with PyKinect2, THIS REQUIRES EITHER A KINECT TO BE PLUGGED INTO THE COMPUTER OF KINECT STUDIO TO BE RUNNING A RECORDING to work, despite the fact the we are operating on saved rather than live Kinect data. 

#### Data Storage Files
###### CSV_save_filtered_data
Saves filtered pose trajectory data as a CSV file for the MATLAB analysis code

###### save_unfiltered_data_easter
Saves unfiltered pose trajectory as a pickle file, for analysis/animation in python

###### save_filtered_data_easter
Saves filtered pose trajectory as a pickle file, for analysis/animation in python

#### Data View/ Analysis Files
###### display_smoothed_data
Plots smoothed 2D wrist trajectory

###### plotfilteredunfiltered
Plots both the smoothed and unsmoothed X trajectory of the wrist to show the effect of filtering

###### animate_saved_data
Render a 3D wireframe skeleton to show the tracked pose (legs deliberately not rendered since their depth comes out wrong as they are under the table)

###### easter_noise_analysis
Code to get the standard deviation of the wrist position (useful for determining tracking accuracy from videos where the wrist is held stationary)

#### Example Files
###### follow_me_updated_openpose
Code to command the UR5 to move its end effector along the trajectory of the wrist from a recording. 


### Folders

#### JSONTrajectories

Contains kinaesthetically taught UR5 trajectories that were not used in the final cooking demonstrations

#### bin

Contains the watch.py file which called OpenPose from python. This is in the bin folder as it has to be in the same folder as the OpenPoseDemo.exe file (I couldn’t figure out how to call a terminal from python in another folder, it might be possible). 

#### MATLABCode

Contains all of this project's MATLAB code. This contains the code for defining bounding boxes around the kitchen tools, extracting time from the detected pose trajectory, carrying out distance correlation and plotting many of the graphs used in my masters report. This code reads CSV pose trajectory files produced by the python code

#### old_python_code

Contains less important/ malfunctioning variants of the code included in the main folder, as well as test code. Could be worth searching through if you want to extend on this project and you find yourself wanting to carry out some process that I also tried and failed to do very well. 

#### githubgraphics

Contains the gifs/images used in this markdown file

#### depthimages

Empty folder that depthviewer.py can save images from the recorded Kinect depth video to

## Replicating my Work

First, note that the code in this repository is meant to be saved inside the main folder of the downloaded OpenPose folder (hence the name). Folder names in this repository that also occur in OpenPose indicate that the relevant files should be places inside the corresponding OpenPose folder.

With that done, the steps to replicating my work are

1) Set up work surface in front of the Kinect, ensuring that demonstrator is in view

2) Plug Kinect into computer using USB cable

3) (Optional) Calibrate the pose of your Kinect in world coordinates using the MATLAB camera calibration tool, and update coordinate_transforms.py with the appropriate camera to world coordinates transformation matrix. 

4) Run watch.py in the bin folder, then carry out your demonstration. This records a series of colour and depth frames from the Kinect until you press the 'esc' key. It then, at the end of the recording, stiches the colour frames into a video, and passes this to OpenPose with the appropriate commands. OpenPose saved the joint positions in each frame in a JSON file

5) Run CSV_save_filtered_data.py (changing the file_name variable to the name of the saved file of data you want to process) to convert the saved joint positions and depth frames into 3D pose trajectories in world coordinates, and then saved that as  CSV file to pass to the MATLAB code

6) Run import_scipt.m (changing the 'file' variable to the name of the appropriate CSV file) to load the appropriate CSV file into MATLAB

7) Run trajectory_processing_openpose_final.m to extract the key times from the trajectory

8) Update UR5CookingProgram.py with said key times.

9) Power on the UR5, and set it up as described before if you have not already done so. Connect it to your computer using an ethernet cable. Make sure that the gripper Arduino board is connected to you PC, powered on, and has no loose cables. 

10) Execute UR5CookingProgram.py, to make the UR5 cook

11) (Optional) run saved_filtered_data_easter.py to carrying out slightly different processing on the 3D pose trajectory, that was done to try and create nice looking animations. While the filtering makes the animations look a bit better, the animations still look janky so this is not as polished as it could be

12) (Optional) run animate_saved_data.py to see an animation of the recorded pose


## Notes
OpenPose can fail to track the fingers if they are obscured by the back of the hand, try to choose a camera angle that avoids that from occurring during common recipe motions

The code I have written explicitly commands OpenPose to only track one person in the image. If a second person walks into the video of the demonstration, OpenPose may start tracking them instead. There should be a way to avoid this but I did not investigate it, instead just requiring that only one person was in the field of view of the Kinect.  

