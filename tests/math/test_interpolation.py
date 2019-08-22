#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import commonlibs.math.interpolation as m


def test_lin_interpol():
    """
    Test function for linear interpolation
    """

    x12 = (0, 10)
    y12 = (20, 40)
    assert m.lin_interpol(y12=y12, x12=x12, x=5) == 30

    x12 = (0, 1)
    y12 = (0, 1)
    assert m.lin_interpol(y12=y12, x12=x12, x=0.5) == 0.5
