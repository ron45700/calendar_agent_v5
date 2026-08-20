from dataclasses import dataclass
from typing import Optional

@dataclass
class Event :
    title: str
    start_time: str
    duration_in_min: int
    location: Optional[str] = None


    def print_event(self) -> None:
        print(self)

    def check_equals(self , second:"Event" ) -> None:
        print(self == second)
          



def main() -> None:

    first_event = Event("Gym" , "11:30" , 60)
    first_event.print_event()

    second_event = Event("meet with friend" , "20:15" , 120 , "Home")
    second_event.print_event()

    print("does the two event are the same?")
    first_event.check_equals(second_event)


    
if __name__ == "__main__" :
    main()