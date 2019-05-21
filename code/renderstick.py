#!/usr/bin/env python
#Author: Cedric Flamant

import numpy as np
import vpython as vp
#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
import angletopos


def tovec(arr):
    """Converts numpy 3-vector into vp.vector
    Input =>
        arr: 3 element numpy array
    Returns =>
        vec: vpython vector
    """
    return vp.vec(arr[0],arr[1],arr[2])

def renderstick(positions):
    '''Draws the stick figure in 3D

    Input
      positions: 2d array of joint positions.
    '''
    vp.scene.caption = """Right button drag or Ctrl-drag to rotate "camera" to view scene.
    To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
        On a two-button mouse, middle is left + right.
    Shift-drag to pan left/right and up/down.
    Touch screen: pinch/extend to zoom, swipe or two-finger rotate."""
    vp.scene.width = 800
    vp.scene.height = 600
    avpos = np.average(positions,axis=0)
    pos = positions - np.tile(avpos,(15,1))
    rarm = vp.curve(pos=[tovec(pos[3,:]),tovec(pos[7,:]),tovec(pos[11,:])],radius=1)
    shoulders = vp.curve(pos=[tovec(pos[3,:]),tovec(pos[4,:])],radius=1)
    larm = vp.curve(pos=[tovec(pos[4,:]),tovec(pos[8,:]),tovec(pos[12,:])],radius=1)
    spine = vp.curve(pos=[tovec(pos[0,:]),tovec(pos[2,:])],radius=1)
    hips = vp.curve(pos=[tovec(pos[5,:]),tovec(pos[6,:])],radius=1)
    rleg = vp.curve(pos=[tovec(pos[5,:]),tovec(pos[9,:]),tovec(pos[13,:])],radius=1)
    lleg = vp.curve(pos=[tovec(pos[6,:]),tovec(pos[10,:]),tovec(pos[14,:])],radius=1)

    head = vp.sphere(pos=tovec(pos[0,:]), radius=3.)
    rshoulder = vp.sphere(pos=tovec(pos[3,:]), radius=2., color=vp.color.orange)
    lshoulder = vp.sphere(pos=tovec(pos[4,:]), radius=2., color=vp.color.orange)
    rhip = vp.sphere(pos=tovec(pos[5,:]), radius=2., color=vp.color.orange)
    lhip = vp.sphere(pos=tovec(pos[6,:]), radius=2., color=vp.color.orange)
    relbow = vp.sphere(pos=tovec(pos[7,:]), radius=2., color=vp.color.orange)
    lelbow = vp.sphere(pos=tovec(pos[8,:]), radius=2., color=vp.color.orange)
    rknee = vp.sphere(pos=tovec(pos[9,:]), radius=2., color=vp.color.orange)
    lknee = vp.sphere(pos=tovec(pos[10,:]), radius=2., color=vp.color.orange)

if __name__=="__main__":
    angles = np.zeros((11,2))
    pos = angletopos.ang2pos(np.zeros(3),angles)
    renderstick(pos)


