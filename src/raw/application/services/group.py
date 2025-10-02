import shutil

from ...domain import Group, EntityRepository, Config, UseCaseResponse


class GroupService:
    def __init__(self, repo: EntityRepository, config: Config):
        self.repo = repo
        self.config = config

    def create(self, group: Group) -> UseCaseResponse[Group]:
        _path = self.config.core.rootgroup / group.subpath
        if _path.exists():
            return UseCaseResponse(
                status_code=3,
                message=f"Group already exists: {group.subpath}", 
            )
        _path.mkdir(parents=False)
        (_path / f".self.{self.repo.ext}").touch()
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
