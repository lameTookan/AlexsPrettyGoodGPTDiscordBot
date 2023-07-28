from func import InputHandler, confirm
import chat_wrapper
from templates.cw_factory import ChatFactory
from handler.save_handler import JsonSaveHandler
from handler.stream_handler import StdoutStreamHandler

from settings import settings_bag
input_handler = InputHandler()
stream_handler = StdoutStreamHandler()
json_handler = JsonSaveHandler()
factory = ChatFactory()
cw = factory.get_chat()
cw.trim_object.add_chatlog(None)
#cw.add_save_handler(json_handler)
#cw.add_stream_handler(stream_handler)

def get_answer( message: str = "What would you like to choose?", prompt: str = "> ", confirm_message: str = "Are you sure this is what you would like to save?") -> str:
    print(message)
    while True: 
        ans = input(prompt)
        print(confirm_message  )
        print(ans)
        confirm_ans = input("Y/N: ")
        if confirm_ans.lower().strip() == "y":
            return ans
        else:
            print("Please try again")
            continue 
        
        
while True: 
    ans: str  = input_handler()
    ans_lower = ans.lower().strip()
    if ans_lower == "save":
        filename = get_answer(message="What would you like to name the file?", prompt="> ", confirm_message="Are you sure this is what you would like to save?")
        cw.save(filename, overwrite=True)
    elif ans_lower == "load":
        print("Please choose from the following files:")
        print(cw.all_entry_names)
        while True:
            filename = input("> ")
            if not cw.check_entry_name(filename):
                print("Please try again")
                continue
            elif ans_lower == "quit":
                break
            else:
                cw.load(filename)
                break
    elif ans_lower == "quit":
        break 
    elif ans_lower == "debug":
        print(cw.debug())
    else:
        print(cw.chat(ans))