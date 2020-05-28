# F-FI224-4: Robotic cooking through pose extraction from human natural cooking using OpenPose


This GitHub repository contains all the code used durin the F-FI224-4 masters project, carried out from 2019-2020 by Dylan Danno with supervision from Fumiya Iida and assistance from Simon Hauser and Thomas Thuruthel

## Related Libraries

### OpenPose

This project has relied heavy on to OpenPose pretrained neural network to localise joint positions in 2D colour video. This was chosen both because it track fingers, and because it has a compliation free demo. The main OpenPose repository can be found here: https://github.com/CMU-Perceptual-Computing-Lab/openpose

#### OpenPose Windows Portable Demo Installation Instructions

1) Download latest version of the demo from this link: https://github.com/CMU-Perceptual-Computing-Lab/openpose/releases. Each version has multiple files attached to it, im unsure as to the exact difference between these. This project has been using 'openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended', but a more recent version has been released since then. To reiterate, you only need ONE of the cluster of files listed in the most recent version

2) Extract downloaded zip file

3) Follow the instructions in the file 'Instructions.txt'. For clarifty, these are

    a) Open folder 'models'

    b) Double click 'getModels.bat' to download what I believe is aditional information to do with foot and hand tracking (this may take a few minutes)

#### Using the OpenPose Windows Portable Demo

With the above completed, the demo can be run by exceuting the file 'bin/OpenPoseDemo', either by double clicking it or through the command line.

Using the command line allows a numebr of additional parameters to be specified, like which camera to use (if there are multiple), the maximum number of people to track in an image, whether to save the resulting joint positions and in what format they would be saved, and whether to save the video of the human skeletons superimposed on the imput video, etc. 

#### Issues with the OpenPose Windows Portable Demo

At least twice during this project windows defender on the labs Windows 10 dell PC has (apparaently spontaneously) started declaring an error message that 'this file cannot be run on this pc' when attempting to run the demo. Unsintalling (i.e. deleting the OpenPose folder) and reinstalling OpenPose a described above fixes this issue when it comes up

## PyKinect V2

This project also heavily relied on the PyKinect V2 library to communicate with the Kinect 2 colour and depth camera used. This can be found at the following link: https://github.com/Kinect/PyKinect2. 

Before deciding to use this library, please note that it is both undocumented and unsupported, which will increase your develpment time (took me about a month to figure out how to get it to do what I wanted for this project). While it is based on a well documented C++ library (source: https://www.microsoft.com/en-gb/download/details.aspx?id=44561, documentation: https://docs.microsoft.com/en-us/previous-versions/windows/kinect/dn782033(v=ieb.10) ), using the C++ doumentation to get anything more than what functions exist in the python code prooved difficult in my experience. I have written some demonstration programs to better explain to how to use the PyKinect V2 library (https://github.com/Kinect/PyKinect2/issues/79), so hopefully future students wont struggle as much as I did when first using the library. In summary, please note that finding out how to do new commands with this library cans be difficult - even I dont understand what all the defines required to get my code to work mean. 

## Description of Repository Structure

## Advice

# Todo:

* Remoev junk markdown from end
* spellcheck
* did i need any extra stages to get pykinect set up with me environment?

## Usage
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install foobar
```

## Usage

```python
import foobar

foobar.pluralize('word') # returns 'words'
foobar.pluralize('goose') # returns 'geese'
foobar.singularize('phenomena') # returns 'phenomenon'
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
