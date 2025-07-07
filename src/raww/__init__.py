from pathlib import Path
import json

import click

from .config import load_config, save_config, CONFIG_FILE, DEFAULT_RAWW_DIR
from .tags import tag
from .sessions import begin_session, finish_session, pause_session, check_sessions


@click.group()
@click.version_option(package_name='raww')
@click.pass_context
def raw(ctx: click.Context):
    config = load_config()
    raww_directory = Path(config.get('raww_directory', str(DEFAULT_RAWW_DIR)))

    if not raww_directory.exists():
        raww_directory.mkdir(parents=True, exist_ok=True)

    ctx.obj = {'raww_directory': raww_directory, 'config': config}

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
    click.echo(f'raww data directory: {config.get('raww_directory', DEFAULT_RAWW_DIR)}')

@config.command()
@click.option('-n', '--new-directory', type=click.Path(exists=False), help='')
def update(new_directory: str):
    config = load_config()
    config['raww_directory'] = new_directory

    save_config(config)
    click.echo(f'raww data directory set to "{new_directory}"')


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
