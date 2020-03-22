#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from commonlibs.dicts.special import rangedict


def test_rangedict():
    d = rangedict({
        (0, 3): 'a',
        (3, 6): 'b',
        (6, 9): 'c',
    })

    assert d[0] == 'a'
    assert d[1] == 'a'
    assert d[3] == 'b'
    assert d[5] == 'b'
    assert d[6] == 'c'

    with pytest.raises(KeyError):
        d[10]
