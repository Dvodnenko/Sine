from pathlib import Path
import json

import click

from .config import load_config, DEFAULT_RAWW_DF
from .tags import tag
from .sessions import begin_session, finish_session, pause_session, check_sessions


@click.group()
@click.version_option(package_name='raww')
@click.pass_context
def raw(ctx: click.Context):
    config = load_config()
    raww_datafile = Path(config.get('raww_datafile', str(DEFAULT_RAWW_DF)))

    if not raww_datafile.parent.exists():
        raww_datafile.parent.mkdir(parents=True, exist_ok=True)
    if not raww_datafile.exists():
        raww_datafile.touch()
        with open(raww_datafile, 'w') as file:
            # filling datafile with basic stuff
            json.dump({
                'tags': [],
                'active_session': {},
                'sessions': [],
            }, file, indent=4)

    ctx.obj = {'raww_datafile': raww_datafile}


## commands ##

# tags
raw.add_command(tag)

# sessions
raw.add_command(check_sessions, name='sessions')
raw.add_command(begin_session, name='begin')
raw.add_command(begin_session, name='start')
raw.add_command(finish_session, name='finish')
raw.add_command(finish_session, name='stop')
raw.add_command(pause_session, name='pause')
