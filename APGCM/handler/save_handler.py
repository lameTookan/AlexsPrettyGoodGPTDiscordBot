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
    version = "2.0.0"
    name = "AbstractCWSaveHandler"
    """
    Abstract Save Handler is the base class for all save handlers. It is an abstract class. This allows for the creation of custom save handlers, which can be used with the ChatWrapper class, thus not tying the ChatWrapper class to a specific save system.
    
    Terminology:
        Entry - An entry is a unique identifier for a save. It doesn't matter how it refers to the save data -- just that is unique and the SaveHandler can use it to retrieve and save a save dictionary 
        Save Dictionary - A save dictionary is a dictionary that is used for chat wrapper serialization. It contains all of the information needed to save and load a chat wrapper. It has a specific format, which is described in the documentation for ChatWrapper, and outlined in the make_save_dict() load_save_dict() and _verify_save_dict() methods in the ChatWrapper class. See the docs folder for examples and more information.
        ChatWrapper or CW - The ChatWrapper class, which is the main class of the APGCM package. It is used to serialize and deserialize chat logs, as well as to chat with the OpenAI API.
        Save Handler:  A child class of this class that can be added to the ChatWrapper using the add_save_handler() method. It is used to save and load chat wrappers.
    Dependencies:
        - BaseLogger, DEFAULT_LOGGING_LEVEL from log_config.py
        - Used by ChatWrapper
        
    Required Methods:
        - check_entry: Should output True if the entry exists, False if it doesn't.
        - write_entry: Should write the entry to the save file, overwriting if overwrite is True. Should raise an exception if overwrite is False and the entry already exists. Chat wrapper passes a save dictionary to this method, which should be written to the save file.
        - read_entry: Should return the entry from the save file. Should raise a FileNotFoundError if the entry doesn't exist.
        - entry_names: Should return a list of entry names, which are used to identify the entries. 
        - delete_entry: Should delete the entry from the save system. Should raise a FileNotFoundError if the entry doesn't exist.
    Attributes:
        Only 3 are included in the abstract class 
        name: The name of the save handler. This is used for logging purposes, and should be set in the child class.
        version: The version of the save handler. This is used to keep track of the version of the handler. Completely optional, but it is recommended to set this in the child class.
        logger - A BaseLogger object, which is used for logging. This is set in the child class, optionally using the BaseLogger class.
    Includes a __repr__ and __str__ method which is recommended to be overwritten for ease of use and debugging but not required.
    ...
    How ChatWrapper uses this class:
        See load_entry, save_entry, and add_save_handler in the ChatWrapper class. 
        Also used in the auto save rotation system, which is described in the documentation for ChatWrapper.
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
    See JsonSaveHandler for a more detailed and practical example.
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
    
class DummySaveHandler(AbstractCWSaveHandler):
    """Used for testing purposes does not save anything aside from in memory."""
    name = "DummySaveHandler"
    version = "1.0.0"
    def __init__(self):
        self.logger = BaseLogger(__file__, filename="dummy_save_handler.log", identifier="SaveHandler: " + self.name, level=DEFAULT_LOGGING_LEVEL)
        self.logger.info("Initializing DummySaveHandler")
        self.save_dict = {}
        self.logger.info("Initialized DummySaveHandler")
    def _check_name(self, name: str ) -> bool:
        """Checks if the name is a valid entry name"""
        if name in self.save_dict.keys():
            return True
        else:
            return False
    def check_entry(self, entry_name: str) -> bool:
        if entry_name in self.save_dict.keys():
            return True
        else:
            return False
    def write_entry(self, entry_name: str, save_dict: dict, overwrite: bool = False) -> None:
        if entry_name in self.save_dict.keys() and not overwrite:
            raise e.FileExistsError(f"Entry {entry_name} already exists!")
        self.save_dict[entry_name] = save_dict
        self.logger.info(f"Saved entry {entry_name}")
    def read_entry(self, entry_name: str) -> dict:
        if entry_name not in self.save_dict.keys():
            raise e.FileNotFoundError(f"Entry {entry_name} does not exist!")
        self.logger.info(f"Read entry {entry_name}")
        return self.save_dict[entry_name]
    def delete_entry(self, entry_name: str) -> None:
        if self.check_entry(entry_name):
            del self.save_dict[entry_name]
            self.logger.info(f"Deleted entry {entry_name}")
        else:
            raise e.FileNotFoundError(f"Entry {entry_name} does not exist!")
    @property
    def entry_names(self) -> list[str]:
        return list(self.save_dict.keys())
    def log_save_dict(self, print_save: bool = False) -> None:
        """Logs the save dictionary to the console"""
        self.logger.info(f"Save Dictionary: {self.save_dict}")
        if print_save:
            print(f"Save Dictionary: {self.save_dict}")
    def save_to_file(self, name: str = "Test_Save_File", auto_make_filename = True):
        """Save the dictionary to a file so we can look at it later for debugging purposes
        Returns the file handler object so that we can do more operations on it if want to. 
        """
        file_handler = JsonFileHandler(DEFAULT_SAVES_DIR + "Dummy_files/", "DummySaveHandler")
        filename = f"{name}_{str(len(file_handler.get_filenames()))}" if auto_make_filename else name    
        file_handler.write_to_file(filename, self.save_dict, overwrite=True)
        self.logger.info(f"Saved DummySaveHandler save dictionary to file {name}")
        return file_handler 
    