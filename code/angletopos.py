#!/usr/bin/env python
#Author: Cedric Flamant

import numpy as np
from rotmat import rotation_matrix as RM
from meas import *

def ang2pos(head_pos,angles):
    """ 
    Input =>
    head_pos:
        (x,y,z) position of the head
    angles:
        2d array of theta,phi for each of the following (in order):
         -neck
         -shoulder girdle
         -pelvis girdle
         -right upper arm
         -left upper arm
         -right thigh
         -left thigh
         -right forearm
         -left forearm
         -right foreleg
         -left foreleg

    Returns =>
    pos:
      2d array of positions, where the row index corresponds to:
       -head
       -collarbone
       -tailbone
       -right shoulder
       -left shoulder
       -right hip
       -left hip
       -right elbow
       -left elbow
       -right knee
       -left knee
       -right wrist
       -left wrist
       -right ankle
       -left ankle
    """
    pos = np.zeros((15,3))

    # initialize default limb vectors
    neck = NECK*np.array([0.,-1.,0.])
    spine = SPINE*np.array([0.,-1.,0.])
    rcollar = SHOULDER/2.*np.array([-1.,0.,0.])
    rpelvis = PELVIC/2.*np.array([-1.,0.,0.])
    rupperarm = UPPER_ARM*np.array([-1.,0.,0.])
    lupperarm = UPPER_ARM*np.array([1.,0.,0.])
    rthigh = THIGH*np.array([0.,-1.,0.])
    lthigh = THIGH*np.array([0.,-1.,0.])
    rforearm = FOREARM*np.array([-1.,0.,0.])
    lforearm = FOREARM*np.array([1.,0.,0.])
    rforeleg = FORELEG*np.array([0.,-1.,0.])
    lforeleg = FORELEG*np.array([0.,-1.,0.])

    # calculate rotation matrices for each joint
    neckRM = RM([-np.cos(angles[0,1]),0.,np.sin(angles[0,1])],angles[0,0])
    collarRM = RM([0.,np.cos(angles[1,1]),-np.sin(angles[1,1])],angles[1,0])
    pelvisRM = RM([0.,np.cos(angles[2,1]),-np.sin(angles[2,1])],angles[2,0])
    rshoulderRM = RM([0.,np.cos(angles[3,1]),-np.sin(angles[3,1])],angles[3,0])
    lshoulderRM = RM([0.,-np.cos(angles[4,1]),-np.sin(angles[4,1])],angles[4,0])
    rhipRM = RM([-np.cos(angles[5,1]),0.,-np.sin(angles[5,1])],angles[5,0])
    lhipRM = RM([-np.cos(angles[6,1]),0.,-np.sin(angles[6,1])],angles[6,0])
    relbowRM = RM([0.,np.cos(angles[7,1]),-np.sin(angles[7,1])],angles[7,0])
    lelbowRM = RM([0.,-np.cos(angles[8,1]),-np.sin(angles[8,1])],angles[8,0])
    rkneeRM = RM([-np.cos(angles[9,1]),0.,-np.sin(angles[9,1])],angles[9,0])
    lkneeRM = RM([-np.cos(angles[10,1]),0.,-np.sin(angles[10,1])],angles[10,0])

    # calculate the rotated vectors
    neck = neckRM @ neck
    spine = neckRM @ spine
    rcollar = neckRM @ collarRM @ rcollar
    rpelvis = neckRM @ pelvisRM @ rpelvis
    rupperarm = neckRM @ collarRM @ rshoulderRM @ rupperarm
    lupperarm = neckRM @ collarRM @ lshoulderRM @ lupperarm
    rthigh = neckRM @ pelvisRM @ rhipRM @ rthigh
    lthigh = neckRM @ pelvisRM @ lhipRM @ lthigh
    rforearm = neckRM @ collarRM @ rshoulderRM @ relbowRM @ rforearm
    lforearm = neckRM @ collarRM @ lshoulderRM @ lelbowRM @ lforearm
    rforeleg = neckRM @ pelvisRM @ rhipRM @ rkneeRM @ rforeleg
    lforeleg = neckRM @ pelvisRM @ lhipRM @ lkneeRM @ lforeleg
    
    # set the head position first
    pos[0,:] = head_pos
    # set collar position
    pos[1,:] = pos[0,:] + neck
    # set tailbone position
    pos[2,:] = pos[1,:] + spine
    # set right shoulder position
    pos[3,:] = pos[1,:] + rcollar
    # set left shoulder position
    pos[4,:] = pos[1,:] - rcollar
    # set right hip position
    pos[5,:] = pos[2,:] + rpelvis
    # set left hip position
    pos[6,:] = pos[2,:] - rpelvis
    # set right elbow
    pos[7,:] = pos[3,:] + rupperarm
    # set left elbow
    pos[8,:] = pos[4,:] + lupperarm
    # set right knee
    pos[9,:] = pos[5,:] + rthigh
    # set left knee
    pos[10,:] = pos[6,:] + lthigh
    # set right wrist
    pos[11,:] = pos[7,:] + rforearm
    # set left wrist
    pos[12,:] = pos[8,:] + lforearm
    # set right ankle
    pos[13,:] = pos[9,:] + rforeleg
    # set left ankle
    pos[14,:] = pos[10,:] + lforeleg

    return pos

