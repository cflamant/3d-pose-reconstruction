#!/usr/bin/env python
#Author: Cedric Flamant

# How to launch:
# In a terminal, while in this directory, simply run

# python run.py

import numpy as np
import pointstopos
import renderstick
import gui
import displaynewpoints
import optimizepoints


points,pradii,relorder,File=gui.selectpoints()
newpoints,newrelorder = optimizepoints.opt(points,pradii,relorder)
pos,scale = pointstopos.points2pos(newpoints,newrelorder,0.)
displaynewpoints.showpoints(points,newpoints,pradii,File)
renderstick.renderstick(pos)




