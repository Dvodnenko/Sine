from sqlalchemy import (
    Table, Column, ForeignKey, Enum, String
)

from ....domain import Group, Entity, Color
from ..orm_registry import mapping_registry


groups = Table(
    "groups", mapping_registry.metadata,
    Column("title", ForeignKey("entities.title"), primary_key=True),
    Column("color", Enum(Color, name="color_enum", create_type=True)),
    Column("icon", String, default="", nullable=False),
)

def map_groups_table():
    mapping_registry.map_imperatively(
        Group, groups,
        inherits=Entity,
        polymorphic_identity="group",
    )
