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
Schema dictionaries
"""

import operator
from uuid import uuid4


OPERATORS = {
    '>': operator.gt,
    '<': operator.lt,
    '<=': operator.le,
    '>=': operator.ge,
}

SPECIAL_KEY_CHECK_REQ_KEYS = '__REQUIRED_KEYS'

SPECIAL_KEYS = [
    SPECIAL_KEY_CHECK_REQ_KEYS,
]

# Special 'type' used for checks
NOTHING = f'__NOTHING__{uuid4()}'


class SchemaError(Exception):
    """Raised if the schema dictionary is ill-defined"""

    pass


def check_dict_against_schema(test_dict, schema_dict):
    """
    Check that a dictionary conforms to a schema dictionary

    This function will raise an error if the 'test_dict' is not in alignment
    with the 'schema_dict'

    Args:
        :schema_dict: Schema dictionary
        :test_dict: Dictionary to test against schema dictionary

    Raises:
        :KeyError: If test dictionary does not have a required key
        :SchemaError: If the schema itself is ill-defined
        :TypeError: If test dictionary has a value of wrong type
        :ValueError: If test dictionary has a value of wrong 'size'

    Note:
        * Schema validation inspired by JSON schema, see

        https://json-schema.org/understanding-json-schema/reference/index.html
    """

    # TODO
    # LIST check
    # -- check numerical items in range...

    # STRING check
    # -- check REGEX patterns

    for key, form in schema_dict.items():

        # ----- Check that dictionary has required keys -----
        if key == SPECIAL_KEY_CHECK_REQ_KEYS:
            check_keys_in_dict(form, test_dict)
            continue

        # Note: Required keys are checked separately
        test_dict_value = test_dict.get(key, None)
        if test_dict_value is None and key not in schema_dict.get(SPECIAL_KEY_CHECK_REQ_KEYS, []):
            continue

        # ----- Basic type check -----
        schema_dict_type = form.get('type', None)
        if schema_dict_type is None:
            raise SchemaError(f"Expected type is not defined in schema (key: {key})")

        if not isinstance(test_dict_value, schema_dict_type):
            raise TypeError(
                f"""
                Unexpected data type for key '{key}'.
                Expected {schema_dict_type}, got {type(test_dict_value)}.
                """
            )

        # ----- TYPE dict -----
        if schema_dict_type is dict:
            sub_schema_dict = form.get('schema', None)
            if sub_schema_dict is not None:
                check_dict_against_schema(test_dict_value, sub_schema_dict)

        # ----- TYPE bool -----
        # No further checks required

        # ----- TYPE float/int -----
        elif schema_dict_type in (float, int):
            for check_key in OPERATORS.keys():
                check_value = form.get(check_key, None)
                if check_value is None:
                    continue
                schema_dict_value = form.get(check_key, None)
                if not isinstance(schema_dict_value, (int, float)):
                    raise SchemaError("Comparison value is not of type 'int' or 'float'")

                if not OPERATORS[check_key](test_dict_value, schema_dict_value):
                    raise ValueError(
                        f"""
                        Test dictionary has wrong value for key '{key}'.
                        Expected {check_key}{schema_dict_value}, but test value is '{test_dict_value}'.
                        """
                    )

        # ----- TYPE str -----
        elif schema_dict_type is str:
            min_len = form.get('min_len', None)
            if min_len is not None:
                if len(test_dict_value) < min_len:
                    raise ValueError(
                        f"""
                        String is too short for key '{key}'.
                        Minimum length is '{min_len}', got length '{len(test_dict_value)}'
                        """
                    )

            max_len = form.get('max_len', None)
            if max_len is not None:
                if len(test_dict_value) > max_len:
                    raise ValueError(
                        f"""
                        String is too long for key '{key}'.
                        Maximum length is '{max_len}', got length '{len(test_dict_value)}'
                        """
                    )

        # ----- TYPE tuple/list -----
        elif schema_dict_type in (tuple, list):
            min_len = form.get('min_len', None)
            if min_len is not None:
                if len(test_dict_value) < min_len:
                    raise ValueError(
                        f"""
                        Array is too short for key '{key}'.
                        Minimum length is '{min_len}', got length '{len(test_dict_value)}'
                        """
                    )
            max_len = form.get('max_len', None)
            if max_len is not None:
                if len(test_dict_value) > max_len:
                    raise ValueError(
                        f"""
                        Array is too long for key '{key}'.
                        Maximum length is '{max_len}', got length '{len(test_dict_value)}'
                        """
                    )

            # Check type of the items
            item_types = form.get('item_types', None)
            if item_types is not None:
                if not all(isinstance(item, item_types) for item in test_dict_value):
                    raise TypeError(
                        f"""
                        Array for key '{key}' has item(s) with wrong type.
                        """
                    )


def check_keys_in_dict(required_keys, test_dict):
    """
    Check that required keys are in a test dictionary

    Args:
        :required_keys: List of keys required in the test dictionary
        :test_dict: Test dictionary

    Raises:
        :KeyError: If a required key is not found in the test dictionary
    """

    # TODO: check that required_keys is list of strings

    test_dict_keys = list(test_dict.keys())
    for required_key in required_keys:
        if not required_key in test_dict_keys:
            err_msg = f"""
            Key '{required_key}' is required, but not found in test dictionary
            """
            raise KeyError(err_msg)


def get_default_value_dict(schema_dict):
    """
    Return a dictionary with default values based on a schema dict

    Default values are genereated as follows:

        * If a key 'default' exists, the corresponding value will be used
            * If value is callable object, then the called value will be used
            * If value is non-callable, the value itself will be used
        * If no key, 'default' exists, 'type' will be called (if callable type)
        * Otherwise the default value will be None

    Example:

    .. code:: python

        from datetime import datetime

        def time_now():
            return datetime.strftime(datetime.now(), '%H:%S')

        schema_dict = {
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

    The function will return

    .. code:: python

        defaults = {
            'time': '08:40',
            'person': 'C.Lindbergh',
            'age': 0,
            'pets': {
                'dog': None,
                'cat': False,
            }
        }
    """

    defaults = {}
    for key, form in schema_dict.items():
        if key in SPECIAL_KEYS:
            continue

        # ----- Basic type check -----
        schema_dict_type = form.get('type', None)
        if schema_dict_type is None:
            raise SchemaError(f"Expected type is not defined in schema (key: {key})")

        # ----- Recursion -----
        if schema_dict_type is dict:
            defaults[key] = get_default_value_dict(form.get('schema', {}))
            continue

        # ----- Set default value -----
        # Hint: default value could be intentionally set to None
        default_value = form.get('default', NOTHING)
        if default_value is not NOTHING:
            if callable(default_value):
                defaults[key] = default_value()
            else:
                defaults[key] = default_value
            # TODO: maybe check that defaults[key] has type schema_dict_type
        elif callable(schema_dict_type):
            defaults[key] = schema_dict_type()
        else:
            defaults[key] = None

    return defaults
