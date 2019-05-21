#!/usr/bin/env python
#Author: Cedric Flamant

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import angletopos

def set_axes_equal(ax):
    '''Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().

    Credit for this function: karlo on StackOverflow
    https://stackoverflow.com/questions/13685386/matplotlib-equal-unit-length-with-equal-aspect-ratio-z-axis-is-not-equal-to
    '''

    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5*max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])

def drawstick(pos):
    '''Draws the stick figure in 3D

    Input
      pos: 2d array of joint positions.
    '''
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    ax.set_aspect('equal')
    
    ax.plot([pos[0,2],pos[2,2]],[pos[0,0],pos[2,0]],[pos[0,1],pos[2,1]],linewidth=4)
    ax.plot([pos[0,2]],[pos[0,0]],[pos[0,1]],'o',markersize=12,linewidth=4)
    ax.plot([pos[3,2],pos[4,2]],[pos[3,0],pos[4,0]],[pos[3,1],pos[4,1]],'o-',markersize=8,linewidth=4)
    ax.plot([pos[5,2],pos[6,2]],[pos[5,0],pos[6,0]],[pos[5,1],pos[6,1]],'o-',markersize=8,linewidth=4)
    ax.plot([pos[3,2],pos[7,2]],[pos[3,0],pos[7,0]],[pos[3,1],pos[7,1]],'o-',markersize=8,linewidth=4)
    ax.plot([pos[4,2],pos[8,2]],[pos[4,0],pos[8,0]],[pos[4,1],pos[8,1]],'o-',markersize=8,linewidth=4)
    ax.plot([pos[5,2],pos[9,2]],[pos[5,0],pos[9,0]],[pos[5,1],pos[9,1]],'o-',markersize=8,linewidth=4)
    ax.plot([pos[6,2],pos[10,2]],[pos[6,0],pos[10,0]],[pos[6,1],pos[10,1]],'o-',markersize=8,linewidth=4)
    ax.plot([pos[7,2],pos[11,2]],[pos[7,0],pos[11,0]],[pos[7,1],pos[11,1]],'o-',markersize=8,linewidth=4)
    ax.plot([pos[8,2],pos[12,2]],[pos[8,0],pos[12,0]],[pos[8,1],pos[12,1]],'o-',markersize=8,linewidth=4)
    ax.plot([pos[9,2],pos[13,2]],[pos[9,0],pos[13,0]],[pos[9,1],pos[13,1]],'o-',markersize=8,linewidth=4)
    ax.plot([pos[10,2],pos[14,2]],[pos[10,0],pos[14,0]],[pos[10,1],pos[14,1]],'o-',markersize=8,linewidth=4)
    #ax.scatter(pos[:,0],pos[:,1],pos[:,2], marker = "o", s=110)
    ax.set_xlabel('z')
    ax.set_ylabel('x')
    ax.set_zlabel('y')
    
    set_axes_equal(ax)
    plt.show()



