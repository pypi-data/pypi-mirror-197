# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import copy
from datetime import datetime, timedelta

import click
import pytermor as pt

from ._base import CliCommand, CommandOption, FloatRange, DayMonthOption, _catch_and_log_and_exit
from ..shared import Styles, get_stdout, SunCalc


@click.command(
    name=__file__,
    cls=CliCommand,
    short_help="display sunrise and sunset timings",
    command_examples=[
        f"%s {s}\n"
        for s in (
            "--date Nov-15",
            "--date 11-15",
            "--date 15-Nov --lat 52.12 --long 36.32",
            "--date 15nov --lat 90.00 --long 00.00",
        )
    ],
)
@click.option("-d", "--date", cls=DayMonthOption)
@click.option(
    "-φ",
    "--lat",
    type=FloatRange(-90, 90),
    default=55.755833,
    show_default=True,
    cls=CommandOption,
    help="A coordinate that specifies the north–south position of a point of interest.",
)
@click.option(
    "-λ",
    "--long",
    type=FloatRange(-180, 180),
    default=37.617222,
    show_default=True,
    cls=CommandOption,
    help="A coordinate that specifies the east–west position of a point of interest.",
)
@_catch_and_log_and_exit
class SunCommand:
    """
    @TODO curl ip-api.com -> geolocation [timeout 1s, disablable]
    """

    PADDING_LEFT = 1
    TIMES_ORDER = [
        "dawn",
        "sunrise",
        "sunset",
        "dusk",
    ]
    TIMES_DESCS = {
        "now": ("--", "Now -->"),
        "dawn": ("🌃", "Dawn"),
        "sunrise": ("🌄", "Sunrise"),
        "sunset": ("🌇", "Sunset"),
        "dusk": ("🌆", "Dusk"),
    }

    def __init__(
        self,
        date: datetime | None,
        lat: float,
        long: float,
    ):
        self._now = datetime.now()
        self._is_today = date is None
        self._is_daytime = None
        date = datetime(self._now.year, date.month, date.day) if date else self._now

        self._pad_left = "".ljust(self.PADDING_LEFT)
        self._gap = "".ljust(2)

        self._run(date, lat, long)

    def _run(self, dt: datetime, lat: float, long: float):
        sun_calc = SunCalc()

        times = sun_calc.get_times(dt, lat, long)
        sunrise = times.get("sunrise")
        sunset = times.get("sunset")

        dt12 = datetime(dt.year, dt.month, dt.day, hour=12)
        _, altitude = sun_calc.get_position(dt12, lat, long)
        self._is_daytime = altitude > 0

        self._echo_date(dt)
        self._echo_location(lat, long)
        self._echo_duration("Day length", sunset, sunrise)
        get_stdout().echo()

        times_filtered = {k: v for k, v in times.items() if k in self.TIMES_DESCS.keys() and v}

        now_insert_pos = 0
        times_order = copy.copy(self.TIMES_ORDER)  # @refactorme ну OrderedDict же
        for idx, k in enumerate(times_order):
            t = times_filtered.get(k)
            if not t:
                continue
            if t.time() < self._now.time():
                now_insert_pos = idx + 1

        if self._is_today:
            times_order.insert(now_insert_pos, "now")
            times_filtered.update({"now": self._now})

        for idx, k in enumerate(times_order):
            time_desc = self.TIMES_DESCS.get(k)
            if now_insert_pos == len(times_order) - 1:
                show_delta = idx == 0
            else:
                show_delta = idx == now_insert_pos + 1
            if not self._is_today:
                show_delta = False
            self._echo_time(*time_desc, times_filtered.get(k), show_delta=show_delta)

    def _echo_location(self, lat: float, long: float):
        text = pt.Text()
        self._append_label_long(text, "Location")
        self._append_note(text, f"{lat:.6f}, {long:.6f}")
        get_stdout().echo_rendered(text)

    def _echo_date(self, dt: datetime):
        text = pt.Text()
        self._append_label_long(text, "Date")
        self._append_note(text, f"{dt:%-e-%b-%y}")
        get_stdout().echo_rendered(text)

    def _echo_duration(self, label: str, sunset: datetime | None, sunrise: datetime | None):
        if sunset and sunrise:
            day_length = sunset - sunrise
            delta_str = pt.format_time_delta(day_length.total_seconds(), 10)
        else:
            delta_str = "polar " + ("day" if self._is_daytime else "night")

        text = pt.Text()
        self._append_label_long(text, label)
        self._append_note(text, delta_str)
        get_stdout().echo_rendered(text)

    def _echo_time(self, icon: str, label: str, dt: datetime, show_delta: bool):
        text = pt.Text()
        self._append_label(text, icon, label)
        if not dt:
            self._append_note(text, "--")
            self._echo_rendered(text)
            return
        self._append_value(text, dt.strftime("%T"))

        if show_delta:
            delta = dt - self._now
            next_str = ""
            if delta.total_seconds() < 0:
                delta += timedelta(days=1)
                next_str = " (next)"
            delta_str = pt.format_time_delta(delta.total_seconds(), 6) + next_str
            self._append_note(text, f"Δ {delta_str}")

        get_stdout().echo_rendered(text)

    def _append_label_long(self, text: pt.Text, string: str):
        text += pt.Fragment(f"{self._pad_left}{string:>10s}{self._gap}", Styles.TEXT_LABEL)

    def _append_label(self, text: pt.Text, icon: str, string: str):
        text += pt.Fragment(f"{self._pad_left}{icon} {string:<7s}" + self._gap, Styles.TEXT_LABEL)

    def _append_value(self, text: pt.Text, string: str):
        text += pt.Fragment(string + self._gap, Styles.TEXT_ACCENT)

    def _append_note(self, text: pt.Text, string: str):
        text += pt.Fragment(string, Styles.TEXT_DEFAULT)
