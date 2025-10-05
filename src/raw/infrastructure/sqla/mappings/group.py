from sqlalchemy import Table, Column, Integer, ForeignKey, String, Enum

from ....domain import Group, Entity, Color
from ..orm_registry import mapping_registry


groups_table = Table(
    "groups",
    mapping_registry.metadata,
    Column("id", Integer, ForeignKey("entities.id"), primary_key=True, autoincrement=True),
    Column("color", 
           Enum(Color, name="color_enum", create_type=True),
           nullable=False, default=Color.WHITE
    ),
    Column("icon", String, nullable=False, default="")
)


def map_groups_table():
    mapping_registry.map_imperatively(
        Group, groups_table, inherits=Entity, 
        polymorphic_identity="group",
    )
