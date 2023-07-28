import chat
import exceptions
import uuid

import datetime

from log_config import BaseLogger, DEFAULT_LOGGING_LEVEL
from typing import List, Dict, Union, Optional, Any, Tuple, Generator, Iterable
from collections import deque, namedtuple
from enum import Enum

class MessageReturnType(Enum):
    DICT = "dict"
    MESSAGE = "message"
    STRING = "string"




class TrimChatLog:

    """ 
    TrimChatLog is a class that is used to trim a chat log to a certain number of tokens, and acts as a wrapper for the chatlog, message, and system prompt classes.
    Dependencies:
        Custom:
            chat.ChatLog -> The chat log object, see chatlog.py for more information.
            chat.SystemPrompt -> The system prompt object, see system_prompt.py for more information.
            chat.MessageFactory -> The message factory object, see message.py for more information, can be retrieved with the get_message_factory method.
            chat.Message -> The message object, see message.py for more information.
            exceptions -> Custom exceptions
            log_config -> Logging object for logging(pre-configured logging object )
        Python:
            uuid -> For generating uuids
            datetime -> For getting the current time
            typing -> For type hinting
            collections -> deque and namedtuple for the trimmed chat log
        Args:
            model= "gpt-4": The model to use for the chatlog, message, and system prompt objects. Required to correctly count the number of tokens in a string. Defaults to "gpt-4".
            system_prompt: The system prompt string. Optional but recommended. Can be set later using the system_prompt property.
            chatlog: The chatlog object. Optional, defaults to a new chatlog object.
            max_tokens=8000: The max amount of tokens allowed in the trimmed chatlog, gets set to 8000 by default(max for gpt-4)
            max_messages=200: The max amount of messages allowed in the trimmed chatlog, gets set to 200 by default. Can be disabled by setting to None.
            max_completion_tokens=1000: The max amount of tokens allowed in a completion, gets set to 1000 by default.
            token_padding=500: The amount of tokens subtracted from the max tokens to allow for the system prompt, gets set to 500 by default(everything, including model params is counted as a token so this helps prevent errors)
        Attributes:
            Objects:
                chatlog: The chatlog object, see chatlog.py for more information.
                logger: BaseLogger The logger object for logging(pre-configured logging object )
                MessageFactory: The message factory object, see message.py for more information, can be retrieved with the get_message_factory method.
                system_prompt_object: The system prompt object, see system_prompt.py for more information.
            Booleans:
                is_set_up: Weather or not the tokens have been worked out and the class is ready to use
                is_sys_set: Weather or not the system prompt has been set
                is_loaded: Weather or not the chatlog has been loaded from a save dict
            Debug and Identification:
                version: The version of the class
                uuid: The uuid of the instance, used to save the chatlog, for debugging purposes and to identify the chatlog.
            Token Information:
                trimmed_chatlog_tokens: The number of tokens in the trimmed chatlog
                max_tokens(int): The max amount of tokens allowed in the trimmed chatlog, gets set to 8000 by default(max for gpt-4)
                token_padding(int): The amount of tokens subtracted from the max tokens to allow for the system prompt, gets set to 500 by default(everything, including model params is counted as a token so this helps prevent errors)
                max_chatlog_tokens(int): The number of tokens that can be in the chat log, calculated by the work_out_tokens method.
                max_completion_tokens: The max amount of tokens allowed in a completion, gets set to 1000 by default.
                max_messages(int): The max amount of messages allowed in the trimmed chatlog, gets set to 200 by default.
                max_tokens(int): The max amount of tokens allowed in the trimmed chatlog, gets set to 8000 by default(max for gpt-4)
            Trim Information:
                trimmed_messages(int): The number of messages trimmed from the chatlog
                most_recent_trimmed_message(Message): The last message trimmed from the chatlog
            Misc:
                _system_prompt_string: The system prompt string.
                _model: The model to use for the chatlog, message, and system prompt objects. Required to correctly count the number of tokens in a string.
                most_recent_message(Message): The last message added to the chatlog.
            Setters and Getters:
                system_prompt: The system prompt, can be set with the set_system_prompt method or the system_prompt property.
                    Returns as a Message object.
                    Set as a string.
                model: The model, can be set with the set_model method or the model property.
                system_prompt_tokens: The number of tokens in the system prompt, returns 0 if the system prompt is not set.
                    No setter.
                assistant_message, user_message(str)- convenience methods for adding/retrieving  user or assistant messages to the log as strings.
                assistant_message_as_Message, user_message_as_Message(Message)- convenience methods for adding/retrieving  user or assistant messages to the log as Message objects.
        Methods:
            Core:
                add_message: Adds a message to the chatlog, and trims the chatlog if it is too long.
                work_out_tokens: Works out the number of tokens in the chatlog and system prompt.
                trim_chatlog: Trims the chatlog to the correct length.
                get_finished_chatlog: Returns the chatlog as a list of dictionaries (with system prompt) ready to be sent to the API.


            Adding / Getting Messages:
                add_messages: Adds a list of messages to the chatlog.
                add_messages_from_dict: Adds a list of messages from a list of dictionaries to the chatlog.


                get_trimmed_messages_as_dict: Returns messages as a list of dictionaries.using the get_trimmed_messages method.
                More methods for getting messages can be found in the chatlog class.
            Saving and Loading:
                make_save_dict: Returns a dictionary containing all the information needed to load the object's state.
                load_from_save_dict: Loads the object's state from a save dict.
                _check_save_dict: Verifies that a save dict is valid. Private method. Private.
            Misc:
                _check_message: Checks that a message is valid. Private method.
                get_message_factory: Returns the message factory object, used to create messages with the correct model.
                __repr__: Returns a string representation of the object.
                __str__: Returns a pretty string of the entire chat log, using the __str__ method of the chatlog object.
        Example Usage:
            trim_chat_log = TrimChatLog()
            trim_chat_log.user_message = "Hello"
            trim_chat_log.assistant_message = "Hi"
            send_to_api(trim_chat_log.get_finished_chatlog())
            save_dict = trim_chat_log.make_save_dict()
            save_to_file(save_dict, "save_dict.json")
    """

    version = "0.2.0"

    def __init__(
        self,
        model: str = "gpt-4",
        system_prompt: str = None,
        chatlog: chat.ChatLog = None,
        
        max_tokens: int = 8000,
        max_messages: int = 200,
        max_completion_tokens: int = 1000,
        token_padding: int = 500,
        auto_setup_chatlog: bool = True
    ) -> None:
        self.logger = BaseLogger(
           module_name= __file__,
            filename="trim_chat_log.log",
            level=DEFAULT_LOGGING_LEVEL,
            identifier="TrimChatLog",
        )
        self.logger.info(f"TrimChatLog version: {str(self.version)} Initialized.")
        self._model = model
        self.trimmed_chatlog = deque()
        self.is_set_up = False
        self.trimmed_chatlog_tokens = 0
        self.most_recent_trimmed_message: chat.Message = None
        self.most_recent_message: chat.Message = None
        
        if not isinstance(chatlog, chat.AbstractChatLog) and chatlog is not None:
            raise exceptions.IncorrectObjectTypeError(
                "The chatlog is not a chatlog object. Please use the chat.ChatLog class to create a chatlog, or get a factory using the get_chatlog_factory method."
            )
        if chatlog is not None:
            chatlog.model = model
        self._system_prompt_string = system_prompt
        if system_prompt is None:
            self.system_prompt_object: chat.SystemPrompt = chat.SystemPrompt(model)
            self.is_sys_set = False
        else:
            self._system_prompt_string = system_prompt
            self.system_prompt_object: chat.SystemPrompt = chat.SystemPrompt(
                model, system_prompt
            )
            self.is_sys_set = True
        if auto_setup_chatlog and chatlog is None:
            self.auto_make_chatlog()
        
        self.uuid = str(uuid.uuid4())
        self.chatlog = chatlog
        self.max_tokens = max_tokens
        self.max_messages = max_messages
        self.max_completion_tokens = max_completion_tokens
        self.token_padding = token_padding
        self.message_factory = chat.MessageFactory(model)
        self.max_chatlog_tokens = 0
        self.work_out_tokens()
        self.trimmed_messages = 0

        self.is_loaded = False
    def add_chatlog(self, chatlog: chat.AbstractChatLog) -> None:
        """Sets the chatlog object. Can be unset by passing None."""
        if not isinstance(chatlog, chat.AbstractChatLog) and  chatlog is not  None:
            raise exceptions.IncorrectObjectTypeError(
                "The chatlog is not a chatlog object. Please use the chat.ChatLog class to create a chatlog, or get a factory using the get_chatlog_factory method."
            )
        if chatlog is None:
            self.logger.info("Unsetting chatlog")
        self.chatlog = chatlog
        self.logger.info("Chatlog set to: " + repr(chatlog))
    def _has_chatlog(self) -> bool:
        if self.chatlog is None:
            return False
        return True
    def auto_make_chatlog(self) -> None:
        """Makes a chatlog object using the default user list concrete chatlog class, if one is provided in save dict."""
        self.logger.info("Auto making chatlog")
        self.chatlog = chat.ChatLog(model=self.model)
    @property
    def system_prompt_tokens(self) -> int:
        """Using the SystemPrompt object, returns the number of tokens in the system prompt. If the system prompt is not set, returns 0."""
        if self.is_sys_set is False:
            return 0
        else:
            return self.system_prompt_object.system_prompt_tokens

    @property
    def system_prompt(self) -> chat.Message:
        """Returns the system prompt as a message object. If the system prompt is not set, returns None, and if the system prompt is set, returns a message object using the SystemPrompt Object"""
        if self.is_sys_set is False:
            return None
        else:
            return self.system_prompt_object.system_prompt_message

    @system_prompt.setter
    def system_prompt(self, system_prompt: str) -> None:
        """Sets the system prompt. If the system prompt is not set, sets the system prompt object, and then works out the tokens. If the system prompt is set, changes the system prompt object, and then works out the tokens."""
        self._system_prompt_string = system_prompt
        self.system_prompt_object = chat.SystemPrompt(self.model, system_prompt)
        self.logger.info("System prompt set to: " + system_prompt)
        self.work_out_tokens()
        self.is_sys_set = True

    @property
    def model(self) -> str:
        """Returns the model for the chat log."""
        return self._model

    @model.setter
    def model(self, model: str) -> None:
        """Sets the model for the chat log, and then changes all objects in the class and works out tokens again."""
        self._model = model
        self.system_prompt_object.model = model
        if self._has_chatlog():
            self.chatlog.model = model
        self.logger.info("Model set to: " + model)
        self.message_factory.set_model(model)
        self.work_out_tokens()
        self.trim_chatlog()

    def work_out_tokens(self) -> None:
        """Works out the max tokens that can be used for the chat log. One of the core methods of this class."""
        self.is_set_up = True
        system_prompt_tokens = self.system_prompt_tokens if self.is_sys_set else 0
        max_tokens = self.max_tokens
        token_padding = self.token_padding
        max_completion_tokens = self.max_completion_tokens
        self.max_chatlog_tokens = max_tokens - (
            system_prompt_tokens + token_padding + max_completion_tokens
        )
        self.logger.info("Max chatlog tokens set to: " + str(self.max_chatlog_tokens))
        if self.max_chatlog_tokens < 0:
            self.logger.warning("Max chatlog tokens is less than 0, setting to 1000")
            self.max_chatlog_tokens = 1000
    def get_message_factory(self, role: str = None) -> chat.MessageFactory:
        """Returns a message factory for the chat log."""
        self.message_factory = chat.MessageFactory(self.model)
        return self.message_factory

    def _check_message(self, message: chat.Message) -> chat.Message:
        """Checks the message is valid."""
        if not isinstance(message, chat.Message):
            self.logger.error("Message is not a message object.")
            raise exceptions.NotAMessageError(
                "The message is not a message object. Please use the chat.Message class to create a message, or get a factory using the get_message_factory method."
            )
        return message

    def add_message(self, message: chat.Message) -> None:
        """Adds a message to the chat log. Only accepts Message objects. One of the core methods of this class."""
        message = self._check_message(message)
        self.trimmed_chatlog_tokens += message.tokens
        if self._has_chatlog():
            self.chatlog.add_message(message)
        self.most_recent_message = message
        self.trimmed_chatlog.append(message)

        self.trim_chatlog()
    def reset(self)-> None:
        """Resets the chatlog but keeps the system prompt"""
        if self._has_chatlog():
            self.chatlog.reset()
        self.trimmed_chatlog = deque()
        self.most_recent_message = None
        self.most_recent_trimmed_message = None
        self.trimmed_chatlog_tokens = 0 
        self.trimmed_messages = 0
        self.is_loaded = False
        self.logger.info("Chatlog reset")
    def recount_tokens(self) -> None:
        """Recounts the tokens in the chatlog"""
        self.trimmed_chatlog_tokens = 0
        for msg in self.trimmed_chatlog:
            self.trimmed_chatlog_tokens += msg.tokens
        self.logger.info("Recounted tokens, new token count: " + str(self.trimmed_chatlog_tokens))
    def trim_chatlog(self) -> None:
        """
        Trims a chat log to the max tokens and max messages.
        Core method of this class
        """
        while self.trimmed_chatlog_tokens > self.max_chatlog_tokens and len(self.trimmed_chatlog) > 0:
            trimmed_message: chat.Message = self.trimmed_chatlog.popleft()
            self.most_recent_trimmed_message = trimmed_message
            self.trimmed_messages += 1
            self.trimmed_chatlog_tokens -= trimmed_message.tokens

        if self.max_messages is not None:
            while len(self.trimmed_chatlog) > self.max_messages:
                trimmed_message = self.trimmed_chatlog.popleft()
                self.most_recent_trimmed_message = trimmed_message
                self.trimmed_chatlog_tokens -= trimmed_message.tokens
                self.trimmed_messages += 1
        if self.trimmed_chatlog_tokens < 0:
            self.trimmed_chatlog_tokens = 0
        if self.trimmed_messages < 0:
            self.trimmed_messages = 0
       

    def get_trimmed_messages_as_dict(
        self, role: str = None, limit: int = None, reverse: bool = False
    ) -> list[dict]:
        """Gets the trimmed messages as a list of dictionaries for use with the API.
        Args:
            role: Optional filtering by role.add()
            limit: Optional limit to the number of messages returned.
            reverse: Optional reverse the order of the messages.
        Returns:
            A list of dictionaries containing the keys 'role' and 'content' for each message.

        Only works on the trimmed chat log, use methods in chatlog to get messages from the full chat log
        """
        result = []
        chatlog = self.trimmed_chatlog[::-1] if reverse else self.trimmed_chatlog
        count = 0
        for message in chatlog:
            if role is None or message.role == role:
                result.append(message.as_dict())
                count += 1
            if limit is not None and count >= limit:
                break
                
        return result
    

    def get_finished_chatlog(self) -> list[dict]:
        """Returns the finished chat log, with the system prompt as a list of dictionaries for use with the API"""
        if self.is_sys_set is False:
            return self.get_trimmed_messages_as_dict()
        system_prompt = self.system_prompt.as_dict()
        trimmed_chat_log = self.get_trimmed_messages_as_dict()
        return [system_prompt] + trimmed_chat_log
    @property
    def finished_chatlog(self) -> list[dict]:
        """Using the get_finished_chatlog method, returns the finished chat log, with the system prompt as a list of dictionaries for use with the API"""
        return self.get_finished_chatlog()

    def add_messages(self, lst: list[chat.Message]) -> None:
        """Adds a list of messages to the chat log."""
        for message in lst:
            self.add_message(message)

    def add_messages_from_dict(self, lst: list[dict]) -> None:
        """Adds a list of messages from a list of dictionaries to the chat log."""
        for message in lst:
            self.add_message(self.message_factory(**message))

    def make_save_dict(self) -> dict:
        """Makes a save dictionary for the chat log."""
        self.logger.info("Making save dict.")
        d =  {
            "model": self.model,
            "system_prompt": self.system_prompt_object.system_prompt_raw
            if self.is_sys_set
            else None,
            "token_info": {
                "max_tokens": self.max_tokens,
                "max_messages": self.max_messages,
                "max_completion_tokens": self.max_completion_tokens,
                "token_padding": self.token_padding,
                "max_chatlog_tokens": self.max_chatlog_tokens,
            },
            "trimmed_chatlog_tokens": self.trimmed_chatlog_tokens,
            "trimmed_messages": self.trimmed_messages,
            "uuid": self.uuid,
            "is_sys_set": self.is_sys_set,
            "most_recent_message": self.most_recent_message.as_dict()
            if self.most_recent_message is not None
            else None,
            "most_recent_trimmed_message": self.most_recent_trimmed_message.as_dict()
            if self.most_recent_trimmed_message is not None
            else None,
            "is_set_up": self.is_set_up,
            "timestamp": str(datetime.datetime.now().timestamp()),
            
            "trimmed_chatlog": self.get_trimmed_messages_as_dict(),
        }
        if self._has_chatlog():
            d["chatlog"] = self.chatlog.make_save_dict()
        else:
            d["chatlog"] = None
        return d
    def _check_save_dict(self, save_dict: dict) -> dict:
        """Checks that a save dictionary is valid and has the correct keys. Raises BadSaveDictionaryError if not. Returns the save dictionary if it is valid."""
        if not isinstance(save_dict, dict):
            raise exceptions.BadSaveDictionaryError(
                "Trimmed ChatLog must be a dictionary not." + str(type(save_dict)) + "."
            )
        required_keys = {
            
            "model": str,
            "trimmed_chatlog": list,
            "trimmed_chatlog_tokens": int,
            "trimmed_messages": int,
            "uuid": str,
            "is_sys_set": bool,
            "most_recent_message": dict,
            "most_recent_trimmed_message": dict,
            "is_set_up": bool,
            "system_prompt": str,
            "token_info": dict,
        }
        for key, value in required_keys.items():
            if key not in save_dict:
                raise exceptions.BadSaveDictionaryError(
                    "Trimmed ChatLog must have a key called " + key + "."
                )
            if not isinstance(save_dict[key], value) and save_dict[key] is not None:
                raise exceptions.BadSaveDictionaryError(
                    "Trimmed ChatLog key " + key + " must be a " + str(value) + "."
                )
        if save_dict['chatlog'] is not None:
            if not isinstance(save_dict['chatlog'], dict):
                raise exceptions.BadSaveDictionaryError("Chatlog must be a dictionary or None.")
        required_keys = {
            "max_tokens",
            "max_messages",
            "max_completion_tokens",
            "token_padding",
            "max_chatlog_tokens",
        }
        missing_keys = save_dict["token_info"].keys() - required_keys
        if len(missing_keys) > 0:
            raise exceptions.BadSaveDictionaryError(
                "Trimmed ChatLog token_info must have keys "
                + " ,".join(required_keys)
                + "."
                + " Missing keys: "
                + " ,".join(missing_keys)
                + "."
            )
        for key, value in save_dict["token_info"].items():
            if not isinstance(value, int):
                raise exceptions.BadSaveDictionaryError(
                    "Trimmed ChatLog key " + key + " must be an integer."
                )
        return save_dict

    def load_from_save_dict(self, save_dict: dict) -> None:
        """Loads a chat log from a save dictionary."""
        save_dict = self._check_save_dict(save_dict)
        # will raise an error is the save dict is bad, so we can assume it is good from here on out.
        self.logger.info("Loading from save dict.")
        if save_dict["chatlog"] is not None:
            if not  self._has_chatlog():
                self.logger.warning("Chatlog is not set, auto making chatlog. If you want to use a custom chatlog, set it before loading from a save dict.")
                self.auto_make_chatlog()
            self.chatlog.load_from_dict(save_dict["chatlog"])
        self.uuid = save_dict["uuid"]
        self.is_sys_set = save_dict["is_sys_set"]
        if save_dict["is_sys_set"] is True:
            self.system_prompt = save_dict["system_prompt"]
        self.trimmed_chatlog_tokens = save_dict["trimmed_chatlog_tokens"]
        self.trimmed_messages = save_dict["trimmed_messages"]
        self.model = save_dict["model"]
        self.trimmed_chatlog = deque(
            [
                self.message_factory(**message)
                for message in save_dict["trimmed_chatlog"]
            ]
        )
        self.most_recent_message = (
            self.message_factory(**save_dict["most_recent_message"])
            if save_dict["most_recent_message"] is not None
            else None
        )
        self.most_recent_trimmed_message = (
            self.message_factory(**save_dict["most_recent_trimmed_message"])
            if save_dict["most_recent_trimmed_message"] is not None
            else None
        )
        self.is_loaded = True
        self.is_set_up = save_dict["is_set_up"]
        self.max_chatlog_tokens = save_dict["token_info"]["max_chatlog_tokens"]
        self.max_completion_tokens = save_dict["token_info"]["max_completion_tokens"]
        self.max_messages = save_dict["token_info"]["max_messages"]
        self.max_tokens = save_dict["token_info"]["max_tokens"]
        self.token_padding = save_dict["token_info"]["token_padding"]
    
    @property
    def user_message(self) -> str | None:
        """Returns the user message."""
        result =  self.get_messages_as_list(role="user", limit=1, reverse=True, format=MessageReturnType.STRING)
        if len(result) > 0:
            return result[0]
        return None

    @user_message.setter
    def user_message(self, value: str) -> None:
        """Adds a user message to the chat log, as a string"""
        message = self.message_factory(content=value, role="user")
        self.add_message(message)

    @property
    def user_message_as_Message(self) -> chat.Message:
        """Adds a user message to the chat log, as a Message object."""
        for msg in self.get_messages(role="user", limit=1, reverse=True):
            if msg is not None:
                return msg
        return None

    @user_message_as_Message.setter
    def user_message_as_Message(self, value: chat.Message) -> None:
        """Adds a user message to the chat log, as a Message object."""
        self.add_message(value)

    @property
    def assistant_message(self) -> str:
        """Returns the  last assistant message as a string."""
        
        for msg in self.get_messages(role="assistant", limit=1, reverse=True):
            return msg.content if msg is not None else None
        return None

    @assistant_message.setter
    def assistant_message(self, value: str) -> None:
        """Adds an   assistant message as a string."""
        return self.add_message(self.message_factory(content=value, role="assistant"))

    @property
    def assistant_message_as_Message(self) -> chat.Message:
        """Returns the assistant message as a Message object."""
        for msg in self.get_messages_as_list(role="assistant", limit=1, reverse=True,format=MessageReturnType.MESSAGE ):
            return msg
        return None

    @assistant_message_as_Message.setter
    def assistant_message_as_Message(self, value: chat.Message) -> None:
        """Adds an assistant message to the chat log, as a Message object."""
        self.add_message(value)
    def get_messages(self,  role: str = None, limit: int = None, reverse: bool = True ) -> Iterable[chat.Message]:
        """Gets the messages from the chatlog as a list of Message objects."""
        chatlog = reversed(self.trimmed_chatlog) if reverse else self.trimmed_chatlog
        counter = 0 
        for msg in chatlog:
            if role is None or msg.role == role:
                yield msg
                limit -=1
            if limit is not None and limit >0:
                
                break
    def get_messages_as_list(self, role: str = None, limit: int = None, reverse: bool = True, format: str = MessageReturnType.MESSAGE) -> List[chat.Message | dict | str]:
        """Returns the messages from the chatlog as a list of Message objects, dictionaries, or strings.
        Possible formats are:
            MessageReturnType.MESSAGE: Returns the messages as Message objects.
            MessageReturnType.DICT: Returns the messages as dictionaries.
            MessageReturnType.STRING: Returns the messages as strings.
        
        """
        result = []
       
        for msg in self.get_messages(role=role, limit=limit, reverse=reverse):
            if format == MessageReturnType.MESSAGE:
                result.append(msg)
            elif format == MessageReturnType.DICT:
                result.append(msg.as_dict())
            elif format == MessageReturnType.STRING:
                result.append(msg.content)
            else:
                raise exceptions.BadMessageReturnTypeError("Invalid message return type: " + str(format))
        return result

            
    def set_token_info(
        self,
        max_tokens: int = None,
        max_messages: int = None,
        max_completion_tokens: int = None,
        token_padding: int = None,
    ) -> None:
        """Sets the token info for the chat log."""
        if max_tokens is not None:
            self.max_tokens = max_tokens
        if max_messages is not None:
            self.max_messages = max_messages
        if max_completion_tokens is not None:
            self.max_completion_tokens = max_completion_tokens
        if token_padding is not None:
            self.token_padding = token_padding
        self.work_out_tokens()
        self.trim_chatlog()

    def __repr__(self) -> str:
        msg_list = [
            "Trimmed ChatLog object with the following attributes:",
            "uuid: " + str(self.uuid),
            "is_sys_set: " + str(self.is_sys_set),
            "system_prompt: " + str(self._system_prompt_string),
            "trimmed_chatlog_tokens: " + str(self.trimmed_chatlog_tokens),
            "trimmed_messages: " + str(self.trimmed_messages),
            "trimmed_chatlog length " + str(len(self.trimmed_chatlog)),
            "most_recent_trimmed_message: " + str(self.most_recent_trimmed_message),
            "max_chatlog_tokens: " + str(self.max_chatlog_tokens),
            "max_completion_tokens: " + str(self.max_completion_tokens),
            "max_messages: " + str(self.max_messages),
            "max_tokens: " + str(self.max_tokens),
            "token_padding: " + str(self.token_padding),
            
            "is_loaded: " + str(self.is_loaded),
            "is_set_up: " + str(self.is_set_up),
            "most_recent_message: " + str(self.most_recent_message),
            "model: " + str(self.model),
        ]
        if self._has_chatlog():
            msg_list.append("Chatlog: " + repr(self.chatlog))
            msg_list.append("Chatlog length: " + str(len(self.chatlog)))
        return "\n".join(msg_list)
    @property
    def pretty_trimmed_chatlog(self) -> str:
        """Returns a pretty string of the trimmed chat log"""
        result = []
        for msg in self.trimmed_chatlog:
            result.append(msg.pretty)
        return "\n".join(result)
    def get_raw_history_for_export(self):
        """Used for exporting. If a chat log exists, returns the raw history for export. If not, returns the trimmed chat log as a list of dictionaries.
        
        """
        if self._has_chatlog():
            return self.chatlog.data
        else:
            return self.get_messages_as_list(format=MessageReturnType.DICT)
            
    def __str__(self):
        """Returns a pretty string of the entire chat log, usiing the __str__ method of the chatlog object."""
        if self._has_chatlog():
            return self.chatlog.__str__()
        else:
            return self.pretty_trimmed_chatlog
        
if __name__ == "__main__":
    trim = TrimChatLog()
    trim.user_message = "Hello"
    print(trim)
    print(trim.get_finished_chatlog())
    print(trim.get_trimmed_messages_as_dict())
    print(trim.make_save_dict())
