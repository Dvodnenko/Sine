import shutil
from pathlib import Path
from typing import Generator, Any

from ...domain import Group, EntityRepository, Config, UseCaseResponse


class GroupService:
    def __init__(self, repo: EntityRepository, config: Config):
        self.repo = repo
        self.config = config

    def meets_condition(self, subpath: str, condition: tuple[str]) -> UseCaseResponse:
        _path = self.config.core.rootgroup / subpath
        OPERATOR_MAP = {
            "=": "__eq__",
            "!=": "__ne__",
            ">": "__gt__",
            "<": "__lt__",
            ">=": "__ge__",
            "<=": "__le__",
            "c": "__contains__",
            "in": "__contains__",
        }
        TYPES_MAP = {
            "str": str,
            "int": int,
        }
        if not _path.exists() or not _path.is_dir():
            return UseCaseResponse(
                message=f"Group not found: {subpath}", status_code=4
            )
        key, oper, value = condition
        group = self.repo.load(_path)
        is_method = callable(group.getattr(key))
        if not OPERATOR_MAP.get(oper):
            exit(4)
        try:
            if is_method:
                key = group.getattr(key)()
            else:
                key = group.getattr(key)
            method = key.__getattribute__(OPERATOR_MAP.get(oper))
        except AttributeError as error:
            return UseCaseResponse(message=error, status_code=4)
        answer = method(TYPES_MAP.get(key.__class__.__name__)(value))
        return UseCaseResponse(message=answer)
        
    
    def yield_all(self) -> Generator[str, Any, None]:
        rg = self.config.core.rootgroup
        for group in rg.rglob("*"):
            if group.is_dir():
                yield str(group.relative_to(rg))

    def create(self, group: Group) -> UseCaseResponse[Group]:
        _path = self.config.core.rootgroup / group.subpath
        if _path.exists():
            return UseCaseResponse(
                status_code=3,
                message=f"Group already exists: {group.subpath}", 
            )
        _path.mkdir(parents=False)
        (_path / f".self").touch()
        self.repo.dump(_path/ f".self", group)
        return UseCaseResponse(
            message=f"Group created: {group.subpath}"
        )
    
    def update(self, group: str, new: Group) -> UseCaseResponse[Group]:
        _path = self.config.core.rootgroup / group
        if not _path.exists() or not _path.is_dir():
            return UseCaseResponse(
                message=f"Group not found: {group}", status_code=4
            )
        if group != str(new.subpath):
            self.repo.mv(
                _path, 
                self.config.core.rootgroup / new.subpath, 
                rootgroup=self.config.core.rootgroup
            )
        self.repo.dump(self.config.core.rootgroup / new.subpath / ".self", new)
        return UseCaseResponse(
            message=f"Group updated: {group}"
        )
    
    def delete(self, subpath: str) -> UseCaseResponse[Group]:
        _path = self.config.core.rootgroup / subpath
        if not _path.exists() or not _path.is_dir():
            return UseCaseResponse(
                message=f"Group not found: {subpath}", status_code=4
            )
        shutil.rmtree(_path)
        return UseCaseResponse(
            message=f"Group deleted: {subpath}"
        )
