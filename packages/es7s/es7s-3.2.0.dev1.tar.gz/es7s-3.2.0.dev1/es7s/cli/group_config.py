# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import os
import subprocess

import click
import pytermor as pt

from ._base import CliGroup, CliCommand, _catch_and_log_and_exit, CommandOption
from ..shared import (
    get_config,
    reset_config,
    save_config,
    get_user_config_filepath,
    get_default_config, get_stdout,
)


@click.group(__file__, cls=CliGroup)
@click.pass_context
@_catch_and_log_and_exit
def group(ctx: click.Context, **kwargs):
    """Show/edit es7s preferences."""


@group.command("list", cls=CliCommand)
@click.option(
    "--default",
    is_flag=True,
    default=False,
    cls=CommandOption,
    help="List default variables and values instead of user's. Actually this is "
         "not a self-determined option, rather a reference to common (or global) "
         "option with the same name and effect, "
         "which is making the config loader ignore user config file and read only "
         "the default one. In other words, this option can be used with each and "
         "every command.",
)
@_catch_and_log_and_exit
class ListCommand:
    """Display user [by default] config variables with values."""

    HEADER_STYLE = pt.Style(fg=pt.cv.YELLOW)
    OPT_NAME_STYLE = pt.Style(fg=pt.cv.GREEN)
    OPT_VALUE_STYLE = pt.Style(bold=True)

    def __init__(self, default: bool):
        self._run(default)

    def _run(self, default: bool):
        config = get_default_config() if default else get_config()
        stdout = get_stdout()
        for idx, section in enumerate(config.sections()):
            if idx > 0:
                stdout.echo()
            stdout.echo_rendered(f"[{section}]", self.HEADER_STYLE)
            for option in config.options(section):
                option_fmtd = stdout.render(option, self.OPT_NAME_STYLE)
                value_fmtd = stdout.render(config.get(section, option), self.OPT_VALUE_STYLE)
                stdout.echo_rendered(option_fmtd + " = " + value_fmtd)

@click.option(
    "-p",
    "--prune",
    is_flag=True,
    default=False,
    cls=CommandOption,
    help="Silently overwrite original config, do not make a backup."
)
@group.command("reset", cls=CliCommand)
@_catch_and_log_and_exit
class ResetCommand:
    """
    Replace current user config with the default one. The original is preliminarily
    renamed to "<filename>.bak".
    """

    def __init__(self, prune: bool):
        self._run(prune)

    def _run(self, prune: bool):
        reset_config(backup=not prune)
        get_stdout().echo("Config was reset to default")


@group.command("get", cls=CliCommand)
@click.argument("name")
@_catch_and_log_and_exit
class GetCommand:
    """Display config variable value."""

    def __init__(self, name: str):
        self._run(name)

    def _run(self, name: str):
        section, option = split_name(name)
        value = get_config().get(section, option)
        get_stdout().echo(value)


@group.command("set", cls=CliCommand)
@click.argument("name")
@click.argument("value")
@_catch_and_log_and_exit
class SetCommand:
    """Set config variable value."""

    def __init__(self, name: str, value: str):
        self._run(name, value)

    def _run(self, name: str, value: str):
        section, option = split_name(name)
        get_config().set(section, option, value)
        save_config()
        get_stdout().echo("Done")


@group.command("edit", cls=CliCommand)
@_catch_and_log_and_exit
class EditCommand:
    """Open current user config in text editor."""

    def __init__(self):
        self._run()

    def _run(self):
        user_config_filepath = get_user_config_filepath()
        editor = os.getenv("EDITOR", "xdg-open")
        subprocess.run(f"{editor} {user_config_filepath}", shell=True)
        get_stdout().echo("Done")


def split_name(name: str) -> list[str, str]:
    if "." not in name:
        raise ValueError(f'Invalid format, expected: "SECTION.OPTION", got: "{name}"')
    return name.rsplit(".", 1)
