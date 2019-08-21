#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from commonlibs.fileio.paths import ProjectPaths
from pytest import raises


ROOT = 'root'

def test_project_paths_basics():
    """
    Test basics
    """

    paths = ProjectPaths(ROOT)
    assert str(paths.root.name) == ROOT
    assert paths.root == paths(ProjectPaths.UID_ROOT)


def test_add_paths():
    """
    Test functions for adding paths
    """

    uid1 = 'uid1'
    uid2 = 'uid2'
    path1 = 'path1'
    path2 = 'path2'
    group1 = 'group1'
    group2 = 'group2'

    paths = ProjectPaths(ROOT)
    paths.add_path(uid=uid1, path=path1, uid_groups=group1)

    # Adding same UID must raise error
    with raises(ValueError):
        paths.add_path(uid=uid1)

