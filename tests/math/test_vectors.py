#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import commonlibs.math.vectors as m

UNIT_X = [1, 0, 0]
SOME_VECTOR = [55, 89.33, 190.03]

def test_unit_vector():
    """
    Test unit vector function
    """

    # Assert vector have length 1
    for v in [UNIT_X, SOME_VECTOR]:
        v = m.unit_vector(v)
        assert np.linalg.norm(v) == 1

    # Assert list/numpy arrays produce same output
    v_from_list = m.unit_vector(list(SOME_VECTOR))
    v_from_np = m.unit_vector(np.array(SOME_VECTOR))
    assert np.testing.assert_array_equal(v_from_list, v_from_np) is None


def test_angle_between():
    """
    Test function to determine angle between vectors
    """

    assert m.angle_between((1, 0, 0), (0, 1, 0)) == 1.5707963267948966
    assert m.angle_between((1, 0, 0), (1, 0, 0)) == 0.0
    assert m.angle_between((1, 0, 0), (-1, 0, 0)) == 3.141592653589793
