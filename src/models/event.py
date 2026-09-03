from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Event:
    title: str
    start_date: datetime
    end_date: datetime
    duration: timedelta
    location: str | None = None


def event_to_dict (event: "Event") ->dict:
    try:
        dict_event = {
            "title": event.title,
            "start_date": event.start_date.strftime("%Y-%m-%d %H:%M"),
            "end_date": event.end_date.strftime("%Y-%m-%d %H:%M"),
            "duration": str(event.duration),
            "location": event.location
        }
        return dict_event
    except TypeError as e:
        print(f"faild to convert dict: {e}")
    