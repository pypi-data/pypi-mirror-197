# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import click

from ._base import (
    CliCommand,
    OptionScope,
    Context,
    HelpFormatter,
    CommonOption,
    IntRange,
    _catch_and_log_and_exit,
    EpilogPart,
)


class OptionsCliCommand(CliCommand):
    COMMON_OPTIONS = [
        CommonOption(
            param_decls=["-v", "--verbose"],
            count=True,
            type=IntRange(0, 3, clamp=True, show_range=False),
            default=0,
            help="Increase the amount of details: '-v' for more verbose info "
            "and exception stack traces, '-vv' for even more info, and '-vvv' for data "
            "dumps. The logging level also depends on this option; see the table below.",
        ),
        CommonOption(
            param_decls=["-q", "--quiet"],
            is_flag=True,
            default=False,
            help="Disables printing anything to a standard error stream, which includes: "
            "warnings, errors, debugging information and tracing. Note that silencing the "
            "application does not affect the logging system behaviour in the slightest.",
        ),
        CommonOption(
            param_decls=["-c", "--color"],
            is_flag=True,
            default=None,
            help="Explicitly enable output formatting using escape sequences.",
        ),
        CommonOption(
            param_decls=["-C", "--no-color"],
            is_flag=True,
            default=None,
            help="Explicitly disable output formatting.",
        ),
        CommonOption(
            param_decls=["--tmux"],
            is_flag=True,
            default=False,
            help="Transform output SGRs to tmux markup (respecting '-c|-C').",
        ),
        CommonOption(
            param_decls=["--debug"],
            is_flag=True,
            default=False,
            help="Alias for '-vvv'.",
        ),
        CommonOption(
            param_decls=["--default"],
            is_flag=True,
            default=False,
            help="Ignore user configuration file (if it exists), so that the "
            "default values are loaded.",
        ),
    ]

    EPILOG_INTRO = [
        EpilogPart(
            title="introduction",
            text="There are three different option scopes:",
        ),
        EpilogPart(
            "(1) Command-specific      (2) Group-specific       (3) Common",
        ),
        EpilogPart(
            "The first scope is referenced simply as *Options* and represents a set of "
            "local options for a defined command (e.g., '--recursive' for 'es7s exec "
            "list-dir' command)."
        ),
        EpilogPart(
            "The options in the second scope do not refer to a single command, but "
            "to a group of commands (e.g., '--demo' for 'es7s monitor' group) and belong "
            "to all the commands of that group."
        ),
        EpilogPart(
            "The third scope is application-wide -- all the options listed below can be "
            "added to any 'es7s' command whatsoever. Their descriptions were moved into "
            "a dedicated command to avoid useless repetitions and save some screen space."
        ),
        EpilogPart(
            title="Options order",
            text="Unlike the regular approach, (3) common options can be placed anywhere "
            "in the command and they `will` be correctly recognized, e.g.: "
            "\"'es7s -c exec -v list-dir'\" is the equivalent of \"'es7s exec list-dir -cv'\".",
        ),
        EpilogPart(
            "On the contrary, (1) command-specific and (2) group-specific options should "
            "always be placed *after* the command, as groups themselves are not actual commands "
            "and do not have arguments). To summarize:"
        ),
        EpilogPart("'es7s' @(3)@ 'group' @(3)@ 'command' @(1)@ @(2)@ @(3)@"),
    ]

    EPILOG = [
        EpilogPart(
            title="forcing/prohibiting the colors",
            text="/*(this part was written in the middle stage of es7s development, when the "
            "application ignored options in question in case no actual command was invoked, "
            "and the output consisted of help text only; later that was fixed, but I didn't "
            "find the strength to just purge these sections, as they can be still useful; "
            "therefore they were kept)*/",
        ),
        EpilogPart(
            "If neither of '--color' and '--no-color' is set, the output mode "
            "will be set depending on the output device (i.e. if the app "
            "sees a terminal, the colors will be enabled, and the opposite "
            "otherwise). This approach is common, but some applications do not implement "
            "options to forcefully enable or disable colors, and always rely on auto-"
            "detection instead. However, there are several ways to bypass this:",
        ),
        EpilogPart(
            "- To forcefully disable SGRs simply redirect or pipe the output stream "
            "somewhere, even a rudimentary 'cat' will work: 'es7s options | cat'. "
            "The application will see that the output is not an interactive terminal "
            'and thus will switch to "no formatting allowed" mode.',
        ),
        EpilogPart(
            "- Enabling SGRs by force is a bit trickier and requires some preparations, "
            "as well as Linux OS or similar. Install the 'unbuffer' small utility and "
            "launch the needed command like this: 'unbuffer es7s options'. It will work "
            "for almost any CLI application, not just for 'es7s', so personally I find "
            "it very handy. It doesn't matter if the output is redirected or not; the "
            "behaviour of the applications will be as if there *is* a terminal on the "
            "receiving side. To test it, run 'unbuffer es7s options | cat' -- the "
            "formatting should be present.",
        ),
        EpilogPart(
            "'unbuffer' homepage: https://core.tcl-lang.org/expect/home",
        ),
        EpilogPart(
            title="verbosity",
            text="""
    \b
    +==================================================================+                     
    | OPTS |   STANDARD OUTPUT LEVELS    |        SYSLOG LEVELS        |
    |------|-----------------------------|-----------------------------|
    |      | error(brief) warn           | error warn info             |
    |"-v"  | error warn info             | error warn info debug       |
    |"-vv" | error warn info debug       | error warn info debug trace |
    |"-vvv"| error warn info debug trace | error warn info debug trace |
    +==================================================================+
    """,
        ),
    ]
    ENVIRONMENT = [
        ("{ES7S_CLI}", "Path to CLI entrypoint of 'es7s' system. Used by tmux."),
        ("",),
        ("{ES7S_DEV}", "Non-empty string enables development mode, which: "),
        *[
            ("", s)
            for s in (
                " - increases the verbosity to max level (same as *--debug* " "or *-vvv*);",
                " - uses different socket server address for daemon-monitor IPC, "
                "which helps to avoid conflicts with installed and running "
                "'es7s' daemon instance; ",
                " - allows the python debugger to stay connected "
                "by keeping the daemon process attached;",
                " - enables extended debug output of 'pytermor' formatting library "
                "with{PYTERMOR_TRACE_RENDERS}.",
                "",
            )
        ],
        (
            "{ES7S_MONITOR_DEBUG}",
            "Enables/disables monitor debugging output if set to a non-empty "
            "string or to an empty string, accordingly. Has the same effect "
            "as <monitor.debug> config variable, but with higher priority -- "
            "when env variable is defined, config variable will be ignored. Is "
            "set by tmux, but can also be used manually, as a regular env var.",
        ),
        ("",),
    ]

    option_scopes: list[OptionScope] = [
        OptionScope.COMMON,
    ]

    def _include_common_options_epilog(self) -> bool:
        return False

    def _make_short_help(self, **kwargs) -> str:
        return kwargs.get("short_help")

    def format_usage(self, ctx: Context, formatter: HelpFormatter) -> None:
        pass

    def format_options(self, ctx: Context, formatter: HelpFormatter):
        pass

    def format_epilog(self, ctx: Context, formatter: HelpFormatter) -> None:
        self._format_epilog_parts(formatter, self.EPILOG_INTRO)
        formatter.write_paragraph()

        formatter.write_heading("Common options list", newline=True, colon=False)
        with formatter.indentation():
            formatter.write_dl([p.get_help_record(ctx) for p in self.COMMON_OPTIONS])

        self._format_epilog_parts(formatter, self.EPILOG)

        formatter.write_paragraph()
        formatter.write_heading("Environment", newline=True, colon=False)
        with formatter.indentation():
            formatter.write_dl(self.ENVIRONMENT)


@click.command(
    name="options",
    cls=OptionsCliCommand,
    short_help="show shared command options",
)
@click.pass_context
@_catch_and_log_and_exit
def options_command(ctx: click.Context, **kwargs):
    click.echo(ctx.get_help())
