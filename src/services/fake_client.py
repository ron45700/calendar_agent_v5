def send_fake_msg(prompt: str, schema: dict) -> str:
    return (
        ""
        '{"status":"ok","clarification_question":null,'
        '"event":{'
        '"summary":"gym time",'
        '"location":null,'
        '"start":{"dateTime":"2026-06-09T12:00:00+03:00","timeZone":"Asia/Jerusalem"},'
        '"end":{"dateTime":"2026-06-09T13:30:00+03:00","timeZone":"Asia/Jerusalem"}}}'
    )
