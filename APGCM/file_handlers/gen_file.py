import exceptions 
from func import is_filename_valid
import os 

import logging
import uuid
import json
from pathlib import Path
from typing import Union, List, Dict, Any, Optional, Tuple, Callable, Iterable, TypeVar, Generic, Sequence, Mapping, Set, Deque, Iterator, NamedTuple, overload, cast, no_type_check
from log_config  import DEFAULT_LOGGING_LEVEL 
class GeneralFileHandler:
    """
    A class for handling files in a general way
    Attributes:
        name: str, name of the GeneralFileHandler object.
        uuid: str, uuid of the GeneralFileHandler object.
        save_folder: str, path to the folder where files will be saved. Created if it does not exist.
        logging_level: int, logging level of the GeneralFileHandler object.
        version: str, version of the GeneralFileHandler object.
        file_extension: str, file extension of the files that will be saved.
        logger: logging.Logger object, logger for the GeneralFileHandler object.
    Methods:
        Private:
            _make_logger: makes the logger for the GeneralFileHandler object.
            _add_path: adds the save folder to the filename if it is not already there, as well as the file extension.
            _remove_path: removes the save folder from the filename if it is there, as well as the file extension.
        Core:
            write_to_file: writes the contents of a string to a file.
            get_file_contents: returns the contents of a file as a string.
            check_file_exists: returns True if the file exists, False otherwise.
            get_file_size: returns the size of the file in bytes.
           
            
        Misc:
            __repr__: returns a string representation of the GeneralFileHandler object.
    Example Usage:
        handler = GeneralFileHandler("gpt_cli/text_files/", ".txt")
        handler.write_to_file("Hello, how are you?", "hello.txt")
        handler.append_to_file("I am doing well, how are you?", "hello.txt")
        contents = handler.get_file_contents("hello.txt")
        print(contents)
        handler.delete_file("hello.txt")
    Dependencies:
        os
        logging
        uuid 
    Raises:
        exceptions.FileExistsError: if the file already exists and overwrite is False.
        exceptions.FileNotFoundError: if the file does not exist.
        exceptions.BadTypeError: if incorrect type is passed to a method.
        
        
    """
    version = "2.0.0"
    # the handler type is used for the logger
    handler_type = "GeneralFileHandler"

    def __init__(self,  save_folder: str, file_extension: str, name: str = "gen_file_handler", ):
        self.name = name
        self.logging_level = DEFAULT_LOGGING_LEVEL
        self._make_logger()
        self.save_folder = Path(save_folder)
        self.save_folder.mkdir(parents=True, exist_ok=True)
        self.logger.info("Created save folder: "+save_folder)
            
        self.uuid = str(uuid.uuid4())   
       
        if not file_extension.startswith('.'):
            file_extension = '.'+file_extension
            self.logger.info("Added leading dot to file extension: "+file_extension)
        
        self.file_extension = file_extension
        self.logger.info(f"Initialized {self.handler_type} name" +self.name+ " with save_folder: "+save_folder+" and file_extension: "+file_extension)
        
    def _make_logger(self)-> None:
        """Makes the logger for the GeneralFileHandler object"""
        logger = logging.getLogger(__name__)
        logger.setLevel(self.logging_level)
        path = Path(".") / "logs/"
        path.mkdir(parents=True, exist_ok=True)
        str_path = path / "file_handlers/" /f"{self.handler_type}_file_handler.log"
        str_path.parent.mkdir(parents=True, exist_ok=True)
        str_path.touch(exist_ok=True)
        str_path = str(str_path)
        file_handler = logging.FileHandler(str_path)
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s #%(lineno)d: %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        self.logger = logger
        self.logger.info("Made logger for GeneralFileHandler name: "+self.name)
        self.logger.debug("Logging level: "+str(self.logging_level))
    def set_logging_level(self, log_level: int) -> None:
        """Sets the logging level of the GeneralFileHandler object"""
        self.logger.setLevel(log_level)
        
    def _add_path(self, filename: str) -> str:
        """Returns a string with the save folder and filename"""
        filename = str(filename).strip()
        # if  not  is_filename_valid(filename):
        #     raise exceptions.BadFileNameError("Filename must be a string without prohibited characters(special characters, spaces, etc)")
        if filename.startswith(str(self.save_folder)):
            self.logger.info("Save folder already in filename: "+filename)
        else:
            filename = self.save_folder / filename
            self.logger.info("Added save folder to filename: "+str(filename))
        if not str(filename).endswith(self.file_extension):
            filename =str(filename) + self.file_extension
        return str(filename)
    
    
    def _remove_path(self, filename: str) -> str:
        """Returns a string without the save folder and filename"""
        if filename.startswith(str(self.save_folder)):
            filename = filename.replace(str(self.save_folder), '')
            self.logger.info("Removed save folder from filename: "+filename)
        if filename.endswith(self.file_extension):
            filename = filename.replace(self.file_extension, '')
            self.logger.info("Removed file extension from filename: "+filename)
        return str(filename)
    def get_filenames(self, remove_path: bool = False) -> list:
        """Returns a list of filenames in the save folder"""
        filenames = map( lambda x: str(x.name),
            self.save_folder.glob("*"+self.file_extension))
        if remove_path:
            filenames = [self._remove_path(filename) for filename in filenames]
        return list(filenames)
    def check_if_file_exists(self, filename: str) -> bool:
        """Returns True if the file exists, False otherwise"""
        filename = self._add_path(filename)
        return os.path.exists(filename)
    def delete_file(self, filename: str) -> None:
        """Deletes the file"""
        filename = self._add_path(filename)
        if not self.check_if_file_exists(filename):
            raise exceptions.FileNotFoundError("File not found: "+filename)
        os.remove(filename)
        self.logger.info("Deleted file: "+filename)
    def delete_all_files(self) -> None:
        """Deletes all files in the save folder
        WARNING: This is a destructive operation. Use with caution. 
        """
        filenames = self.get_filenames()
        for filename in filenames:
            self.delete_file(filename)
    def get_file_contents(self, filename: str) -> str:
        """Gets the contents of the file as a string"""
        filename = self._add_path(filename)
        if not self.check_if_file_exists(filename):
            raise exceptions.FileNotFoundError("File not found: "+filename)
        with open(filename, "r") as f:
            contents = f.read()
        return contents
    
    def write_to_file(self, filename: str, contents: str, overwrite = False) -> None:
        """Writes the contents to the file"""
        filename = self._add_path(filename)
        if not overwrite:
            if self.check_if_file_exists(filename):
                raise exceptions.FileExistsError("File already exists: "+filename)
        self.logger.info("Writing to file: "+filename)
        try:
            with open(filename, "w") as f:
                f.write(contents)   
        except Exception as e:
            self.logger.error("Error writing to file: "+filename)
            raise e
    
    def get_file_size(self, filename: str) -> int:
        """Gets the size of the file in bytes"""
        filename = self._add_path(filename)
        if not self.check_if_file_exists(filename):
            raise exceptions.FileNotFoundError("File not found: "+filename)
        return os.path.getsize(filename)
    def __repr__(self):
        """Returns a string representation of the object"""
        return "GeneralFileHandler(name="+self.name+", save_folder="+self.save_folder+", file_extension="+self.file_extension+")" + " version: "+self.version + " uuid: "+self.uuid
    
    
            
        
class TextFileHandler(GeneralFileHandler):
    """A class for handling text files
    See GeneralFileHandler for more information
    Note: The file extension is automatically set to .txt
    Additional Methods:
    append_to_file: appends the contents to the file.
    get_file_contents_as_list: returns the contents of the file as a list of strings.
    """
    handler_type = "TextFileHandler"
    
    def __init__(self, save_folder: str, name: str = "text_file_handler", log_level: int = DEFAULT_LOGGING_LEVEL):
        super().__init__(save_folder=save_folder, file_extension=".txt", name=name )
        self.logger.info("Initialized TextFileHandler name" +self.name+ " with save_folder: "+save_folder)
        
    def get_file_contents_as_list(self, filename: str) -> list:
        """Gets the contents of the file as a list of strings"""
        with open(self._add_path(filename), "r") as f:
            contents = f.readlines()
        return contents
    def append_to_file(self, filename: str, contents: str) -> None:
        """Appends the contents to the file"""
        filename = self._add_path(filename)
        if not self.check_if_file_exists(filename):
            raise exceptions.FileNotFoundError("File not found: "+filename)
        self.logger.info("Appending to file: "+filename)
        try:
            with open(filename, "a") as f:
                f.write(contents)   
        except Exception as e:
            self.logger.error("Error appending to file: "+filename)
            raise e
    @property 
    def all_files(self) -> list:
        """Returns a list of all files in the save folder"""
        return self.get_filenames(remove_path=True)
        
class JsonFileHandler(GeneralFileHandler):
    """
    For handling json files
    Modified Methods:
        write_to_file - Writes the contents to the file, overwriting if overwrite is True. The contents must be a dict. 
        get_file_contents - Gets the file contents as a dict
    
    
    Default file extension: .json
    
    """
    handler_type = "JsonFileHandler"
    def __init__(self, save_folder: str, name: str = "json_file_handler"):
        super().__init__(save_folder, ".json", name)
        self.logger.info("Initialized JsonFileHandler name" +self.name+ " with save_folder: "+save_folder)
    def write_to_file(self, filename: str, contents: dict, overwrite = False) -> None:
        """Writes the contents to the file, overwriting if overwrite is True. The contents must be a dict."""
        if not isinstance(contents, dict):
            raise exceptions.BadTypeError("Contents must be a dict")
        contents = json.dumps(contents, indent=4)
        super().write_to_file(filename, contents, overwrite)
    def get_file_contents(self, filename: str) -> dict:
        """Gets the file contents as a dict"""
        contents = super().get_file_contents(filename)
        try:
            contents = json.loads(contents)
        except json.JSONDecodeError as e:
            self.logger.error("Bad or corrupt JSON file: "+filename)
            raise exceptions.BadJSONFileError("Bad or corrupt JSON file: "+filename) from e
        return contents
    
class MarkDownFileHandler(GeneralFileHandler):
    handler_type = "MarkDownFileHandler"
    def __init__(self, save_folder: str, name: str = "markdown_file_handler"):
        super().__init__(save_folder=save_folder, file_extension= ".md", name = name)
        self.logger.info("Initialized MarkDownFileHandler name" +self.name+ " with save_folder: "+save_folder)
    
    
