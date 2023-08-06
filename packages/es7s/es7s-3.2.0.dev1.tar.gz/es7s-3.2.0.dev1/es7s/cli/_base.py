# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import abc
import enum
import inspect
import os
import re
import sys
import typing as t
from abc import abstractmethod
from dataclasses import dataclass
from functools import update_wrapper
from os.path import basename, dirname, splitext, isfile, join

import click
import pytermor as pt
from pytermor.utilstr import StringReplacer

from .. import APP_NAME
from ..shared import (
    get_logger,
    get_stdout,
    format_attrs,
    shutdown_threads,
    shutdown_started,
    Styles,
)


# -----------------------------------------------------------------------------
# Parameter types


class IntRange(click.IntRange):
    def __init__(
        self,
        _min: t.Optional[float] = None,
        _max: t.Optional[float] = None,
        min_open: bool = False,
        max_open: bool = False,
        clamp: bool = False,
        show_range: bool = True,
    ):
        self._show_range = show_range
        super().__init__(_min, _max, min_open, max_open, clamp)

    def get_metavar(self, param: click.Parameter = None) -> t.Optional[str]:
        return "N"

    def _describe_range(self) -> str:
        if not self._show_range:
            return ""
        return super()._describe_range().replace("x", self.get_metavar())


class FloatRange(click.FloatRange):
    def __init__(
        self,
        _min: t.Optional[float] = None,
        _max: t.Optional[float] = None,
        min_open: bool = False,
        max_open: bool = False,
        clamp: bool = False,
        show_range: bool = True,
    ):
        self._show_range = show_range
        super().__init__(_min, _max, min_open, max_open, clamp)

    def get_metavar(self, param: click.Parameter = None) -> t.Optional[str]:
        return "X"

    def _describe_range(self) -> str:
        if not self._show_range:
            return ""
        return super()._describe_range().replace("x", self.get_metavar())


class EnumChoice(click.Choice):
    def __init__(self, impl: t.Any | enum.Enum, show_choices=True):
        self.__impl = impl
        self._show_choices = show_choices
        super().__init__(choices=[item.value for item in impl], case_sensitive=False)

    def get_metavar(self, param: click.Parameter) -> str:
        if not self._show_choices:
            return ""
        return super().get_metavar(param)

    def convert(self, value, param, ctx):
        if value is None or isinstance(value, enum.Enum):
            return value

        converted_str = super().convert(value, param, ctx)
        return self.__impl(converted_str)


# -----------------------------------------------------------------------------
# Command options


class OptionScope(str, enum.Enum):
    COMMON = "Common options"
    GROUP = "Group options"
    COMMAND = "Options"

    def __str__(self):
        return self.value


class ScopedOption(click.Option, metaclass=abc.ABCMeta):
    @property
    @abstractmethod
    def scope(self) -> OptionScope:
        raise NotImplementedError

    def has_argument(self):
        if isinstance(self.type, click.IntRange):
            return not self.count
        return isinstance(
            self.type,
            (
                click.FloatRange,
                click.Choice,
                click.DateTime,
            ),
        )


class CommonOption(ScopedOption):
    scope = OptionScope.COMMON


class GroupOption(ScopedOption):
    scope = OptionScope.GROUP


class CommandOption(ScopedOption):
    scope = OptionScope.COMMAND


class DayMonthOption(CommandOption):
    _date_formats = ["%b-%d", "%m-%d", "%d-%b", "%d-%b", "%b%d", "%m%d", "%d%b", "%d%m"]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("type", click.DateTime(self._date_formats))
        kwargs.setdefault("show_default", "current")
        kwargs.setdefault("metavar", "DD-MM")
        kwargs.setdefault(
            "help",
            "Date of interest, where DD is a number between 1 and 31, and MM is "
            "either a number between 1 and 12 or month short name (first 3 characters). "
            "MM-DD format is also accepted. Hyphen can be omitted.",
        )
        super().__init__(*args, **kwargs)


# -----------------------------------------------------------------------------
# Command epilogs


@dataclass()
class EpilogPart:
    text: str
    title: str = None
    group: str = None


EPILOG_COMMAND_HELP = EpilogPart(
    "Run '%s' 'COMMAND' '--help' to get the detailed description of the COMMAND (e.g. 'es7s exec').",
    group="run",
)
EPILOG_COMMON_OPTIONS = EpilogPart(
    "Run 'es7s options' to see common options details ('-v', '-q', '-c', '-C', '--tmux', '--default').",
    group="run",
)
EPILOG_ARGS_NOTE = EpilogPart(
    "Mandatory or optional arguments to long options are also mandatory or optional for any corresponding short options."
)


# -----------------------------------------------------------------------------
# Command extensions


@dataclass(frozen=True)
class Examples:
    title: str
    content: t.Sequence[str]

    def __bool__(self) -> bool:
        return len(self.content) > 0


# fmt: off
class HelpStyles(Styles):
    TEXT_HEADING = pt.Style(fg=pt.cv.YELLOW, bold=True)           # <- SYNOPSIS      |   | explicit manual usage only      #
    TEXT_COMMAND_NAME = pt.Style(fg=pt.cv.BLUE)                   # <- es7s exec     |   | auto-detection                  #
    TEXT_OPTION_DEFAULT = pt.Style(fg=pt.cv.HI_YELLOW)            # <- [default: 1]  |[ ]| requires wrapping in [ ]        #
    TEXT_LITERAL = pt.Style(bold=True)                            # <- 'ls | cat'    | ' | non-es7s commands (punctuation) #
    TEXT_LITERAL_WORDS = pt.Style(underlined=True)                # <- 'ls | cat'    | ' | non-es7s commands (words)       #
    TEXT_EXAMPLE = pt.Style(fg=pt.cv.CYAN, bg='full-black')       # <- ` 4 11`       | ` | output example                  #
    TEXT_ENV_VAR = pt.Style(fg=pt.cv.GREEN, bold=True)            # <- {ES7S_LE_VAR} |{ }| environment variable name       #
    TEXT_ABOMINATION = pt.Style(bg=pt.cv.BLUE).autopick_fg()      # <- :NOTE:          :   needs to be wrapped in :        #
    TEXT_INLINE_CONFIG_VAR = pt.Style(fg=pt.cv.MAGENTA)           # <- <section.opt> |< >| config variable name            #
    TEXT_ALTER_MODE = pt.Style(italic=True)                       # <- ^ALT MODE^    |^ ^| alt monitor mode                #
    TEXT_COMMENT = pt.Style(fg=pt.cv.GRAY)                        # <- // COMMENT    |// | till end of the line            #
    TEXT_ACCENT = pt.Style(bold=True)                             # <- *important*   | * | needs to be wrapped in *        #
                                                                  #  + '--option'    | ' | auto-detection if wrapped in '  #
                                                                  #  + "--option"    | " | " -> space instead of removing  #
# fmt: on


class HelpFormatter(click.HelpFormatter):
    # fmt: off
    OPT_DEFAULT_REGEX = re.compile(r"(default:\s*)(.+?)([];])|(\[[\w\s]+)(default)(])")

    OPT_REF_REGEX = re.compile(r"'(\n\s*)?(--?[\w-]+)'")
    OPT_REF_FIX_REGEX = re.compile(r'"(\n\s*)?(--?[\w-]+)"')  # < @TODO join with regular
    ACCENT_REGEX = re.compile(r"(^|)?\*([\w!-]+?)\*")
    LITERAL_REGEX = re.compile(r"'(\n\s*)?([\w/ \n|-]+?)'")
    EXAMPLE_REGEX = re.compile(r"`(\n\s*)?(.+?)`")
    INLINE_CONFIG_VAR_REGEX = re.compile(r"<(\n\s*)?([\w\s.-]+?)>")
    ENV_VAR_REGEX = re.compile(r"\{(\n\s*)?([\w.-]+?)}")  # @FIXME join with other wrappers?
    INLINE_ENV_VAR_REGEX = re.compile(r"@([()\w._-]+?)@")  # @FIXME join with other wrappers?
    ABOMINATION_REGEX = re.compile(r"::([\w.-]+?:*)::")
    ALTER_MODE_REGEX = re.compile(r"\^([\w .!-]+?)\^")
    COMMENT_REGEX = re.compile(r"(\s//\s?)(.+)($)")
    COMMENT_BLOCK_REGEX = re.compile(r"/\*()(.+)()\*/", flags=re.DOTALL)
    # fmt: on

    def __init__(
        self,
        indent_increment: int = 2,
        width: t.Optional[int] = None,
        max_width: t.Optional[int] = None,
    ):
        width = pt.get_preferable_wrap_width(False)
        super().__init__(indent_increment, width, max_width)

        self.help_filters: t.List[StringReplacer] = [
            StringReplacer(self.OPT_DEFAULT_REGEX, self.format_option_default),
            StringReplacer(self.OPT_REF_REGEX, self.format_accent),
            StringReplacer(self.OPT_REF_FIX_REGEX, self.format_accent_fixed),
            StringReplacer(self.ACCENT_REGEX, self.format_accent),
            StringReplacer(self.LITERAL_REGEX, self.format_literal),
            StringReplacer(self.EXAMPLE_REGEX, self.format_example),
            StringReplacer(self.INLINE_CONFIG_VAR_REGEX, self.format_inline_config_var),
            StringReplacer(self.ENV_VAR_REGEX, self.format_env_var),
            StringReplacer(self.INLINE_ENV_VAR_REGEX, self.format_inline_env_var),
            StringReplacer(self.ABOMINATION_REGEX, self.format_abomination),
            StringReplacer(self.ALTER_MODE_REGEX, self.format_alter_mode),
            StringReplacer(self.COMMENT_REGEX, self.format_comment),
            StringReplacer(self.COMMENT_BLOCK_REGEX, self.format_comment),
        ]

        self.command_names = [APP_NAME]
        if (ctx := click.get_current_context(True)) is None:
            return
        self.command_names = self._find_all_command_names(ctx.find_root().command)

    def _find_all_command_names(self, command: click.Command) -> set[str]:
        names = set()
        names.add(command.name)
        if hasattr(command, "commands") and isinstance(command.commands, dict):
            for nested_command in command.commands.values():
                names = names.union(self._find_all_command_names(nested_command))
        return names

    def format_option_default(self, m: re.Match) -> str:
        return (
            (m.group(1) or m.group(4))
            + get_stdout().render(m.group(2) or m.group(5), HelpStyles.TEXT_OPTION_DEFAULT)
            + (m.group(3) or m.group(6))
        )

    def format_command_name(self, m: re.Match) -> str:
        return get_stdout().render(m.group(1), HelpStyles.TEXT_COMMAND_NAME)

    def format_accent(self, m: re.Match) -> str:
        return get_stdout().render((m.group(1) or "") + m.group(2), HelpStyles.TEXT_ACCENT)

    def format_accent_fixed(self, m: re.Match) -> str:
        return get_stdout().render(
            " " + (m.group(1) or "") + m.group(2) + " ", HelpStyles.TEXT_ACCENT
        )

    def format_example(self, m: re.Match) -> str:
        return get_stdout().render((m.group(1) or "") + m.group(2), HelpStyles.TEXT_EXAMPLE)

    def format_inline_config_var(self, m: re.Match) -> str:
        result = m.group(1) or ""
        return result + ".".join(
            get_stdout().render(name, HelpStyles.TEXT_INLINE_CONFIG_VAR)
            for name in re.split(r"\.\s*", m.group(2))
        )

    def format_env_var(self, m: re.Match):
        return get_stdout().render(
            (m.group(1) or "") + " " + m.group(2) + " ", HelpStyles.TEXT_ENV_VAR
        )

    def format_inline_env_var(self, m: re.Match):
        return get_stdout().render(m.group(1), HelpStyles.TEXT_ENV_VAR)

    def format_abomination(self, m: re.Match):
        return " " + get_stdout().render(" " + m.group(1) + " ", HelpStyles.TEXT_ABOMINATION) + " "

    def format_alter_mode(self, m: re.Match):
        return get_stdout().render(m.group(1), HelpStyles.TEXT_ALTER_MODE) + "  "

    def format_comment(self, m: re.Match):
        return (
            "." * len(m.group(1))
            + get_stdout().render(m.group(2), HelpStyles.TEXT_COMMENT)
            + ":" * len(m.group(3))
        )

    def format_literal(self, sm: re.Match) -> str:
        text_literal_is_present = False
        word_count = 0

        def replace_literal(wm: re.Match) -> str:
            nonlocal text_literal_is_present, word_count
            word_count += 1
            word = wm.group()
            if len(word) < 2:
                text_literal_is_present = True
                style = HelpStyles.TEXT_LITERAL
            elif word in self.command_names or word.startswith(APP_NAME):
                style = HelpStyles.TEXT_COMMAND_NAME
            elif word.startswith("-"):
                style = HelpStyles.TEXT_ACCENT
            else:
                text_literal_is_present = True
                style = HelpStyles.TEXT_LITERAL_WORDS
            return get_stdout().render(word, style)

        replaced = re.sub(r"(\S+)", replace_literal, (sm.group(1) or "") + sm.group(2))
        if text_literal_is_present and word_count > 1:
            replaced = f"'{replaced}'"
        return replaced

    def write_heading(self, heading: str, newline: bool = False, colon: bool = True):
        heading = get_stdout().render(heading + (colon and ":" or ""), HelpStyles.TEXT_HEADING)
        self.write(f"{'':>{self.current_indent}}{heading}")
        self.write_paragraph()
        if newline:
            self.write_paragraph()

    def write_squashed_text(self, string: str):
        indent = " " * self.current_indent
        wrapped_text = click.wrap_text(
            string,
            self.width,
            initial_indent=indent,
            subsequent_indent=indent,
            preserve_paragraphs=True,
        )
        self.write(wrapped_text.replace("\n\n", "\n"))
        self.write("\n")

    def write(self, string: str) -> None:
        stripped = string.strip()
        if stripped in self.command_names:
            string = get_stdout().render(string, HelpStyles.TEXT_COMMAND_NAME)
        if stripped.startswith(APP_NAME):
            string = re.sub("([a-z0-9_-]+)", lambda m: self.format_command_name(m), string, 3)
        else:
            string = pt.utilstr.apply_filters(string, *self.help_filters)
        self.buffer.append(string)


class Context(click.Context):
    formatter_class = HelpFormatter

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.failed = False
        self.color = get_stdout().color

    def fail(self, message: str):
        self.failed = True
        super().fail(message)


class CliBaseCommand(click.Command):
    context_class = Context

    def parse_args(self, ctx: Context, args: t.List[str]) -> t.List[str]:
        get_logger().debug(f"Pre-click args:  {format_attrs(args)}")
        parsed_args = super().parse_args(ctx, args)
        return parsed_args

    def invoke(self, ctx: Context) -> t.Any:
        get_logger().debug(f"Post-click args: {format_attrs(ctx.params)}")
        try:
            return super().invoke(ctx)
        except click.ClickException as e:
            ctx.failed = True
            self.show_error(ctx, e)

    def show_error(self, ctx: Context, e: click.ClickException):
        logger = get_logger()
        logger.error(e.format_message())
        if logger.quiet:
            return

        hint = ""
        if ctx.command.get_help_option(ctx):
            hint = f"\nTry '{ctx.command_path} {ctx.help_option_names[0]}' for help."
        get_stdout().echo(f"{ctx.get_usage()}\n{hint}")

    def _make_command_name(self, orig_name: str) -> str:
        dir_name = dirname(orig_name)
        filename_parts = splitext(basename(orig_name))[0].lstrip("_").split("_")
        if filename_parts[0] == "group":
            filename_parts.pop(0)
        if len(filename_parts) == 1:
            return filename_parts[0]
        while filename_parts:
            if isfile(join(dir_name, f"group_{filename_parts[0]}.py")):
                filename_parts.pop(0)
                continue
            return "-".join(filename_parts)

    def _make_short_help(self, **kwargs) -> str:
        help_str = kwargs.get("help")
        if not help_str:
            if logger := get_logger(require=False):
                logger.warning(f"Missing help for '{kwargs.get('name')}' command")
            help_str = "..."

        short_help = kwargs.get("short_help")
        short_help_auto = help_str.lower().removesuffix(".")
        if isinstance(short_help, t.Callable):
            return short_help(short_help_auto)
        elif short_help:
            return short_help
        return short_help_auto

    def format_epilog(self, ctx: Context, formatter: HelpFormatter) -> None:
        epilog_parts = []

        if self.epilog:
            if not isinstance(self.epilog, list):
                self.epilog = [self.epilog]
            epilog_parts.extend(self.epilog)
        if any(self._is_option_with_argument(opt) for opt in ctx.command.params):
            epilog_parts.append(EPILOG_ARGS_NOTE)
        if self._include_command_help_epilog():
            epilog_parts.append(
                EpilogPart(
                    EPILOG_COMMAND_HELP.text % ctx.command_path,
                    group=EPILOG_COMMAND_HELP.group,
                )
            )
        if self._include_common_options_epilog():
            epilog_parts.append(EPILOG_COMMON_OPTIONS)

        self._format_epilog_parts(formatter, epilog_parts)

    def _include_command_help_epilog(self) -> bool:
        return False

    def _include_common_options_epilog(self) -> bool:
        return True

    def _is_option_with_argument(self, option: click.Parameter) -> bool:
        if isinstance(option, ScopedOption):
            return option.has_argument()
        return False

    def _format_epilog_parts(self, formatter: HelpFormatter, parts: list[EpilogPart]):
        squashed_parts = []
        for idx, part in enumerate(parts):
            if (
                len(squashed_parts)
                and not part.title
                and part.group
                and part.group == squashed_parts[-1].group
            ):
                squashed_parts[-1].text += "\n\n" + part.text
                continue
            squashed_parts.append(part)

        for part in squashed_parts:
            self._format_epilog_part(formatter, part)

    def _format_epilog_part(self, formatter: HelpFormatter, part: EpilogPart):
        formatter.write_paragraph()
        if part.title:
            formatter.write_heading(part.title.capitalize(), newline=True, colon=False)

        with formatter.indentation():
            formatter.write_squashed_text(inspect.cleandoc(part.text))


class CliGroup(click.Group, CliBaseCommand):
    def __init__(self, **kwargs):
        kwargs["name"] = self._make_command_name(kwargs.get("name"))
        kwargs["short_help"] = self._make_short_help(**kwargs)

        super().__init__(**kwargs)

    def format_usage(self, ctx: Context, formatter: HelpFormatter) -> None:
        pieces = self.collect_usage_pieces(ctx)
        with formatter.section("Usage"):
            formatter.write_usage(ctx.command_path, " ".join(pieces), prefix="")

    def format_options(self, ctx: Context, formatter: HelpFormatter) -> None:
        # no options for groups
        self.format_commands(ctx, formatter)

    def _include_command_help_epilog(self) -> bool:
        return True

    def add_commands(self, *commands: click.Command):
        for cmd in commands:
            self.add_command(cmd)

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx) if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail(f"Too many matches: {', '.join(sorted(matches))}")

    def resolve_command(self, ctx, args):
        # always return the full command name
        _, cmd, args = super().resolve_command(ctx, args)
        return cmd.name, cmd, args


class CliCommand(CliBaseCommand):
    option_scopes: list[OptionScope] = [
        OptionScope.COMMAND,
        OptionScope.GROUP,
    ]

    def __init__(self, **kwargs):
        kwargs.update(
            {
                "name": self._make_command_name(kwargs.get("name")),
                "params": self._build_options(kwargs.get("params", [])),
                "short_help": self._make_short_help(**kwargs),
            }
        )
        self.command_examples = Examples("Command examples", kwargs.pop("command_examples", []))
        self.output_examples = Examples("Output examples", kwargs.pop("output_examples", []))

        super().__init__(**kwargs)

    def _build_options(self, subclass_options: list[click.Option]) -> list[click.Option]:
        return [
            *subclass_options,
            *self._get_group_options(),
        ]

    def _get_group_options(self) -> list[click.Option]:
        return []

    def format_usage(self, ctx: Context, formatter: HelpFormatter) -> None:
        pieces = self.collect_usage_pieces(ctx)
        with formatter.section("Usage"):
            formatter.write_usage(ctx.command_path, " ".join(pieces), prefix="")

    def format_help_text(self, ctx: Context, formatter: HelpFormatter) -> None:
        super().format_help_text(ctx, formatter)
        self.format_examples(ctx, formatter, self.output_examples)

    def format_options(self, ctx: Context, formatter: HelpFormatter):
        opt_scope_to_opt_help_map: dict[str, list[tuple[str, str]] | None] = {
            k: [] for k in OptionScope
        }
        for param in self.get_params(ctx):
            rv = param.get_help_record(ctx)
            if rv is not None and hasattr(param, "scope"):
                opt_scope_to_opt_help_map[param.scope].append(rv)

        for opt_scope in self.option_scopes:
            opt_helps = opt_scope_to_opt_help_map[opt_scope]
            if not opt_helps:
                continue
            if opt_scope.value:
                with formatter.section(opt_scope.value):
                    formatter.write_dl(opt_helps)
            else:
                formatter.write_paragraph()
                with formatter.indentation():
                    formatter.write_dl(opt_helps)

    def format_epilog(self, ctx: Context, formatter: HelpFormatter) -> None:
        super().format_epilog(ctx, formatter)
        self.format_examples(ctx, formatter, self.command_examples)

    def format_examples(self, ctx: Context, formatter: HelpFormatter, examples: Examples) -> None:
        if not examples:
            return
        with formatter.section(examples.title.capitalize()):
            for example in examples.content:
                if "%s" in example:
                    example %= ctx.command_path
                formatter.write_text(example)


class CliExtPlaceholderCommand(CliCommand):
    MSG = pt.FrozenText(
        pt.Fragment("This is an external application placeholder\n\n"),
        pt.Fragment("Invoke directly instead:\n" + pt.pad(2), Styles.WARNING),
    )

    def _make_short_help(self, **kwargs) -> str:
        return '[external] ' + kwargs.get('short_help', '')

    def invoke(self, ctx: Context) -> t.Any:
        text = self.MSG.append(pt.Fragment(ctx.info_name, HelpStyles.TEXT_COMMAND_NAME))
        # get_stdout().echo_rendered(text)
        print(get_stdout().render(text))

    def _make_command_name(self, orig_name: str) -> str:
        return orig_name

    def format_usage(self, ctx: Context, formatter: HelpFormatter) -> None:
        self.invoke(ctx)

    def format_help_text(self, ctx: Context, formatter: HelpFormatter) -> None:
        pass

    def format_epilog(self, ctx: Context, formatter: HelpFormatter) -> None:
        pass


F = t.TypeVar("F")


def _catch_and_log_and_exit(func: F) -> F:
    def wrapper(*args, **kwargs):
        logger = get_logger()
        try:
            logger.debug("Starting command execution")
            func(*args, **kwargs)
        except Exception as e:
            logger.exception(e)
            _exit(1, "Terminating due to exception")
        logger.debug("Command executed")
        return func

    return update_wrapper(t.cast(F, wrapper), func)


def _catch_and_print(func: F) -> F:
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception:
            if stdout := get_stdout(require=False):
                stdout.echo("ERROR")
            else:
                sys.stdout.write("ERROR\n")
            raise
        return func

    return update_wrapper(t.cast(F, wrapper), func)


def _exit(code: int = 0, msg: str = "Terminating"):
    logger = get_logger(False)

    if shutdown_started():
        if logger:
            logger.info("Forcing the termination")
        os._exit(2)  # noqa
    else:
        logger.debug("Shutting threads down")
        shutdown_threads()

    if logger:
        logger.info(msg)
    sys.exit(code)
