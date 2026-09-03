import requests
import json
import os
from dotenv import load_dotenv

from src.models.event import Event , event_to_dict
from src.interpretation.parser import create_eventResult
from src.config.settings import MODEL


def build_prompt(event:dict ,prompt:str ) -> str:
        full_message = {
            "prompt": prompt,
            "event": event
        }
        if  isinstance(event, Event):
            raise TypeError(f"event does not match dict type, the tpye is: {type(event)}")
        return json.dumps(full_message)


def send_prompt(prompt:str) -> str:
        load_dotenv()
        api_key = os.environ["OPENAI_KEY"]

        response = requests.post(
        url = "https://api.openai.com/v1/chat/completions",
        headers = {"Authorization": f"bearer {api_key}"},
        json = {
            "model": MODEL ,
            "messages": [
        {"role": "user", "content": prompt}
    ]})
        
        print(response.raise_for_status())
        return response.json()
    



def main():

    
    title = "Gym time"
    first_date = "30/08/2026 15:00"
    prompt_message = "Imagain you are a calendar agent that help users to set events in there's google calendar. You will get an example of title and date for some event , please answer in some form what the event name is , the time its start and the time its end."
    
    create_event = create_eventResult(title, first_date)
    print (create_event)
    if create_event.success:
        event = event_to_dict(create_event.event)
        try:
            prompt = build_prompt(event=event, prompt=prompt_message)
        except TypeError as e:
            print(f"Failed to build prompt: {e}")
        else:
            response = send_prompt(prompt=prompt)
            print(f"the response is: {response}")
    else:
         print(f"Faild to create new event: {create_event.error_message}")



if __name__ == "__main__":
    main()


