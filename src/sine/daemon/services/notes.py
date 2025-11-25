from ..repositories.note import saNoteRepository
from ..repositories.folder import saFolderRepository
from ..entities import Note
from ..database.funcs import get_all_by_titles, filter
from .decorators import cast_kwargs
from .base import Service
from ...common import load_config, parse_afk, drill, CONFIG_GLOBALS
from ...common.constants import DEFAULT_FMT
from ..funcs import asexc


PARSER = parse_afk
class NoteService(Service):
    def __init__(self, repository: saNoteRepository):
        self.repository = repository
        self.folders_repository = saFolderRepository(repository.session)

    def execute(self, argv):
        if not hasattr(self, argv[0]):
            yield f"Command not found: {argv}", 1
            return
        try:
            if len(argv) > 1:
                args, flags, kwargs = PARSER(argv[1:])
            else:
                args, flags, kwargs = PARSER([])
            gen = getattr(self, argv[0])(args=args, flags=flags, **kwargs)
            yield from gen
        except Exception as e:
            yield asexc(e), 1

    @cast_kwargs(Note)
    def create(self, args: list, flags: list, **kwargs):
        note = Note(**kwargs)
        if next(self.repository.get(note.title)):
            yield f"Note already exists: {note.title}", 1
            return
        next(self.repository.create(note))
        yield f"Note created: {note.title}", 0
    
    def all(self, args: list, flags: list, **kwargs):
        sortby = kwargs.pop("sortby", "title")
        if "t" in flags:
            for note in self.repository.get_all(sortby):
                yield note.title, 0
        else:
            config = load_config()
            fmt = kwargs.get("fmt", "0")
            pattern: str = drill(
                config, ["output", "notes", "formats", fmt], default=DEFAULT_FMT)
            for note in self.repository.get_all(sortby):
                yield eval(f"f'{pattern}'", globals={**CONFIG_GLOBALS, "e": note}), 0

    def filter(self, args: list, flags: list, **kwargs):
        sortby = kwargs.pop("sortby", "title")
        fmt = kwargs.pop("fmt", "0")
        if "t" in flags:
            for note in filter(self.repository.session, Note, kwargs, sortby):
                yield note.title, 0
        else:
            config = load_config()
            pattern: str = drill(
                config, ["output", "notes", "formats", fmt], default=DEFAULT_FMT)
            for note in filter(self.repository.session, Note, kwargs, sortby):
                yield eval(f"f'{pattern}'", globals={**CONFIG_GLOBALS, "e": note}), 0
    
    def print(self, args: list, flags: list, **kwargs):
        config = load_config()
        fmt = kwargs.pop("fmt", "0")
        pattern: str = drill(
            config, ["output", "notes", "formats", fmt], default=DEFAULT_FMT)
        for note in get_all_by_titles(self.repository.session, Note, args):
            yield eval(f"f'{pattern}'", globals={**CONFIG_GLOBALS, "e": note}), 0
    
    @cast_kwargs(Note)
    def update(self, args: list, flags: list, **kwargs):
        current = next(self.repository.get(args[0]))
        if not current:
            yield f"Note not found: {args[0]}", 1
            return
        next(self.repository.update(args[0], **kwargs))
        yield f"Note updated: {args[0]}", 0

    def delete(self, args: list, flags: list, **kwargs):
        note = next(self.repository.get(args[0]))
        if not note:
            yield f"Note not found: {args[0]}", 1
            return
        next(self.repository.delete(note))
        yield f"Note deleted: {args[0]}", 0
