from src.interpretation.parser import parse 
from src.config import settings

def run():
    while True:
        name = input("what is your full name? : ").strip()
        if name == "quit":
            break
        elif name== "":
            continue
        print(parse(name))
        time = input("write how long or default : ").strip()
        if time == "default":
            print(f"default time= {settings.DEFAULT_DURATION_MINUTES}")
        elif time.isdigit(): 
            print(time)
        else:
            print("its not a number!")


if __name__ == "__main__":
    run()