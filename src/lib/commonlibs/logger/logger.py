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

import os
import logging


def init(log_filename, level=None):
    """
    Inititalise a logger

    Note:
        * A stream handler and a console handler will be added, only if there are
          no existing handlers
        * The logger level is determined by the attributes of 'level'
            * Attributes can be True or False
            * Accepted levels are:
                * 'verbose'
                * 'debug'
                * 'quiet'
                * Default level is waring

    Args:
        :log_filename: Filename of the log file
        :level: Logger level
    """

    logger = logging.getLogger()

    # NOTE:
    # * Multiple calls to getLogger() with the same name will return a reference to the same logger object
    # * However, there can be any number of handlers (!)
    # * If a logger already as one or more handlers, none will be added

    if len(logger.handlers) > 0:
        return

    if getattr(level, 'verbose', False):
        level = logging.INFO
    elif getattr(level, 'debug', False):
        level = logging.DEBUG
    elif getattr(level, 'quiet', True):
        level = logging.ERROR
    else:
        level = logging.WARNING

    logger.setLevel(level)

    log_filename = os.path.abspath(log_filename)
    message_format = '[%(asctime)s %(levelname)s] @ %(name)s | %(message)s'

    # Create handlers
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(filename=log_filename, mode='w')

    # Set logging level
    console_handler.setLevel(level=level)
    file_handler.setLevel(level=level)

    # Add formatter to handlers
    formatter = logging.Formatter(fmt=message_format, datefmt='%F %H:%M:%S')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # ----- make matplotlib quiet -----
    mpl_logger = logging.getLogger('matplotlib')
    mpl_logger.setLevel(logging.WARNING)


def truncate_filepath(filepath, max_len=25, basename_only=True):
    """
    Truncate a long filepath

    Args:
        :filepath: filepath to truncate
        :max_len: maximum string lenght to return
        :basename_only: if True, only use the basename of 'filepath'

    Returns:
        :trunc_string: truncated filepath
    """

    pathname = os.path.basename(filepath) if basename_only else filepath

    if len(pathname) > max_len:
        pathname = pathname[-max_len:]
        prefix = '...'
    else:
        prefix = '.../'

    return prefix + pathname


def decorate(string, decoration="=", n1=10, n2=None):
    """
    Decorate a string to emphasise it

    Args:
        :string: string to decorate
        :decoration: string used
        :n1: prefix multiplier
        :n2: suffix multiplier

    Returns:
        :mod_string: modified string
    """

    if not isinstance(string, str):
        raise TypeError("'string' must be of type str")

    if not isinstance(decoration, str):
        raise TypeError("'decoration' must be of type str")

    if not isinstance(n1, int):
        raise TypeError("'n1' must be of type int")

    if n2 is None:
        n2 = n1

    mod_string = decoration*n1 + ' ' + string + ' ' + decoration*n2
    return mod_string
