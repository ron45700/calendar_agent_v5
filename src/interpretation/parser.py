
def convert_str_to_list(sentence:str) -> list:
    words_list = sentence.split()
    return words_list

def convert_list_to_dict(somelist:list) -> dict:
    d= {}
    for index , word in enumerate(somelist):
        d[word.lower()] = index
    return d

def check_set_in_string (key_list:set , somelist:list) -> dict:
    d = {}
    for k in key_list :
            if k in somelist: 
              d[k] = True
            else:
              d[k] = False
    return d

def convert_list_to_set(somelist:list) -> set:
    s = {word for word in somelist}
    return s



def main() -> None:

    sentence = "Hello my name is ron "
    key_set = {"with" , "at" , "tomorrow" , "name"}


    sent_list = convert_str_to_list(sentence)
    print(f"the list is: {sent_list}")

    sent_dict = convert_list_to_dict(sent_list)
    print(f"the dict is: {sent_dict}")

    checker = check_set_in_string(key_set , sent_list)
    print(checker)

    check_set = convert_list_to_set(sent_list)
    print(f"the set is: {check_set}")


if __name__ == "__main__" :  
    main()  


