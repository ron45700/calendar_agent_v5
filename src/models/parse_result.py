from dataclasses import dataclass

from src.models.event import Event
from src.models.status import Status


@dataclass
class ParseResult:
    status: Status
    event: Event | None = None
    exception: ValueError | str | None = None
    need_clarification: str | None = None
