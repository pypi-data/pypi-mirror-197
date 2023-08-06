# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from ._base import _BaseIndicator
from ..shared import SocketMessage
from ..shared.dto import TemperatureInfo


class IndicatorTemperature(_BaseIndicator[TemperatureInfo]):
    def __init__(self):
        super().__init__("temperature", icon_name="applications-health-symbolic")

    def _render(self, msg: SocketMessage[TemperatureInfo]):
        orig_values = msg.data.values_c
        sorted_values = sorted(orig_values, key=lambda v: v[1], reverse=True)

        values_limit = 3
        top_values_origin_indexes = []
        for (k, v) in sorted_values[:values_limit]:
            top_values_origin_indexes.append(orig_values.index((k, v)))

        values = []
        warning = False
        for oindex in sorted(top_values_origin_indexes):
            _, val = orig_values[oindex]
            if val > 90:  # @TODO to config
                warning = True
            val_str = str(round(val)).rjust(2)
            values.append(val_str)
        result = " ".join([*values, '°C'])

        self._render_result(result, warning)
