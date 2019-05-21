#!/usr/bin/env python
#Author: Cedric Flamant

import numpy as np

def project(pos,scale):
    """ Given 3D positions and a scale factor, this method
    performs scaled orthographic projection to return 2D image points
    """
    # First 3 points of position vector, for the head, collarbone,
    # and tailbone, are not needed in the points vector which
    # only stores the image position of the joints (those three
    # can be calculated from the rest of the joint positions)
    points = np.copy(pos[3:,:2])*scale 
    return points
    
