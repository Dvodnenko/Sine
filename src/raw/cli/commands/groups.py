import click

from ...application import GroupService
from ...domain import Color, Group
from ...infrastructure import saGroupRepository, Session


@click.command("create")
@click.argument("title")
@click.option("--color", 
              type=click.Choice([c.value for c in Color], 
                                case_sensitive=False), 
              default=Color.WHITE)
@click.option("--icon")
@click.pass_context
def groups_create(ctx: click.Context, title: str, color: str, icon: str):
    repo = saGroupRepository(session=Session())
    service = GroupService(repository=repo, config=ctx.obj)
    color = Color._member_map_.get(color.upper(), Color.WHITE)
    group = Group(title=title, refs=[], color=color, 
                  icon=icon, children=[])
    response = service.create(group)
    click.echo(response.message)
    exit(response.status_code)
