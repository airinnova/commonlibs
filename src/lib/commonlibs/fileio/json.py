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
JSON
"""

import json
from functools import partial

import numpy as np


class NDArrayEncoder(json.JSONEncoder):
    """
    Serialise Numpy arrays

    Use like this: json.dump(obj, fp, cls=NDArrayEncoder)
    """

    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()  # Covert Numpy array to list (Numpy method)
        return json.JSONEncoder.default(self, obj)


# Dump pretty-formatted JSON with support for numpy arrays
dump_pretty_json = partial(json.dump, cls=NDArrayEncoder, indent=4, separators=(',', ': '))
