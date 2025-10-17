from sqlalchemy import Table, Column, Integer, ForeignKey

from ...entities import Folder, Entity
from ..orm_registry import mapping_registry


folders_table = Table(
    "folders",
    mapping_registry.metadata,
    Column("id", Integer, ForeignKey("entities.id"), 
           primary_key=True, autoincrement=True),
)


def map_folders_table():
    mapping_registry.map_imperatively(
        Folder, folders_table, inherits=Entity, 
        polymorphic_identity="folder",
    )
