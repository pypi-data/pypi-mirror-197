# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import click

from ._base import CliCommand, _catch_and_log_and_exit
from ..shared import get_stdout
from ..shared.system import get_socket_path


@click.command(name=__file__, cls=CliCommand, short_help="get monitor socket path")
@click.argument("topic")
@click.pass_context
@_catch_and_log_and_exit
class GetSocketCommand:
    """
    @TODO fix click ARGUMENT output
    """

    def __init__(self, ctx: click.Context, topic: str, **kwargs):
        self._run(topic)

    def _run(self, topic: str):
        socket_path = get_socket_path(topic)  # @TODO validate ?
        get_stdout().echo(socket_path)
