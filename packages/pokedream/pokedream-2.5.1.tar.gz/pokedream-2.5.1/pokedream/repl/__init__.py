# -*- coding: utf-8 -*-

"""
pokedream.repl
~~~~~~~~~~~~

Repl-related operations and tools for pokedream.

:copyright: (c) 2021 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""

# pylint: disable=wildcard-import
from pokedream.repl.compilation import *  # noqa: F401
from pokedream.repl.disassembly import create_tree, disassemble  # type: ignore  # noqa: F401
from pokedream.repl.inspections import all_inspections  # type: ignore  # noqa: F401
from pokedream.repl.repl_builtins import get_var_dict_from_ctx  # type: ignore  # noqa: F401
from pokedream.repl.scope import *  # noqa: F401
