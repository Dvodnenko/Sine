from ...domain import Group, EntityRepository, Config, UseCaseResponse


class GroupService:
    def __init__(
            self, 
            repository: EntityRepository, 
            config: Config
    ):
        self.repository = repository
        self.config = config

    def create(self, group: Group) -> None:
        if self.repository.get(group.title):
            return UseCaseResponse(f"Group already exists: {group.title}", status_code=5)
        if not self.repository.get(group.title.parent):
            return UseCaseResponse(f"Group '{group.title.parent}' does not exist", status_code=4)
        self.repository.save(group)
        return UseCaseResponse(f"Group created: {group.title}")
        
    