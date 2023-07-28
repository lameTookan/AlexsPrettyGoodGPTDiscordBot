import sys 
from abc import ABC, abstractmethod
import json 
#sys.path.append("../gpt_cli")

from file_handlers.gen_file import MarkDownFileHandler, TextFileHandler, GeneralFileHandler, JsonFileHandler
from log_config import BaseLogger, DEFAULT_LOGGING_LEVEL
from settings import DEFAULT_SAVES_DIR
import exceptions as e 
import func as f

class AbstractCWSaveHandler(ABC):
    version = "Rough Draft 1.0.0"
    """
    ...
    
    Example usage:
    ```
    my_save_handler = MySaveHandler()
    chat_wrapper.add_save_handler(my_save_handler)
    
    # Saving a new entry
    if not chat_wrapper.check_entry("my_new_entry"):
        chat_wrapper.save("my_new_entry")
    else:
        output_to_user("Entry name already exists! Please choose a different name.")
    
    # Overwriting an existing entry
    if chat_wrapper.check_entry("my_existing_entry"):  
        output_to_user("Entry name already exists! Would you like to overwrite it?")
        if user_confirms():
            chat_wrapper.write_entry("my_existing_entry", overwrite=True)
    ```
    """

    name="AbstractSaveHandler"
    def __init__(self):
        self.logger = BaseLogger(__file__, filename="save_handler.log", identifier="SaveHandler: " + self.name, level=DEFAULT_LOGGING_LEVEL)
        
        self.logger.info(f"Created SaveHandler {self.name}")
        
    @abstractmethod
    def check_entry(self, entry_name: str) -> bool:
        """Returns True if the entry exists, False if it doesn't."""
        pass
    @abstractmethod
    def write_entry(self, entry_name: str, save_dict: dict, overwrite: bool = False) -> None:
        """Writes the entry to the save file, overwriting if overwrite is True. Should raise an exception if overwrite is False and the entry already exists."""
        pass
    @abstractmethod
    def read_entry(self, entry_name: str) -> dict:
        """Returns the entry from the save file."""
        pass
    @property
    @abstractmethod 
    def entry_names(self) -> list[str]:
        """Returns a list of entry names."""
        pass
    @abstractmethod
    def delete_entry(self, entry_name: str) -> None:
        """Deletes the entry from the save system. Should raise an exception if the entry doesn't exist."""
    def __str__(self):
        return self.name
    def __repr__(self):
        return f"ChatWrapper SaveHandler: {self.name} <{id(self)}>"
        
class JsonSaveHandler(AbstractCWSaveHandler):
    version = "1.0.0"
    name = "JsonSaveHandler"
    """A file handler that uses json to save entries.
    Notes:
        - Here the entry names are just the file names. They can include a .json file extension, however they don't need to(JsonFileHandler will deal with this)
        -Default save directory is DEFAULT_SAVES_DIR, which is set in settings.py(.env file, default is ../files/saves in the parent dir) 
        - If this class is being used in a public manner (for example, a public discord bot on a sever), this would not be secure, as the actual filenames are used as the entry names, giving users direct access to the file system. 
    Dependencies:
        - JsonFileHandler
        - BaseLogger, DEFAULT_LOGGING_LEVEL from log_config.py
        - DEFAULT_SAVES_DIR from settings.py
    Raises:
        This class does not raise any exceptions on its own, however JsonFileHandler does raise the following exceptions, all children of PrettyGoodError:
            - FileNotFoundError
            - FileExistsError
            - BadFileNameError(if a file name includes prohibited characters)
        These exceptions can be found in exceptions.py, and are described in more detail in the docstring/documentation for JsonFileHandler.
    Example usage:
        ```
        save_handler = JsonSaveHandler()
        chat_wrapper.add_save_handler(save_handler)
        ...use the save and load methods described in both the documentation for ChatWrapper and AbstractCWSaveHandler...
        ```
    
    """
    def __init__(self, save_dir=DEFAULT_SAVES_DIR):
        self.logger = BaseLogger(__file__, filename="save_handler.log", identifier="SaveHandler: " + self.name, level=DEFAULT_LOGGING_LEVEL)
        self.logger.info("Initializing JsonSaveHandler")
        self.save_dir = save_dir
        self.file_handler = JsonFileHandler(self.save_dir, "SaveFileHandler")
        self.logger.info("Initialized JsonSaveHandler")
    def check_entry(self, entry_name: str) -> bool:
        """Returns True if the entry exists, False if it doesn't."""
        return self.file_handler.check_if_file_exists(entry_name)
    def write_entry(self, entry_name: str, save_dict: dict, overwrite: bool = False) -> None:
        """Uses the file handler to write an entry to a save file(file handler handles the json conversion)
        Will raise an FileExistsError(PrettyGoodError) if overwrite is False and the entry already exists. Either use the check_entry method or catch the exception if you don't want to overwrite -- otherwise set overwrite to True. 
        """
        self.file_handler.write_to_file(filename=entry_name, contents=save_dict ,  overwrite=overwrite)
    def read_entry(self, entry_name: str)-> dict:
        """Returns the entry from the save file, a dictionary of the save file contents. Will raise a FileNotFoundError(PrettyGoodError) if the entry doesn't exist."""
        return self.file_handler.get_file_contents(entry_name)
    def delete_entry(self, entry_name: str) -> None:
        """Deletes the entry from the save system. Will raise a FileNotFoundError(PrettyGoodError) if the entry doesn't exist."""
        self.file_handler.delete_file(entry_name)
    @property
    def entry_names(self) -> list[str]:
        """Returns a list of entry names."""
        return self.file_handler.get_filenames(remove_path=True)
    
        