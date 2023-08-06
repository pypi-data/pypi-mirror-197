# -*- coding: utf-8 -*-

"""
pokedream.meta
~~~~~~~~~~~~

Meta information about pokedream.

:copyright: (c) 2021 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""

import typing

import pkg_resources

__all__ = (
    '__author__',
    '__copyright__',
    '__docformat__',
    '__license__',
    '__title__',
    '__version__',
    'version_info'
)


class VersionInfo(typing.NamedTuple):
    """Version info named tuple for pokedream"""
    major: int
    minor: int
    micro: int
    releaselevel: str
    serial: int


version_info = VersionInfo(major=2, minor=5, micro=1, releaselevel='final', serial=0)

__author__ = 'Gorialis'
__copyright__ = 'Copyright 2021 Devon (Gorialis) R'
__docformat__ = 'restructuredtext en'
__license__ = 'MIT'
__title__ = 'pokedream'
__version__ = '.'.join(map(str, (version_info.major, version_info.minor, version_info.micro)))

# This ensures that when pokedream is reloaded, pkg_resources requeries it to provide correct version info
pkg_resources.working_set.by_key.pop('pokedream', None)  # type: ignore
