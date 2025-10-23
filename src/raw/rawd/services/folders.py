from .base import BaseService
from ..repositories.folder import saFolderRepository
from ..entities import Folder, Entity
from ..database.session import Session
from ..database.funcs import get_all_by_titles
from ..decorators import provide_conf


class FolderService(BaseService):
    def __init__(self):
        self.repository = saFolderRepository(Session())

    def cast_kwargs(self, **kwargs):
        _tcm = {
            "color": lambda x: int(x),
            "links": lambda x: get_all_by_titles(Entity, x.split(",")),
        }
        keys = set(_tcm.keys()).intersection(kwargs.keys())
        for key in keys:
            kwargs[key] = _tcm[key](kwargs[key])
        return kwargs

    def create(self, args: list, flags: list, **kwargs) -> tuple[str, int]:
        folder = Folder(**self.cast_kwargs(**kwargs))
        if self.repository.get(folder.title):
            return f"Folder already exists: {folder.title}", 1
        if folder.parentstr != "":
            if not self.repository.get(folder.parentstr):
                return f"Folder not found: {folder.parentstr}", 1
        self.repository.create(folder)
        return f"Folder created: {folder.title}", 0
    
    @provide_conf
    def all(self, args: list, flags: list, **kwargs):
        sortby = kwargs.get("sortby", "title")
        folders = self.repository.get_all()
        folders = sorted(
            folders,
            key=lambda f: getattr(f, sortby),
            reverse="r" in flags
        )
        pattern: str = kwargs["__cnf"]["formats"]["folder"]
        if "t" in flags:
            return "".join(f"{f.title}\n" for f in folders)[:-1], 0
        return "".join([f"{pattern.format(
            **f.to_dict())}" for f in folders]).rstrip(), 0
    
    @provide_conf
    def print(self, args: list, flags: list, **kwargs):
        folders = get_all_by_titles(self.repository.session, Folder, args)
        pattern: str = kwargs["__cnf"]["formats"]["folder"]
        return "".join([f"{pattern.format(
            **f.to_dict())}" for f in folders]).rstrip(), 0
        
    def update(self, args: list, flags: list, **kwargs):
        kwargs = self.cast_kwargs(**kwargs)
        current = self.repository.get(args[0])
        if not current:
            return f"Folder not found: {args[0]}", 1
        self.repository.update(args[0], **kwargs)
        return f"Folder updated: {args[0]}", 0

    def delete(self, args: list, flags: list, **kwargs):
        folder = self.repository.get(args[0])
        delete = False
        if not folder:
            return f"Folder not found: {args[0]}", 1
        if folder.children:
            if "F" in flags:
                delete = True
        else: delete = True
        if delete:
            self.repository.delete(folder)
            return f"Folder deleted: {args[0]}", 0
        else:
            return (f"cannot delete Folder '{args[0]}' because it is not empty"), 1
