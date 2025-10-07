import click

from ..config import load_config
from ..infrastructure.sqla import mapping_registry, map_tables, engine


@click.group()
@click.version_option(package_name="raw")
@click.pass_context
def raw(ctx: click.Context):
    config = load_config()

    ctx.obj = config



@raw.command("init")
@click.pass_context
def raw_init(ctx: click.Context):
    map_tables()
    mapping_registry.metadata.create_all(bind=engine)
