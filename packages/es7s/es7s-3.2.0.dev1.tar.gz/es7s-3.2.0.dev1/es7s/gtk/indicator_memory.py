# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import random

from pytermor import format_auto_float, format_bytes_human

from ._base import _BaseIndicator
from ..shared import SocketMessage
from ..shared.dto import MemoryInfo


class IndicatorMemory(_BaseIndicator[MemoryInfo]):
    def __init__(self):
        super().__init__("memory", icon_name="view-continuous")

    def _render(self, msg: SocketMessage[MemoryInfo]):
        md = msg.data
        result = self._format_memory(msg.data.virtual_used, msg.data.virtual_total)
        warning = (msg.data.swap_used/msg.data.swap_total > .70)  # @todo
        self._render_result(result, warning)

    def _format_memory(self, used: float, total: float) -> str:
        abs = ''.join(self._format_used_value(round(used)))
        return f"{100 * used / total:^3.0f}%  {abs}"

    def _format_used_value(self, used: int) -> tuple[str, str]:
        used_kb = used / 1024
        used_mb = used / 1024**2
        used_gb = used / 1024**3
        if used_kb < 1000:
            return format_auto_float(used_kb, 4, False), "k"
        if used_mb < 10000:
            return format_auto_float(used_mb, 4, False), "M"
        return format_auto_float(used_gb, 4, False), "G"
