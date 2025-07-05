from pathlib import Path
import json

import click

from .config import load_config, save_config, CONFIG_FILE, DEFAULT_RAWW_DF
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

    ctx.obj = {'raww_datafile': raww_datafile, 'config': config}

@raw.group()
def config():
    ...

@config.command()
def create():
    config = load_config()
    save_config(config)
    click.echo('🦇 configuration created')

@config.command()
def show():
    if not CONFIG_FILE.exists():
        click.echo('🦇 no configuration found')
        exit(1)
    
    config = load_config()
    click.echo(f'raww data file: {config.get('raww_datafile', DEFAULT_RAWW_DF)}')

@config.command()
@click.option('-n', '--new-directory', type=click.Path(exists=False), help='')
def update(new_directory: str):
    config = load_config()
    config['raww_datafile'] = new_directory + '/data.json'

    save_config(config)
    click.echo(f'raww datafile set to "{new_directory + '/data.json'}"')


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
