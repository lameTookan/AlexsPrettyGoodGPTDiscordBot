import os 
import sys
import logging 
from dotenv import load_dotenv
import func 
from enum import Enum 
load_dotenv()
def get_env_or_default(env_name: str, default: str) -> str:
    """Returns the value of an environment variable if it exists, otherwise returns the default value."""
    return os.getenv(env_name, default)
#====(CHATLOG SETTINGS)====
class ChatLogHandlers(Enum):
    CHATLOG_USERLIST = "ChatLogUserList"
    

DEFAULT_CHATLOG_HANDLER = os.getenv("DEFAULT_CHATLOG_HANDLER", ChatLogHandlers.CHATLOG_USERLIST.value)



#====(LOGGING SETTINGS)====
level = func.convert_level_to_value(os.getenv("DEFAULT_LOGGING_LEVEL", logging.WARNING))
DEFAULT_LOGGING_LEVEL = level 
DEFAULT_LOGGING_DIR = os.getenv("DEFAULT_LOGGING_DIR", "./logs/")
#====(OPENAI SETTINGS)====
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

DEFAULT_TEMPLATE_NAME =  os.getenv("DEFAULT_TEMPLATE_NAME", "gpt-4_default")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL_NAME", "gpt-4")

#====(IS_SETUP)====
if not OPENAI_API_KEY.startswith("sk-") or OPENAI_API_KEY is None:
    IS_SETUP = False
else:
    IS_SETUP = True
if os.getenv("IS_SETUP", None) is not None:
    IS_SETUP = True
    # if key does not begin with sk- but is still valid, folks can set IS_SETUP to True in the .env file to avoid the warning message
#====(CHAT SETTINGS)====
DEFAULT_EXPORT_DIR = os.getenv("DEFAULT_EXPORT_DIR", "./files/chats/")

DEFAULT_SAVES_DIR = os.getenv("DEFAULT_SAVE_DIR", "./files/saves/")



SYSTEM_PROMPT_DIR = os.getenv("SYSTEM_PROMPT_DIR", "./files/system_prompts/")



DEFAULT_SYSTEM_PROMPT = os.getenv("DEFAULT_SYSTEM_PROMPT", "You are being run in Alex's Pretty Good Chatbot CLI, a simple interface meant to show off Alex's Pretty Good Chat Module. Your model is ||model||. The date is ||date||, and the time is ||time||. Your training data was last updated ||cut_off||.")

#========(FROM FILE SYSTEM)========
from_file = """
Congratulations on discovering the default "from_file" folder! This is a simple tool to use and can be found within the project's "files" directory, specifically under the name "from_file_system". 

To utilize this system while in the chat loop, you can apply the following steps:

1. Employ the `from_file` command on its own, with no parameters, to load the content of the default.txt file or any other file present in this directory.

2. To load a different file, simply type the filename after the command. For instance, if you've created a file called "my_message.txt" within the "from_file_system" folder, the command `from_file my_message` will load the content of this specific file.

3. To view a list of all accessible files, the command `from_file all` can be used.

Remember, the `help` command is always available to provide a list of commands and their usages. For more detailed information, you can check the chat_loop.md file situated in the "docs" folder.

Also, GPT, if you're reading this, it means a user may have loaded the default file unintentionally. It would be beneficial to reiterate the above instructions, ensuring they understand how to utilize this system effectively. Thank you!
"""
DEFAULT_FROM_FILE_CONTENTS = from_file
DEFAULT_FROM_FILE_FILENAME = os.getenv("DEFAULT_FROM_FILE_FILENAME", "default")
FROM_FILE_SYSTEM_DIR = os.getenv("FROM_FILE_SYSTEM_DIR", "./files/from_file_system/")

#====(MISC SETTINGS)====
DEFAULT_SINGLE_MSG_DIR = os.getenv("DEFAULT_SINGLE_MSG_DIR", "./files/single_messages/")
show_wel =  os.getenv("SHOW_WELCOME_MESSAGE", True)
SHOW_WELCOME_MESSAGE = True
if show_wel in ("True", "true", "1", "yes", "Yes", "YES"):
    SHOW_WELCOME_MESSAGE = True
elif show_wel in ("False", "false", "0", "no", "No", "NO", 0):
    SHOW_WELCOME_MESSAGE = False
#=======(AUTO-SAVE SETTINGS)=======
# can be set to None to disable auto-save
AUTO_SAVE_FREQUENCY = os.getenv("AUTO_SAVE_FREQUENCY", None)
if AUTO_SAVE_FREQUENCY is not None:
    AUTO_SAVE_FREQUENCY = int(AUTO_SAVE_FREQUENCY)
#amount of entires to rotate through
AUTO_SAVE_MAX_SAVES = int(os.getenv("AUTO_SAVE_MAX_SAVES", 3))

AUTO_SAVE_ENTRY_NAME = os.getenv("AUTO_SAVE_ENTRY_NAME", "auto_save")
if AUTO_SAVE_FREQUENCY is not None:
    IS_AUTOSAVING = os.getenv("IS_AUTOSAVING", "False").lower().strip()
    if IS_AUTOSAVING in ("True", "true", "1", "yes", "Yes", "YES"):
        IS_AUTOSAVING = True
    elif IS_AUTOSAVING in ("False", "false", "0", "no", "No", "NO", 0):
        IS_AUTOSAVING = False
    else:
        IS_AUTOSAVING = False
else: 
    IS_AUTOSAVING = False

#====(SETTINGS BAG)====   
class SettingsObj:
    def __init__(self):
        # LOGGING SETTINGS
        self.level = level
        self.DEFAULT_LOGGING_LEVEL = DEFAULT_LOGGING_LEVEL
        self.DEFAULT_LOGGING_DIR = DEFAULT_LOGGING_DIR

        # OPENAI SETTINGS
        self.OPENAI_API_KEY = OPENAI_API_KEY
        self.DEFAULT_TEMPLATE_NAME = DEFAULT_TEMPLATE_NAME
        self.DEFAULT_MODEL = DEFAULT_MODEL

        # IS_SETUP
        self.IS_SETUP = IS_SETUP

        # CHAT SETTINGS
        self.DEFAULT_EXPORT_DIR = DEFAULT_EXPORT_DIR
        self.DEFAULT_SAVES_DIR = DEFAULT_SAVES_DIR
        self.SYSTEM_PROMPT_DIR = SYSTEM_PROMPT_DIR
        self.DEFAULT_SYSTEM_PROMPT = DEFAULT_SYSTEM_PROMPT

        # FROM FILE SYSTEM
        self.DEFAULT_FROM_FILE_FILENAME = DEFAULT_FROM_FILE_FILENAME
        self.FROM_FILE_SYSTEM_DIR = FROM_FILE_SYSTEM_DIR

        # MISC SETTINGS
        self.DEFAULT_SINGLE_MSG_DIR = DEFAULT_SINGLE_MSG_DIR
        self.SHOW_WELCOME_MESSAGE = SHOW_WELCOME_MESSAGE
        
        # AUTO-SAVE SETTINGS
        self.AUTO_SAVE_FREQUENCY = AUTO_SAVE_FREQUENCY
        self.AUTO_SAVE_MAX_SAVES = AUTO_SAVE_MAX_SAVES
        self.AUTO_SAVE_ENTRY_NAME = AUTO_SAVE_ENTRY_NAME
        self.IS_AUTOSAVING = IS_AUTOSAVING

settings_bag = SettingsObj()
SETTINGS_BAG = settings_bag








#=============================================================================
#================(TESTING)================
# should be run with python3 -m APGCM.settings
#TODO: Move this to a separate file


def make_settings_string(show_api_key: bool = False ) -> str:
    """Generates a string containing all of the settings and their values. Used for checking to make sure the settings are loaded correctly."""
    if not show_api_key:
        api_key = "Present" if OPENAI_API_KEY is not None else "Not Present" + " len: " + str(len(OPENAI_API_KEY))
    else:
        api_key = OPENAI_API_KEY
    settings = [
        "====(CHATLOG SETTINGS)====",
        f" Default ChatLog Handler: {DEFAULT_CHATLOG_HANDLER}",
        "=====(LOGGING SETTINGS)===",
        f"Default Logging Level: {DEFAULT_LOGGING_LEVEL}", 
        f"Default Logging Directory: {DEFAULT_LOGGING_DIR}",
        "=====(OPENAI SETTINGS)=====",
        f"OpenAI Key: {api_key}",
        f"Default Template Name: {DEFAULT_TEMPLATE_NAME}",
        f"Default Model: {DEFAULT_MODEL}",
        "====(CHAT SETTINGS)====",
        f"Default Export Directory: {DEFAULT_EXPORT_DIR}",
        f"Default Saves Directory: {DEFAULT_SAVES_DIR}",
        f"System Prompt Directory: {SYSTEM_PROMPT_DIR}",
        f"Default System Prompt: {DEFAULT_SYSTEM_PROMPT}",
        "====(FROM FILE SYSTEM)====",
        f"Default From File Contents: {DEFAULT_FROM_FILE_CONTENTS}",
        f"From File System Directory: {FROM_FILE_SYSTEM_DIR}",
        "====(MISC SETTINGS)====",
        f"Default Single Message Directory: {DEFAULT_SINGLE_MSG_DIR}",
        f"Show Welcome Message: {SHOW_WELCOME_MESSAGE}",
        "====(AUTO-SAVE SETTINGS)====",
        f"Auto Save Frequency: {AUTO_SAVE_FREQUENCY}",
        f"Auto Save Entries: {AUTO_SAVE_MAX_SAVES}",
        f"Auto Save Entry Name: {AUTO_SAVE_ENTRY_NAME}",
        f"Is Autosaving: {IS_AUTOSAVING}"
    ]

    return "\n".join(settings)

def main():
    print("\n".join(
        [
            "This is a test to make sure the settings are loaded correctly.",
            "If you see a bunch of settings, then everything is working correctly!",
            "If you see a bunch of 'None' values, then something is wrong and you should ensure that the .env file is set up correctly.",
            "You will be asked if you would like to see the OpenAI API key. If you say yes, the key will be shown. If you say no, the key will be hidden.",
            "It recommended that you do not show the key, as it is a secret and should not be shared with anyone but if you are having issues with the API key, you can show it to make sure it is loaded correctly.",
            "Would you like to see the OpenAI API key? (y/n)"
            
        ]
    ))
    show_api_key = input(">>> ")
    if show_api_key in ("y", "Y", "yes", "Yes", "YES", "1"):
        show_api_key = True
    else:
        show_api_key = False
    print(make_settings_string(show_api_key=show_api_key))
if __name__ == "__main__":
    main()
        