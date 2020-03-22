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
Special dicts
"""


# Idea from:
# James Powell, https://www.youtube.com/watch?v=AmHE0kZhLIQ (see t=3282)
class rangedict(dict):
    def __missing__(self, key):
        for (lower, upper), value in ((k, v) for k, v in self.items() if isinstance(k, tuple)):
            if lower <= key < upper:
                return value
        raise KeyError(f"Cannot find {key} in ranges")
