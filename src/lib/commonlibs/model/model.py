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
from collections import namedtuple
import logging

from schemadict import schemadict

FORMAT = '%(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)


def get_uuid():
    """
    Return a (universally) unique identifier in a string representation.
    This function uses UUID4 (https://en.wikipedia.org/wiki/Universally_unique_identifier).
    """
    return str(uuid.uuid4())


class PropertyHandler:

    _PROP_SCHEMA_ENTRY = namedtuple('schema', ['schema', 'is_unique', 'is_required'])

    def __init__(self):
        """
        Meta class for handling model properties

        Usage:
            * Add as a meta class for some model class
            * Allows complex models to be easily built from key-value pairs
            * Values are checked agains expected data types, even nested dicts
            * A high-level API is provided for user to build model with 'set()' and 'add()' methods

        Attr:
            :_prop_schemas: (dict) specification of expected user data
            :_props: (dict) actual user data
        """

        self._prop_schemas = {}
        self._props = {}

    def _add_prop_spec(self, key, schema, is_unique=True, is_required=False):
        """
        Add a specification for a key-property pair

        Args:
            :key: (str) UID of property
            :schema: (any) schema dict or type of expected value
            :is_unique: (bool) if True, the set() method applies otherwise the add() method
            :is_required: (bool) specify if property must be defined by user or not

        Raises:
            :ValueError: if input argument is of unexpected type
            :KeyError: if a property for 'key' already exists
        """

        # Check type of arguments
        if not isinstance(key, str):
            raise ValueError(f"'key' must be of type string, got {type(key)}")
        for arg in (is_unique, is_required):
            if not isinstance(arg, bool):
                raise ValueError(f"Agument of type boolean expected, got {type(arg)}")

        # Keys must be unique, do not allow overwrite
        if key in self._prop_schemas.keys():
            raise KeyError(f"Property for '{key}' already defined")

        self._prop_schemas[key] = self._PROP_SCHEMA_ENTRY(schema, is_unique, is_required)

    def set(self, key, value):
        """
        Set a value to a property

        Args:
            :key: (str) name of the property to set
            :value: (any) value of the property
        """

        self._raise_err_key_not_allowed(key)
        self._raise_err_incorrect_type(key, value)
        if not self._prop_schemas[key].is_unique:
            raise RuntimeError(f"Method 'set()' does not apply to '{key}', try 'add()'")

        logger.info(f"Set value for property {key!r}")
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
        if self._prop_schemas[key].is_unique:
            raise RuntimeError(f"Method add() does not apply to '{key}'")

        # Append value to a property list
        if key not in self._props:
            self._props[key] = []
        elif not isinstance(self._props[key], list):
            raise ValueError
        logger.info(f"Add value for property {key!r}")
        self._props[key].append(value)

    def get(self, key):
        return self._props[key]

    def iter(self, key):
        if self._prop_schemas[key].is_unique:
            raise KeyError(f"Method 'iter()' not supported for property '{key}', try 'get()'")
        for value in self._props[key]:
            yield value

    def _raise_err_key_not_allowed(self, key):
        if key not in self._prop_schemas.keys():
            raise KeyError(f"Key '{key}' is not allowed")

    def _raise_err_incorrect_type(self, key, value):
        if isinstance(self._prop_schemas[key].schema, dict):
            schemadict.validate(self._prop_schemas[key].schema, value)
        elif not isinstance(value, self._prop_schemas[key].schema):
            raise ValueError(f"Value of type {self._prop_schemas[key].schema} expected, got {type(value)}")
