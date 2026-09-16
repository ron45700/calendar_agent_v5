import json
from datetime import datetime
from zoneinfo import ZoneInfo

from src.interpretation.prompts.create_event_prompt import EVENT_INSTRUCTIONS
from src.models.event import Event
from src.models.parse_result import ParseResult
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
                    "status": {
                        "type": "string",
                        "enum": [
                            s.value for s in Status if s.value != Status.FAILED.value
                        ],
                    },
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


def response_to_parseresult(response: str) -> ParseResult:
    content = json.loads(response)
    stat = content.get("status")
    try:
        stat_obj = Status(stat)
        if stat_obj == Status.OK:
            event_fields = content["event"]
            try:
                start_date = datetime.fromisoformat(event_fields["start"]["dateTime"])
                end_date = datetime.fromisoformat(event_fields["end"]["dateTime"])
                if start_date < end_date:
                    new_event = Event(
                        summary=event_fields["summary"],
                        start=start_date,
                        end=end_date,
                        location=event_fields["location"],
                    )
                    # status OK , event filled
                    return ParseResult(status=stat, event=new_event)
                else:
                    # status OK turn to FAILED , dates range are mismatch
                    return ParseResult(
                        status=Status.FAILED,
                        exception=f"mismatch dates range (end date comes before start date). start_date:{start_date} , end_date:{end_date}",
                    )
            except ValueError as e:
                # status OK turns to FAILED , exception at creating datetime object
                return ParseResult(
                    status=Status.FAILED,
                    exception=f"one of the dates is missing or not in the correct format. start date:{event_fields["start"]["dateTime"]} , end date{event_fields["end"]["dateTime"]} || Formal error:{e}",
                )

        elif stat_obj == Status.NEED_CLARIFICATION:
            clarification = content["clarification_question"]
            # status NEED_CLARIFICATION , calrification filled
            return ParseResult(status=stat, need_clarification=clarification)
        else:
            return ParseResult(
                status=Status.FAILED,
                exception=f"status value isnt from Status class options: {stat}",
            )
    except ValueError as e:
        # status value isnt in Status enum options
        return ParseResult(
            status=Status.FAILED,
            exception=f"status value isnt from Status class options: {e}",
        )
