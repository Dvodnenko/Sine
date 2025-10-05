from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from ...domain import Group, EntityRepository


class saGroupRepository(EntityRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, entity: Group) -> None:
        if entity.parentstr != "":
            entity.parent = self.get(entity.parentstr)
        self.session.add(entity)
        self.session.commit()
        return None

    def get(self, title: str) -> Group | None:
        query = select(Group) \
            .where(Group.title == title)
        obj = self.session.scalars(query).first()
        return obj

    def get_all(self) -> list[Group]:
        query = select(Group)
        groups = self.session.scalars(query).all()
        return groups

    def update(self, title: str, new: Group) -> None:
        if new.title != title:
            children = self.session.query(Group).where(Group.title.like(f"{title}/%")).all()
            for g in children:
                relative = Path(g.title).relative_to(title)
                g.title = f"{new.title}/{relative}"
        group = self.session.query(Group).where(Group.title==title).first()
        group.title,group.refs,group.color,group.icon,group.parent=(
            new.title,new.refs,new.color,new.icon,new.parent
        )
        self.session.commit()
        return None

    def delete(self, entity: Group) -> None:
        self.session.delete(entity)
        return None
