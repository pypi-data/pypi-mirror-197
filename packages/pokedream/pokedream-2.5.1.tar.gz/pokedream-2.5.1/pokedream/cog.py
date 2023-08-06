# -*- coding: utf-8 -*-

"""
pokedream.cog
~~~~~~~~~~~~

The pokedream debugging and diagnostics cog implementation.

:copyright: (c) 2021 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""

import inspect
import typing

from discord.ext import commands

from pokedream.features.baseclass import Feature
from pokedream.features.filesystem import FilesystemFeature
from pokedream.features.guild import GuildFeature
from pokedream.features.invocation import InvocationFeature
from pokedream.features.management import ManagementFeature
from pokedream.features.python import PythonFeature
from pokedream.features.root_command import RootCommand
from pokedream.features.shell import ShellFeature
from pokedream.features.sql import SQLFeature
from pokedream.features.voice import VoiceFeature

__all__ = (
    "pokedream",
    "STANDARD_FEATURES",
    "OPTIONAL_FEATURES",
    "setup",
)

STANDARD_FEATURES = (VoiceFeature, GuildFeature, FilesystemFeature, InvocationFeature, ShellFeature, SQLFeature, PythonFeature, ManagementFeature, RootCommand)

OPTIONAL_FEATURES: typing.List[typing.Type[Feature]] = []

try:
    from pokedream.features.youtube import YouTubeFeature
except ImportError:
    pass
else:
    OPTIONAL_FEATURES.insert(0, YouTubeFeature)


class pokedream(*OPTIONAL_FEATURES, *STANDARD_FEATURES):  # type: ignore  # pylint: disable=too-few-public-methods
    """
    The frontend subclass that mixes in to form the final pokedream cog.
    """


async def async_setup(bot: commands.Bot):
    """
    The async setup function defining the pokedream.cog and pokedream extensions.
    """

    await bot.add_cog(pokedream(bot=bot))  # type: ignore


def setup(bot: commands.Bot):  # pylint: disable=inconsistent-return-statements
    """
    The setup function defining the pokedream.cog and pokedream extensions.
    """

    if inspect.iscoroutinefunction(bot.add_cog):
        return async_setup(bot)

    bot.add_cog(pokedream(bot=bot))  # type: ignore[reportUnusedCoroutine]
