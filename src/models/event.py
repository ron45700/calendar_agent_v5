from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Event:
    title: str
    start_date: datetime
    end_date: datetime
    duration: timedelta
    location: str | None = None

