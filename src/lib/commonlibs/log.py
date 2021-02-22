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
Logger
"""

import logging

MSG_FMT = '[%(asctime)s %(levelname)s] @ %(name)s | %(message)s'
DATE_FMT = '%F %H:%M:%S'


class PackageLogger:

    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt=MSG_FMT, datefmt=DATE_FMT)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    @property
    def off(self):
        self.logger.setLevel(logging.ERROR)

    @property
    def on(self):
        self.logger.setLevel(logging.DEBUG)
