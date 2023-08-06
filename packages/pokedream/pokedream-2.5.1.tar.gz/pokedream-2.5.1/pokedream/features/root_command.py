# -*- coding: utf-8 -*-

"""
pokedream.features.root_command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The pokedream root command.

:copyright: (c) 2021 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""

import sys
import typing
from importlib.metadata import distribution, packages_distributions

import discord
from discord.ext import commands

from pokedream.features.baseclass import Feature
from pokedream.flags import Flags
from pokedream.math import natural_size
from pokedream.modules import package_version
from pokedream.paginators import PaginatorInterface
from pokedream.types import ContextA

try:
    import psutil
except ImportError:
    psutil = None


class RootCommand(Feature):
    """
    Feature containing the root psk command
    """

    def __init__(self, *args: typing.Any, **kwargs: typing.Any):
        super().__init__(*args, **kwargs)
        self.psk.hidden = Flags.HIDE  # type: ignore

    @Feature.Command(name="pokedream", aliases=["psk"],
                     invoke_without_command=True, ignore_extra=False)
    async def psk(self, ctx: ContextA):
        """
        The pokedream debug and diagnostic commands.

        This command on its own gives a status brief.
        All other functionality is within its subcommands.
        """

        # Try to locate what vends the `discord` package
        distributions: typing.List[str] = [
            dist for dist in packages_distributions()['discord']  # type: ignore
            if any(
                file.parts == ('discord', '__init__.py')  # type: ignore
                for file in distribution(dist).files  # type: ignore
            )
        ]

        if distributions:
            dist_version = f'{distributions[0]} `{package_version(distributions[0])}`'
        else:
            dist_version = f'unknown `{discord.__version__}`'

        summary = [
            f"pokedream v{package_version('pokedream')}, {dist_version}, "
            f"`Python {sys.version}` on `{sys.platform}`".replace("\n", ""),
            f"Module was loaded <t:{self.load_time.timestamp():.0f}:R>, "
            f"cog was loaded <t:{self.start_time.timestamp():.0f}:R>.",
            ""
        ]

        # detect if [procinfo] feature is installed
        if psutil:
            try:
                proc = psutil.Process()

                with proc.oneshot():
                    try:
                        mem = proc.memory_full_info()
                        summary.append(f"Using {natural_size(mem.rss)} physical memory and "
                                       f"{natural_size(mem.vms)} virtual memory, "
                                       f"{natural_size(mem.uss)} of which unique to this process.")
                    except psutil.AccessDenied:
                        pass

                    try:
                        name = proc.name()
                        pid = proc.pid
                        thread_count = proc.num_threads()

                        summary.append(f"Running on PID {pid} (`{name}`) with {thread_count} thread(s).")
                    except psutil.AccessDenied:
                        pass

                    summary.append("")  # blank line
            except psutil.AccessDenied:
                summary.append(
                    "psutil is installed, but this process does not have high enough access rights "
                    "to query process information."
                )
                summary.append("")  # blank line
        s_for_guilds = "" if len(self.bot.guilds) == 1 else "s"
        s_for_users = "" if len(self.bot.users) == 1 else "s"
        cache_summary = f"{len(self.bot.guilds)} guild{s_for_guilds} and {len(self.bot.users)} user{s_for_users}"

        # Show shard settings to summary
        if isinstance(self.bot, discord.AutoShardedClient):
            if len(self.bot.shards) > 20:
                summary.append(
                    f"This bot is automatically sharded ({len(self.bot.shards)} shards of {self.bot.shard_count})"
                    f" and can see {cache_summary}."
                )
            else:
                shard_ids = ', '.join(str(i) for i in self.bot.shards.keys())
                summary.append(
                    f"This bot is automatically sharded (Shards {shard_ids} of {self.bot.shard_count})"
                    f" and can see {cache_summary}."
                )
        elif self.bot.shard_count:
            summary.append(
                f"This bot is manually sharded (Shard {self.bot.shard_id} of {self.bot.shard_count})"
                f" and can see {cache_summary}."
            )
        else:
            summary.append(f"This bot is not sharded and can see {cache_summary}.")

        # pylint: disable=protected-access
        if self.bot._connection.max_messages:  # type: ignore
            message_cache = f"Message cache capped at {self.bot._connection.max_messages}"  # type: ignore
        else:
            message_cache = "Message cache is disabled"

        remarks = {
            True: 'enabled',
            False: 'disabled',
            None: 'unknown'
        }

        *group, last = (
            f"{intent.replace('_', ' ')} intent is {remarks.get(getattr(self.bot.intents, intent, None))}"
            for intent in
            ('presences', 'members', 'message_content')
        )

        summary.append(f"{message_cache}, {', '.join(group)}, and {last}.")

        # pylint: enable=protected-access

        # Show websocket latency in milliseconds
        summary.append(f"Average websocket latency: {round(self.bot.latency * 1000, 2)}ms")

        await ctx.send("\n".join(summary))

    # pylint: disable=no-member
    @Feature.Command(parent="psk", name="hide")
    async def psk_hide(self, ctx: ContextA):
        """
        Hides pokedream from the help command.
        """

        if self.psk.hidden:  # type: ignore
            return await ctx.send("pokedream is already hidden.")

        self.psk.hidden = True  # type: ignore
        await ctx.send("pokedream is now hidden.")

    @Feature.Command(parent="psk", name="show")
    async def psk_show(self, ctx: ContextA):
        """
        Shows pokedream in the help command.
        """

        if not self.psk.hidden:  # type: ignore
            return await ctx.send("pokedream is already visible.")

        self.psk.hidden = False  # type: ignore
        await ctx.send("pokedream is now visible.")
    # pylint: enable=no-member

    @Feature.Command(parent="psk", name="tasks")
    async def psk_tasks(self, ctx: ContextA):
        """
        Shows the currently running pokedream tasks.
        """

        if not self.tasks:
            return await ctx.send("No currently running tasks.")

        paginator = commands.Paginator(max_size=1980)

        for task in self.tasks:
            if task.ctx.command:
                paginator.add_line(f"{task.index}: `{task.ctx.command.qualified_name}`, invoked at "
                                   f"{task.ctx.message.created_at.strftime('%Y-%m-%d %H:%M:%S')} UTC")
            else:
                paginator.add_line(f"{task.index}: unknown, invoked at "
                                   f"{task.ctx.message.created_at.strftime('%Y-%m-%d %H:%M:%S')} UTC")

        interface = PaginatorInterface(ctx.bot, paginator, owner=ctx.author)
        return await interface.send_to(ctx)

    @Feature.Command(parent="psk", name="cancel")
    async def psk_cancel(self, ctx: ContextA, *, index: typing.Union[int, str]):
        """
        Cancels a task with the given index.

        If the index passed is -1, will cancel the last task instead.
        """

        if not self.tasks:
            return await ctx.send("No tasks to cancel.")

        if index == "~":
            task_count = len(self.tasks)

            for task in self.tasks:
                if task.task:
                    task.task.cancel()

            self.tasks.clear()

            return await ctx.send(f"Cancelled {task_count} tasks.")

        if isinstance(index, str):
            raise commands.BadArgument('Literal for "index" not recognized.')

        if index == -1:
            task = self.tasks.pop()
        else:
            task = discord.utils.get(self.tasks, index=index)
            if task:
                self.tasks.remove(task)
            else:
                return await ctx.send("Unknown task.")

        if task.task:
            task.task.cancel()

        if task.ctx.command:
            await ctx.send(f"Cancelled task {task.index}: `{task.ctx.command.qualified_name}`,"
                           f" invoked at {task.ctx.message.created_at.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        else:
            await ctx.send(f"Cancelled task {task.index}: unknown,"
                           f" invoked at {task.ctx.message.created_at.strftime('%Y-%m-%d %H:%M:%S')} UTC")
