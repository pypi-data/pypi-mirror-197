# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import io

import pkg_resources

from .. import APP_NAME


class DemoText:
    @classmethod
    def open(cls) -> io.StringIO:
        return io.StringIO(pkg_resources.resource_string(APP_NAME, f'data/demo-text.txt').decode())
