from dataclasses import dataclass

from .entity import Entity


@dataclass(kw_only=True, eq=False)
class Tag(Entity):

    def to_dict(self):
        return {
            ## From Entity
            "title": self.title,
            "color": self.color,
            "icon": self.icon,
            "description": self.description,
            "links": self.links,
            "parent": self.parent,
            "parent_id": self.parent_id,
        }
