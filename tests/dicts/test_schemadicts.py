#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

from pytest import raises

from commonlibs.dicts.schemadicts import check_dict_against_schema, get_default_value_dict


def time_now():
    return datetime.strftime(datetime.now(), '%H:%M')


SCHEMA_1 = {
    '__REQUIRED_KEYS': ['name', 'age'],
    'name': {
        'type': str,
        'min_len': 3,
        'max_len': 12,
    },
    'age': {
        'type': int,
        '>=': 0,
        '<': 120,
    },
    'is_working': {
        'type': bool
    }
}

SCHEMA_1_DEFAULT_VALUE_DICT = {
    'name': '',
    'age': 0,
    'is_working': False,
}

# Simple nested schema
SCHEMA_2 = {
    '__REQUIRED_KEYS': ['name', 'age'],
    'name': {
        'type': str,
        'min_len': 3,
        'max_len': 12,
    },
    'age': {
        'type': int,
        '>=': 0,
        '<': 120,
    },
    'child': {
        'type': dict,
        'schema': SCHEMA_1,
    }
}

SCHEMA_3 = {
    'fruits': {
        'type': list,
        'min_len': 3,
        'max_len': 3,
        'item_types': str,
        },
    'numbers': {
        'type': tuple,
        'min_len': 3,
        'item_types': (int, float),
    },
}


SCHEMA_4 = {
    'time': {'type': str, 'default': time_now},
    'person': {'type': str, 'default': 'C.Lindbergh'},
    'age': {'type': int},
    'pets': {
        'type': dict,
        'schema': {
            'dog': {'type': bool, 'default': None},
            'cat': {'type': bool}
        },
    },
}

SCHEMA_4_DEFAULT_VALUE_DICT = {
    'time': '08:40',
    'person': 'C.Lindbergh',
    'age': 0,
    'pets': {
        'dog': None,
        'cat': False,
    }
}


def test_schema_dict():
    """
    Schema dicts
    """

    test = {
        'name': 'Aaron',
        'age': 22,
        'is_working': True,
    }

    check_dict_against_schema(test, SCHEMA_1)

    test = {
        'name': 'Aaron',
        'age': 200,  # Value too large
    }

    with raises(ValueError):
        check_dict_against_schema(test, SCHEMA_1)

    test = {
        'name': 'Aaron',
        'age': -1,  # Value too small
    }

    with raises(ValueError):
        check_dict_against_schema(test, SCHEMA_1)

    test = {
        'name': 'Aaron',
    }

    with raises(KeyError):
        check_dict_against_schema(test, SCHEMA_1)

    test = {
        'name': 'Aaron NameTooLong',
        'age': 22,
    }

    with raises(ValueError):
        check_dict_against_schema(test, SCHEMA_1)

    test = {
        'name': 'A',  # Name too short
        'age': 22,
    }

    with raises(ValueError):
        check_dict_against_schema(test, SCHEMA_1)


def test_nested_dict():
    # ----- Test nested schema -----

    test = {
        'name': 'Aaron',
        'age': 22,
        'child': {
            'name': 'Test',
            'age': 3,
        }
    }

    check_dict_against_schema(test, SCHEMA_1)  # Validation against schema 1 must still work
    check_dict_against_schema(test, SCHEMA_2)

    test = {
        'name': 'Aaron',
        'age': 22,
        'child': {
            'name': 'Test',
            'age': -3,  # Wrong age
        }
    }

    with raises(ValueError):
        check_dict_against_schema(test, SCHEMA_2)


def test_arrays():
    """
    TODO
    """

    test = {
        'fruits': ['apple', 'pear', 'strawberry'],
        'numbers': (3.14159, 42, 1792, 5050),
    }

    check_dict_against_schema(test, SCHEMA_3)

    test = {
        'fruits': ['apple', 'pear', 'strawberry'],
        'numbers': (3.14159, 42, 1792, 5050, 'string_not_allowed'),
    }

    with raises(TypeError):
        check_dict_against_schema(test, SCHEMA_3)


def test_default_value_dict():
    """
    Test 'get_default_value_dict()'
    """

    defaults = get_default_value_dict(SCHEMA_1)
    assert defaults == SCHEMA_1_DEFAULT_VALUE_DICT

    defaults = get_default_value_dict(SCHEMA_4)
    assert isinstance(defaults['time'], str)

    # Time may vary
    del SCHEMA_4_DEFAULT_VALUE_DICT['time']
    del defaults['time']

    assert defaults == SCHEMA_4_DEFAULT_VALUE_DICT
