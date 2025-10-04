from dataclasses import dataclass, field
from pathlib import Path

from .enums import Color


@dataclass(eq=False)
class Entity:

    title: Path
    color: Color = field(default=Color.WHITE, kw_only=True)
    icon: str | None = field(default=None, kw_only=True)
