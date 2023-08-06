# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import os

from es7s._version import __version__


APP_NAME = "es7s"
APP_VERSION = __version__
APP_DEV = bool(os.getenv("ES7S_DEV"))
if APP_DEV:
    os.environ.setdefault("PYTERMOR_TRACE_RENDERS", "true")
