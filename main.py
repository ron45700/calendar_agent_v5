from datetime import datetime

from src.config.settings import TIMEZONE
from src.interpretation.parser import build_event_prompt, response_to_event
from src.models.event import Event
from src.services.fake_client import send_fake_msg
from src.services.openai_client import send_prompt
from src.services.send_msg_model import send_message


def main() -> None:

    current_time = datetime.now(tz=TIMEZONE)

    msg, schema = build_event_prompt(
        raw_text=f"gym time , start at {current_time} and time that you got and its end one and half hour after (for you to know the time its end for 'end' field you need to fill) ",
        now=current_time,
        timezone=TIMEZONE,
    )

    # -------- for real model --------
    response = send_message(send_prompt, msg, schema)
    print(response)
    print()

    event = response_to_event(response)
    if isinstance(event, Event):
        print(f"the event is: {event}")
        print()
    else:
        print(f"the calrification request is: {event}")

        # -------- for fake model --------
    fake_response = send_message(send_fake_msg, msg, schema)
    print(response_to_event(fake_response))

    # -------- for real model , need clarification from user --------
    print()
    print("trying to get request_clarification")
    msg1, schema1 = build_event_prompt(
        "gym time , start at tomrrow and time that you got and its end one and half hour after (for you to know the time its end for 'end' field you need to fill)",
        current_time,
        TIMEZONE,
    )
    response = send_message(send_prompt, msg1, schema1)

    event = response_to_event(response)
    if isinstance(event, Event):
        print(f"the event is: {event}")
        print()
    else:
        print(f"the calrification request is: {event}")


if __name__ == "__main__":
    main()
