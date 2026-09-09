import json
from datetime import datetime
from zoneinfo import ZoneInfo

from src.interpretation.prompts.create_event_prompt import EVENT_INSTRUCTIONS
from src.models.event import Event
from src.models.status import Status


def build_event_prompt(
    raw_text: str, now: datetime, timezone: ZoneInfo
) -> tuple[str, dict]:
    filled_instructions = EVENT_INSTRUCTIONS.format(
        now=now.isoformat(), timezone=timezone
    )
    prompt_text = f"{filled_instructions}\n\nUser message: {raw_text}"
    event_response_schema = {
        "type": "json_schema",
        "json_schema": {
            "name": "create_event",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "status": {"type": "string", "enum": [s.value for s in Status]},
                    "clarification_question": {"type": ["string", "null"]},
                    "event": {
                        "anyOf": [
                            {
                                "type": "object",
                                "properties": {
                                    "summary": {"type": "string"},
                                    "location": {"type": ["string", "null"]},
                                    "start": {
                                        "type": "object",
                                        "properties": {
                                            "dateTime": {"type": "string"},
                                            "timeZone": {"type": "string"},
                                        },
                                        "required": ["dateTime", "timeZone"],
                                        "additionalProperties": False,
                                    },
                                    "end": {
                                        "type": "object",
                                        "properties": {
                                            "dateTime": {"type": "string"},
                                            "timeZone": {"type": "string"},
                                        },
                                        "required": ["dateTime", "timeZone"],
                                        "additionalProperties": False,
                                    },
                                },
                                "required": ["summary", "location", "start", "end"],
                                "additionalProperties": False,
                            },
                            {"type": "null"},
                        ]
                    },
                },
                "required": ["status", "clarification_question", "event"],
                "additionalProperties": False,
            },
        },
    }
    return prompt_text, event_response_schema


def response_to_event(response: str) -> Event | str:
    content = json.loads(response)
    if Status(content.get("status")) == Status.OK:
        event_fields = content["event"]
        return Event(
            summary=event_fields["summary"],
            start=datetime.fromisoformat(event_fields["start"]["dateTime"]),
            end=datetime.fromisoformat(event_fields["end"]["dateTime"]),
            location=event_fields["location"],
        )
    else:
        return content["clarification_question"]
