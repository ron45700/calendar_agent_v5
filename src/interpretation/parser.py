from dataclasses import dataclass
from datetime import datetime, timedelta

from src.models.event import Event
from src.config.settings import DEFAULT_DURATION_MINUTES


@dataclass
class ParseResult:
    success: bool
    event: "Event | None" = None
    error_message: str | None = None


def str_to_datetime(date: str) -> datetime:
    return datetime.strptime(date, "%d/%m/%Y %H:%M")


def create_eventResult(title: str, date: str) -> ParseResult:
    try:
        parse_start_date = str_to_datetime(date)
        gap = timedelta(minutes=DEFAULT_DURATION_MINUTES)
        parse_end_date = parse_start_date + gap
        new_event = Event(title, parse_start_date, parse_end_date, gap)
        return ParseResult(success=True, event=new_event)

    except ValueError as e:
        return ParseResult(
            success=False,
            event=None,
            error_message=f"Conversion str to datetime failed: {e}",
        )


def main() -> None:

    title = "Gym time"
    first_date = "30/08/2026 15:00"
    second_date = "31/08/2025"

    print(create_eventResult(title, first_date))
    print()
    print(create_eventResult(title, second_date))


if __name__ == "__main__":
    main()
