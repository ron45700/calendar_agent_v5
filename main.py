from datetime import datetime, timedelta

from src.config.settings import DEFAULT_DURATION_MINUTES, TIMEZONE
from src.models.event import Event


def main()->None:

    start_date = datetime(2026 , 6 , 9, 12 , tzinfo=TIMEZONE)
    duration = timedelta(minutes=DEFAULT_DURATION_MINUTES)
    end_date = start_date + duration
    print(Event(summary="test" , start=start_date , end=end_date))

if __name__ == "__main__" :
    main()

