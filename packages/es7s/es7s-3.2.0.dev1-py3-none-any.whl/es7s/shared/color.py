# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import pytermor as pt

from .config import get_config


# noinspection PyMethodMayBeStatic
class Color:
    def get_theme_color(self) -> pt.CT:
        color_name = get_config().get('general', 'theme-color', fallback='red')
        try:
            return pt.resolve_color(color_name)
        except LookupError:
            return pt.cv.RED

    def get_monitor_separator_color(self) -> pt.CT:
        hue, _, _ = self.get_theme_color().to_hsv()
        return pt.ColorRGB(hex_value=pt.hsv_to_hex(hue, .59, .50))


_color = Color()


def get_color() -> Color:
    return _color
