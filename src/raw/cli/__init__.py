import click

from .config import load_config


@click.group()
@click.version_option(package_name="raw")
@click.pass_context
def raw(ctx: click.Context):
    config = load_config()

    if not config.core.rootgroup.exists():
        config.core.rootgroup.mkdir(parents=True, exist_ok=True)

    ctx.obj = config
