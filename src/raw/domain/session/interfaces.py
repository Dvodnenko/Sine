from abc import ABC, abstractmethod
from pathlib import Path

from ..session.entity import Session


class SessionRepository(ABC):
    
    @abstractmethod
    def save(self, session: Session): ...

    @abstractmethod
    def load(self, path: Path): ...
