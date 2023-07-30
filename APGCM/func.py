import tiktoken
import json
import re
import logging 
import threading
import sys 
import time 




def count_tokens_in_str(string: str, model: str) -> int:
    """Returns the number of tokens in a string."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(string))


def get_test_chat_log(filename="short_2000_messages.json"):
    """Returns a chat log from the test data folder"""
    with open("testing/test_chat_logs/" + filename, "r") as f:
        chat_log = json.load(f)
    return chat_log


def toggle(b: bool) -> bool:
    """Disables b if it is enabled, and enables b if it is disabled. Dirt simple utility function."""
    return not b

def confirm(prompt: str = "Are you sure?", y_n = "(y/n)", y: str = "y", n: str = "n") -> bool:
    """Returns True if the user enters y, False if the user enters n. If the user enters anything else, the prompt is repeated until the user enters y or n.
    Args:
        - prompt (str, optional): The prompt to show the user. Defaults to "Are you sure?". Should not include the y_n arg.
        - y_n (str, optional): The string to show the user, indicating that they should enter either y or n. Defaults to "(y/n)". (will be appended to the prompt)
        y (str, optional): The string to enter to confirm. Defaults to "y".
        n (str, optional): The string to enter to deny. Defaults to "n".
    Returns:
        bool: True if the user enters y, False if the user enters n.
    Example Usage:
        if confirm("Are you sure you want to delete this file?"):
            delete_file()
        else:
            print("File not deleted.")
            
    """
    print(prompt + " " + y_n)
    while True:
        ans = input("> ").lower()
        if ans == y:
            return True
        elif ans == n:
            return False
        else:
            print(f"Invalid input, please enter either {y} or {n}")
def print_dir():
    """Prints the directory of the current file."""
    import os

    print(os.path.dirname(os.path.realpath(__file__)))


def print_file():
    """Prints the file name of the current file."""
    import os

    print(os.path.basename(__file__))


def bool_to_yes(b: bool, y: str = "Yes", n: str = "No") -> str:
    """Returns the string 'Yes' if b is True, and 'No' if b is False.
    Example:
        is_lights_on = True
        print("Are the lights on?", bool_to_yes(is_lights_on)
    """
    if b:
        return y
    else:
        return n


class InputHandler:
    """A class for handling user input, namely for chunking input. 
    Chunking in this context, refers to the process of appending a user input to a list, and returning the list as a string when the user submits an empty string.
    This is useful as many terminals have a limit on the number of characters that can be entered at once, and this allows the user to enter more characters than the limit.
    Also supports resetting the input if user makes a mistake and wants to start over.
    
    Args:
        prompt (str, optional): The prompt to show the user(in the input() func ). Defaults to "> ".
        ini_message (str, optional): The initial message to show the user, before input loop Defaults to "Type enter twice when done". Can be disabled by setting to None or an empty string.
        
        reset_commands (list | tuple, optional): The commands to reset the input. Defaults to ["reset", "restart", "discard"]. Can be disabled by setting to None or an empty list.
        reset_cmd_message (str, optional): The message to show the user when showing the reset commands. Defaults to "To discard input and restart, enter one of the following commands: (followed by reset commands joined with ', ')".
        show_reset_commands (bool, optional): Whether to show the reset commands. Defaults to True.
        chunk_glue (str, optional): The string to use to join the chunks. Defaults to " ".
        chunking (bool, optional): Whether to use chunking. Defaults to True. If false a normal input() is used.
    Properties:
        _chunking (bool) (private): Whether to use chunking. Defaults to True. If false a normal input() is used.
        ...all other properties are public and named the same as their args in __init__...
    Dependencies:
        bool_to_yes (func): Returns the string 'Yes' if b is True, and 'No' if b is False. Simple utility function.
        
    
    Methods:
        Getters and Setters:
            chunking (bool): Whether to use chunking. Defaults to True. If false a normal input() is used.
            (When using setter chunking MUST be a boolean, otherwise a TypeError is raised)
        Public/Core Methods:
            toggle_chunking(show_message: bool = True) -> None: Toggles chunking on or off(ie the opposite of the current setting ). If show_message is True, a message is printed to the console.
            
            __call__() -> str | None: Returns the user input joined with chunk_glue if chunking is True, otherwise returns the user input.
    Private Methods:
        _handle_reset(user_input: str) -> bool: Returns if reset_commands is not an empty list and user_input is in reset_commands, otherwise returns False.
        _show_reset_commands() -> None: Prints the reset commands if show_reset_commands is True.
        _show_ini_message() -> None: Prints the initial message if ini_message is not None and not an empty string.
        _get_user_input() -> str: Chunking loop, returns the user input joined with chunk_glue when the user submits an empty string. Called by __call__() if chunking is True.
    Example Usage:
        While True:
            input_handler = InputHandler()
            user_input = input_handler()
            if user_input.lower() == "toggle chunking":
                input_handler.toggle_chunking()
                continue
            ...other logic here...
        
    """
    def __init__(
        self,
        prompt: str = "> ",
        ini_message: str = "Type enter twice when done",
        reset_commands: list | tuple = None,
        show_reset_commands: bool = True,
        reset_cmd_message: str = "To discard input and restart, enter one of the following commands: ",
        reset_message: str = "Discarding input...",
        chunk_glue=" ",
        chunking: bool = True,
    ):
        self.input_prompt = prompt
        self.ini_message = ini_message
        self.show_reset_commands = show_reset_commands
        self.reset_commands = (
            reset_commands if reset_commands else ["reset", "restart", "discard"]
        )
        self.reset_cmd_message = reset_cmd_message
        self._chunking = chunking
        self.chunk_glue = chunk_glue
        self.reset_message = reset_message

    def _handle_reset(self, user_input: str) -> bool:
        """Returns True if the user wants to reset, False otherwise"""
        if user_input.lower() in self.reset_commands:
            print(self.reset_message)
            return True
        else:
            return False

    def _show_reset_commands(self):
        """Prints the reset commands"""
        if self.show_reset_commands:
            print(self.reset_cmd_message + ", ".join(self.reset_commands))

    def _show_ini_message(self):
        """Prints the initial message"""
        if self.ini_message is not  None and self.ini_message != "":
            print(self.ini_message)

    def _get_user_input(self) -> str:
        self._show_ini_message()
        self._show_reset_commands()
        result = []
        while True:
            user_input = input(self.input_prompt)
            if self._handle_reset(user_input):
                result = []
                self._show_ini_message()
                self._show_reset_commands()
                continue
            if user_input == "":
                return self.chunk_glue.join(result)
            result.append(user_input)

    def toggle_chunking(self, show_message: bool = True):
        """If chunking is True, it becomes False, and vice versa. If show_message is True, a message is printed to the console, explaining the new state of chunking."""
        self._chunking = not self._chunking
        if show_message:
            print(f"Chunking is now {bool_to_yes(self._chunking, 'On', 'Off')}")

    @property
    def chunking(self) -> bool:
        return self._chunking

    @chunking.setter
    def chunking(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("Chunking must be a boolean")
        self._chunking = value

    def __call__(self) -> str:
        """Returns the user input, or None if the user wants to reset"""
        if self.chunking:
            return self._get_user_input()
        else:
            return input(self.input_prompt)

chunk_input = InputHandler(chunking=True)


def is_filename_valid(filename: str) -> bool:
    """
    Check if a filename is valid.

    Args:
        filename: The filename to check.

    Returns:
        True if the filename is valid, False otherwise.
    """
    if not isinstance(filename, str):
        return False
    bad_chars = ["/", "\\", "?", "%", "*", ":", "|", '"', "<", ">"]
    if any(char in filename for char in bad_chars):
        return False
    return True
def convert_level_to_value(logging_level: str) -> int:
    """Converts a logging level name to its value. Returns None if the logging level is invalid."""
    if isinstance(logging_level, int):
        return logging_level # already a value
    levels = {
        "CRITICAL": logging.CRITICAL,
        "ERROR": logging.ERROR,
        "WARNING": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
    }
    if logging_level.upper() in levels:
        return levels[logging_level.upper()]
    else:
        return logging.WARNING # default to warning if invalid
    
class LoadingSpinner:
    """A simple loading spinner, used to show the user that something is loading. Can be used as a context manager or manually with start() and stop().
    Dependencies:
        time (module): Used for sleeping.
        threading (module): Used for threading.
        sys (module): Used for writing to stdout.
        typing (module): Used for type hinting.(Self)
    Args:
        Message (str, optional): The message to show the user along with the spinner. Defaults to "Loading...".
    Attributes:
        message (str): The message to show the user along with the spinner.
        event (threading.Event): The event used to stop the spinner.
        thread (threading.Thread): The thread used to run the spinner.
        
    Methods:
        _spin() -> None: The function that runs the spinner. Called by start(). (Private)
        start() -> None: Starts the spinner.
        Stop() -> None: Stops the spinner. And clears the spinner from the console along with the message.
        __enter__() -> self: Starts the spinner. (Called when used as a context manager)
        __exit__() -> None: Stops the spinner. (Called when used as a context manager)
    Example Usage:
        with LoadingSpinner("Loading..."):
            something_that_takes_a_while()
        print("Done! No more loading spinner!")
    """
    def __init__(self, message: str = "Loading..."):
        self.message = message
        self.event = threading.Event()
        
    def _spin(self) -> None:
        """The function that runs the spinner. Called by start(). (Private)"""
        while not self.event.is_set():
            for char in "|/-\\":
                sys.stdout.write(f"\r{self.message} {char}")
                sys.stdout.flush()
                time.sleep(0.1)
                sys.stdout.write("\b \b")
                sys.stdout.flush()
    def start(self) -> None:
        """Starts the spinner."""
        self.event.clear()
        self.thread = threading.Thread(target=self._spin)
        self.thread.start()
       
    def stop(self) -> None: 
        """Stops the spinner. And clears the spinner from the console along with the message."""
        self.event.set()
        self.thread.join()
        sys.stdout.write("\r" + ( " " * (len(self.message) + 2)))
        sys.stdout.write("\r")
        sys.stdout.write("\n")
        sys.stdout.flush()
    def __repr__(self) -> str:
        return f"LoadingSpinner(message={self.message})"
    #==(Context Manager Protocol)==
       
    def __enter__(self):
        """Called when used as a context manager. Starts the spinner. 
       
        I  can't imagine a what you would do to this class within the context manager, but hey, it's there if you need it."""
        self.start()
        return self 
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Called when used as a context manager. Stops the spinner. Does nothing with the exception info."""
        self.stop()
def quick_make_chat_wrapper(self):
    """This will make a chat wrapper with the defaults you have set in your .env file. Useful for testing and if you don't want to use any of the customization options in the ChatFactory class."""
    from templates.cw_factory import ChatFactory
    fact = ChatFactory()
    return fact.get_chat()
