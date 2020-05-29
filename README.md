# F-FI224-4: Robotic cooking through pose extraction from human natural cooking using OpenPose

<img src=humangif.gif width="450" height="254" /> <img src=robotgif.gif width="450" height="254" />

This GitHub repository contains all the code used durin the F-FI224-4 masters project, carried out from 2019-2020 in the BIRL lab

## Related Libraries

### OpenPose

This project has relied heavy on to OpenPose pretrained neural network to localise joint positions in 2D colour video. This was chosen both because it track fingers, and because it has a compliation free demo. The main OpenPose repository can be [found here](https://github.com/CMU-Perceptual-Computing-Lab/openpose)

#### OpenPose Windows Portable Demo Installation Instructions

1) Download latest version of the demo from [this link](https://github.com/CMU-Perceptual-Computing-Lab/openpose/releases). Each version has multiple files attached to it, im unsure as to the exact difference between these. This project has been using 'openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended', but a more recent version has been released since then. To reiterate, you only need ONE of the cluster of files listed in the most recent version

2) Extract downloaded zip file

3) Follow the instructions in the file 'Instructions.txt'. For clarifty, these are

    a) Open folder 'models'

    b) Double click 'getModels.bat' to download what I believe is aditional information to do with foot and hand tracking (this may take a few minutes)

#### Using the OpenPose Windows Portable Demo

With the above completed, the demo can be run by exceuting the file 'bin/OpenPoseDemo', either by double clicking it or through the command line.

Using the command line allows a numebr of additional parameters to be specified, like which camera to use (if there are multiple), the maximum number of people to track in an image, whether to save the resulting joint positions and in what format they would be saved, and whether to save the video of the human skeletons superimposed on the imput video, etc. 

The way the output of the demo is/can be structures is [described here](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/output.md)

#### Issues with the OpenPose Windows Portable Demo

At least twice during this project windows defender on the labs Windows 10 dell PC has (apparaently spontaneously) started declaring an error message that 'this file cannot be run on this pc' when attempting to run the demo. Unsintalling (i.e. deleting the OpenPose folder) and reinstalling OpenPose a described above fixes this issue when it comes up

### PyKinect2

This project also heavily relied on the PyKinect2 library to communicate with the Kinect 2 colour and depth camera used. This can be found at the following [link](https://github.com/Kinect/PyKinect2).

#### Installation Instructions

The package is avaialble through pip, so can be installed with 

````bash
pip install pykinect2
````

#### Issues with PyKinect2 - PLEASE READ

Before deciding to use this library, please note that it is both undocumented and unsupported, which will increase your develpment time (took me about a month to figure out how to get it to do what I wanted for this project). While it is based on a well documented C++ library ([source](https://www.microsoft.com/en-gb/download/details.aspx?id=44561), [documentation](https://docs.microsoft.com/en-us/previous-versions/windows/kinect/dn782033(v=ieb.10)) ), using the C++ doumentation to get anything more than what functions exist in the python code prooved difficult in my experience. I have written some demonstration programs to better explain to how to use the PyKinect V2 library ([linked here](https://github.com/Kinect/PyKinect2/issues/79)), so hopefully future students wont struggle as much as I did when first using the library. In summary, please note that finding out how to do new commands with this library cans be difficult - even I dont understand what all the defines required to get my code to work mean. 

### Generic UR5 Controller

To command the UR5, this project used the [generic UR5 controller](https://github.com/kg398/Generic_ur5_controller) library

#### Setting up the UR5

Setting up the UR5 to accept commands via this library requires changing some settings on the UR5 itself, via its touch screen interface. A guide to how to do this is laid out below

1)	Connect your computer to the UR5 (this requires an ethernet cable, if your computer lacks such a port use a USB to ethernet converter). The robots ethernet port is (I believe) on its black controll box

2) Ensure that the robot is on

3) On your computer, use ````ipconfig````  in command line to get your ethernet IP adress (you want the top IP adress listed in the ethernet IP block of text)

4) On your computer, open the 'kg_robot' file

5) Update self.host (line 27 in the version I am using) with the ethernet IP you recorded in step 3

6) Go to the file Generic_ur5_controller.py (or whichever file you intend to use to command the robot from python). You will see a line along the lines of ````burt = kgr.kg_robot(port=30010,db_host="192.168.1.10")````, which initiates communication between your computer and teh robot. Change the ````db_host```` variable to an IP adress similar to your ethernet IP from step 3, but with the last number changes. You will need to use an adress like your IP but with the last number changed in ANY file fro which you want to command the robot

7) Swap to the UR5 touch screen

8) load program 'kg client' on the UR5 touch screen

9)	Press the 'robot program' button to open a list of varaibles. Open var1 (socket) (it should be open by default) and change to the IP adress you recorded in step 3

10) Press 'Setup robot' on the touchscreen

11) Press 'network' on the touchscreen

12) Enter the dashboard IP you used in step 6 in the 'dashboard' section

13) Press apply


## Description of Repository Structure

The main folder of the repository contains both the majority of the relavant python files, as well as the UR5's used kinaesthteic trajectories as JSON files. 

### Files

#### Kinect Output Viewer Files
##### colur_3D_locator
Allows you to click on a pixel from the Kinect colour stream and read its depth

##### depthviewer
Allows you to view the current connect depth stream

### Pose Transform Files
##### coordinate_transforms
Provides functions to transform from camera centric coordinates to world coordiantes (i.e. z is up), and from world coordinates to the UR5 arm's coordinate system

##### get_3D_pose
Takes the values recorded by OpenPose in a JSON file, converts them to a more understandable format, then converts the to UR5 arm centric coordinates. Due to quirks with PyKinect2, THIS REQUIRES EITHER A KINECT TO BE PLUGGED INTO THE COMPUTER OF KINECT STUDIO TO BE RUNNING A RECORDING to work, despite the fact the we are operating on saved rather than live kinect data. 

### Data Storage Files
#### CSV_save_unfiltered_data

##### save_unfiltered_data_easter
##### save_filtered_data_easter

### Data View/ Analysis Files
##### display_smoothed_data
##### plotfilteredunfiltered

##### animate_saved_data

##### easter_noise_analysis


### Example Files
##### follow_me_updated_openpose
Code to command the UR5 to move its end effector along the trajectory of the wrist from a recording. 


### Folders

#### JSONTrajectories

Contains kinaesthetically taught UR5 trajectories that were not used in the final cooking demonstrations

#### bin

Contains the watch.py file which calles openpose from python. This is in the bin folder as it has to be in the same folder as the OpenPoseDemo.exe file (I couldnt figure out how to call a terminal from python in another folder, it might be possible). 

#### MATLABCode

Contains all of this project's MATLAB code. This contains the code for defining bounding boxes around the kitchen tools, extracting time from the detected pose trajectory, carrying out distance correlation and plotting many of the graphs used in my masters report. This code reads CSV pose trajectory files produced by the python code

#### old_python_code

Contains less important/ malfunctioning variants of the code included in the main folder, as well as test code. Could be worth searching through if you want to extend on this project and you find yourself wanting to carry out some process that I also tried and failed to do very well. 

## Advice

## Kinect Studio

## Matlab Camerea Calibration Tool

# Todo:

* spellcheck
* only keep final json files in front page of repository
* subfolder readmes
