# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import click
import typing as t

from ._base import CliCommand, _catch_and_log_and_exit, CliGroup
from ..shared import get_stdout


@click.command(name=__file__, cls=CliCommand, short_help="list all es7s commands (incl. this one)")
@click.pass_context
@_catch_and_log_and_exit
class ListCommandsCommand:
    """
    .
    """

    def __init__(self, ctx: click.Context, **kwargs):
        self._run()

    def _run(self):
        from ._entrypoint import root_commands
        self._iterate(root_commands)

    def _iterate(self, els: t.Iterable[click.BaseCommand], stack: list[str] = None):
        if not stack:
            stack = []
        for el in els:
            if isinstance(el, CliGroup):
                self._iterate(el.commands.values(), [*stack, el.name])
            else:
                get_stdout().echo(' '.join([*stack, el.name]))
