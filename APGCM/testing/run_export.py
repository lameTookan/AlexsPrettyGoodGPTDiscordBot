import chat_wrapper
from  templates.cw_factory import ChatFactory
import settings 
import exceptions
import func 
import file_handlers 
from log_config import BaseLogger, DEFAULT_LOGGING_LEVEL

logger = BaseLogger(__file__, filename="run_export.log", level=DEFAULT_LOGGING_LEVEL,  identifier="InTesting")
logger.info("Making ChatFactory instance")
factory = ChatFactory()
logger.info("Making ChatWrapper instance")
wrap = factory.get_chat()
logger.info("ChatWrapper instance made")
wrap.system_prompt = "The application your model is using to communicate called Alex's Pretty Good Chatbot Module. Alex is currently doing some integrated testing, to ensure that everything is working okay. Your model is ||model|| . Today's date is ||date|| . The time is ||time||. Your training data was last updated ||cut_off|| "
def save_menu(chat_wrapper_obj: chat_wrapper.ChatWrapper):
    save_handler = file_handlers.SaveFileHandler(chat_wrapper_obj=chat_wrapper_obj)
    files = save_handler.get_current_files()
    print("Current files:")
    print(files)
    while True:
        print("Enter a filename to save to, or enter 'q' to go exit, or enter 'ls' to list the current files")
        ans = input(">>")
        ans_lower = ans.lower()
        if ans_lower == "q":
            return None 
        elif ans_lower == "ls":
            print("Current files:")
            print(files)
        else:
            if not save_handler.check_if_file_exists(ans):
                save_handler.save(filename=ans)
                print("Saved to file: " + ans)
                print("Exiting...")
                return None
            else:
               if func.confirm(f"File {ans} already exists would you like to overwrite it?"):
                     save_handler.save(filename=ans, overwrite=True)
                     print("Saved to file: " + ans)
                     print("Exiting...")
                     return None
               else:
                    print("Try entering a different filename")
                    continue 
                
def load_menu(chat_wrapper: chat_wrapper.ChatWrapper):
    save_handler = file_handlers.SaveFileHandler(chat_wrapper_obj=chat_wrapper)
    files = save_handler.get_current_files()
    print("Current files:")
    print(files)
    while True:
        print("Enter a filename to load from, or enter 'q' to go exit, or enter 'ls' to list the current files")
        ans = input(">>")
        ans_lower = ans.lower()
        if ans_lower == "q":
            return chat_wrapper 
        elif ans_lower == "ls":
            print("Current files:")
            print(files)
        else:
            if save_handler.check_if_file_exists(ans):
                chat_wrapper = save_handler.load(filename=ans)
                print("Loaded from file: " + ans)
                print(chat_wrapper)
                print("Exiting...")
                return chat_wrapper
            else:
                print("Try entering a different filename")
                continue    
def export_menu(chat_wrapper: chat_wrapper.ChatWrapper):
    logger.info("Making ChatExporter instance")
    exporter = file_handlers.ChatExporter(chat_wrapper_obj=chat_wrapper)
    files ="\n".join( exporter.get_current_files())
    print("Current files:")
    print(files)
    while True:
        print('Enter a filename to export to, or enter "q" to go exit, or enter "ls" to list the current files')
        ans = input(">>")
        ans_lower = ans.lower().strip()
        if ans_lower == "q":
            print('Exiting...')
        elif ans_lower == "ls":
            print("Current files:")
            print(files)
        else:
            if not exporter.check_if_file_exists(ans):
                exporter.save(filename=ans)
                print("Exported to file: " + ans)
                print("Exiting...")
                return None
            else:
               if func.confirm(f"File {ans} already exists would you like to overwrite it?"):
                     exporter.export(filename=ans, overwrite=True)
                     print("Exported to file: " + ans)
                     print("Exiting...")
                     return None
               else:
                    print("Try entering a different filename")
                    continue
    

while True:
    ans = func.chunk_input()
    ans_lower = ans.lower().strip()
    if ans_lower == "exit":
        break
    elif ans_lower == "toggle_chunk":
        func.chunk_input.toggle_chunking()
    elif ans_lower == "save":
       save_menu(wrap)
    elif ans_lower == "load":
        wrap = load_menu(wrap)
    elif ans_lower == "debug":
        print(repr(wrap))
    elif ans_lower == "export":
        export_menu(wrap)
    elif ans_lower == "" or  ans_lower == " ":
        print("No input detected")
        continue    
    else:
        print(wrap.chat(ans))
       