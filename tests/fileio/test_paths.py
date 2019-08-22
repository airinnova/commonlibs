#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from commonlibs.fileio.paths import ProjectPaths
from pytest import raises


ROOT = 'root'

UID1 = 'uid1'
UID2 = 'uid2'
UID3 = 'uid3'
UID4 = 'uid4'
PATH1 = 'path1'
PATH2 = 'path2'
UID_GROUP1 = 'group1'
UID_GROUP2 = 'group2'
SUBPATH1 = 'sub1'
SUBPATH2 = 'sub2'

def test_project_paths_basics():
    """
    Test basics
    """

    paths = ProjectPaths(ROOT)
    assert str(paths.root.name) == ROOT
    assert paths.root == paths(ProjectPaths.UID_ROOT)


def test_adding_paths():
    """
    Test functions for adding paths
    """

    # ----- add_path() -----

    paths = ProjectPaths(ROOT)
    paths.add_path(uid=UID1, path=PATH1, uid_groups=UID_GROUP1)

    # Adding same UID must raise error
    with raises(ValueError):
        paths.add_path(uid=UID1, path=PATH1)

    # Add new path
    paths.add_path(uid=UID2, path=PATH2, uid_groups=(UID_GROUP1, UID_GROUP2))

    assert len(paths._groups[UID_GROUP1]) == 2
    assert len(paths._groups[UID_GROUP2]) == 1
    assert len(paths._abs_paths) == 3

    # ----- add_subpath() -----
    paths.add_subpath(uid_parent=UID1, uid=UID3, path=SUBPATH1, uid_groups=UID_GROUP1)
    paths.add_subpath(uid_parent=UID2, uid=UID4, path=SUBPATH2, uid_groups=(UID_GROUP1, UID_GROUP2))

    assert len(paths._groups[UID_GROUP1]) == 4
    assert len(paths._groups[UID_GROUP2]) == 2
    assert len(paths._abs_paths) == 5



def test_calling_paths():
    """
    Test calling functions
    """

    paths = ProjectPaths(ROOT)

    paths.add_path(uid=UID1, path=PATH1, uid_groups=UID_GROUP1)
    assert str(paths(UID1)).endswith(f'/{ROOT}/{PATH1}')


def test_mk_rm_dirs():
    """
    Test making/remove directories
    """

    paths = ProjectPaths(ROOT)

    paths.add_path(uid=UID1, path=PATH1, uid_groups=UID_GROUP1)
    paths.add_path(uid=UID2, path=PATH2, uid_groups=UID_GROUP1)
    paths.make_dirs_for_groups(UID_GROUP1, is_dir=True)
    assert os.path.exists(paths(UID1))
    assert os.path.exists(paths(UID2))

    paths.rm_dirs_for_groups(UID_GROUP1)
    assert not os.path.exists(paths(UID1))
    assert not os.path.exists(paths(UID2))


def test_join_paths():
    """
    Test function to join file paths
    """

    join = ProjectPaths.join_paths

    path_joined = join(PATH1, PATH2)
    assert str(path_joined) == f"{PATH1}/{PATH2}"
