from collections.abc import Callable

Model = Callable[[str, dict], str]


def send_message(model: Model, prompt: str, schema: dict) -> str:
    return model(prompt, schema)
