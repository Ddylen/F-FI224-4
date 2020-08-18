## Instructions


First, note that the code in this repository is meant to be saved inside the main folder of the downloaded OpenPose package. Folder names in this repository that also occur in OpenPose indicate that the relevant files should be places inside the corresponding OpenPose folder.

With that done, the steps to replicating my work are

1) Set up work surface in front of the Kinect, ensuring that the demonstrator is in view

2) Plug Kinect into computer using USB cable

3) (Optional) Calibrate the pose of your Kinect in world coordinates using the MATLAB camera calibration tool, and update coordinate_transforms.py with the appropriate camera to world coordinates transformation matrix. 

4) Run watch.py in the bin folder, then carry out your demonstration. This records a series of colour and depth frames from the Kinect until you press the 'esc' key. It then, at the end of the recording, stiches the colour frames into a video, and passes this to OpenPose with the appropriate commands. OpenPose saves the joint positions in each frame in a JSON file

5) Run CSV_save_filtered_data.py (changing the file_name variable to the name of the saved file of data you want to process) to convert the saved joint positions and depth frames into 3D pose trajectories in world coordinates, and then save that as a CSV file to pass to the MATLAB code

6) Run import_scipt.m (changing the 'file' variable to the name of the appropriate CSV file) to load the appropriate CSV file into MATLAB

7) Run trajectory_processing_openpose_final.m to extract the key times from the trajectory

8) Update UR5CookingProgram.py with said key times.

9) Power on the UR5, and set it up as described before if you have not already done so. Connect it to your computer using an ethernet cable. Make sure that the gripper Arduino board is connected to you PC, powered on, and has no loose cables. 

10) Execute UR5CookingProgram.py, to make the UR5 cook

11) (Optional) run saved_filtered_data_easter.py to carrying out slightly different filtering on the 3D pose trajectory, that was done to try and create nice looking animations. While the filtering makes the animations look a bit better, the animations still look janky so this is not as polished as it could be

12) (Optional) run animate_saved_data.py to see an animation of the recorded pose


## Notes
OpenPose can fail to track the fingers if they are obscured by the back of the hand, try to choose a camera angle that avoids that from occurring during common recipe motions

The code I have written explicitly commands OpenPose to only track one person in the image. If a second person walks into the video of the demonstration, OpenPose may start tracking them instead. There should be a way to avoid this but I did not investigate it, instead just requiring that only one person was in the field of view of the Kinect. 
