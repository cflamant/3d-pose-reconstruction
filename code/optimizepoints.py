#!/usr/bin/env python
#Author: Cedric Flamant

import numpy as np
import pointstopos
from scipy.optimize import minimize


def calc_com(points):
    """Calculates the center of mass of the given points"""
    return np.average(points,axis=0)

def objectivefn(flatpoints,com,relorder,indexlist):
    """The objective function minimized by my method.

    Inputs =>
      flatpoints: 1D (flattened) array of 2D image points
      com: center of mass of joints (no longer used)
      relorder: relative order array
      indexlist: indices of limbs in plane

    Returns =>
      penalty: the penalty for having designated perpendicular
              limbs not be parallel to image plane
    """
    points = np.reshape(flatpoints,(-1,2))
    pos,scale=pointstopos.points2pos(points,relorder,0.)
    penalty = 0.
    for i in indexlist:
        if i == 0: # r shoulder & l shoulder
            penalty += (pos[3,2]-pos[4,2])**2
        elif i == 1: # collarbone & tailbone
            penalty += (pos[1,2]-pos[2,2])**2
        elif i == 2: # r hip & l hip
            penalty += (pos[5,2]-pos[6,2])**2
        elif i == 3: # r elbow & r shoulder
            penalty += (pos[7,2]-pos[3,2])**2
        elif i == 4: # l elbow & l shoulder
            penalty += (pos[8,2]-pos[4,2])**2
        elif i == 5: # r knee & r hip
            penalty += (pos[9,2]-pos[5,2])**2
        elif i == 6: # l knee & l hip
            penalty += (pos[10,2]-pos[6,2])**2
        elif i == 7: # r wrist & r elbow
            penalty += (pos[11,2]-pos[7,2])**2
        elif i == 8: # l wrist & l elbow
            penalty += (pos[12,2]-pos[8,2])**2
        elif i == 9: # r ankle & r knee
            penalty += (pos[13,2]-pos[9,2])**2
        elif i == 10: # l ankle & l knee
            penalty += (pos[14,2]-pos[10,2])**2
    return penalty
    
def reversedbinary(i,numbits):
    """Takes integer i and returns its binary representation
    as a list, but in reverse order, with total number of bits
    numbits. Useful for trying every possibility of numbits choices
    of two."""
    num = i
    count = 0
    revbin = []
    while count < numbits:
        revbin.append(num%2)
        num = num//2
        count += 1
    return revbin

def ineq_constraint(flatpoints,points0,pradii):
    """Inequality constraint passed to minimizer. It ensures that
    trial points are within the radius of uncertainty.
    
    Inputs =>
      flatpoints: 1D (flattened) array of image points
      points0: User-selected points at the center of uncertainty circle
      pradii: array of uncertainty radii for each joint

    Returns =>
      radius - (distance between point and point0 for each joint)
    """
    dists = np.linalg.norm(np.reshape(flatpoints,(-1,2))-points0,axis=1)
    return pradii - dists

def opt(points0,pradii,relorder,method='COBYLA'):
    """ Optimizer at the heart of the method. Takes guess 2D
    joint positions and their radii of uncertainty and optimizes in
    order to keep in-plane joints in-plane.

    Inputs =>
      points0: center points guessed by user
      pradii: array of uncertainty radii for each joint
      relorder: relative order array
      method: COBYLA or SLSQP (slower).
    """
    com = calc_com(points0)
    indexlist = []
    relorders = []
    res = []
    # constraints
    cons = ({'type':'ineq','fun':ineq_constraint,'args':(points0,pradii)})
    for i in range(len(relorder)):
        if relorder[i] == 0:
            indexlist.append(i)
    if len(indexlist) > 0:
        numtrials = 2**len(indexlist)
        for i in range(numtrials):
            print("Trial {} of {}".format(i,numtrials))
            trialrelorder = np.copy(relorder)
            revbin = reversedbinary(i,len(indexlist))
            for j,index in enumerate(indexlist):
                trialrelorder[index] = revbin[j]*2 - 1 #make it +1 or -1
            relorders.append(trialrelorder)
            res.append(minimize(objectivefn,points0.flatten(),args=(com,trialrelorder,indexlist),method=method, constraints=cons))
            print("penalty = {}".format(res[i].fun))
        minind = 0
        for i in range(len(res)):
          if res[i].fun < res[minind].fun:
            minind = i
        optpoints = np.reshape(res[minind].x,(-1,2))
        optrelorder = relorders[minind]
    else: # Nothing to optimize, return givens
        optpoints = points0
        optrelorder = relorder
    return optpoints,optrelorder
        

