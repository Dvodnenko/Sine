import os
import signal

import click

from ..constants import DAEMON_PID_PATH


def getdpid() -> int | None:
    if DAEMON_PID_PATH.exists():
        with open(DAEMON_PID_PATH, "r") as pidfile:
            return int(pidfile.read())
    return None


@click.command("start")
@click.pass_context
def daemon_start(ctx: click.Context):
    from raw.rawd.daemon import main
    main()
    exit(0)

@click.command("stop")
@click.pass_context
def daemon_stop(ctx: click.Context):
    dpid = getdpid()
    if not dpid:
        click.echo("raw: daemon is not started")
        exit(1)
    os.kill(dpid, signal.SIGTERM)
    click.echo(f"raw: daemon stoped: {dpid}")
    exit(0)
