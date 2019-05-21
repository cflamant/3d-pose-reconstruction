#!/usr/bin/env python
#Author: Cedric Flamant

import numpy as np
import matplotlib.pyplot as plt
import pointstopos
import postopoints
import angletopos
import optimizepoints
from meas import HEIGHT
from scipy.optimize import minimize
from testpose1 import angles1, relorder1, consrelorder1, pos1
from testpose2 import angles2, relorder2, consrelorder2, pos2
from testpose3 import angles3, relorder3, consrelorder3, pos3
from testpose4 import angles4, relorder4, consrelorder4, pos4

# For this test we take scale = 1 for simplicity
# Thus, height in the picture is the same as height in reality
numsamples = 10
noisespread = 0.05*HEIGHT
pradius = 3*noisespread

def calcerror(rescale, pos, refpos):
    """ Calculates the error as explained in the writeup.

    Inputs =>
      rescale: rescaling factor alpha
      pos: trial 3D position
      refpos: reference joint positions

    Returns =>
      error
    """
    avgdist = np.sum(np.sqrt(np.sum(np.square(rescale*pos-refpos),axis=1)))/refpos.shape[0]
    return avgdist/HEIGHT # normalize this value by the height

def opterror(pos, refpos):
    """Optimized error as explained in writeup. Optimizes away alpha parameter

    Inputs =>
      pos: trial 3D positions
      refpos: reference joint positions

    Returns =>
      error
    """
    avpos = np.average(pos,axis=0)
    avrefpos = np.average(refpos,axis=0)
    poscentered = pos - np.tile(avpos,(15,1))
    refposcentered = refpos - np.tile(avrefpos,(15,1))
    res = minimize(calcerror, 1.0, method='BFGS',args=(poscentered,refposcentered))
    return res.fun

def getdata(points,relorder,consrelorder,pos,noiseamp):
    """Generates data to make a quantitative performance plot for a 
    given pose.
    
    Inputs =>
      points: exact image points
      relorder: relative order array
      consrelorder: augmented order array
      pos: 3D positions of stick figure
      noiseamp: amplitude of 2D noise to add to image.

    Returns =>
      errorA: error in Taylor method
      errorB: error in my method
    """
    errorA = np.zeros(numsamples)
    errorB = np.zeros(numsamples)
    errorC = np.zeros(numsamples)
    for t in range(numsamples):
        noise = np.random.normal(np.zeros_like(points),noiseamp)
        givenpoints = points + noise
        
        pradii = np.ones(points.shape[0])*pradius
        # No optimization
        posA,scaleA = pointstopos.points2pos(givenpoints,relorder,0.0)
        errorA[t] = opterror(posA,pos)
        # COBYLA
        newpointsB,newrelorderB = optimizepoints.opt(givenpoints,pradii,consrelorder,method='COBYLA')
        posB,scaleB = pointstopos.points2pos(newpointsB,newrelorderB,0.)
        errorB[t] = opterror(posB,pos)
    return errorA, errorB


regmean = []
regsdev = []
optmean = []
optsdev = []

# Test 1
# Simple default pose, all limbs in plane
points1 = postopoints.project(pos1,1.0)
regerrors1, opterrors1 = getdata(points1,relorder1,consrelorder1,pos1,noisespread)
regmean.append(np.average(regerrors1))
regsdev.append(np.std(regerrors1))
optmean.append(np.average(opterrors1))
optsdev.append(np.std(opterrors1))

# Test 2
points2 = postopoints.project(pos2,1.0)
regerrors2, opterrors2 = getdata(points2,relorder2,consrelorder2,pos2,noisespread)
regmean.append(np.average(regerrors2))
regsdev.append(np.std(regerrors2))
optmean.append(np.average(opterrors2))
optsdev.append(np.std(opterrors2))


# Test 3
# Two limbs nearly in plane, rest heavily distorted
points3 = postopoints.project(pos3,1.0)
regerrors3, opterrors3 = getdata(points3,relorder3,consrelorder3,pos3,noisespread)
regmean.append(np.average(regerrors3))
regsdev.append(np.std(regerrors3))
optmean.append(np.average(opterrors3))
optsdev.append(np.std(opterrors3))

# Test 4
# Only one limb nearly in plane, rest heavily distorted
points4 = postopoints.project(pos4,1.0)
regerrors4, opterrors4 = getdata(points4,relorder4,consrelorder4,pos4,noisespread)
regmean.append(np.average(regerrors4))
regsdev.append(np.std(regerrors4))
optmean.append(np.average(opterrors4))
optsdev.append(np.std(opterrors4))


ind = np.arange(len(regmean)) # x locations for groups
width = 0.35 # width of bars

# Make bar plot of results
fig, ax = plt.subplots()
regrects = ax.bar(ind, regmean, width, color='orange', yerr=regsdev,ecolor='black',capsize=2,error_kw={'linewidth':2})
optrects = ax.bar(ind+width, optmean, width, color='green', yerr=optsdev, ecolor='black',capsize=2,error_kw={'linewidth':2})

ax.set_ylabel('Avg. Joint Position Error')
ax.set_xticks(ind + width)
ax.set_xticklabels(('All Limbs Perp.','Four Perp. Limbs','Two Perp. Limbs', 'One Perp. Limb'))
ax.legend((regrects[0],optrects[1]),('Regular','With Optimization'))

plt.savefig('../fig/performance.png',bbox_inches='tight')
plt.show()





