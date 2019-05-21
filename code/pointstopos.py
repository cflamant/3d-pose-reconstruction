#!/usr/bin/env python
#Author: Cedric Flamant

import numpy as np
from meas import *

def points2pos(points,relorder,scale):
    """ 
    Input =>
    points:
        2d array of u,v image points for each of the following:
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
    relorder:
        relative depth order, (+1 if first closer, -1 otherwise)
        of the following segments:
         -right shoulder - left shoulder
         -collarbone - tailbone
         -right hip - left hip
         -right elbow - right shoulder
         -left elbow - left shoulder
         -right knee - right hip
         -left knee - left hip
         -right wrist - right elbow
         -left wrist - left elbow
         -right ankle - right knee
         -left ankle - left knee
    scale:
        Guess of scale. If it is not consistent with constraint,
        gets set to the minimum.

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
    scale:
      The scale used, whether it is the supplied one or the minimum one
    """
    pos = np.zeros((15,3))
    collarpoint = (points[0,:] + points[1,:])/2.
    tailpoint = (points[2,:] + points[3,:])/2.

    # First compute the constraint on the minimum size of s.
    smins = np.zeros(14)
    smins[0] = s_constraint(points[0,:]-collarpoint,SHOULDER/2.)
    smins[1] = s_constraint(points[1,:]-collarpoint,SHOULDER/2.)
    smins[2] = s_constraint(collarpoint-tailpoint,SPINE)
    smins[3] = s_constraint(points[2,:]-tailpoint,PELVIC/2.)
    smins[4] = s_constraint(points[3,:]-tailpoint,PELVIC/2.)
    smins[5] = s_constraint(points[4,:]-points[0,:],UPPER_ARM)
    smins[6] = s_constraint(points[5,:]-points[1,:],UPPER_ARM)
    smins[7] = s_constraint(points[6,:]-points[2,:],THIGH)
    smins[8] = s_constraint(points[7,:]-points[3,:],THIGH)
    smins[9] = s_constraint(points[8,:]-points[4,:],FOREARM)
    smins[10] = s_constraint(points[9,:]-points[5,:],FOREARM)
    smins[11] = s_constraint(points[10,:]-points[6,:],FORELEG)
    smins[12] = s_constraint(points[11,:]-points[7,:],FORELEG)
    smins[13] = scale
    s = np.amax(smins) #Set to specified scale or minimum allowed scale

    # Now compute the 3D positions assuming the scale and using the 
    # relative ordering. 
    # Set right shoulder at (0,0,0).
    pos[3,:] = np.zeros(3)
    # left shoulder
    pos[4,:2] = pos[3,:2] + (points[1,:]-points[0,:])/s
    pos[4,2] = pos[3,2] - relorder[0]*dz(points[1,:]-points[0,:],SHOULDER,s)
    # collarbone
    pos[1,:] = (pos[3,:]+pos[4,:])/2.
    # tailbone
    pos[2,:2] = pos[1,:2] + (tailpoint-collarpoint)/s
    pos[2,2] = pos[1,2] - relorder[1]*dz(tailpoint-collarpoint,SPINE,s)
    # right hip
    pos[5,:2] = pos[2,:2] + (points[2,:]-tailpoint)/s
    pos[5,2] = pos[2,2] + relorder[2]*dz(points[2,:]-tailpoint,PELVIC/2.,s)
    # left hip
    pos[6,:2] = pos[2,:2] + (points[3,:]-tailpoint)/s
    pos[6,2] = pos[2,2] - relorder[2]*dz(points[3,:]-tailpoint,PELVIC/2.,s)
    # right elbow
    pos[7,:2] = pos[3,:2] + (points[4,:]-points[0,:])/s
    pos[7,2] = pos[3,2] + relorder[3]*dz(points[4,:]-points[0,:],UPPER_ARM,s)
    # left elbow
    pos[8,:2] = pos[4,:2] + (points[5,:]-points[1,:])/s
    pos[8,2] = pos[4,2] + relorder[4]*dz(points[5,:]-points[1,:],UPPER_ARM,s)
    # right knee
    pos[9,:2] = pos[5,:2] + (points[6,:]-points[2,:])/s
    pos[9,2] = pos[5,2] + relorder[5]*dz(points[6,:]-points[2,:],THIGH,s)
    # left knee
    pos[10,:2] = pos[6,:2] + (points[7,:]-points[3,:])/s
    pos[10,2] = pos[6,2] + relorder[6]*dz(points[7,:]-points[3,:],THIGH,s)
    # right wrist
    pos[11,:2] = pos[7,:2] + (points[8,:]-points[4,:])/s
    pos[11,2] = pos[7,2] + relorder[7]*dz(points[8,:]-points[4,:],FOREARM,s)
    # left wrist
    pos[12,:2] = pos[8,:2] + (points[9,:]-points[5,:])/s
    pos[12,2] = pos[8,2] + relorder[8]*dz(points[9,:]-points[5,:],FOREARM,s)
    # right ankle
    pos[13,:2] = pos[9,:2] + (points[10,:]-points[6,:])/s
    pos[13,2] = pos[9,2] + relorder[9]*dz(points[10,:]-points[6,:],FORELEG,s)
    # left ankle
    pos[14,:2] = pos[10,:2] + (points[11,:]-points[7,:])/s
    pos[14,2] = pos[10,2] + relorder[10]*dz(points[11,:]-points[7,:],FORELEG,s)
    # compute the head position
    pos[0,:] = NECK/SPINE*(pos[1,:]-pos[2,:]) + pos[1,:]

    return pos,s

    

def s_constraint(dpoint,l):
    """ Check the minimum value of scale implied by the constraint
    on segment length and image position delta

    Input =>
    dpoint: array corresponding to (u1-u2,v1-v2) point difference
    l: relative length of joint segment

    Returns =>
    smin: minimum scale allowed by constraint
    """
    # add a little to the constraint to avoid floating point issues
    return np.sqrt(dpoint[0]**2 + dpoint[1]**2)/l + 1e-10

def dz(dpoint,l,s):
    """ Compute the |delta Z| implied by the delta image point,
    length of segment, and scale.

    Input =>
    dpoint: array corresponding to (u1-u2,v1-v2) point difference
    l: relative length of joint segment
    s: scale

    Returns =>
    dz: absolute value of the predicted delta z in 3D reconstruction
    """
    return np.sqrt(l**2 - (dpoint[0]**2+dpoint[1]**2)/s**2)

