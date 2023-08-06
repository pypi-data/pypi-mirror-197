# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import click
import pytermor as pt

from ._base import _catch_and_log_and_exit, _catch_and_print
from ._base_monitor import CoreMonitor, MonitorCliCommand, CoreMonitorSettings, CoreMonitorConfig
from .exec_list_dir import Styles
from ..shared import SocketMessage
from ..shared.dto import NetworkLatencyInfo

OUTPUT_WIDTH = 5


@click.command(
    name=__file__,
    cls=MonitorCliCommand,
    short_help="network latency",
)
@click.pass_context
@_catch_and_log_and_exit
@_catch_and_print
def invoker(ctx: click.Context, demo: bool, **kwargs):
    """
    ``
    """
    NetworkLatencyMonitor(ctx, demo, **kwargs)


class NetworkLatencyMonitor(CoreMonitor[NetworkLatencyInfo, CoreMonitorConfig]):
    def _init_settings(
        self, debug_mode: bool, force_cache: bool
    ) -> CoreMonitorSettings[CoreMonitorConfig]:
        return CoreMonitorSettings[CoreMonitorConfig](
            socket_topic="network-latency",
            network_comm_indic=True,
            config=CoreMonitorConfig("monitor.network-latency", debug_mode, force_cache),
        )

    def get_output_width(self) -> int:
        return OUTPUT_WIDTH

    def _format_data_impl(self, msg: SocketMessage[NetworkLatencyInfo]) -> pt.Text:
        if msg.data.failed_ratio is None:
            return pt.Text("---".center(5), Styles.TEXT_DISABLED)

        if msg.data.failed_ratio > 0:
            st = Styles.WARNING
            if msg.data.failed_ratio > 0.5:
                st = Styles.ERROR
            return pt.Text(f"{100*msg.data.failed_ratio:3.0f}%", st)

        val, sep, pfx, unit = pt.utilnum.formatter_time_ms._format_raw(
            msg.data.latency_s * 1000,
            as_tuple=True,
        )
        val = f"{val:<2s}"
        val = " " * max(0, 4 - len(val + sep + pfx + unit)) + val
        return pt.Text(
            pt.Fragment(val, Styles.VALUE_PRIM_2),
            pt.Fragment(sep),
            pt.Fragment(pfx + unit, Styles.VALUE_UNIT_4),
        )
