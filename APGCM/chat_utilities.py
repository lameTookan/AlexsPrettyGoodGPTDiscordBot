from templates.cw_factory import ChatFactory
from chat_wrapper import ChatWrapper
from file_handlers.export_context_manager import ExportContextManager
import func as f 

def quick_make_chat_wrapper():
    """This will make a chat wrapper with the defaults you have set in your .env file. Useful for testing and if you don't want to use any of the customization options in the ChatFactory class."""
    
    fact = ChatFactory()
    return fact.get_chat()

def print_test_ai_response(cw: ChatWrapper, message: str = "You are currently being testing. Just respond with 'All systems are go!' to confirm you are working " ) -> str:
    """This will print a test response from the AI to the console. Useful for testing and debugging.
    Also includes my cute little loading spinner, so you can see that something is happening and the program hasn't frozen.
    Keep in mind, if you are using my StdoutStreamHandler class, this may look a little wonky because the loading spinner will be printed to the console as well.
    
    """
   
    loading_spinner = f.LoadingSpinner()
    with loading_spinner as spin:
        response = cw.chat(message)
        spin.stop()
        print(response)

def get_test_ai_response(cw: ChatWrapper, message: str = "You are currently being testing. Just respond with 'All systems are go!' to confirm you are working " ) -> str:
    """
    Just returns the response from the AI. Useful for testing and debugging.
    If you are using my StdoutStreamHandler class, you will also see the response in the console as it comes in.
    If you want something a little more fancy, use print_test_ai_response instead.
    """
    return cw.chat(message)
   
def quick_and_dirty_chatloop(cw: ChatWrapper, spinner: bool = True) -> None:
    """A quick and dirty chatloop. Useful for testing and debugging.
    Includes a optional loading spinner, so you can see that something is happening and the program hasn't frozen.
    Has a debug command, which will print the chat wrapper's debug information to the console(a bunch of useful information about the chat wrapper's state)
    """
    while True:
        ans = input(">>> ")
        if ans.lower().strip() == "debug":
             print(cw.debug())
        elif ans.lower().strip() in ("exit", "quit", "q"):
            break
        else:
            if spinner:
                loading_spinner = f.LoadingSpinner()
                with loading_spinner as spin:
                    response = cw.chat(ans)
                    spin.stop()
                    print(response)
            
            else:
                print(cw.chat(ans))
                
def auto_get_exporter(cw: ChatWrapper) -> ExportContextManager:
    """
    Extracts the data from the chat wrapper and returns an ExportContextManager object. Faster than doing this yourself, while not making ExportContextManager rely on the chat wrapper.
    :param cw: The chat wrapper to extract the data from.
    returns: An ExportContextManager object.
    """
    data = cw.trim_object.get_raw_history_for_export()
    system_prompt = cw.trim_object.raw_system_prompt
    model = cw.model
    extra_data = {
        "Reminder Value ":  cw.reminder, 
        
        
    }
    if cw.template is not None:
        # template formats are standardized and verified, so we will never have a template without a name key
        extra_data["Template"] = cw.template['name']
    return ExportContextManager(data=data, model=model, system_prompt=system_prompt, **extra_data)

if __name__ == "__main__":
    cw = quick_make_chat_wrapper()
    quick_and_dirty_chatloop(cw)