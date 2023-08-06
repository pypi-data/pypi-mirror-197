# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import click

from ._base import CommandOption, CliGroup, CliCommand, _catch_and_log_and_exit


@click.group(__file__, cls=CliGroup)
@click.pass_context
@_catch_and_log_and_exit
def group(ctx: click.Context, **kwargs):
    """Manage es7s components."""


@group.command("install", cls=CliCommand)
@click.option(
    "-n",
    "--dry-run",
    is_flag=True,
    default=None,
    cls=CommandOption,
    help="Don't actually do anything, just pretend to.",
)
@click.pass_context
@_catch_and_log_and_exit
class InstallCommand:
    """Install es7s system."""

    # @TODO *********************************
    #       INVOKE invoke
    #       *********************************

    def __init__(self, ctx: click.Context, dry_run: bool, **kwargs):
        super().__init__(ctx, **kwargs)
        self._run(dry_run)

    def _run(self, dry_run: bool):
        self.__prepare()
        self.__copy_core()
        self.__inject_bashrc()
        self.__inject_gitconfig()
        self.__copy_bin()
        self.__install_with_apt()
        self.__install_with_pip()
        self.__dload_install()
        self.__build_install_tmux()
        self.__build_install_less()
        self.__install_es7s_exts()

        raise NotImplementedError("OH NOES")

    def __prepare(self):
        # install docker
        # sudo xargs -n1 <<< "docker syslog adm sudo" adduser $(id -nu)
        # ln -s /usr/bin/python3 ~/.local/bin/python
        pass

    def __copy_core(self):
        # install i -cp -v
        # git+ssh://git@github.com/delameter/pytermor@2.1.0-dev9
        pass

    def __inject_bashrc(self):
        pass

    def __inject_gitconfig(self):
        pass

    def __copy_bin(self):
        pass

    def __install_with_apt(self):
        pass

    def __install_with_pip(self):
        pass

    def __dload_install(self):
        # ginstall exa
        # ginstall bat
        pass

    def __build_install_tmux(self):
        # install tmux deps
        # build_tmux
        # ln -s `pwd`/tmux ~/bin/es7s/tmux
        # git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
        # tmux run-shell /home/delameter/.tmux/plugins/tpm/bindings/install_plugins
        pass

    def __build_install_less(self):
        # install less deps
        # build_less
        pass

    def __install_es7s_exts(self):
        # install i -i -v

        # colors
        # fonts?
        # > pipx install kolombos
        # leo
        # > pipx install macedon
        # watson
        # nalog
        pass
