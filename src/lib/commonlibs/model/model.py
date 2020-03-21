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
Model tools
"""

import uuid

from commonlibs.dicts.schemadicts import check_dict_against_schema


def get_uuid():
    """
    Return a (universally) unique identifier in a string representation.
    This function uses UUID4 (https://en.wikipedia.org/wiki/Universally_unique_identifier).
    """
    return str(uuid.uuid4())


class PropertyHandler:
    """
    Meta class for handling model properties

    Usage:
        * Add as a meta class for some model class
        * Allows complex models to be easily built from key-value pairs
        * Values are checked agains expected data types, even nested dicts
        * A high-level API is provided for user to build model with 'set()' and 'add()' methods
    """

    def __init__(self):
        """
        Attr:
            :_prop_schemas: (dict) specification of user data
            :_props: (dict) user data
        """

        self._prop_schemas = {}
        self._props = {}

    def _add_prop_spec(self, key, schema, is_listlike=False, is_required=False, allow_overwrite=True):
        """
        Add a specification for a key-property pair

        Args:
            :key: (str) UID of property
            :schema: (any) schema dict or type of expected value
            :is_listlike: (bool) if true, the add() method applies otherwise the set() method
            :is_required: (bool) specify if property must be defined by user or not
            :allow_overwrite: (bool) allow value to be overwritten (applies only to set() method)

        Raises:
            :ValueError: if input argument is of unexpected type
            :KeyError: if a property for 'key' already exists
        """

        # Check type of arguments
        if not isinstance(key, str):
            raise ValueError(f"'key' must be of type string, got {type(key)}")
        for arg in (is_listlike, is_required, allow_overwrite):
            if not isinstance(arg, bool):
                raise ValueError(f"Agument of type boolean expected, got {type(arg)}")

        # Keys must be unique, do not allow overwrite
        if key in self._prop_schemas.keys():
            raise KeyError(f"Property for '{key}' already defined")

        self._prop_schemas[key] = {
            'schema': schema,
            'is_required': is_required,
            'is_listlike': is_listlike,
            'allow_overwrite': allow_overwrite,
        }

    def set(self, key, value):
        """
        Set a value to a property

        Args:
            :key: (str) name of the property to set
            :value: (any) value of the property
        """

        # Check added value
        self._raise_err_key_not_allowed(key)
        self._raise_err_overwrite_not_allowed(key)
        if self._prop_schemas[key]['is_listlike']:
            raise RuntimeError(f"Method 'set()' does not apply to '{key}', try 'add()'")
        self._raise_err_incorrect_type(key, value)

        self._props[key] = value

    def add(self, key, value):
        """
        Attach a value to a property list

        Args:
            :key: (str) name of the property to set
            :value: (any) value of the property
        """

        # Check added value
        self._raise_err_key_not_allowed(key)
        self._raise_err_incorrect_type(key, value)
        if not self._prop_schemas[key]['is_listlike']:
            raise RuntimeError(f"Method add() does not apply to '{key}'")

        # Append value to a property list
        if key not in self._props:
            self._props[key] = []
        elif not isinstance(self._props[key], list):
            raise ValueError
        self._props[key].append(value)

    def get(self, key):
        return self._props[key]

    def iter(self, key):
        for value in self._props[key]:
            yield value

    def _raise_err_key_not_allowed(self, key):
        if key not in self._prop_schemas.keys():
            raise KeyError(f"Key '{key}' is not allowed")

    def _raise_err_overwrite_not_allowed(self, key):
        if key in self._props.keys() and self._prop_schemas[key]['allow_overwrite'] is False:
            raise KeyError(f"Property '{key}' is set and cannot be overwritten")

    def _raise_err_incorrect_type(self, key, value):
        value_template = self._prop_schemas[key]['schema']
        if isinstance(value_template, dict):
            check_dict_against_schema(value, value_template)
        elif isinstance(value, value_template) is False:
            raise ValueError
