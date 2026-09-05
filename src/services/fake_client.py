

def send_fake_msg(prompt:str) -> dict:
     return {
        "choices": [
            {"message": {"content": "Gym time, 30/08/2026 15:00-16:00"}}
        ]
    }