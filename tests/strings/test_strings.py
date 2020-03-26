#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test string manipulation
"""

import os

import commonlibs.strings.strings as s

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_FILE_a = os.path.join(HERE, 'a.txt')


def test_is_string_in_file():
    assert s.is_string_in_file("phone number", TEST_FILE_a) is True
