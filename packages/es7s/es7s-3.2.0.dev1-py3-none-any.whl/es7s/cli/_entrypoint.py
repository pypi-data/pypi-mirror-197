# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import os
import re
import signal
import sys

import click
import pytermor as pt

from ._base import (
    _catch_and_log_and_exit,
    EpilogPart,
    CliGroup,
    Context,
    HelpFormatter,
    CommandOption,
    _exit,
)
from .group_config import group as config_group
from .group_exec import group as execute_group
from .group_manage import group as manage_group
from .group_monitor import group as monitor_group
from .group_print import group as print_group
from .options import options_command
from .. import APP_NAME, APP_VERSION, APP_DEV
from ..shared import (
    LoggerParams,
    IoParams,
    init_logger,
    init_io,
    get_stdout,
    get_stderr,
    init_config,
)
from ..shared.config import ConfigLoaderParams


def invoker():
    os.environ.update({"ES7S_DOMAIN": "CLI"})
    init_cli()
    try:
        callback()
    except SystemExit as e:
        if stdout := get_stdout(False):
            stdout.echo()
        raise


def init_cli():
    pre_filtered_args = sys.argv
    logger_params, io_params, cfg_params, spec_args = _filter_common_args(sys.argv)
    sys.argv = spec_args

    logger = init_logger(params=logger_params)
    _, _ = init_io(io_params)
    init_config(cfg_params)

    post_filtered_args = sys.argv

    if hasattr(sys, "orig_argv"):
        logger.log_init_params(("Original app args:", getattr(sys, "orig_argv")))
    logger.log_init_params(
        ("Post-pipx app args:", pre_filtered_args),
        ("Post-init app args:", post_filtered_args),
        ("Log configuration:", logger_params),
        ("Logger setup:", {"handlers": logger.handlers}),
        ("IO configuration:", io_params),
        ("Stdout proxy setup:", get_stdout().as_dict()),
        ("Stderr proxy setup:", get_stderr().as_dict()),
    )

    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)


def exit_gracefully(signal_code: int, *args):
    _exit(0, f"Terminating due to {signal.Signals(signal_code).name} ({signal_code})")


class EntrypointCliGroup(CliGroup):
    def format_usage(self, ctx: Context, formatter: HelpFormatter) -> None:
        if ctx.failed:
            super().format_usage(ctx, formatter)
            return

        class LogoFormatter(pt.StringReplacer):
            REGEX = re.compile(r"(\^+)|((╲╲╲)|(╱╲|╲╱))(╲+(╱+(?!╲))?|╱+(?!╲)|)")
            LOGO_ACCENT = pt.Style(fg=pt.cv.YELLOW, overlined=True)
            LOGO_DEFAULT = pt.Style(fg=pt.cv.BLUE, overlined=True)

            def __init__(self):
                super().__init__(self.REGEX, self.replace)

            def replace(self, m: re.Match) -> str:
                group_overline_marks = m.group(1)
                group_accent_left = m.group(3)
                group_accent = m.group(4)
                group_default = m.group(5)
                result = ""

                if group_overline_marks:
                    result += render(" " * len(group_overline_marks), pt.Style(self.LOGO_DEFAULT))
                if group_accent_left:
                    result += render(group_accent_left, pt.Style(self.LOGO_ACCENT, overlined=False))
                if group_accent:
                    if group_accent.endswith("╲"):
                        result += render(
                            group_accent[0], pt.Style(self.LOGO_ACCENT, overlined=False)
                        )
                        result += render(
                            group_accent[1:], pt.Style(self.LOGO_ACCENT, overlined=True)
                        )
                    else:
                        result += render(group_accent, pt.Style(self.LOGO_ACCENT, overlined=False))
                if group_default:
                    if group_default.endswith("╲"):
                        result += render(group_default[:-1], self.LOGO_DEFAULT)
                        result += render(
                            group_default[-1],
                            pt.Style(self.LOGO_DEFAULT, overlined=False),
                        )
                    else:
                        result += render(group_default, self.LOGO_DEFAULT)
                return result

        render = get_stdout().render

        version_main, sep, version_sub = APP_VERSION.partition("-")
        version_sub = (sep + version_sub if version_sub else "").ljust(13 - len(version_main))
        version_str = (
            render("v", LogoFormatter.LOGO_ACCENT)
            + render(version_main, pt.Style(LogoFormatter.LOGO_DEFAULT, bold=True))
            + render(version_sub, LogoFormatter.LOGO_DEFAULT)
        )

        # fmt: off
        formatter.buffer.extend([pt.utilstr.apply_filters(line, LogoFormatter) for line in [
        r"                                                                             ""\n",
        r" ╱╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲     ╱╲╲╲╲╲╲╲╲╲╲╲    ╱╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲   ╱╲╲╲╲╲╲╲╲╲╲╲        ""\n",
        r" ╲╲╲╲╲╱╱╱╱╱╱╱╱╱╱╱    ╱╲╲╲╱╱╱╱╱╱╱╱╱╲╲╲ ╲╱╱╱╱╱╱╱╱╱╱╱╱╱╲╲╲ ╱╲╲╲╱╱╱╱╱╱╱╱╱╲╲╲     ""\n",
        r"  ╲╲╲╲╲^^^^^^^^^     ╲╱╱╲╲╲╲^^^^^╲╱╱╱  ^^^^^^^^^^^╱╲╲╲╱ ╲╱╱╲╲╲╲^^^^^╲╱╱╱     ""\n",
        r"   ╲╲╲╲╲╲╲╲╲╲╲╲╲      ^╲╱╱╱╱╲╲╲╲  ^^             ╱╲╲╲╱   ^╲╱╱╱╱╲╲╲╲  ^^      ""\n",
        r"    ╲╲╲╲╲╱╱╱╱╱╱╱        ^^^╲╱╱╱╱╲╲╲╲            ╱╲╲╲╱      ^^^╲╱╱╱╱╲╲╲╲      ""\n",
        r"     ╲╲╲╲╲^^^^^             ^^^╲╱╱╱╱╲╲╲        ╱╲╲╲╱           ^^^╲╱╱╱╱╲╲╲   ""\n",
        r"      ╲╲╲╲╲              ╱╲╲╲   ^^^╲╱╱╲╲╲     ╱╲╲╲╱         ╱╲╲╲   ^^^╲╱╱╲╲╲ ""\n",
        r"       ╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲ ╲╱╱╱╲╲╲╲╲╲╲╲╲╲╲╱    ╱╲╲╲╱          ╲╱╱╱╲╲╲╲╲╲╲╲╲╲╲╱ ""\n",
        r"        ╲╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱  ^^╲╱╱╱╱╱╱╱╱╱╱╱     ╲╱╱╱            ^^╲╱╱╱╱╱╱╱╱╱╱╱  ""\n",
       fr"         {version_str }      ^^^^^^^^^^       ^^                ^^^^^^^^^^   ""\n",
        ]])
        # fmt: on
        super().format_usage(ctx, formatter)


class VersionOption(CommandOption):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("is_flag", True)
        kwargs.setdefault("expose_value", False)
        kwargs.setdefault("is_eager", True)
        kwargs.setdefault("help", "Show the version and exit.")
        kwargs["callback"] = self.callback
        super().__init__(*args, **kwargs)

    def callback(self, ctx: click.Context, param: click.Parameter, value: bool):
        if not value or ctx.resilient_parsing:
            return
        fmt = lambda s: pt.Fragment(s, pt.Style(fg="green"))
        get_stdout().echo(f"{APP_NAME:<10s} {fmt(APP_VERSION):<11s}")
        get_stdout().echo(f"{'pytermor':<10s} {fmt(pt.__version__):s}")
        get_stdout().echo(f"{'python':<10s} {fmt(sys.version.split()[0]):s}")
        self._echo_gi_version(fmt)
        ctx.exit()

    def _echo_gi_version(self, fmt: callable):
        try:
            import gi
        except ImportError:
            return
        else:
            gi_v = '.'.join(str(p) for p in gi.version_info)
            get_stdout().echo(f"{'[gtk]':<10s} "+pt.render(gi_v, 'blue'))


@click.group(
    name=__file__,
    cls=EntrypointCliGroup,
    epilog=EpilogPart(
        "Run 'es7s -V' (or '--version') to get the application version.", group="run"
    ),
)
@click.option("--version", "-V", cls=VersionOption)
@click.pass_context
@_catch_and_log_and_exit
def callback(ctx: click.Context, **kwargs):
    """
    Entrypoint of es7s system CLI.
    """
    # triggers before subcommand invocation


all_commands: list[callable] = []
all_groups: list[callable] = []
root_commands: list[callable] = [
    config_group,
    execute_group,
    manage_group,
    monitor_group,
    print_group,
    options_command,
]
for c in root_commands:
    callback.add_command(c)
    if isinstance(c, CliGroup):
        all_groups.append(c)
        all_commands.extend(c.commands.values())
    else:
        all_commands.append(c)


def _filter_common_args(
    args: list[str],
) -> tuple[LoggerParams, IoParams, ConfigLoaderParams, list[str]]:
    filtered = []
    lp = LoggerParams()
    iop = IoParams()
    clp = ConfigLoaderParams()

    def process_arg(arg: str):
        is_lopt = arg.startswith("--")
        is_shopt = arg.startswith("-") and not is_lopt

        if is_lopt or (is_shopt and len(arg) == 2):
            match arg:
                case "--verbose" | "-v":
                    lp.verbosity += 1
                case "--debug":
                    lp.verbosity += 3
                case "--quiet" | "-q":
                    lp.quiet = True
                case "--tmux":
                    iop.tmux = True
                case "--color" | "-c":
                    iop.color = True
                case "--no-color" | "-C":
                    iop.color = False
                case "--default":
                    clp.default = True
                case _:
                    filtered.append(arg)
        elif is_shopt:
            for c in arg.lstrip("-"):
                process_arg("-" + c)
        else:
            filtered.append(arg)

    for a in args:
        process_arg(a)

    if APP_DEV:
        lp.verbosity = 3
    if lp.debug:
        iop.debug = True

    return lp, iop, clp, filtered
