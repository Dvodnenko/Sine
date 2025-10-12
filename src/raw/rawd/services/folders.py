from ..entities import Response
from ..repositories.folder import saFolderRepository
from ..database.mappings.folder import Folder
from ..database.session import Session


class FolderService:
    def __init__(self):
        self.repository = saFolderRepository(Session())

    def create(self, folder: Folder) -> Response:
        if self.repository.get(folder.title):
            return Response(f"Folder already exists: {folder.title}")
        if not folder.parentstr == "":
            if not self.repository.get(folder.parent):
                return Response(f"Folder not found: {folder.parent}")
        self.repository.create(folder)
        return Response(f"Folder created: {folder.title}")
    
    def get(self, title: str) -> Folder | None:
        return self.repository.get(title)
        
    def update(self, title: str, new: Folder):
        if not self.repository.get(title):
            return Response(f"Folder not found: {title}")
        if self.repository.get(new.title):
            return Response(f"Folder already exists: {new.title}")
        self.repository.update(title, new)
        return Response(f"Folder updated: {title}")

    def delete(self, title: str, force: bool = False):
        folder = self.repository.get(title)
        if not folder:
            return Response(f"Folder not found: {title}")
        if folder.children:
            if force:
                self.repository.delete(folder)
            else:
                return Response(
                    f"Cannot delete Folder '{title}' because it is not empty")
        return Response(f"Folder deleted: {title}")
