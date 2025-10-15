from dataclasses import dataclass, field

from .enums import Color


@dataclass(eq=False)
class Entity:

    title: str # /a/b/b, not just c
    color: Color = Color.WHITE
    icon: str = ""

    refs: list["Entity"] = field(
        default_factory=lambda: [])
    parent_id: int = None
    parent: "Entity" = None
    children: list["Entity"] = field(
        default_factory=lambda: [])

    def __post_init__(self):
        if not self.title.startswith("/"):
            self.title = f"/{self.title}"

    @property
    def parentstr(self) -> str:
        return self.title[0:self.title.rfind("/")]

    @property
    def name(self) -> str:
        return self.title[self.title.rfind("/")+1 :]
