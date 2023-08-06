# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import os
import typing as t

import click
import pytermor as pt

from ._base import CliCommand, _catch_and_log_and_exit
from ..shared import get_logger, get_stdout

STATIC_DIR_PATH = os.path.dirname(__file__)


class StaticCommandFactory:
    FILE_TO_HELP_MAP = {
        "print_printscr.txt": "Ubuntu print screen modifiers.",
    }

    def make_all(self) -> t.Iterable[click.Command]:
        for filename in os.listdir(STATIC_DIR_PATH):
            filepath = os.path.join(STATIC_DIR_PATH, filename)
            if not os.path.isfile(filepath) or os.path.splitext(filepath)[1] != ".txt":
                continue

            cmd = lambda filepath=filepath: StaticCommand(filepath)
            cmd = _catch_and_log_and_exit(cmd)
            cmd = click.command(
                name=filename.removeprefix("print_"),
                short_help=lambda auto: "\b   " + auto,
                help=self.FILE_TO_HELP_MAP.get(filename, f"{filename} contents"),
                cls=CliCommand,
            )(cmd)
            yield cmd


class StaticCommand:
    def __init__(self, filepath: str):
        get_logger().debug(f"Input filepath: '{filepath}'")
        with open(filepath, "rt") as f:
            tpl = f.read()
        get_logger().debug(f"Input size: " + pt.format_si_binary(len(tpl)))

        engine = pt.text.TemplateEngine()
        text = engine.parse(tpl)
        get_stdout().echo_rendered(text)
