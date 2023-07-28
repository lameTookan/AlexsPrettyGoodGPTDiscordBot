
from pathlib import Path
from chat_wrapper import ChatWrapper 

import exceptions
from file_handlers.gen_file import TextFileHandler, MarkDownFileHandler
from log_config import DEFAULT_LOGGING_LEVEL, BaseLogger
from settings import DEFAULT_SAVES_DIR, DEFAULT_EXPORT_DIR
import uuid as uuid
from chat import export_data


        
   
            
class ChatExporter:
    """Class for exporting a chat log to a file, abstracts away the process of exporting the chat log to a file."""
    version = "0.1.0"
    def __init__(self, chat_wrapper_obj: ChatWrapper = None, save_dir: str = DEFAULT_EXPORT_DIR,):
        self.logger = BaseLogger(
            __file__, filename="chat_exporter.log", identifier="chat_exporter", level=DEFAULT_LOGGING_LEVEL
        ) 
        self.logger.debug("ChatExporter initialized")
        self._chat_wrapper_obj: ChatWrapper = chat_wrapper_obj
        self.save_dir = save_dir 
        self.file_handler = MarkDownFileHandler(save_folder=save_dir, name ="chatlog_md_exporter")
        self.exporter = export_data
    @property
    def chat_wrapper(self) -> ChatWrapper | None:
        """Returns the chat wrapper object"""
        return self._chat_wrapper_obj
    @chat_wrapper.setter
    def chat_wrapper(self, chat_wrapper_obj: ChatWrapper | None):
        """Sets the chat wrapper object, can be None(ie unset). Will raise an error if the chat wrapper object is not a ChatWrapper object"""
        if not isinstance(chat_wrapper_obj, ChatWrapper) and chat_wrapper_obj is not None:
           raise exceptions.IncorrectObjectTypeError("chat_wrapper_obj must be a ChatWrapper object or None(ie unset))")
        self.logger.debug(f"Setting chat wrapper to {chat_wrapper_obj}")
        self._chat_wrapper_obj = chat_wrapper_obj
    def _check_chat_wrap(self) -> bool:
        """Checks if the chat wrapper object is set, returns True if it is, False otherwise"""
        return isinstance(self.chat_wrapper, ChatWrapper)
    def _make_md_data(self, **kwargs) -> str:
        """Uses the exporter function to make the markdown data"""
        if not self._check_chat_wrap():
            raise exceptions.ObjectNotSetupError("Chat exporter requires a chat wrapper to export data. Set the chat wrapper using the chat_wrapper property")
        if self.chat_wrapper.system_prompt is not None:
            kwargs["system_prompt"] = self.chat_wrapper.system_prompt
        self.logger.debug(f"Making markdown data with kwargs: {kwargs}")
        return self.exporter(data =self.chat_wrapper.trim_object.chatlog.data, model=self.chat_wrapper.model, exporter_type="markdown", **kwargs)
    def save(self, filename: str, overwrite: bool = False, **kwargs) -> None:
        """Creates the markdown data from the chat log, using the exporter function, and saves it to a file
        Will raise an error if the chat wrapper is not set, or if the file already exists and overwrite is False, so either catch the error or use check_if_file_exists to check if the file exists before saving it.
        Uses the file handler to save the data to a file
        """
        if not self._check_chat_wrap():
            raise exceptions.ObjectNotSetupError("Chat exporter requires a chat wrapper to export data. Set the chat wrapper using the chat_wrapper property")
        data = self._make_md_data(**kwargs)
        self.file_handler.write_to_file(contents=data, filename=filename, overwrite=overwrite)
        self.logger.debug(f"Saved chat log to {filename}")
    def check_if_file_exists(self, filename: str) -> bool:
        """Checks if a file exists in the export dir"""
        return self.file_handler.check_if_file_exists(filename)
    def get_current_files(self, remove_path: bool = True) -> list:
        """Exports the chat log as markdown to a file"""
        return self.file_handler.get_filenames(remove_path=remove_path)
    def delete_file(self, filename: str) -> None:
        """Deletes a file from the export dir"""
        self.file_handler.delete_file(filename=filename)
    
    
    
        
       
        
    



 
