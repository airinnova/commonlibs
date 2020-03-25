#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test the PropertyHandler in the Python API
"""

from commonlibs.model.model import PropertyHandler

import pytest


def test_property_handler():
    """Test the property handler meta class"""

    class TestModel(PropertyHandler):
        def __init__(self):
            super().__init__()

    model = TestModel()
    model._add_prop_spec('A', int)
    model._add_prop_spec('B', int)
    model._add_prop_spec('C', int, is_unique=False)
    model._add_prop_spec('D', int)

    # Check that schemas cannot be defined twice
    with pytest.raises(KeyError):
        model._add_prop_spec('D', str)

    # ========== set() method ==========
    model.set('A', 5)
    model.set('B', 8)
    model.set('B', 9)

    # Check the added values
    assert model.get('A') == 5
    assert model.get('B') == 9

    # Check that keys which are not allowed cannot be set
    with pytest.raises(KeyError):
        model.set("PROPERTY_DOES_NOT_EXIST", 10)

    # ========== add() method ==========
    model.add('C', 11)
    model.add('C', 22)
    model.add('C', 33)

    # Check that keys which are not allowed cannot be added
    with pytest.raises(KeyError):
        model.add("PROPERTY_DOES_NOT_EXIST", 10)

    # Check the added values
    assert model.get('C') == [11, 22, 33]

    exp_items = [11, 22, 33]
    for i, item in enumerate(model.iter('C')):
        assert item == exp_items[i]

    # Cannot iterate over unique property
    with pytest.raises(KeyError):
        for _ in model.iter('A'):
            pass
