#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2019 Airinnova AB and the CommonLibs authors
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
Better file path handling
"""

from collections import defaultdict
from pathlib import Path, PurePath
import os
import shutil
import string


class ProjectPaths:

    UID_ROOT = 'root'
    FORMATTER_COUNTER = 'counter'

    def __init__(self, root_dir):
        """
        Class providing tools for filepath handling

        This class automatically converts filepaths into absolute paths,
        which helps to avoid change directories during runtime of a script.

        Paths stored and returned in this class are based on the 'Path()'
        object from the pathlib standard library, see also:

            * https://docs.python.org/3/library/pathlib.html

        Args:
            :root_dir: Project root directory (as abs. or rel. path)

        The 'root_dir' is the project root directory. All other other added
        to this class are assumed to reside inside the 'root_dir'. In other
        words, absolute file paths are assembled based on the 'root_dir'.

        Attributes:
            :_counter: Index to create numbered paths
            :_abs_paths: Dictionary with absolute paths
            :groups: Dictionary with grouped file UIDs
        """

        self._counter = 0
        self._abs_paths = {}
        self._groups = defaultdict(list)

        self._set_root_dir(root_dir)

    def __call__(self, uid, make_dirs=False, is_dir=False):
        """
        Return a path for given UID

        Args:
            :uid: Unique identifier for the path
        """

        path = self._format_path(uid)

        if make_dirs:
            parent_dirs = path if is_dir else path.parent
            parent_dirs.mkdir(parents=True, exist_ok=True)

        return path

    def _set_root_dir(self, root_dir):
        """
        Set the project root directory (rel. path will be converted to abs.)

        Args:
            :root_dir: Project root directory
        """

        self._abs_paths[self.UID_ROOT] = Path(root_dir).resolve()

    @property
    def root(self):
        """Return the Path() object for the project root directory"""

        return self.__call__(self.UID_ROOT)

    @property
    def counter(self):
        return self._counter

    @counter.setter
    def counter(self, counter):
        if not isinstance(counter, int):
            raise ValueError("Counter must be of type 'int'")

        self._counter = counter

    def add_path(self, uid, path, uid_groups=None, is_absolute=False):
        """
        Add a path

        Args:
            :uid: Unique identifier for the path
            :path: Path string or Path() object
            :uid_groups: Optional UID(s) to identify files by groups
            :is_absolute: Flag indicating if given 'path' is absolute
        """

        if uid in self._abs_paths.keys():
            raise ValueError(f"UID '{uid}' already used")

        path = Path(path)

        if not is_absolute:
            path = self.__class__.join_paths(self.root, path)

        self._abs_paths[uid] = path

        # ----- Group bookkeeping -----
        if uid_groups is not None:
            if not isinstance(uid_groups, (str, list, tuple)):
                raise TypeError(f"'uid_groups' must be of type (str, list, tuple)")

            if isinstance(uid_groups, str):
                uid_groups = (uid_groups,)

            for uid_group in uid_groups:
                self._groups[uid_group].append(uid)

    def add_subpath(self, uid_parent, uid, path, uid_groups=None):
        """
        Add a child path to an existing parent path

        Args:
            :uid_parent: UID of the parent directory
            :uid: UID of the new path
            :path: relative path to add
            :uid_groups: Optional UID(s) to identify files by groups
        """

        if uid_parent not in self._abs_paths.keys():
            raise ValueError(f"Parent UID '{uid_parent}' not found")

        parent_path = self._abs_paths[uid_parent]
        assembled_path = self.__class__.join_paths(parent_path, path)
        self.add_path(uid, assembled_path, uid_groups)

    def _format_path(self, uid):
        """
        TODO: UPDATE docstring

        Run a string format() method on a path and return new path

        Args:
            :uid: Unique identifier

        All other standard arguments and keyword arguments are forwarded to the
        format() method of 'str'
        """

        if uid not in self._abs_paths.keys():
            raise ValueError(f"UID '{uid}' not found")

        formatted_path = str(self._abs_paths[uid])
        # formatted_path = str(self._abs_paths[uid]).format(*args, **kwargs)

        ##### TODO: IMPROVE!!! ####
        # - Make more general
        formatters = [f for (_, f, _, _) in string.Formatter().parse(formatted_path)]
        if self.FORMATTER_COUNTER in formatters:
            formatted_path = formatted_path.format(counter=self.counter)
        ###########################

        return Path(formatted_path)

    @staticmethod
    def join_paths(path1, path2):
        """
        Join two paths

        Args:
            :path1: Leading path
            :path2: Trailing path
        """

        path = PurePath(path1).joinpath(path2)
        return Path(path)

    def iter_group_paths(self, uid_groups, make_dirs=False, is_dir=False):
        """
        Return a generator with paths belong to group with given UID

        Args:
            :uid_groups: Optional UID(s) to identify files by groups
        """

        if not isinstance(uid_groups, (str, list, tuple)):
            raise TypeError(f"'uid_groups' must be of type (str, list, tuple)")

        if isinstance(uid_groups, str):
            uid_groups = (uid_groups,)

        for uid_group in uid_groups:
            for uid in self._groups[uid_group]:
                yield self.__call__(uid, make_dirs=make_dirs, is_dir=is_dir)

    def make_dirs_for_groups(self, uid_groups, is_dir=True):
        """
        Create directories for all paths belonging to specified group(s)

        Args:
            :uid_groups: Optional UID(s) to identify files by groups
        """

        for _ in self.iter_group_paths(uid_groups, make_dirs=True, is_dir=is_dir):
            pass

    def rm_dirs_for_groups(self, uid_groups):
        """
        TODO

        Args:
            :uid_groups: Optional UID(s) to identify files by groups
        """

        for path in self.iter_group_paths(uid_groups):
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
            else:
                ############## TODO : better
                # - ignore_errors etc...
                try:
                    os.remove(path)
                except:
                    pass
