# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import click


from ..cli import print_regex, print_weather_icons, print_static
from ._base import CliGroup, EpilogPart, _catch_and_log_and_exit


@click.group(
    name=__file__,
    cls=CliGroup,
    epilog=EpilogPart("[~] indicates dynamic presets"),
)
@click.pass_context
@_catch_and_log_and_exit
def group(ctx: click.Context, **kwargs):
    """Display preset cheatsheet."""


# noinspection PyTypeChecker
commands: list[click.Command] = [
    print_regex.RegexPrinter,
    print_weather_icons.WeatherIconsPrinter,
    *print_static.StaticCommandFactory().make_all(),
]
for command in commands:
    group.add_command(command)
