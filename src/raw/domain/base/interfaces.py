from abc import ABC, abstractmethod
from pathlib import Path

from ..base.entity import Entity


class EntityRepository(ABC):
    
    @abstractmethod
    def save(self, entity: Entity) -> None: ...

    @abstractmethod
    def get(self, title: Path) -> Entity | None: ...

    @abstractmethod
    def get_all(self) -> list[Entity]: ...

    @abstractmethod
    def delete(self, title: Path) -> None: ...
