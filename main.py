from src.interpretation.parser import create_eventResult 
from src.config import settings

def run():
   
     title = "Gym time"
     first_date = "30/08/2026 15:00"
     second_date = "31/08/2025"
     print(create_eventResult(title, first_date))
     print()
     print(create_eventResult(title, second_date))
    

if __name__ == "__main__":
    run()