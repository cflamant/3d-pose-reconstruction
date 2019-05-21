#!/usr/bin/env python
#Author: Cedric Flamant

import numpy as np
import angletopos
import renderstick


# Test 2
# Slightly more intricate pose, four limbs nearly in plane

angles2 = np.zeros((11,2))
# Tilt torso slightly forward
angles2[0,0] = -0.02
# Angle shoulders
angles2[1,0] = 0.8
angles2[1,1] = 0.2
# Angle hips
angles2[2,0] = -0.3
angles2[2,1] = 0.2
# right arm down
angles2[3,0] = np.pi/2
angles2[3,1] = -np.pi/2
# left arm somewhere
angles2[4,0] = 0.67
angles2[4,1] = 0.24
# right thigh somewhere
angles2[5,0] = 0.8
angles2[5,1] = 0.2
# left thigh somewhere
angles2[6,0] = -0.45
angles2[6,1] = 0.1
# right forearm
angles2[7,0] = 0.14
angles2[7,1] = -0.1
# left forearm
angles2[8,0] = 0.74
angles2[8,1] = -0.71
# right foreleg angled down
angles2[9,0] = -0.68
angles2[9,1] = -0.27
# left foreleg
angles2[10,0] = -0.84
angles2[10,1] = 0.21

# relorder
relorder2 = np.array([1,1,-1,1,-1,1,-1,1,1,1,-1],dtype=int)
# relative order with the constraints of certain joints being 
# roughly equal in z
consrelorder2 = np.array([1,0,-1,0,-1,1,-1,0,1,0,-1],dtype=int)

pos2 = angletopos.ang2pos(np.zeros(3),angles2)
if __name__ == "__main__":
    print(pos2)
    renderstick.renderstick(pos2)
