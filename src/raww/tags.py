import click

from .data import get_tags, update_datafile


@click.command('tags')
@click.option('--new')
def tag(
    new: str
):

    mytags = get_tags()

    if new:
        if new in mytags:
            click.echo(f'🦇 tag {new} already exists')
            exit(1)
        else:
            update_datafile(tags=[*mytags, new])
            click.echo(f'🦇 new tag - {new}')
            exit(0)
    else:
        if mytags == []:
            click.echo('🦇 your tag list is empty right now')
            exit(1)
        for tag in mytags:
            click.echo(f'* {tag}')
