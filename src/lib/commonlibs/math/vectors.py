#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2019-2020 Airinnova AB and the CommonLibs authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------

# Author: Aaron Dettmann

"""
Vectors
"""

import numpy as np


def unit_vector(vector):
    """Return the unit vector of a vector."""

    return vector/np.linalg.norm(vector)


def direction_cosine(vector1, vector2):
    """
    Returns the direcion cosine between vectors 'vector1' and 'vector2'

    See also:

    * https://en.wikipedia.org/wiki/Euclidean_vector#Conversion_between_multiple_Cartesian_bases

    Args:
        :vector1: First vector
        :vector2: Second vector

    Returns:
        :direction_cosine: Direction cosine
    """

    v1_u = unit_vector(vector1)
    v2_u = unit_vector(vector2)

    return np.clip(np.dot(v1_u, v2_u), a_min=-1.0, a_max=1.0)


def angle_between(vector1, vector2):
    """Return the angle in radians between vectors 'vector1' and 'vector2'

    # See also: https://stackoverflow.com/questions/2827393/
                angles-between-two-n-dimensional-vectors-in-python/13849249#13849249
    """

    return np.arccos(direction_cosine(vector1, vector2))


def axis_rot_matrix(axis, angle):
    """
    Return a rotation matrix associated with counterclockwise rotation about a given axis by angle radians.

    Note:
        * The rotation matrix is computed using the Euler-Rodrigues formula:
          https://en.wikipedia.org/wiki/Euler%E2%80%93Rodrigues_formula

    Args:
        :axis: 3x1 axis vector
        :angle: rotation aangle in radians

    Returns:
        :R: rotation matrix
    """

    # Parse and normalise the axis vector
    axis = np.asarray(axis)
    axis = axis/np.sqrt(np.dot(axis, axis))

    a = np.cos(angle/2.0)
    b, c, d = -axis*np.sin(angle/2.0)

    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d

    return np.array([[aa + bb - cc - dd, 2*(bc + ad),       2*(bd - ac)],
                     [2*(bc - ad),       aa + cc - bb - dd, 2*(cd + ab)],
                     [2*(bd + ac),       2*(cd - ab),       aa + dd - bb - cc]])


def rotate_vector_around_axis(vector, axis, angle, return_unit=False):
    """
    Rotate a vector by an angle around a defined axis.

    Note:

        * Returns the original vector if the Euclidean norm of 'vector' or
          'axis' is zero or if 'angle' is zero

    Args:
        :vector: Vector to be rotated
        :axis: 3x1 axis vector
        :angle: Rotation angle in radians

    Returns:
        :rot_vector: rotated vector
    """

    if np.linalg.norm(vector) == 0 or np.linalg.norm(axis) == 0 or angle == 0:
        return vector

    rot_vector = np.dot(axis_rot_matrix(axis, angle), vector)

    if return_unit:
        rot_vector = unit_vector(rot_vector)

    return rot_vector


def get_plane_line_intersect(plane_normal, plane_point, line_direction, line_point, epsilon=1e-6):
    """
    Get the intersection point for a line and a plane in 3D space.

    Note:
        * The line is defined by its direction (vector) and any point on the line
        * The plane is defined by its normal (vector) and any point on the plane

    Args:
        :plane_normal: 3x1 normal vector of the plane
        :plane_point: point (3x1 vector) of the plane (any)
        :line_direction: 3x1 vector with the direction of the line
        :line_point: point (3x1 vector) of the line (any)
        :epsilon: tolerance for near-orthogonal 'plane_normal' and 'line_direction'
    """

    dot_pn_ld = np.dot(plane_normal, line_direction)

    # If plane normal and line direction are (nearly) orthogonal, abort
    if abs(dot_pn_ld) < epsilon:
        raise RuntimeError("No intersection with plane")

    from_pp2lp = line_point - plane_point
    si = -np.dot(plane_normal, from_pp2lp)/dot_pn_ld
    intersect_point = plane_point + from_pp2lp + si*line_direction

    return intersect_point


def vector_projection(a, b):
    """
    Return the vector projection from vector a onto vector b

    See:
        * https://en.wikipedia.org/wiki/Vector_projection

    Args:
        :a: vector to be projected
        :b: vector onto which a is projected

    Returns:
        :a1: vector projection
    """

    a1 = np.dot(a, unit_vector(b))*unit_vector(b)
    return a1


def vector_rejection(a, b):
    """
    Return the vector rejection from vector a onto vector b

    See:
        * https://en.wikipedia.org/wiki/Vector_projection

    Args:
        :a: vector to be projected
        :b: vector onto which a is projected

    Returns:
        :a2: vector rejection
    """

    a1 = vector_projection(a, b)
    return a - a1


def vector_projection_onto_plane(vector, plane_normal):
    """
    Project a vecor onto a plane

    Args:
        :vector: vector to be projected
        :plane_normal: normal vector of the plane

    Returns:
        :vector_proj: projected vector
    """

    # The projected vector equal to the vector minus the "vertical"
    # component of the vector, i.e. the component which points in
    # the plane normal direction.  The vertical component is given by
    # a vector projection

    return vector - vector_projection(vector, plane_normal)
