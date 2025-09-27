from pathlib import Path

from ...domain import Group, FileRepository, Config, UseCaseResponse


class GroupService:
    def __init__(self, repo: FileRepository, config: Config):
        self.repo = repo
        self.config = config

    def create(self, group: Group) -> UseCaseResponse[Group]:
        _path = self.config.core.raw_path / group.group / f"{group.title}"
        self.repo.load(_path)
        if _path.exists():
            return UseCaseResponse(
                status_code=3,
                message=f"Group already exists: {group.group}/{group.title}", 
            )
        _path.mkdir(parents=True)
        self.repo.save(group)
        return UseCaseResponse(
            message=f"Group created: {group.group}/{group.title}"
        )
    
    def update(self, group: str, new: Group) -> UseCaseResponse[Group]:
        _path = self.config.core.raw_path / group
        if not _path.exists() or not _path.is_dir():
            return UseCaseResponse(
                message=f"Group not found: {group}", status_code=4
            )
        self.repo.save(new)
        return UseCaseResponse(
            message=f"Group updated: {group}"
        )
    
    def delete(self, group: str) -> UseCaseResponse[Group]:
        _path = self.config.core.raw_path / group
        if not _path.exists() or not _path.is_dir():
            return UseCaseResponse(
                message=f"Group not found: {group}", status_code=4
            )
        _path.rmdir()
        return UseCaseResponse(
            message=f"Group deleted: {group}"
        )
