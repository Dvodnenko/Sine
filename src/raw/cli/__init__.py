import click

from ..config import load_config
from ..infrastructure.sqla import mapping_registry, map_tables, engine
from .commands.groups import groups_create


@click.group()
@click.version_option(package_name="raw")
@click.pass_context
def raw(ctx: click.Context):
    config = load_config()
    map_tables()

    ctx.obj = config

@raw.command("init")
@click.pass_context
def raw_init(ctx: click.Context):
    mapping_registry.metadata.create_all(bind=engine)


@raw.group
def groups(): ...

groups.add_command(groups_create)
