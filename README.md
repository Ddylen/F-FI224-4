# F-FI224-4: Robotic cooking through pose extraction from human natural cooking using OpenPose

<img src=docs/githubgraphics/humangif.gif width="450" height="254" /> <img src=docs/githubgraphics/robotgif.gif width="450" height="254" />

This GitHub repository contains all the code used during the F-FI224-4 masters project, carried out from 2019-2020 in the BIRL lab

## Prerequisites

See [prerequisites](docs/prerequisites.md)


## Replicating my Work
 
See [instructions](docs/instructions.md)


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

###### UR5Cookingprogram
Code to get a UR5 to cook pancakes according to input timings

###### follow_me_updated_openpose
Code to command the UR5 to move its end effector along the trajectory of the wrist from a recording. 

#### JSON Files
Various JSON files that contain the kinaesthetically taught trajectories that the UR5 uses to cook are also included in this folder

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

