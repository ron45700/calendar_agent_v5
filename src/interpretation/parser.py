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
    try:
        # try to convert JSON object to python data structure
        content = json.loads(response)
    except json.JSONDecodeError as e:
        # status turn to FAILED , error raised at decoding rsponse
        return ParseResult(
            status=Status.FAILED, exception=f"response is not JSON object: {e}"
        )
    stat = content.get("status")
    try:
        # try to convert the status str from response to Status object
        stat_obj = Status(stat)
        if stat_obj == Status.OK:
            try:
                # try to get the event fields from the response
                event_fields = content["event"]
                try:
                    # try to converte dates to datetime objects
                    start_date = datetime.fromisoformat(
                        event_fields["start"]["dateTime"]
                    )
                    end_date = datetime.fromisoformat(event_fields["end"]["dateTime"])
                    if start_date.tzinfo is not None and end_date.tzinfo is not None:
                        if start_date < end_date:
                            new_event = Event(
                                summary=event_fields["summary"],
                                start=start_date,
                                end=end_date,
                                location=event_fields["location"],
                            )
                            # status OK , event filled
                            return ParseResult(status=stat_obj, event=new_event)
                        else:
                            # status OK turn to FAILED , dates range are mismatch
                            return ParseResult(
                                status=Status.FAILED,
                                exception=f"mismatch dates range (end date comes before start date). start_date:{start_date} , end_date:{end_date}",
                            )
                    else:
                        # status OK turn to FAILED , one of the dates are naive
                        return ParseResult(
                            status=Status.FAILED,
                            exception=f"one of the dates are naive. start:{start_date.tzinfo} , end date:{end_date.tzinfo}",
                        )
                except ValueError as e:
                    # status OK turns to FAILED , exception at creating datetime object
                    return ParseResult(
                        status=Status.FAILED,
                        exception=f"one of the dates is missing or not in the correct format. start date:{event_fields["start"]["dateTime"]} , end date{event_fields["end"]["dateTime"]} || Formal error:{e}",
                    )
            except TypeError as e:
                # status OK turn to FAILED , event is missing
                return ParseResult(
                    status=Status.FAILED,
                    exception=f"event is missing (null) or not in the correct place in dictionary: {e}",
                )

        elif stat_obj == Status.NEED_CLARIFICATION:
            clarification = content["clarification_question"]
            if clarification is None or not clarification.strip():
                # status turn to FAILED , clarification field is empty
                return ParseResult(
                    status=Status.FAILED,
                    exception="status is 'need_clarification' but the question is missing or empty",
                )
            # status NEED_CLARIFICATION , calrification filled
            return ParseResult(status=stat_obj, need_clarification=clarification)
        else:
            # status is not one of the options that set in Status class
            return ParseResult(
                status=Status.FAILED,
                exception=f"status value isnt from Status class options: {stat}",
            )
    except ValueError as e:
        # status value isnt in Status enum options
        return ParseResult(
            status=Status.FAILED,
            exception=f"status value isnt from Status class options or missing: {e}",
        )
