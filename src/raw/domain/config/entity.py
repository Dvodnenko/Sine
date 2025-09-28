from dataclasses import dataclass
from pathlib import Path


@dataclass(kw_only=True)
class CoreSettings:
    rootgroup: Path

@dataclass(kw_only=True)
class Config:
    core: CoreSettings
