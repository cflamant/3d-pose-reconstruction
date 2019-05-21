#!/usr/bin/env python
#Author: Cedric Flamant

import numpy as np
import angletopos
import renderstick


# Test 4
# Tricky pose, only one limb in plane

angles4 = np.zeros((11,2))
# Tilt torso 
angles4[0,0] = -0.42
angles4[0,1] = -0.82
# square up shoulders
angles4[1,0] = 0.04
angles4[1,1] = 0.02
# Angle hips
angles4[2,0] = -0.9
angles4[2,1] = -0.2
# right arm down
angles4[3,0] = 1.1
angles4[3,1] = -0.26
# left arm somewhere
angles4[4,0] = -0.91
angles4[4,1] = 0.84
# right thigh somewhere
angles4[5,0] = 0.28
angles4[5,1] = -0.2
# left thigh somewhere
angles4[6,0] = -0.25
angles4[6,1] = -0.31
# right forearm
angles4[7,0] = -0.14
angles4[7,1] = -0.19
# left forearm
angles4[8,0] = 1.94
angles4[8,1] = 0.71
# right foreleg angled down
angles4[9,0] = -0.98
angles4[9,1] = -0.17
# left foreleg
angles4[10,0] = -0.24
angles4[10,1] = -0.91

# relorder
relorder4 = np.array([-1,1,-1,1,-1,-1,-1,1,1,-1,-1],dtype=int)
# relative order with the constraints of certain joints being 
# roughly equal in z
consrelorder4 = np.array([0,1,-1,1,-1,-1,-1,1,1,-1,-1],dtype=int)

pos4 = angletopos.ang2pos(np.zeros(3),angles4)
if __name__ == "__main__":
    print(pos4)
    renderstick.renderstick(pos4)
