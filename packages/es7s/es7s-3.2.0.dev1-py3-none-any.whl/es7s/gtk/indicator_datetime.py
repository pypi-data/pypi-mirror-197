# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from datetime import datetime

from ._base import _BaseIndicator
from ..shared import SocketMessage


class IndicatorDatetime(_BaseIndicator):
    def __init__(self):
        super().__init__("datetime")

    def _render(self, msg: SocketMessage):
        ts = datetime.fromtimestamp(msg.timestamp)
        self._render_result(ts.strftime("%D %T"))
