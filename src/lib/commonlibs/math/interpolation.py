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
Interpolation
"""


def lin_interpol(y12, x12, x):
    """
    Return linear interpolation between two support points.

    Args:
        :y12: (tuple) y1 and y2 value
        :x12: (tuple) x1 and x2 value
        :x: (float) position for which to return the interpolation

    Returns:
        :y_x: (float) linearly interpolated y(x)
    """

    return y12[0] + (y12[1] - y12[0])/(x12[1] - x12[0])*(x - x12[0])
