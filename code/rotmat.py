#!/usr/bin/env python
#Author: Cedric Flamant
#
# Produces a rotation matrix for a rotation of theta
# about an axis.

import numpy as np


def rotation_matrix(axis, theta):
    """
    Return rotation matrix associated with CCW rotation about the
    given axis by an angle theta. Uses the Euler-Rodrigues formula
    (written following a stackoverflow post and Wikipedia)
    """
    axis = np.asarray(axis)
    axis = axis / np.linalg.norm(axis)
    a = np.cos(theta/2.0)
    b, c, d = axis * np.sin(theta / 2.0)
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    return np.array([[aa+bb-cc-dd, 2*(bc-ad), 2*(bd+ac)],
                     [2*(bc+ad), aa+cc-bb-dd, 2*(cd-ab)],
                     [2*(bd-ac), 2*(cd+ab), aa+dd-bb-cc]])

