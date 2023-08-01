# SaveHandlers

## Overview

Save handlers are designed to allow ChatWrapper to save and load chat logs without being tied down to a particular format.

ChatWrapper uses dictionaries for serialization and deserialization. The save handlers are responsible for processing and saving these dictionaries, paired with unique identifier called an entry name. These entry names should be unique to each save.

It does not matter how these entries are stored. It could be a database, a file, or even a cloud service. The only requirement is that the save handler can retrieve the entry using the entry name.

## AbstractCWSaveHandler Class

Save handlers must be children of this class. It provides the basic interface for saving and loading chat logs.

### Class Variables

* name - The name of the save handler. This is used for debugging purposes.
* version - The version of the save handler. This is used for debugging purposes. Optional but recommended.

### Methods

#### `.check_entry(entry_name) -> bool`

Should return `True` if an entry with the specified name exists, otherwise return `False`.

#### `.write_entry(entry_name: str, save_dict: dict, overwrite: bool = False) -> None`

Saves the specified entry with the entry_name and save_dict. If overwrite is `True`, overwrite the existing entry with the same name, otherwise it should raise `FileExistsError`, a custom exception that is a child of `PrettyGoodError`, for easy catching. This exception can be found in the `exceptions.py` file.

#### `.read_entry(entry_name: str) -> dict`

Reads the specified entry and returns the save_dict. If the entry does not exist, it should raise `FileNotFoundError`, a custom exception that is a child of `PrettyGoodError`, for easy catching. This exception can be found in the `exceptions.py` file.

#### `delete_entry(entry_name: str) -> None`

Deletes the specified entry. If the entry does not exist, it should raise `FileNotFoundError`, a custom exception that is a child of `PrettyGoodError`, for easy catching. This exception can be found in the `exceptions.py` file.

#### `entry_names` property

Should return a list of all entry names.

#### Recommended Additional Methods

* `__repr__` - Should return a string representation of the save handler. This is used for debugging purposes.
* `__str__` - Should return a string representation of the save handler. This is used for debugging purposes.

**This class along with two examples can be found in the `handler/SaveHandler.py` file.**

### Adding a save handler to ChatWrapper

```python
import APGCM
chat_wrapper = APGCM.chat_utils.quick_make_chat_wrapper()
# this makes a chat wrapper with the default settings
save_handler = MySaveHandler()
chat_wrapper.add_save_handler(save_handler)
# you can now use methods like chat_wrapper.save_entry() and chat_wrapper.load_entry()
```

### Example Save Handler

The following is one of the save handlers included in the `SaveHandler.py` file. It is not a **Real** save handler, but rather a dummy one used for testing that simply saves the entries to class attribute called `save_dict`. It is however, a valid save handler and should give you an idea of the structure of a save handler.

```python
class DummySaveHandler(AbstractCWSaveHandler):
    """Used for testing purposes does not save anything aside from in memory.
    Includes all required methods for a save handler.

    Also has 2 additional methods for debugging purposes:
    - log_save_dict() - Logs the save dictionary to the console, and prints it
    - save_to_file() - Saves the save dictionary to a file so we can look at it later for debugging purposes
    """
    name = "DummySaveHandler"
    version = "1.0.0"
    def __init__(self):
        # this is just how I have set up logging in my project. You can use whatever logging system you want, or none at all. 
        self.logger = BaseLogger(__file__, filename="dummy_save_handler.log", identifier="SaveHandler: " + self.name, level=DEFAULT_LOGGING_LEVEL)
        self.logger.info("Initializing DummySaveHandler")
        self.save_dict = {}
        self.logger.info("Initialized DummySaveHandler")
    
    def check_entry(self, entry_name: str) -> bool:
        """Returns True if the entry exists, otherwise returns False"""
        if entry_name in self.save_dict.keys():
            return True
        else:
            return False
    def write_entry(self, entry_name: str, save_dict: dict, overwrite: bool = False) -> None:
        """Writes a SaveDict dictionary, and raises a FileExistsError if the entry already exists"""
        if entry_name in self.save_dict.keys() and not overwrite:
            raise e.FileExistsError(f"Entry {entry_name} already exists!")
        self.save_dict[entry_name] = save_dict
        self.logger.info(f"Saved entry {entry_name}")
    def read_entry(self, entry_name: str) -> dict:
        """Reads a SaveDict dictionary, and raises a FileNotFoundError if the entry does not exist"""
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
        """Returns a list of all entry names"""
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
        # JsonFileHandler is in the file_handler folder. These classes abstract away the file handling process. Documentation for this class is not included as it doesn't have a real purpose in this project beyond being used for the included JsonSaveHandler class 
        file_handler = JsonFileHandler(DEFAULT_SAVES_DIR + "Dummy_files/", "DummySaveHandler")
        filename = f"{name}_{str(len(file_handler.get_filenames()))}" if auto_make_filename else name  
          
        file_handler.write_to_file(filename, self.save_dict, overwrite=True)
        self.logger.info(f"Saved DummySaveHandler save dictionary to file {name}")
        return file_handler 
```

As you can see, creating SaveHandlers is pretty simple, and can accommodate any file system or database. Don't hesitate to reach out if you have any questions or need help creating a SaveHandler for your project.

Happy Coding! 
