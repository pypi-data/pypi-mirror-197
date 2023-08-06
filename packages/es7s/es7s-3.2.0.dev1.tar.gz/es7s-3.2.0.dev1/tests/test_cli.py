# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from dataclasses import dataclass
import io
import os
import re
import typing as t

import click
import pytest
from click.testing import CliRunner
import pytermor as pt

from es7s.cli import _entrypoint as ep
from es7s.shared import init_logger, init_config, init_io, IoParams, destroy_io, destroy_logger


def rt_str(val) -> str | None:
    if isinstance(val, str):
        return str(val)
    if isinstance(val, click.Command):
        return repr(val)
    return str(val)


@dataclass
class CommandStreams:
    cmd: t.Callable[[click.Context, ...], click.BaseCommand] | click.BaseCommand
    stdout: t.IO
    stderr: t.IO


@pytest.fixture(scope="function")  # , autouse=True)
def cli_streams(request) -> CommandStreams:
    io_params = IoParams()
    if io_params_setup := request.node.get_closest_marker("io_params"):
        io_params = IoParams(**io_params_setup.kwargs)

    os.environ.update({"ES7S_DOMAIN": "CLI_TEST"})
    init_config()
    init_logger()

    stdout = io.StringIO()
    stderr = io.StringIO()
    init_io(io_params, stdout=stdout, stderr=stderr)
    yield CommandStreams(ep.callback, stdout, stderr)

    destroy_io()
    destroy_logger()


class TestHelp:
    def test_entrypoint_help(self, cli_streams: CommandStreams):
        result = CliRunner(mix_stderr=False).invoke(cli_streams.cmd, [])

        assert result.stderr == ""
        assert result.exit_code == 0, "Exit code > 0"
        assert re.search(r"Usage:\s*entrypoint", result.stdout, flags=re.MULTILINE), "Missing usage"

    @pytest.mark.parametrize("group", ep.all_groups, ids=rt_str)
    def test_groups_help(self, cli_streams: CommandStreams, group):
        result = CliRunner(mix_stderr=False).invoke(group, ["--help"])
        expected_output = rf"Usage:\s*{group.name}"

        assert result.stderr == ""
        assert result.exit_code == 0, "Exit code > 0"
        assert re.search(expected_output, result.stdout, flags=re.MULTILINE), "Missing usage"

    @pytest.mark.parametrize("command", ep.all_commands, ids=rt_str)
    def test_commands_help(self, cli_streams: CommandStreams, command):
        result = CliRunner(mix_stderr=False).invoke(command, ["--help"])
        expected_output = rf"((Usage|Invoke directly instead):\s*{command.name})|Introduction"

        assert result.stderr == ""
        assert result.exit_code == 0, "Exit code > 0"
        assert re.search(expected_output, result.stdout, flags=re.MULTILINE), "Missing usage"


class TestCommand:
    @pytest.mark.parametrize(
        "argstr, expected_output",
        [
            ["exec get-socket test-topic", "test-topic"],
            ["exec hilight-num --demo", "text text"],
            ["exec list-dir .", "total"],
            pytest.param("exec notify test", "", marks=[pytest.mark.skip()]),
            ["exec sun", "Day length"],
            ["exec wrap --demo", "text text"],
        ],
        ids=rt_str,
    )
    def test_command_run(self, cli_streams: CommandStreams, argstr: str, expected_output: str):
        result = CliRunner().invoke(cli_streams.cmd, argstr.split(" "))

        cli_streams.stdout.seek(0)
        assert cli_streams.stderr.tell() == 0

        assert result.exit_code == 0, "Exit code > 0"
        assert re.search(expected_output, cli_streams.stdout.read()), "Expected output not found"


class TestCliCommonOptions:
    @pytest.mark.io_params(color=True)
    def test_sgrs_in_output(self, cli_streams: CommandStreams):
        result = CliRunner(mix_stderr=False).invoke(
            cli_streams.cmd,
            ["exec", "hilight-num", "--demo"],
        )
        cli_streams.stdout.seek(0)

        assert result.stderr == ""
        assert result.exit_code == 0, "Exit code > 0"
        assert pt.SGR_SEQ_REGEX.search(cli_streams.stdout.read()), "No SGRs found"


#     def test_no_color_option_disables_sgrs(self):
#         # noinspection PyTypeChecker
#         result = CliRunner(mix_stderr=False).invoke(
#             es7s.cli.entrypoint_fn,
#             ["exec", "highlight-num", "--demo", "--no-color"],
#             prog_name="cli_test",
#         )
#
#         self.assertEqual(result.exit_code, 0, "Exit code > 0")
#         self.assertNotRegex(result.stdout, SGR_SEQ_REGEX, "SGRs found")
#
#     def test_color_option_enables_sgrs_in_help(self):
#         # noinspection PyTypeChecker
#         result = CliRunner().invoke(
#             es7s.cli.entrypoint_fn, ["--help", "--color"], prog_name="cli_test"
#         )
#
#         self.assertEqual(result.exit_code, 0, "Exit code > 0")
#         self.assertRegex(result.stdout, SGR_SEQ_REGEX, "No SGRs found")
#
#     def test_no_color_option_disables_sgrs_in_help(self):
#         # noinspection PyTypeChecker
#         result = CliRunner().invoke(
#             es7s.cli.entrypoint_fn,
#             ["--help", "--no-color"],
#             prog_name="cli_test",
#         )
#
#         self.assertEqual(result.exit_code, 0, "Exit code > 0")
#         self.assertNotRegex(result.stdout, SGR_SEQ_REGEX, "SGRs found")
#
#     def test_stderr_is_empty_with_quiet_flag(self):
#         # noinspection PyTypeChecker
#         result = CliRunner(mix_stderr=False).invoke(
#             es7s.cli.entrypoint_fn,
#             ["run", "non-existing-cmd", "-q"],
#             prog_name="cli_test",
#         )
#
#         self.assertGreater(result.exit_code, 0, "Exit code should be >0")
#         self.assertEqual(result.stderr, "", "stderr should be empty")
#
#     def test_stderr_transmits_error_by_default(self):
#         # noinspection PyTypeChecker
#         result = CliRunner(mix_stderr=False).invoke(
#             es7s.cli.entrypoint_fn,
#             ["run", "non-existing-cmd"],
#             prog_name="cli_test",
#         )
#
#         self.assertGreater(result.exit_code, 0, "Exit code should be >0")
#         self.assertGreater(len(result.stderr), 0, "stderr should be filled")
