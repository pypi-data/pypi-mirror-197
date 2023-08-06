# -*- coding: utf-8 -*-

"""
pokedream
~~~~~~~

A discord.py extension including useful tools for bot development and debugging.

:copyright: (c) 2021 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""

# pylint: disable=wildcard-import
from pokedream.cog import *  # noqa: F401
from pokedream.features.baseclass import Feature  # noqa: F401
from pokedream.flags import Flags  # noqa: F401
from pokedream.meta import *  # noqa: F401

__all__ = (
    'pokedream',
    'Feature',
    'Flags',
    'setup'
)
