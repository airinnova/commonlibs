#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import commonlibs.__version__ as v


def test_version():
    """
    Version
    """

    assert isinstance(v.VERSION, tuple)
    assert isinstance(v.__version__, str)
