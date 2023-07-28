from pathlib import Path
from chat_wrapper import ChatWrapper
import exceptions

from file_handlers.gen_file import JsonFileHandler
from log_config import DEFAULT_LOGGING_LEVEL, BaseLogger
from settings import DEFAULT_SAVES_DIR


class SaveFileHandler:
    """Saves and loads chat wrapper save dictionaries to and from files, abstracts away the file handling and json encoding/decoding
    Dependencies:
        Custom:
            chat_wrapper.ChatWrapper -> Object to load and save from, must have a make_save_dict method that returns a dictionary.
            JsonFileHandler -> Handles the file handling and json encoding/decoding
            BaseLogger -> Logging object for logging
            exceptions -> Custom exceptions
            settings -> Settings for the program
        Python:
            json -> For encoding and decoding json
            Path -> For handling paths
    Raises:
        exceptions.IncorrectObjectTypeError: Raised if the chat wrapper object is not a ChatWrapper object
        exceptions.ObjectNotSetupError: Raised if the chat wrapper object is not set and an operation is attempted that requires it to be set(ie save or load)
    Args:
        save_dir (str, optional): The directory to save the files to. Defaults to DEFAULT_SAVES_DIR.(from settings.py)
        chat_wrapper_obj (ChatWrapper, optional): The chat wrapper object to save. Defaults to None. Can be set later using the chat_wrapper_obj property
    Properties:
        Objects:
            _chat_wrapper_obj (ChatWrapper): The chat wrapper object to save
            logger (BaseLogger): The logger object for logging(pre-configured logging object )
            file_handler (JsonFileHandler): The file handler object for handling the file handling and json encoding/decoding
        Other:
            dir (Path): The path to the save dir
    Methods:
        Core/Public:
            save(filename: str, overwrite: bool = False) -> None: Saves the chat wrapper object to a file. Must have a chat wrapper object set, otherwise will raise an error, also raises an error if the file already exists and overwrite is False
            load(filename:str ) -> ChatWrapper: Loads a save file into the chat wrapper object, will overwrite any existing data in the chat wrapper object. If a chat wrapper object is not set, will raise an error, also raises an error if the file does not exist. Either catch this error or use check_if_file_exists to check if the file exists before loading it.
            check_if_file_exists(filename: str) -> bool: Checks if a file exists in the save dir
            get_current_files(remove_path: bool = True) -> list: Returns a list of the current files in the save dir
        Private:
            _check_chat_wrapper() -> bool: Checks if the chat wrapper object is set, returns True if it is, False otherwise
    Example Usage:
        chat_wrapper = ChatWrapper(API_KEY, model="GPT-4")
        print(chat_wrapper.chat("Hello"))
        chat_wrapper.user_message = "Hello"
        chat_wrapper.assistant_message = "Hello, my name is Bob."
        save_handler = SaveFileHandler( chat_wrapper_obj=chat_wrapper)
        if not save_handler.check_if_file_exists("test_save.json"):
            save_handler.save("test_save.json")
        else:
            print("File already exists")

    """

    def __init__(
        self, chat_wrapper_obj: ChatWrapper = None, save_dir=DEFAULT_SAVES_DIR
    ):
        self.logger = BaseLogger(
            __file__,
            filename="save_file_handler.log",
            identifier="save_file_handler",
            level=DEFAULT_LOGGING_LEVEL,
        )
        self.logger.debug("SaveFileHandler initialized")
        self.dir = Path(save_dir)
        self.file_handler = JsonFileHandler(
            save_folder=save_dir, name="SaveFileHandler"
        )
        self.logger.debug(f"JSON file handler initialized with save dir: {self.dir}")
        self._chat_wrapper_obj = chat_wrapper_obj

    @property
    def chat_wrapper_obj(self) -> ChatWrapper:
        """The chat wrapper object to save"""
        return self._chat_wrapper_obj

    @chat_wrapper_obj.setter
    def chat_wrapper_obj(self, chat_wrapper_obj: ChatWrapper):
        """Sets the chat wrapper object to save. Can be None(ie unset) to unset the chat wrapper object(however, attempting to save will raise an error)"""
        if (
            not isinstance(chat_wrapper_obj, ChatWrapper)
            and chat_wrapper_obj is not None
        ):
            raise exceptions.IncorrectObjectTypeError(
                "chat_wrapper_obj must be a ChatWrapper object"
            )
        self._chat_wrapper_obj = chat_wrapper_obj
        self.logger.debug(f"Chat wrapper object set to {self._chat_wrapper_obj}")

    def _check_chat_wrapper(self):
        """Checks if the chat wrapper object is set, returns True if it is, False otherwise"""
        return isinstance(self.chat_wrapper_obj, ChatWrapper)

    def save(self, filename: str, overwrite: bool = False) -> None:
        """Saves the chat wrapper object to a file"""
        if not self._check_chat_wrapper():
            self.logger.error("Chat wrapper object not set, cannot save")
            raise exceptions.ObjectNotSetupError(
                "chat_wrapper_obj must be set to a ChatWrapper object"
            )
        self.file_handler.write_to_file(
            contents=self.chat_wrapper_obj.make_save_dict(),
            filename=filename,
            overwrite=overwrite,
        )
        self.logger.debug(f"Saved chat wrapper object to {filename}")

    def check_if_file_exists(self, filename: str) -> bool:
        """Checks if a file exists in the save dir"""
        return self.file_handler.check_if_file_exists(filename)

    def get_current_files(self, remove_path: bool = True) -> list:
        """Returns a list of the current files in the save dir"""
        return self.file_handler.get_filenames(remove_path=remove_path)

    def load(self, filename: str) -> ChatWrapper:
        """Loads a save file into the chat wrapper object, will overwrite any existing data in the chat wrapper object. If a chat wrapper object is not set, will raise an error, also raises an error if the file does not exist. Either catch this error or use check_if_file_exists to check if the file exists before loading it."""
        if not self._check_chat_wrapper():
            self.logger.error("Chat wrapper object not set, cannot load")
            raise exceptions.ObjectNotSetupError(
                "SaveFileHandler requires a chat wrapper object to load data into. Set the chat wrapper object using the chat_wrapper_obj property"
            )
        save = self.file_handler.get_file_contents(filename=filename)
        self.chat_wrapper_obj.load_from_save_dict(save_dict=save)
        self.logger.debug(f"Loaded save file {filename} into chat wrapper object")
        return self.chat_wrapper_obj
