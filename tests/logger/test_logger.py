#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from pytest import raises

import commonlibs.logger.logger as m

logger = logging.getLogger(__name__)


def test_logger_init():
    """
    TODO
    """

    m.init('test.log')


def test_truncate_string():
    """
    Test function to truncate file paths
    """

    string1 = m.truncate_filepath("/path/to/some_very_long_file_name.txt")
    assert string1.startswith('...')

    string2 = m.truncate_filepath("/path/to/short.txt")
    assert string2 == ".../short.txt"


def test_decorate():
    """
    Test decorate function
    """

    TEST_STR = 'test'

    mod_string = m.decorate('test')
    assert mod_string == f"{'='*10} {TEST_STR} {'='*10}"

    mod_string = m.decorate('test', n2=20)
    assert mod_string == f"{'='*10} {TEST_STR} {'='*20}"

    with raises(TypeError):
        m.decorate(1000)

    with raises(TypeError):
        m.decorate(TEST_STR, n1='10')

    with raises(TypeError):
        m.decorate(TEST_STR, decoration=10)
