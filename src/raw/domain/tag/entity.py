from dataclasses import dataclass

from src.raw.domain.base.entity import Entity


@dataclass(kw_only=True)
class Tag(Entity):
    title: str
