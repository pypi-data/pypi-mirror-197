# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import click

from . import (
    exec_get_socket,
    exec_hilight_num,
    exec_list_dir,
    exec_notify,
    exec_sun,
    exec_wrap,
    exec_list_commands,
)
from ._base import CliGroup, CliExtPlaceholderCommand, _catch_and_log_and_exit
from ..shared.config import get_app_config_yaml


@click.group(name=__file__, cls=CliGroup, short_help="run an embed component")
@click.pass_context
@_catch_and_log_and_exit
def group(ctx: click.Context, **kwargs):
    """
    Commands that invoke one of es7s subsystems that has been made available
    for standalone manual launching via CLI.
    """


group.add_commands(
    exec_get_socket.GetSocketCommand,
    exec_hilight_num.HighlightNumbersCommand,
    exec_list_dir.ListDirCommand,
    exec_list_commands.ListCommandsCommand,
    exec_notify.NotifyCommand,
    exec_sun.SunCommand,
    exec_wrap.WrapCommand,
)

external_apps = get_app_config_yaml("external-apps")
for cmd, desc in external_apps.items():
    group.add_command(
        click.command(name=cmd, cls=CliExtPlaceholderCommand, short_help=desc)(lambda: None)
    )
