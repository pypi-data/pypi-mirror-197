# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from ._entrypoint import invoker as entrypoint_fn


def main():
    entrypoint_fn()


if __name__ == "__main__":
    main()
