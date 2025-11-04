from dataclasses import dataclass
from datetime import datetime

from .entity import Entity
from .enums import TaskStatus


@dataclass(kw_only=True, eq=False)
class Task(Entity):

    deadline: datetime = None
    status: TaskStatus = TaskStatus.INACTIVE

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

            # Task's itself
            "deadline": self.deadline,
            "status": self.status.name,
        }
