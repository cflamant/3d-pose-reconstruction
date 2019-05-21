#!/usr/bin/env python
#Author: Cedric Flamant

import numpy as np
import angletopos
import renderstick


# Test 1
# Simple default pose, all limbs in plane

angles1 = np.zeros((11,2))
pos1 = angletopos.ang2pos(np.zeros(3),angles1)

# relorder
relorder1 = np.array([1,1,-1,1,-1,1,-1,1,-1,1,-1],dtype=int)
# relative order with the constraints of all joints being 
# equal in z
consrelorder1 = np.array([0,0,0,0,0,0,0,0,0,0,0],dtype=int)
if __name__ == "__main__":
    renderstick.renderstick(pos1)
