from collections.abc import Callable

Model = Callable[[str],dict]

def send_message(model: Model , prompt: str ) -> dict:
    return model(prompt)