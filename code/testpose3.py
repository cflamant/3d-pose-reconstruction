#!/usr/bin/env python
#Author: Cedric Flamant

import numpy as np
import angletopos
import renderstick


# Test 3
# Trickier pose, two limbs in plane

angles3 = np.zeros((11,2))
# Tilt torso 
angles3[0,0] = -0.42
angles3[0,1] = -0.82
# square up Angle shoulders
angles3[1,0] = 0.04
angles3[1,1] = 0.02
# Angle hips
angles3[2,0] = -0.9
angles3[2,1] = -0.2
# right arm down
angles3[3,0] = 1.1
angles3[3,1] = -0.26
# left arm somewhere
angles3[4,0] = -0.91
angles3[4,1] = 0.84
# right thigh in plane
angles3[5,0] = 0.43
angles3[5,1] = -0.2
# left thigh somewhere
angles3[6,0] = -0.25
angles3[6,1] = -0.31
# right forearm
angles3[7,0] = -0.14
angles3[7,1] = -0.19
# left forearm
angles3[8,0] = 1.94
angles3[8,1] = 0.71
# right foreleg angled down
angles3[9,0] = -0.98
angles3[9,1] = -0.17
# left foreleg
angles3[10,0] = -0.24
angles3[10,1] = -0.91

# relorder
relorder3 = np.array([-1,1,-1,1,-1,-1,-1,1,1,-1,-1],dtype=int)
# relative order with the constraints of certain joints being 
# roughly equal in z
consrelorder3 = np.array([0,1,-1,1,-1,0,-1,1,1,-1,-1],dtype=int)

pos3 = angletopos.ang2pos(np.zeros(3),angles3)
if __name__ == "__main__":
    print(pos3)
    renderstick.renderstick(pos3)
