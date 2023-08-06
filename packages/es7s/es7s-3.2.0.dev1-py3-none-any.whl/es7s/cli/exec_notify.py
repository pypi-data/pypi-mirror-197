# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import enum

import click

from ._base import CliCommand, CommandOption, EnumChoice, _catch_and_log_and_exit
from ..shared import run_subprocess


class EventStyle(str, enum.Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"

    @property
    def filename(self) -> str:
        return STYLE_TO_ICON_MAP.get(self, "info")

    def __str__(self):
        return self.value

STYLE_TO_ICON_MAP: dict = {
    EventStyle.INFO: "info",
    EventStyle.WARNING: "emblem-ohno",
    EventStyle.ERROR: "dialog-close",
    EventStyle.SUCCESS: "dialog-ok",
}



@click.command(name=__file__, cls=CliCommand, short_help="create and send a notification")
@click.argument("ident")
@click.argument("message")
@click.option(
    "-s",
    "--style",
    type=EnumChoice(EventStyle, show_choices=False),
    default=EventStyle.INFO,
    show_default=True,
    metavar="NAME",
    cls=CommandOption,
    help="Event style, must be one of: " + ", ".join(EventStyle) + ".",
)
@click.pass_context
@_catch_and_log_and_exit
class NotifyCommand:
    """
    @TODO fix click ARGUMENT output
    """

    def __init__(self, ctx: click.Context, ident: str, message: str, style: EventStyle, **kwargs):
        match ident:
            case "pytermor":
                icon = "/home/a.shavykin/dl/pytermor/docs/_static_src/logo-white-bg.svg"
            case _:
                icon = style.filename

        run_subprocess(  # @TODO temp
            "notify-send",
            "-i",
            icon,
            ident,
            message,
            require_success=True,
        )
