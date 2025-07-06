from datetime import datetime

from .time import TotalWorkTime


class Session:
    def __init__(
            self, 
            tags: list[str], 
            start_datetime: datetime, 
            end_datetime: datetime, 
            breaks: int
    ):
        self.tags = tags
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.breaks = breaks

    @property
    def total(self):
        diff = (self.end_datetime - self.start_datetime).seconds - self.breaks

        hours = diff // 3600
        diff -= hours*3600
        minutes = diff // 60
        diff -= minutes * 60
        seconds = diff

        return TotalWorkTime(hours=hours, minutes=minutes, seconds=seconds)
    