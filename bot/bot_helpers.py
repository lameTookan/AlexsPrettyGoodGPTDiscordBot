import APGCM
from APGCM import exceptions
from APGCM import (ChatFactory, ChatWrapper, JsonSaveHandler, common as func)
from typing import Union, Optional, Any, Tuple, List, Callable, Iterable
def make_chat_wrapper() -> ChatWrapper:
    fact = ChatFactory()
    cw = fact.get_chat()
    cw.trim_object.add_chatlog(chatlog = None)
    cw.return_type = "string"
    save_handler = JsonSaveHandler()
    cw.add_save_handler(save_handler)
    cw.set_is_saving(True)
    cw.auto_setup_autosaving()
    # handler = DisMessageSplitStreamHandler()

    return cw


def process_save_command(cw: ChatWrapper, *args) -> tuple[bool, str]:
    """Processes the save command, and returns a tuple of (success, message)."""
    if len(args) == 0:
        return (False, "Please provide a save name!")
    if len(args) == 1:
        "Just a save name, no overwrite flag"
        if cw.check_entry_name(args[0]):
            return (False, "Save already exists!")
        cw.save(args[0])
        return (True, "Save successful!")
    if len(args) >= 2:
        overwrite = str_to_bool(args[1])
        if not overwrite and cw.check_entry_name(args[0]):
            return (False, "Save already exists!")
        else:
            cw.save(args[0], overwrite=True)
            return (True, "Save successful!")


def get_chat_history(cw: ChatWrapper) -> list[str]:
    """Gets the chat history from the chat wrapper, and returns it as a list of strings."""
    
    history = cw.trim_object.get_messages_as_list(
        reverse=False, format=cw.trim_object.message_return_types.STRING
    )
    return history




def check_cw(cw: ChatWrapper) -> None:
    """Prints the chat wrapper's debug information to the console and attempts to chat with it.
    Requires a ChatWrapper object as a parameter, and a loading spinner object from APGCM.func.
    """
    print(cw.debug())
    print("Loading example response...")
    loading_spinner = func.LoadingSpinner()
    with loading_spinner as s:
        response = cw.chat(
            "Testing you! Just respond with something like 'All systems are go!'"
        )
        s.stop()
        print(response)


def str_to_bool(s: str) -> bool:
    s = s.lower().strip()
    if s in ("true", "t", "yes", "y", "1", "on"):
        return True
    else:
        return False


def split_response(response: str, max_len: int = 1990) -> list:
    """Take a string and split it into a list of strings, each of which is no longer than 2000 characters."""
    if len(response) >= max_len:
        return [response[i : i + max_len] for i in range(0, len(response), max_len)]
    else:
        return [response, ]
HELP_INFO = "\n".join(
    [
        "Welcome to the APGCM discord bot!",
        "Formally called Alex's Maybe Kinda Decent Discord Bot",
        "Powered by the APGCM chat module!",
        "Here is a list of commands:",
        "`sys_prompt` - Sets the system prompt for the chat bot.",
        "`reminder` - Sets a reminder for the chat bot.",
        "`print_history` - Shows chat history(might be long)",
        "`get_saves`[include_autosaves=False] - Shows a list of all save names the bot has. Include autosaves by setting the optional parameter to True.",
        "`load` <save_name> - Loads the save with the given name.",
        "`save` <save_name> [overwrite=False] - Saves the chat wrapper's current state to a save with the given name. Set overwrite to True to overwrite the save if it already exists.",
        "`debug` - Prints the chat wrapper's debug information to the channel.",
        "`reset`[hard_reset=False] - Resets the chat wrapper's chat log. Set hard_reset to True to completely reset the chat wrapper, including the chat log, and deletes autosaves.",
        "`export` - Exports the chat wrapper's chat history to a markdown file.",
        "`manual_autosave` - Manually saves the chat wrapper's current state to an autosave.",
        "`default_mode` - Sets the system prompt to the default system prompt.(Balance between casual and assistant)",
        "`casual_mode` - Sets the system prompt to the casual system prompt.(More casual, less formal)",
        "`assistant_mode` - Sets the system prompt to the assistant system prompt.(More formal, less casual)",
        "`set_temp` <temperature> - Sets the temperature for the model. Can be any number with a decimal point between 0 and 2. However, values between 0 and 1 are recommended.",
        "`delete_saves` <save_names> - Deletes the saves with the given names.",
        "`delete_all_auto_saves` - Deletes all auto saves and backups.",
        "`help_mode` - Toggles help mode.",
        "`which_mode` - Shows the current mode.",
        "`auto_saving_enabled` <enabled> - Enables or disables auto saving.",
        "`change_frequency` <frequency> - Changes the auto save frequency.",
        "`home_channel` <channel_id> - Changes the bot's home channel.",
        
    ]
)
