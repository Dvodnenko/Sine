import pickle
from datetime import datetime
from pathlib import Path

from .session import Session


class ActiveSession:
    def __init__(
            self, 
            tags: list[str], 
            start_datetime: datetime,
            breaks: int
    ):
        self.tags = tags
        self.start_datetime = start_datetime
        self.breaks = breaks
    @staticmethod
    def _begin(tags: list, path: Path): # !underhood method!
        active_session = ActiveSession(tags, datetime.now(), 0)
        with open(path, 'wb') as file:
            pickle.dump(active_session, file)
        return active_session
    @staticmethod
    def _finish(path: Path): # !underhood method!
        with open(path, 'rb') as file:
            active_session: ActiveSession = pickle.load(file)
        with open(path, 'wb') as file:
            pickle.dump(None, file)
        return Session(
            active_session.tags, 
            active_session.start_datetime, 
            datetime.now(),
            active_session.breaks
        )
