import exceptions
from chat.message import Message, MessageFactory
import func
import tiktoken
from typing import List, Dict, Union
import datetime
from collections import namedtuple
import uuid
from log_config import BaseLogger, DEFAULT_LOGGING_LEVEL

wildcard_info = namedtuple(
    "wildcard_info", "wildcard_name, wildcard_value, wildcard_description"
)
system_prompt_wildcards = {
    "model": wildcard_info("model", "__model__", "The name of the model."),
    "cut_off": wildcard_info(
        "cut_off", "September 21, 2021", "The cut off for the chat log."
    ),
    "date": wildcard_info("date", "__date__", "the current date."),
    "time": wildcard_info("time", "__time__", "the current time."),
}


class SystemPrompt:
    """Manages the system prompt for a chat log.
    Dependencies: func, exceptions, tiktoken, datetime, collections.namedtuple, uuid, Message (from chat.message), MessageFactory (from chat.message)

    Attributes:
        version (str): The version of the system prompt object.
        model (str): The name of the model.
        uuid (str): The uuid of the system prompt object(useful in debugging and logging).
        self.system_prompt (str): The system prompt, with wildcards
        self.system_prompt_tokens (int): The number of tokens in the system prompt.
        wildcard_info (namedtuple): A namedtuple containing information about a wildcard.
        system_prompt_wildcards (dict): A dictionary containing the wildcards for the system prompt.(represented as a namedtuple)
        system_prompt_message (Message): The system prompt as a Message object with wildcards added.
    Methods:
        Private:
            _add_wildcards_to_string(string: str) -> str: Adds wildcards to a string.
            _count_tokens_in_str(string: str) -> int: Counts the number of tokens in a string.
        Public:
            Getters and setters:
                system_prompt (str): The system prompt, with wildcards, getter and setter.
                system_prompt_tokens(int), system_prompt_message(Message): The number of tokens in the system prompt, and the system prompt as a Message object with wildcards added. Getters only
            Misc:
                __init__(model: str, system_prompt_content: str = None) -> None: Initialises the system prompt object. If system_prompt_content is None, the system prompt is set to None, and the system_prompt_tokens is set to None. Otherwise, the system prompt is set to system_prompt_content, and the system_prompt_tokens is set to the number of tokens in the system prompt, plus 20 (padding for the system prompt, as wildcards may be replaced with longer strings).
                __str__() -> str: Returns a string representation of the system prompt object.(Using Message.pretty)
                __repr__() -> str: Returns information about the system prompt object, including the model, uuid, system_prompt, and system_prompt_tokens.
        Example Usage:
            system_prompt = SystemPrompt('gpt-4')
            system_prompt.system_prompt = 'You are a helpful AI assistant. Your model is ||model||, todays date is  ||date||, and the time is  ||time||. Your training data was last updated on ||cut_off||.'
            sys_prompt_tokens = system_prompt.system_prompt_tokens
            response = send_to_api([system_prompt.system_prompt_message.data] + [list of messages from chat log])
            print(response)

    """

    version = "0.0.1"

    def __init__(self, model: str, system_prompt_content: str = None) -> None:
        self.model = model
        self.uuid = str(uuid.uuid4())
        self._system_prompt = system_prompt_content
        self.system_prompt = system_prompt_content
        self._system_prompt_tokens = None

    # for wildcard system (values replaced with wildcards in system prompt)
    wildcard_info = wildcard_info
    system_prompt_wildcards = system_prompt_wildcards

    def _add_wildcards_to_string(self, string: str) -> str:
        """Adds wildcards to the system prompt. Wildcards start with || and end with ||."""

        def add_chars(string: str):
            """Adds || to the beginning and || to the end of the string."""
            return f"||{string}||"

        wild_card_dict = {
            add_chars(name): value.wildcard_value
            for name, value in self.system_prompt_wildcards.items()
        }

        for name in wild_card_dict:
            if wild_card_dict[name] == "__model__":
                wild_card_dict[name] = self.model
            elif wild_card_dict[name] == "__date__":
                wild_card_dict[name] = datetime.date.today().strftime("%B %d, %Y")
            elif wild_card_dict[name] == "__time__":
                wild_card_dict[name] = datetime.datetime.now().strftime("%H:%M:%S")
            string = string.replace(name, wild_card_dict[name])
        return string

    @property
    def system_prompt(self) -> str:
        """Returns the system prompt with wildcards."""
        if self._system_prompt == None:
            return None
        return self._add_wildcards_to_string(self._system_prompt)

    @system_prompt.setter
    def system_prompt(self, system_prompt: str) -> None:
        """Sets the system prompt, and works out the number of tokens in the system prompt(plus padding).)"""
        self._system_prompt = system_prompt
        if system_prompt == None:
            self._system_prompt_tokens = None
        else:
            self._system_prompt_tokens = self._count_tokens_in_str(system_prompt) + 20
        # 20 is padding for the system prompt, as wildcards may be replaced with longer strings.

    @property
    def system_prompt_raw(self) -> str:
        """Returns the system prompt without wildcards."""
        return self._system_prompt

    @property
    def system_prompt_tokens(self) -> int:
        """Gets the number of tokens in the system prompt. If the system prompt is None, returns None. If for some reason the system prompt tokens are not set, it will set them."""
        if self.system_prompt == None:
            return 0
        elif self._system_prompt_tokens == None:
            self._system_prompt_tokens = (
                self._count_tokens_in_str(self.system_prompt_raw) + 20
            )
        return (
            self._system_prompt_tokens if self._system_prompt_tokens != None else 0 + 20
        )
    @property
    def has_system_prompt(self):
        return self._system_prompt is not None
    def _count_tokens_in_str(self, string: str) -> int:
        """Counts the number of token in a string using the model and the tiktoken library."""
        try:
            encoding = tiktoken.encoding_for_model(self.model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(string))

    @property
    def system_prompt_message(self) -> Message:
        """Generates a Message object from the system prompt, including wildcards."""
        if self.system_prompt == None:
            return None
        return Message(role="system", content=self.system_prompt, model=self.model)

    def __str__(self) -> str:
        """Returns the system prompt as a string, using the Message object's pretty property."""
        return self._system_prompt

    def __repr__(self) -> str:
        """Returns a representation of the SystemPrompt object, including the model, the number of tokens in the system prompt, the length of the system prompt, and the uuid."""
        constructor = f"SystemPrompt(model={self.model}, system_prompt_content={self._system_prompt_content})"
        info = f"SystemPrompt Object with model with {self.system_prompt_tokens} tokens, and a length of {len(self.system_prompt)} characters, and an id of {self.uuid}."
        return f"{constructor}\n{info}"


class Reminder:
    """Manages the reminder for a chat log.
    Works in a similar way to the SystemPrompt class.
    Dependencies:
        Custom:
            BaseLogger  and DEFAULT_LOGGING_LEVEL(from log_config)
            system_prompt_wildcards, wildcard_info (from this module)
            Message, MessageFactory (from chat.message)
            BadTypeError (from exceptions)
            
        Python:
            uuid
            datetime
            typing (for type hints)
            collections.namedtuple
    Raises:
        BadTypeError: Raised when the type of a variable is incorrect.
    Args:
        model (str): The name of the model.
        content (str): The content of the reminder.(Can be None)
        padding (int): The padding for the reminder(Extra tokens added to token count). Default: 10
        prepend (str): The prepend for the reminder(Added to the beginning of the reminder). Default: "Reminder: "
    Attributes:


        logger (BaseLogger): The logger for the Reminder object.
        version (str): The version of the Reminder object.
        _model (str): The name of the model.
        _reminder_content (str): The content of the reminder.(Private)
        _prepend (str): The prepend for the reminder. Default: "Reminder: "
        _padding (int): The padding for the reminder. Default: 10
        tokens (int): The number of tokens in the reminder.
        uuid (str): The uuid of the Reminder object.
    Methods:
        Getters:
            reminder_content (str): The content of the reminder.
            reminder_tokens (int): The number of tokens in the reminder.
            prepared_reminder (str): The reminder with wildcards and the prepend.
            is_reminder_set (bool): True if the reminder is set, False if it is not.
            prepend (str): The prepend for the reminder.(Added to the beginning of the reminder.)
            padding (int): The padding for the reminder.(Added to the number of tokens in the reminder.)
            model (str): The name of the model.
        Setters:
            set_reminder_content(value: str | None) -> None: Sets the reminder content. Can be either a string or None.
            Can also be set using the reminder_content property.
            model = value: Sets the model.
            prepend = value: Sets the prepend.
            padding = value: Sets the padding.
            
        Private:
            _add_wildcards_to_string(string: str) -> str: Adds wildcards to a string.
            _add_reminder_prepend(string: str) -> str: Adds the prepend to the reminder.
            _count_tokens(string: str) -> int: Counts the number of tokens in a string.
            _prepare_reminder(string: str) -> str: Adds wildcards and the prepend to the reminder.
            _recheck_tokens() -> None: Checks the number of tokens in the reminder. Used when the model, prepend, or padding is changed.
    Example Usage:
        reminder = Reminder('gpt-4')
        reminder.reminder = "You are a helpful AI assistant. Your model is ||model||, todays date is  ||date||, and the time is  ||time||. Your training data was last updated on ||cut_off||."
        print(reminder.reminder)
            Output:
                Reminder: You are a helpful AI assistant. Your model is gpt-4, todays date is {current_date}, and the time is  {current time}. Your training data was last updated on September 21, 2021.
                ((With current_date and current_time replaced with the current date and time.)))




    """

    version = "0.1.0"
    

    def __init__(self, model: str = "gpt-4", reminder_content: str = None, padding: int = 10, prepend: str = "System Reminder: ") -> None:
        self.logger = BaseLogger(
            module_name=__file__,
            level=DEFAULT_LOGGING_LEVEL,
            filename="reminder.log",
            identifier="reminder",
        )
        self.tokens = 0
        self._model = model
        self.reminder_content = reminder_content
        self.uuid = str(uuid.uuid4())
    
        self.padding = padding
        self.prepend = prepend
        self._recheck_tokens()

    system_prompt_wildcards = system_prompt_wildcards
    wildcard_info = wildcard_info
    @property
    def model(self) -> str:
        """Sets the model. Must be a string. Uses the _recheck_tokens method."""
        return self._model
    @model.setter
    def model(self, value: str) -> None:
        """Sets the model. Must be a string. Uses the _recheck_tokens method."""
        if not isinstance(value, str):
            raise exceptions.BadTypeError("Model must be a string.")
        self.logger.info(f"Setting model to {value}")
        self._model = value
        self._recheck_tokens()
    @property
    def prepend(self) -> str:
        """Returns the prepend for the reminder."""
        return self._prepend
    @prepend.setter
    def prepend(self, value: str):
        """Sets the prepend for the reminder. Must be a string. Uses the _recheck_tokens method."""
        if not isinstance(value, str):
            raise exceptions.BadTypeError("Prepend must be a string.")
        self.logger.info(f"Setting prepend to {value}")
        self._prepend = value
        self._recheck_tokens()
    @property
    def padding(self) -> int:
        """Returns the padding for the reminder."""
        
        return self._padding
    @padding.setter
    def padding(self, value: int):
        """Sets the padding for the reminder. Must be an integer. Uses the _recheck_tokens method."""
        if not isinstance(value, int):
            raise exceptions.BadTypeError("Padding must be an integer.")
        self.logger.info(f"Setting padding to {value}")
        self._padding = value
        self._recheck_tokens()

    def _add_wildcards_to_string(self, string: str) -> str:
        """Adds wildcards to the system prompt. Wildcards start with || and end with ||."""

        def add_chars(string: str):
            """Adds || to the beginning and || to the end of the string."""
            return f"||{string}||"

        wild_card_dict = {
            add_chars(name): value.wildcard_value
            for name, value in self.system_prompt_wildcards.items()
        }

        for name in wild_card_dict:
            if wild_card_dict[name] == "__model__":
                wild_card_dict[name] = self.model
            elif wild_card_dict[name] == "__date__":
                wild_card_dict[name] = datetime.date.today().strftime("%B %d, %Y")
            elif wild_card_dict[name] == "__time__":
                wild_card_dict[name] = datetime.datetime.now().strftime("%h:%M:%S")
            string = string.replace(name, wild_card_dict[name])
        return string

    def _add_reminder_prepend(self, string: str) -> str:
        """Adds the prepend to the reminder(The word reminder )."""
        return f"{self.prepend}{string}"

    def _count_tokens(self, string) -> int:
        """Counts the number of tokens in a string using the model and the tiktoken library."""
        model = self.model
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            self.logger.warning(f"Model {model} not found, using cl100k_base instead.")
            encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(string))

    def _prepare_reminder(self, string: str) -> str:
        """Adds wildcards and the prepend to the reminder."""
        return self._add_reminder_prepend(self._add_wildcards_to_string(string))
    def set_reminder_content(self, value: str | None ) -> None:
        """Sets the reminder content. Can be either a string or None."""
        if not isinstance(value, str) and value is not None:
            raise exceptions.BadTypeError("Reminder content must be a string or None.")
        log_value = f"Setting reminder content to {value}" if value else "Setting reminder content to None."
        self.logger.info(log_value)
        self._reminder_content = value
        self._recheck_tokens()
    @property
    def reminder_content(self) -> str:
        """Returns the reminder(without wildcards)."""
        return self._reminder_content
    @reminder_content.setter
    def reminder_content(self, value: str | None) -> None:
        """Sets the reminder content. Can be either a string or None. Uses the set_reminder_content method."""
        self.set_reminder_content(value)

    @property
    def prepared_reminder(self) -> str:
        """Returns the reminder(with wildcards)."""
        return self._prepare_reminder(self._reminder_content)
    
    def _recheck_tokens(self) -> None:
        """Counts the number of  tokens in the reminder. Sets the tokens attribute to the number of tokens in the reminder."""
        if not self.is_reminder_set:
            self.logger.info("Reminder not set, returning 0.")
            self.tokens = 0
            return 
        self.tokens = self._count_tokens(self.prepared_reminder)


    @property
    def is_reminder_set(self) -> bool:
        """Returns True if the reminder is set, False if it is not."""
        if self._reminder_content is not None:
            return True
        else:
            return False

    @property
    def reminder_as_message(self) -> Message:
        """Creates a Message object from the reminder(with wildcards)."""
        return Message(role="system", content=self.prepared_reminder, model=self.model)
