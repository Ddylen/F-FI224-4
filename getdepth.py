# -*- coding: utf-8 -*-

"""
Recover the depth of a defined pixel
"""

import pickle
import numpy as np

xinput = 200/424
yinput = 200/512

datafile = open("depthdata/DEPTH11.15.13.49.pickle", "rb")
depthframe = pickle.load(datafile)
depthframe = np.reshape(depthframe, (424, 512))



datax = round(xinput*424) #TODO: Interpolation/ local averaging of the depth, to reduce noise
datay = round(yinput*512)

measured_depth = depthframe[datax][datay]

print(measured_depth)