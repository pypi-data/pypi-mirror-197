# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import logging
import os
import re
import sys
import threading
import typing as t
from dataclasses import dataclass
from logging import (
    Logger as BaseLogger,
    LogRecord as BaseLogRecord,
    StreamHandler,
    handlers,
    DEBUG,
    INFO,
    WARNING,
    ERROR,
    CRITICAL,
    Formatter,
)

import click
import pytermor as pt
import requests

from .. import APP_NAME, APP_VERSION, APP_DEV
from .io import get_stderr
from .styles import Styles

TRACE = 5
logging.addLevelName(TRACE, "TRACE")

VERBOSITY_TO_LOG_LEVEL_MAP = {
    0: [WARNING, INFO],
    1: [INFO, DEBUG],
    2: [DEBUG, TRACE],
    3: [TRACE, TRACE],
}


@dataclass
class LoggerParams:
    verbosity: int = 0
    quiet: bool = False
    out_stderr: bool = True
    out_syslog: bool = True
    out_file: str | None = None

    @property
    def debug(self) -> bool:
        return self.verbosity >= 2


def get_logger(require=True) -> Logger | DummyLogger:
    if logger := Logger.get_instance(require):
        return logger
    return DummyLogger()


def init_logger(app_name="es7s", ident_part="core", params=LoggerParams()) -> Logger:
    return Logger(app_name, ident_part, params)


def destroy_logger():
    Logger.destroy()


class DummyLogger:
    quiet = False

    def log(self, *args, **kwargs):
        print(str(*args, **kwargs))

    debug = log
    info = log
    warning = log
    error = log


class Logger(BaseLogger):
    _logger: Logger | None = None

    @classmethod
    def get_instance(cls, require: bool) -> Logger | DummyLogger | None:
        if not cls._logger:
            if require:
                raise RuntimeError("Logger is uninitialized")
            return None
        return cls._logger

    @classmethod
    def destroy(cls):
        cls._logger = None

    HTTP_RESPONSE_FILTERS = [
        pt.utilstr.StringLinearizer(),
    ]
    TRACE_EXTRA_FILTERS: t.List[pt.utilstr.IFilter] = [
        pt.SgrStringReplacer(),
        pt.StringMapper({ord("\n"): " "}),
        pt.OmniSanitizer(),
    ]

    def __init__(self, app_name: str, ident_part: str, params: LoggerParams):
        """
        :param app_name:
        :param ident_part:
        :param params:
        """
        super().__init__(app_name)
        Logger._logger = self

        stderr_level, syslog_level = VERBOSITY_TO_LOG_LEVEL_MAP[
            min(len(VERBOSITY_TO_LOG_LEVEL_MAP) - 1, params.verbosity)
        ]
        file_level = syslog_level
        self.setLevel(min(stderr_level, syslog_level))
        self.verbosity = params.verbosity
        self.quiet = params.quiet

        if not self.quiet and params.out_stderr:
            stderr_formatter = _StderrFormatter(params, external=False)
            stderr_handler = _StderrHandler(stream=sys.stderr)
            stderr_handler.setLevel(stderr_level)
            stderr_handler.setFormatter(stderr_formatter)
            self.addHandler(stderr_handler)

        if params.out_syslog:
            syslog_handler = _SysLogHandler(ident=f"{app_name}/{ident_part}")
            syslog_handler.setLevel(syslog_level)
            syslog_handler.setFormatter(_SyslogFormatter())
            self.addHandler(syslog_handler)

        if params.out_file:
            file_handler = _FileHandler(params.out_file, "a")
            file_handler.setLevel(file_level)
            file_handler.setFormatter(_FileFormatter())
            self.addHandler(file_handler)

        self.log_init_info()

        if APP_DEV:
            self._init_pytermor_logging(stderr_level, syslog_level, params)

    def _init_pytermor_logging(self, stderr_level: int, syslog_level: int, params: LoggerParams):
        pt_stderr_handler = StreamHandler(stream=sys.stderr)
        pt_stderr_handler.setLevel(stderr_level)
        pt_stderr_handler.setFormatter(_StderrFormatter(params, external=True))
        logger = logging.getLogger("pytermor")
        logger.handlers.clear()
        logger.addHandler(pt_stderr_handler)
        logger.setLevel(stderr_level)
        pt.init_config()

    def exception(self, msg: object, **kwargs):
        msg = f"{msg.__class__.__qualname__}: {msg!s}"
        super().exception(msg)

    def log_http_request(self, req_id: int | str, url: str, method: str = "GET"):
        self.info(f"[#{req_id}] > {method} {url}")

    def log_http_response(self, req_id: int | str, response: requests.Response, with_body: bool):
        msg_resp = f"[#{req_id}] < HTTP {response.status_code}"
        msg_resp += ", " + pt.format_si(response.elapsed.total_seconds(), "s")
        msg_resp += ", " + pt.format_si_binary(len(response.text))
        if with_body:
            msg_resp += ': "'
            msg_resp += pt.apply_filters(response.text, *self.HTTP_RESPONSE_FILTERS)
            msg_resp += '"'
        self.info(msg_resp)

    def log_init_info(self):
        appver = f"{APP_NAME} {os.getenv('ES7S_DOMAIN')} v{APP_VERSION} "
        appver += "[dev-mode]" if APP_DEV else ""
        self.info(appver)
        self.info(
            format_attrs(
                {
                    "PID": os.getpid(),
                    "PPID": os.getppid(),
                    "UID": os.getuid(),
                    "CWD": os.getcwd(),
                }
            )
        )

    def log_init_params(self, *params_desc: tuple[str, object]):
        for (label, params) in params_desc:
            params_str = format_attrs(params, keep_classname=False) if params else ""
            self.debug(label.ljust(20) + params_str)

    def trace(
        self,
        data: str | bytes | t.Iterable[str | bytes],
        label: str = None,
        out_sanitized: bool = True,
        out_ucp: bool = True,
        out_utf8: bool = False,
        out_hex: bool = True,
    ):
        label = f"[{label}] "
        if isinstance(data, (str, bytes)):
            data = [data]
        for dataline in data:  # @TODO refactor
            if out_sanitized and isinstance(dataline, str):
                self.log(TRACE, label + pt.apply_filters(dataline, *self.TRACE_EXTRA_FILTERS))
        for dataline in data:
            if out_ucp and isinstance(dataline, str):
                [
                    self.log(TRACE, line)
                    for line in pt.utilstr.dump(dataline, label, -40).splitlines()
                ]
        for dataline in data:
            if out_utf8 and isinstance(dataline, str):
                [
                    self.log(TRACE, line)
                    for line in pt.StringTracer()
                    .apply(dataline, pt.TracerExtra(label))
                    .splitlines()
                ]
        for dataline in data:
            if out_hex and isinstance(dataline, bytes):
                [
                    self.log(TRACE, line)
                    for line in pt.BytesTracer().apply(dataline, pt.TracerExtra(label)).splitlines()
                ]

    def makeRecord(
        self,
        name: str,
        level: int,
        fn: str,
        lno: int,
        msg: object,
        args: t.Any,
        exc_info: t.Any,
        func: str | None = ...,
        extra: t.Mapping[str, object] | None = ...,
        sinfo: str | None = ...,
    ) -> LogRecord:
        if not isinstance(extra, dict):
            extra = {}
        rv = LogRecord(name, level, fn, lno, msg, args, exc_info, func, sinfo, **extra)
        return rv


class LogRecord(BaseLogRecord):
    def __init__(
        self,
        name: str,
        level: int,
        pathname: str,
        lineno: int,
        msg: object,
        args: t.Any,
        exc_info: t.Any,
        func: str | None = ...,
        sinfo: str | None = ...,
        pid=None,
        stream=None,
    ) -> None:
        super().__init__(name, level, pathname, lineno, msg, args, exc_info, func, sinfo)
        domain = os.getenv("ES7S_DOMAIN")

        source_1 = domain.upper() if domain else (self.name + "." + self.module)
        self.source = "[" + source_1 + "]"
        if source_2 := self._get_command_name():
            self.source += "[" + re.sub(r"[^a-zA-Z0-9.:-]+", "", source_2[:24]) + "]"

        self.pid = pid
        self.stream = stream

        self.sep_stream = ""
        if self.stream:
            if self.pid:
                self.sep_stream = f"[{self.pid} {self.stream.upper()}]"
            else:
                self.sep_stream = f"[{self.stream.upper()}]"

        self.rel_created_str = pt.format_time_delta(self.relativeCreated / 1000, 5)

    def _get_command_name(self) -> str | None:
        name = None
        if ctx := click.get_current_context(silent=True):
            name = ctx.command.name
        if thread := threading.current_thread():
            if not name or thread != threading.current_thread():
                name = thread.name
        return name


class GenericHandler(logging.Handler):
    def __repr__(self):
        return f"{self.__class__.__qualname__}[{logging.getLevelName(self.level)}]"


class _StderrHandler(GenericHandler, StreamHandler):
    def handle(self, record: LogRecord):
        super().handle(record)
        # reset cached exc_text after _Es7sStderrFormatter
        # so that syslog won't receive SGRs
        record.exc_text = None


class _FileHandler(GenericHandler, logging.FileHandler):
    pass


class _SysLogHandler(GenericHandler, handlers.SysLogHandler):
    level_overrides = {
        "TRACE": "DEBUG",
    }

    def __init__(
        self,
        ident: str,
        address: str = "/dev/log",
        facility: int = handlers.SysLogHandler.LOG_LOCAL7,
        **kwargs,
    ):
        super().__init__(address=address, facility=facility, **kwargs)
        self.ident = f"{ident}[{os.getpid()}]: "

    def mapPriority(self, levelName):
        levelName = self.level_overrides.get(levelName, levelName)
        return super().mapPriority(levelName)


class _SyslogFormatter(Formatter):
    def __init__(self, **kwargs) -> None:
        super().__init__(
            fmt=f"%(source)s%(sep_stream)s(+%(rel_created_str)s) %(message)s", **kwargs
        )


class _FileFormatter(Formatter):
    def __init__(self, **kwargs) -> None:
        super().__init__(
            fmt=f"[%(asctime)s]%(source)s%(sep_stream)s(+%(rel_created_str)s) %(message)s", **kwargs
        )


class _StderrFormatter(Formatter):
    STYLE_DEFAULT = pt.NOOP_STYLE
    STYLE_EXCEPTION = pt.Styles.ERROR

    LEVEL_TO_STYLE_MAP = {
        CRITICAL: pt.Styles.CRITICAL,
        ERROR: pt.Styles.ERROR_ACCENT,
        WARNING: pt.Styles.WARNING,
        INFO: pt.Style(fg=pt.cv.WHITE),
        DEBUG: Styles.STDERR_DEBUG,
        TRACE: Styles.STDERR_TRACE,
    }

    FORMAT_DEFAULT = "%(levelname)s: %(message)s"
    FORMAT_VERBOSE = "[%(levelname)-5.5s]%(source)s%(sep_stream)s(+%(rel_created_str)s) %(message)s"
    FORMAT_EXTERNAL = f"[%(levelname)-5.5s][ - ][%(name)s.%(module)s] %(message)s"

    def __init__(self, params: LoggerParams, external: bool, **kwargs):
        fmt = self.FORMAT_DEFAULT
        if params.verbosity > 0:
            fmt = self.FORMAT_VERBOSE
        if external:
            fmt = self.FORMAT_EXTERNAL
        super().__init__(fmt=fmt, **kwargs)

        self._show_exc_info = params.verbosity > 0

    def formatMessage(self, record: LogRecord) -> str:
        formatted_msg = super().formatMessage(record)
        msg_style = self._resolve_style(record.levelno)
        return self._render_or_raw(formatted_msg, msg_style)

    def formatException(self, ei):
        if not self._show_exc_info:
            return None
        formatted = super().formatException(ei)
        result = "\n".join(
            self._render_or_raw(line, self.STYLE_EXCEPTION)
            for line in formatted.splitlines(keepends=False)
        )
        return result

    def _render_or_raw(self, msg, style):
        if stderr := get_stderr(False):
            return stderr.render(msg, style)
        return msg

    def _resolve_style(self, log_level: int | t.Literal) -> pt.Style:
        return self.LEVEL_TO_STYLE_MAP.get(log_level, self.STYLE_DEFAULT)


def format_attrs(*o: object, keep_classname: bool = True, level: int = 0) -> str:
    def to_str(a) -> str:
        if (s := str(a)).startswith(cn := a.__class__.__name__):
            if keep_classname:
                return s
            return s.removeprefix(cn)
        return f"'{s}'" if s.count(" ") else s

    if len(o) == 1:
        o = o[0]
    if isinstance(o, t.Mapping):
        return "(" + " ".join(f"{to_str(k)}={format_attrs(v)}" for k, v in o.items()) + ")"
    elif isinstance(o, t.Sequence) and not isinstance(o, str):
        return "(" + " ".join(format_attrs(v, level=level + 1) for v in o) + ")"
    return to_str(o)


# resulting syslog output (partial):

# _TRANSPORT=syslog             # logs filtering:
# PRIORITY=7                    #
# SYSLOG_FACILITY=23            #    "journalctl --facility=local7" (all es7s logs are sent to this facility)
# _UID=1001                     # or "journalctl --ident=es7s/corectl" (that's "syslog_ident" argument)
# _GID=1001                     # or "journalctl --grep MONITOR:docker" (filter by group or/and command)
# _EXE=/usr/bin/python3.10
# _CMDLINE=/home/a.shavykin/.local/pipx/venvs/es7s/bin/python /home/a.shavykin/.local/bin/es7s corectl install
# _COMM=es7s
# SYSLOG_PID=846461
# SYSLOG_IDENTIFIER=es7s/corectl
# MESSAGE=[MONITOR:docker] Initialized with (verbose=0 quiet=False c=False color=None) [log.py:92]
