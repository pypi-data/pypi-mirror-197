# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from pytermor import format_auto_float

from ._base import _BaseIndicator
from ..shared import SocketMessage
from ..shared.dto import CpuInfo


class IndicatorCpuLoad(_BaseIndicator[CpuInfo]):
    def __init__(self):
        super().__init__("cpu-load", "cpu", icon_name="jockey-symbolic")

    def _render(self, msg: SocketMessage[CpuInfo]):
        self._render_result(
            f'{msg.data.load_perc:^3.0f}%' + "  " +
            ' '.join(format_auto_float(a, 4) for a in msg.data.load_avg)
        )
