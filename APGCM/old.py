"""
def export(self, format: str = "text") -> str:
        \"""Exports the chatlog to a string, formatted as either text or markdown.
        Default format is text.
        Does not save the chatlog to a file, use the TextFileHandler class for that instead.
        Args:
            format: str = "text" Optional, the format to export the chatlog as. Must be one of "text" or "markdown". Defaults to "text".
        Returns:
            str: The chatlog as a string, formatted as either text or markdown.
        Raises:
            BadFormatError: If the format is not one of "text" or "markdown".
        \"""
        possible_formats = {"text", "markdown"}
        if format not in possible_formats:
            raise exceptions.BadFormatError(f"Format must be one of {possible_formats}")
        
        def format_message_text(msg: message.Message) -> str:
            if msg.role == "system":
                return f"System: {msg.content}"
            elif msg.role == "user":
                return "User: " + msg.content
            elif msg.role == "assistant":
                return "Assistant: " + msg.content
            else:
                return f"{msg.role}: {msg.content}"
        def format_message_md(msg: message.Message) -> str:
            if msg.role == "system":
                return f"_System_: {msg.content}"
            elif msg.role == "user":
                return "_User_: " + msg.content
            elif msg.role == "assistant":
                return "_Assistant_: " + msg.content
            else:
                return f"_{msg.role}_: {msg.content}"   
        if format == "text":
            divider = "-+-" * 10
            result_list = [
                "Chat Log",
                "Meta Data:",
                f"Model: {self.model}",
                "Total Messages: " + str(len(self.data)),
                "Time: " + str(datetime.datetime.now()),
                "Date: " + str(datetime.date.today()), 
                divider,
                "Messages:"
                
                
                
            ]
            short_divider = "-" * 5
           
            for msg in self.get_messages(reverse=False):
                result_list.append(format_message_text(msg))
                result_list.append(short_divider)
            return "\n".join(result_list)
        elif format == "markdown":
            divider = "---"
            def italics(string: str) -> str:
                return f"*{string}*"
            result_list = [
                "# Chat Log",
                divider, 
                "## Meta Data",
                "__Model__: " + italics(self.model),
                "__Total Messages__: " + italics(str(len(self.data))),
                "__Time__: " + italics(str(datetime.datetime.now())),
                "__Date__: " + italics(str(datetime.date.today())),
                divider,
                divider,
                "## Messages", 
                               
                
                ]
            for msg in self.get_messages(reverse=False):
                result_list.append(format_message_md(msg))
                result_list.append(divider)
        return "\n".join(result_list)
"""

# class SystemPromptMenu:
#     """A menu for managing system prompts. By default, the system prompt directory is set to the SYSTEM_PROMPT_DIR in settings.py. This can be changed by passing in a different directory or modifying the associated .env variable.
#     Somewhat more complex than other menus, as it has a few different menus for different purposes.
#     Dependencies:
#         Custom:
#             SystemPromptManager from APGCLI/sys_prompt_manager.py
#             Exceptions from gpt_cli.exceptions
#             InputHandler from gpt_cli.func(Allows for input chunking for long input messages, see gpt_cli/func.py for more info)
#             log_config from gpt_cli.log_config for BaseLogger and DEFAULT_LOGGING_LEVEL
#             common from gpt_cli.common for confirm and split_arg_from_cmd
#             WILD_CARD_INFO , constant listing the wildcards that can be used in a prompt.(so they can be easily changed if needed)
#         Python:
#             typing for type hinting 
            
#     Raises:
#         IncorrectObjectTypeError: If the sys_manager is not of type SystemPromptManager, and if _handle_cmd is not passed a function reference of type Callable.
#         SystemPromptManager Raises:
#             FileNotFoundError: If the file does not exist.
#             FileExistsError: If the file already exists and overwrite is set to False.
#     Returns: Loaded prompt, or None if no prompt is loaded.
#     Attributes:
#         sys_manager (SystemPromptManager): The SystemPromptManager object to use.
#         logger (BaseLogger): A pre-configured logger object.
#         loaded_prompt (str): The currently loaded prompt, if one is loaded.
#     Methods:
#         Properties:
#             all_files: Gets the list of all system prompt files.
#             default_prompt: Gets the default prompt.
#         Helpers:
#             check_file: Checks if a file exists. Returns True if it does, False otherwise.
#             read_file: Reads a file. Returns the contents of the file.
#             write_prompt: Writes a prompt to a file.
#             view_all_files: Prints the names of all system prompts.
#             _handle_cmd: Handles a command, splitting the command from the argument, and passing the argument to a function reference. Protected method, should not be called outside of the class.
#         Menus:
#             load_file_menu_quick: A short menu for loading a prompt, outputting an error message if the prompt does not exist.
#             full_load_menu: A full self contained menu for loading a prompt, providing feedback to the user if the prompt does not exist and allowing them to view the prompt before loading it.
#             menu: Main menu for the system prompt menu, if a prompt is loaded, returns the prompt, otherwise returns None.
#             write_prompt_menu: A menu for writing a prompt, and saving it to a file.
       

#     Example Usage:
#         sys_prompt_manager = SystemPromptManager()
#         sys_prompt_menu = SystemPromptMenu(sys_prompt_manager)
#         loaded_prompt = sys_prompt_menu.menu()
#         if loaded_prompt is not None:
#             # do something with loaded_prompt
#         else:
#             # do something else, or exit


#     """

#     def __init__(self, sys_manager: SystemPromptManager):
#         self.logger = BaseLogger(
#             __file__,
#             level=DEFAULT_LOGGING_LEVEL,
#             identifier="SystemPromptMenu",
#             filename="sys_prompt_menu.log",
#         )
#         self.logger.info("Initializing SystemPromptMenu")
#         if not isinstance(sys_manager, SystemPromptManager):
#             raise exceptions.IncorrectObjectTypeError(
#                 "sys_manager must be of type SystemPromptManager"
#             )
#         self.sys_manager = sys_manager
#         self.loaded_prompt = None

#     @property
#     def all_files(self) -> list[str]:
#         """Returns a list of all system prompt files."""
#         return self.sys_manager.all_files

#     @property
#     def default_prompt(self) -> str:
#         """Returns the default prompt."""
#         return self.sys_manager.default_prompt

#     def check_file(self, filename: str) -> bool:
#         """Returns True if the file exists, False otherwise."""
#         return self.sys_manager.check_name(filename)

#     def read_file(self, filename: str) -> str:
#         """Returns the contents of a file."""
#         return self.sys_manager.get_prompt(filename)

#     def del_prompt(self, filename: str) -> None:
#         """Menu for deleting a prompt, providing feedback to the user if the prompt does not exist."""
#         if self.check_file(filename):
#             if confirm("Are you sure you want to delete this prompt? "):
#                 print("Deleting...")
#                 self.logger.info(f"Deleting prompt {filename}")
#                 self.sys_manager.delete_prompt(filename)
#             else:
#                 print("Exiting without deleting...")
#         else:
#             print("That prompt does not exist.")
#             print("Exiting...")

#     def write_prompt(self, filename: str, prompt: str, overwrite: bool = False) -> None:
#         """Writes a prompt to a file."""
#         self.sys_manager.write_prompt(filename, prompt, overwrite=overwrite)

#     def view_all_files(self) -> None:
#         """Prints the names of all system prompts."""
#         print("\n".join(self.all_files))

#     def view_file(self, filename: str) -> None:
#         """Prints the contents of a file, or prints an error message if the file does not exist."""
#         if self.check_file(filename):
#             print(self.read_file(filename))
#         else:
#             print("That prompt does not exist.")

#     def load_file_menu_quick(self, filename: str) -> None:
#         """A short menu for loading a prompt, outputting an error message if the prompt does not exist."""
#         if self.check_file(filename):
#             self.logger.info(f"Loading prompt {filename}")
#             self.loaded_prompt = self.read_file(filename)
#         else:
#             print("That prompt does not exist.")
#             self.loaded_prompt = None
#             self.logger.warning(f"Prompt {filename} does not exist.")

#     def full_load_menu(self):
#         """A full self contained menu for loading a prompt, providing feedback to the user if the prompt does not exist and allowing them to view the prompt before loading it."""
        

#     def write_prompt_menu(self, filename: str) -> None:
       # """A menu for writing a prompt, and saving it to a file."""
     

    

#     def menu(self) -> str | None:
#         """Main menu for the system prompt menu, if a prompt is loaded, returns the prompt, otherwise returns None."""
    
#         msg = "\n".join(msg_list)
#         cmds = {
#             "help": lambda: print(msg),
#             "list": lambda: self.view_all_files(),
#         }
#         print(msg)
#         while True:
#             ans = input(">")
#             ans_lower = ans.lower().strip()
#             if ans_lower in cmds:
#                 cmds[ans_lower]()
#             elif ans_lower in ("q", "quit", "exit"):
#                 print("Exiting...")
#                 return self.loaded_prompt
#             elif ans_lower.startswith("view"):
#                 self._handle_cmd(
#                     "view",
#                     ans_lower,
#                     self.view_file,
#                     error_msg_none="Please enter a prompt name.",
#                 )
#             elif ans_lower.startswith("load"):
#                 loaded = self._handle_cmd(
#                     "load",
#                     ans_lower,
#                     self.load_file_menu,
#                     error_msg_none="Please enter a prompt name.",
#                 )
#                 if confirm("File loaded successfully. Would you like to exit? "):
#                     return loaded
#             elif ans_lower.startswith("del"):
#                 self._handle_cmd(
#                     "del",
#                     ans_lower,
#                     self.del_prompt,
#                     error_msg_none="Please enter a prompt name.",
#                 )
#             elif ans_lower.startswith("write"):
#                 self._handle_cmd(
#                     "write",
#                     ans_lower,
#                     self.write_prompt_menu,
#                     error_msg_none="Please enter a prompt name.",
#                 )
#             else:
#                 print("Please enter a valid command.")
# class ChatLogExporter:
#     """Class for exporting a chat log to a file, abstracts away the process of exporting the chat log to a file.
#     Dependencies:
#         Custom: 
#             ChatLog (class): The chat log to export
#             MarkDownFileHandler (class): The file handler to use to save the data to a file
#             export_data (func): The function to use to export the data, abstracts the MarkDownExporter away from the chat.exporter module
#             Exception (module): Used for raising exceptions, see exceptions.py for more info
#             BaseLogger (class): Used for logging, see log_config.py for more info
#             DEFAULT_LOGGING_LEVEL (int): The default logging level to use, see log_config.py for more info
#         Python:
#             Path (class): Used for working with file paths
#             uuid (module): Used for generating a unique id for the chat log
#     Raises:
#         exceptions.IncorrectObjectTypeError: Raised if the chat log is not a ChatLog object or None(ie unset)
#         exceptions.ObjectNotSetupError: Raised if the chat log is not set and an attempt is made to export the data
#         exceptions.FileExistsError: Raised if the file already exists and overwrite is False by MarkDownFileHandler
#     Args:
#         chat_log_obj (ChatLog, optional): The chat log to export. Defaults to None, (can be set later using the chat_log property)
#         export_dir (str, optional): The directory to export the chat log to. Defaults to "../files/chats/". Will be created by MarkDownFileHandler if it does not exist.
#     Properties:
#         chat_log (ChatLog): The chat log to export
#         logger (BaseLogger): The logger to use, an instance of BaseLogger from log_config.py
#         export_dir (Path): The directory to export the chat log to. Defaults to "../files/chats/". Will be created by MarkDownFileHandler if it does not exist.
#         exporter (func): The function to use to export the data, abstracts the MarkDownExporter away from the chat.exporter module
#         markdown_file_handler (MarkDownFileHandler): The file handler to use to save the data to a file
#     Methods:
#         Setters and Getters:
#             chat_log (ChatLog): The chat log to export. Can be None(ie unset) to unset the chat log(however, attempting to export will raise an error))
#         Public/Core Methods:
#             check_if_file_exists(filename: str) -> bool: Checks if a file exists in the export dir. Can be a filename without the extension, or a filename with the extension. Will be added by MarkDownFileHandler if not provided.
#             save(file_name: str, overwrite: bool = False, system_prompt: str = None, **kwargs) -> None: Main method for saving the chat log to a file, calls the markdown file handler to save the data to a file. System prompt is optional, if not provided it will not be included in the markdown file. Any additional kwargs will be included in the header. See chat.exporter.py for more information on the header, as well as the export process.add()
#         Private Methods:
#             _check_chatlog() -> bool: Checks if the chat log is set, returns True if it is, False otherwise
#             _make_md_data(system_prompt: str = None, **kwargs) -> str: Creates the markdown data from the chat log, using the exporter function
#     Example Usage:
#         chat_wrapper = ChatWrapper(API_KEY, model="gpt-4")
#         chat_wrapper.auto_setup()
        
        
#         chat_wrapper.load_from_save_dict(save_dict)
#         print(chat_wrapper.chat("Hello"))
#         exporter = ChatLogExporter(chat_wrapper.chat_log)
#         if  not exporter.check_if_file_exists("test"):
#             exporter.save("test", overwrite=True)
#         else: 
#             print("File already exists")
    
            
        
#     """
#     def __init__(self, chat_wrapper_obj: ChatWrapper = None , export_dir: str = "../files/chats/"):
#         self.logger = BaseLogger(__file__, filename="chat_log_exporter.log", identifier="chat_log_exporter", level=DEFAULT_LOGGING_LEVEL)

#         self._chat_wrapper_obj: ChatWrapper = chat_wrapper_obj
#         if not export_dir.endswith("/"):
#             export_dir += "/"
#         # function to export the data, see chat.exporter.py for an example 
#         self.exporter = export_data 
#         self.markdown_file_handler = MarkDownFileHandler(save_folder=export_dir )
        
#         self.logger.debug("ChatLogExporter initialized")
#         self.export_dir = Path(export_dir)
#         self.export_dir.mkdir(parents=True, exist_ok=True)
#         self.export_dir = self.export_dir.resolve()
#         self.logger.debug(f"Export dir: {self.export_dir}")
#     def check_if_file_exists(self, filename: str) -> bool:
#         """Checks if a file exists in the export dir"""
#         return self.markdown_file_handler.check_if_file_exists(filename)
#     @property
#     def chat_log(self,):
#         """The chat log to export"""
        
#         return self._chat_log_obj
#     @chat_log.setter
#     def chat_wrapper(self, chat_log_obj: ChatWrapper):
#         """Sets the chat log to export Can be None(ie unset) to unset the chat log(however, attempting to export will raise an error))"""
#         if not isinstance(chat_log_obj, chat.ChatLog) and chat_log_obj is not None:
#             raise exceptions.IncorrectObjectTypeError("chat_log_obj must be a ChatLog object or None(ie unset))")
#         self.logger.debug(f"Setting chat log to {chat_log_obj}")
#         self._chat_log_obj = chat_log_obj
            
#         self._chat_log_obj = chat_log_obj
#     def _check_chatlog(self) -> bool:
#         """Checks if the chat log is set, returns True if it is, False otherwise"""
#         return isinstance(self.chat_log, chat.ChatLog)
#     def _make_md_data(self, system_prompt: str = None, **kwargs) -> str:
#         """Creates the markdown data from the chat log"""
#         if not self._check_chatlog():
#             raise exceptions.ObjectNotSetupError("Chat log exporter requires a chat log to export data. Set the chat log using the chat_log property")
#         return self.exporter(self.chat_log.data, system_prompt=system_prompt, **kwargs)
#     def save(self, filename: str, overwrite: bool = False, system_prompt: str = None, **kwargs) -> None:
#         """Main method for saving the chat log to a file, calls the markdown file handler to save the data to a file
#         Any kwargs are passed to the exporter function and will be included in header as metadata(underscores are replaced with spaces, title case). 
#         Note: System prompt is optional, if not provided it will not be included in the markdown file.
#         Overwrite: If True, will overwrite the file if it exists, otherwise will raise an error if the file exists.
#         """
#         self.logger.debug(f"Saving chat log to {filename}")
#         self.logger.debug(f"Overwrite: {overwrite}")
#         self.markdown_file_handler.write_to_file(contents = self._make_md_data(system_prompt=system_prompt, **kwargs), filename=filename, overwrite=overwrite)
#     def __repr__(self):
#         return f"ChatLogExporter(chat_log_obj={self.chat_log}, export_dir={self.export_dir})"
        

    