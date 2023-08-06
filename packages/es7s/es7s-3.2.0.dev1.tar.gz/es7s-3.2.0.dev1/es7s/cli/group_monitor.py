# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import click

from . import (
    monitor_battery,
    monitor_cpu_load,
    monitor_cpu_load_avg,
    monitor_cpu_freq,
    monitor_combined,
    monitor_datetime,
    monitor_docker,
    monitor_memory,
    monitor_temperature,
    monitor_timestamp,
    monitor_weather,
    monitor_fan_speed,
    monitor_disk_usage,
    monitor_network_country,
    monitor_network_latency,
)
from ._base import CliGroup, _catch_and_log_and_exit


@click.group(
    name=__file__,
    cls=CliGroup,
    short_help="run system monitor",
)
@click.pass_context
@_catch_and_log_and_exit
def group(ctx: click.Context, **kwargs):
    """
    Launch one of es7s system monitors, or indicators. Mostly
    used by tmux.
    """


# noinspection PyTypeChecker
commands: list[click.Command] = [
    monitor_combined.CombinedMonitor,
    monitor_battery.invoker,
    monitor_datetime.invoker,
    monitor_docker.invoker,
    monitor_cpu_load.invoker,
    monitor_cpu_load_avg.invoker,
    monitor_cpu_freq.invoker,
    monitor_disk_usage.invoker,
    monitor_fan_speed.invoker,
    monitor_memory.invoker,
    monitor_network_country.invoker,
    monitor_network_latency.invoker,
    monitor_timestamp.invoker,
    monitor_temperature.invoker,
    monitor_weather.invoker,
]
for command in commands:
    group.add_command(command)
