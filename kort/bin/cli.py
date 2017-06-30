# -*- coding: utf-8 -*-
from flask import current_app
from flask.cli import FlaskGroup, run_command

from kort.api import create_app


cli = FlaskGroup(add_default_commands=False, create_app=create_app)
cli.add_command(run_command)


@cli.command('shell')
def shell_command():
    """Starts an interactive shell."""
    ctx = current_app.make_shell_context()
    from kort.models import Links, DBSession  # noqa
    session = DBSession()  # noqa

    try:
        from IPython import embed
        from IPython.config.loader import Config
        cfg = Config()
        cfg.InteractiveShellEmbed.confirm_exit = False
        embed(config=cfg, banner1="Welcome to kort shell.")
    except ImportError:
        import code
        code.interact("kort shell", local=locals())


def main():
    cli.main()


if __name__ == '__main__':
    main()
