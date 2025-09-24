from dataclasses import dataclass, field
from pathlib import Path

from .enums import Color


@dataclass(eq=False)
class Entity:

    ID: str
    group: Path # path to the parent folder
    title: str
    color: Color = field(default=Color.WHITE, kw_only=True)
    icon: str | None = field(default=None, kw_only=True)
    
    @property
    def short_ID(self): 
        return self.ID[:10]
    
    def __eq__(self, other):
        return isinstance(other, Entity) and self.group == other.group
