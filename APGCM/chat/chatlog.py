import tiktoken
import exceptions
from chat import message, exporter
from abc import ABC, abstractmethod
from collections import UserList
import csv
import datetime
from typing import (
    Optional,
    Any,
    Union,
    Callable,
    Iterable,
    Mapping,
    Sequence,
    TypeVar,
    Generic,
    List,
    Deque,
    Set,
    Dict,
    Tuple,
    Iterator,
    Generator,
)
import json
import uuid


class AbstractChatLog(ABC):


    @property
    @abstractmethod
    def model(self) -> str:
        """Returns the model of the chatlog. Required for the Message Factory to correctly count tokens(This class doesn't do much with the tokens, but TrimmedChatLog does.)"""
        return self._model

    @model.setter
    @abstractmethod
    def model(self, model: str) -> None:
        """Sets the model of the chatlog. Required for the Message Factory to correctly count tokens(This class doesn't do much with the tokens, but TrimmedChatLog does.)"""
        self._model = model

   

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def get_message_factory(self, role: str = None) -> message.MessageFactory:
        """Creates a message factory with a given role and model. See message. MessageFactory for more information."""
        pass

    @abstractmethod
    def add_message(self, msg: message.Message) -> None:
        """Must be implemented by subclasses. Adds a message to the chatlog. Must be a Message object. Use ChatLog.get_message_factory() to create a Message objects without worrying about the model."""
        pass

    @abstractmethod
    def get_messages(
        self,
        role: str = None,
        limit: str = None,
        reverse: bool = True,
        pretty: bool = False,
    ) -> Iterable:
        """Must have these arguments and return a generator of messages."""
        pass

    @abstractmethod
    def add_message(self, msg: message.Message) -> None:
        """Adds a message to the chatlog. Must be a Message object."""
        pass

    @abstractmethod
    def add_messages(self, messages: list[message.Message]) -> None:
        """Adds a list of messages to the chatlog."""
        pass

    @abstractmethod
    def make_save_dict(self) -> dict:
        """Should return a dictionary that can be used to recreate the state of the chatlog."""
        pass

    @abstractmethod
    def load_from_dict(self) -> None:
        """Should load the chatlog from a save dictionary."""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Resets the chatlog, clearing all messages."""
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class ChatLog( AbstractChatLog, UserList):
    version = "1.0.0"
    """
    This class class is meant to manage a list of Messages objects, and provide a few useful methods for working with them. No trimming is done nor are system prompts appended. TrimmedChatLog will act as a wrapper for this class, and will provide those features.
    
    Relies on:
        - Message, MessageFactory from chat/message.py
        - UserList from collections
        - uuid from uuid
        - exceptions from chat/exceptions.py
        - tiktoken from tiktoken
    Raises:
        - MissingValueError if a model is not provided(General purpose error)
        - NotAMessageError if a message is not a Message object
        - BadSaveDictionaryError if a save dictionary is not formatted correctly
        - BadMessageDictionaryError if a message dictionary is not formatted correctly
    Attributes:
        self.data: A list of Message objects
        self.model: AI model used to count tokens
        self.uuid: A unique identifier for the chatlog
        self.version: The version of the chatlog
    Methods:
        Private:
            _verify_Message: Verifies that a message is a Message object
            _verify_save_dict: Verifies that a save dictionary is formatted correctly
            _verify_message_dict: Verifies that a message dictionary is formatted correctly
        Public:
            General:
                get_message_factory(self) -> message.MessageFactory: Creates a MessageFactory object with a given role and model
                add_message(self, message: Message) -> None : Adds a message to the chatlog
                add_messages(message_list = list[Message]) -> None : Adds a list of messages to the chatlog
            Getting Messages:
                get_messages(self, role: str = None, limit: int = None, reverse: bool = True, pretty: bool = False): -> Iterator[Union[str, Message]] Gets message(s) from the chatlog, 
                get_messages_as_list(self, role: str = None, limit: int = None, reverse: bool = True, pretty: bool = False): -> List[Union[str, Message]] Gets message(s) from the chatlog, 
                get_pretty_messages(self, role: str = None, reverse: bool = False,  limit: int = None): -> Iterator[str] Gets message(s) from the chatlog,
                get_messages_as_dict(self, role: str = None, limit: int = None, reverse: bool = True, pretty: bool = False): -> list:  Gets message(s) from the chatlog,
                get_finished_chat_log() -> List[dict] 
            Saving:
                make_save_dict(self) -> dict: Makes a save dictionary from the chatlog
                load_from_save_dict(self, save_dict: dict) -> None: Loads a chatlog from a save dictionary
            Misc:
                __str__(self) -> str: Returns pretty printed chatlog
                __repr__(self) -> str: Returns a representation of the chatlog
            
                
        
        
    """

    def __init__(self, model=None):
        self._model = model
        self.uuid = str(uuid.uuid4())
        self.data = []

    # model getter and setter
    @property
    def model(self) -> str:
        """Returns the model of the chatlog. Required for the Message Factory to correctly count tokens(This class doesn't do much with the tokens, but TrimmedChatLog does.)"""
        return self._model

    @model.setter
    def model(self, model) -> None:
        """Sets the model of the chatlog. Required for the Message Factory to correctly count tokens(This class doesn't do much with the tokens, but TrimmedChatLog does.)"""
        # NOTE Remove the following note when TrimmedChatLog is implemented.
        """As of writing this docstring TrimmedChatLog is not implemented."""
        self._model = model

    def get_message_factory(self, role: str = None) -> message.MessageFactory:
        """Creates a message factory with a given role and model. See message. MessageFactory for more information."""
        if self.model is None:
            raise exceptions.MissingValueError(
                "Must provide a model to get a message factory."
            )
        return message.MessageFactory(self.model, role)

    def _verify_Message(self, msg: message.Message) -> message.Message:
        """Verifies that the message is a Message object."""
        if not isinstance(msg, message.Message):
            raise exceptions.NotAMessageError(
                f"Must provide a Message object, not {type(msg)}"
            )
        return msg

    def add_message(self, msg: message.Message) -> None:
        """Adds a message to the chatlog. Must be a Message object. Use ChatLog.get_message_factory() to create a Message objects without worrying about the model."""
        msg = self._verify_Message(msg)
        self.data.append(msg)

    def add_messages(self, messages: list) -> None:
        """Adds a list of messages to the chatlog."""
        for msg in messages:
            self.add_message(msg)

    def get_finished_chatlog(self) -> list[dict]:
        """Converts all Message objects to dictionaries, and returns a list of dictionaries. Uses Message.as_dict()"""
        return [msg.as_dict() for msg in self.data]

    def __repr__(self):
        """Returns a representation of the chatlog."""
        constructor = f"ChatLog({self.model})"
        info = f"ChatLog Object with the following attributes:\n\tModel: {self.model}\n\tMessages: {len(self.data)}"
        return f"{constructor}\n{info}"

    def make_save_dict(self) -> dict:
        """Creates a save file for the chatlog.
        Returns a dictionary with the following keys: meta, model, messages.
        Meta includes the version and uuid of the chatlog.(for debugging purposes)

        """
        save_dict = {
            "meta": {"version": self.version, "uuid": self.uuid},
            "model": self.model,
            "messages": self.get_finished_chatlog(),
        }
        return save_dict

    def _verify_save_dict(self, save: dict) -> dict:
        """Verifies that the save is a dictionary with the correct keys.
            Required keys: model, messages.
            Meta is optional, but an empty dict will be added if it is not present. For debugging purposes.
        Returns the save dictionary after verifying it.
        Raises exceptions.BadSaveDictionaryError if the save is not a dictionary or if it is missing required keys.
        """
        if not isinstance(save, dict):
            raise exceptions.BadSaveDictionaryError(
                f"Must provide a dict , not {type(save)}"
            )

        required_keys = {"model", "messages"}
        if not required_keys.issubset(save.keys()):
            raise exceptions.BadSaveDictionaryError(
                f"Chat Log Save is missing required keys: {required_keys}"
            )
        if not isinstance(save["messages"], list):
            raise exceptions.BadSaveDictionaryError(
                f"Chat Log Saves must have a list of dicts not not  {type(save['messages'])}"
            )
        if not isinstance(save["model"], str):
            raise exceptions.BadSaveDictionaryError(
                f"Chat Log Saves must have a model string not not  {type(save['model'])}"
            )
        if "meta" not in save.keys():
            """If the save doesn't have a meta key, add one, we don't really need it its just for debugging. Adding one just makes sure no errors are thrown when loading the save."""
            save["meta"] = {}

        return save

    def _verify_message_dict(self, msg: dict) -> dict:
        """Checks if a message dictionary has a role and content, raises BadMessageDictionaryError if not. Returns the message dictionary after checking it."""
        if not isinstance(msg, dict):
            raise exceptions.BadMessageDictionaryError(
                f"Must provide a dict , not {type(msg)}"
            )
        required_keys = {"role", "content"}
        if not required_keys.issubset(msg.keys()):
            raise exceptions.BadMessageDictionaryError(
                f"Message Dictionary is missing required keys: {required_keys}"
            )
        return msg

    def load_from_dict(self, save: dict) -> None:
        """Loads parameters from a save dictionary into the ChatLog object
        Parameters
            save: dict The save dictionary to load from, must have the following keys: model, messages. If a uuid is provided, it will be used instead of the uuid in the save dictionary.
        Returns
            None, but loads the save into the ChatLog object.
        """
        save = self._verify_save_dict(save)
        self.model = save["model"]
        self.uuid = save["meta"].get("uuid", self.uuid)
        for msg in save["messages"]:
            msg = self._verify_message_dict(msg)
            self.add_message(
                message.Message(
                    role=msg["role"], content=msg["content"], model=self.model
                )
            )
        return None

    def get_messages(
        self,
        role: str = None,
        limit: int = None,
        reverse: bool = True,
        pretty: bool = False,
    ) -> Iterable[Union[message.Message, str]]:
        """
        Generator that yields messages from the chatlog, optionally filtered by role and limited by limit. Starts from the end of the chatlog.

        Parameters
            role: str = None Optional, the role to filter by. If None, no filtering is done.
            limit: int = None Optional, the number of messages to return. If None, no limit is applied.
            pretty: bool = False Optional, if True, returns the pretty attribute of the Message object instead of the Message object itself.
        Returns
            Iterable[Union[message.Message, str]]: A generator that yields messages from the chatlog, optionally filtered by role and limited by limit. Starts from the end of the chatlog if reverse is True, otherwise starts from the beginning.
        """
        count = 0
        msg_list = self.data[::-1] if reverse else self.data
        for message in msg_list:
            if message.role == role or role is None:
                yield message if not pretty else message.pretty
                count += 1
            if limit is not None and count >= limit:
                break

    def get_messages_as_list(
        self,
        role: str = None,
        limit: int = None,
        reverse: bool = True,
        pretty: bool = False,
    ) -> list[Union[message.Message, str]]:
        """Gets  messages from the chatlog, optionally filtered by role and limited by limit. Starts from the end of the chatlog. Returns a list of messages.
        See get_messages for more information on the parameters.
        """
        gen = self.get_messages(role, limit, reverse, pretty)
        result = []
        for message in gen:
            result.append(message)
        if result == []:
            return None
        return result

    def get_messages_as_dict(
        self,
        role: str = None,
        limit: int = None,
        reverse: bool = False,
        pretty: bool = False,
    ) -> list[dict]:
        """"""
        gen = self.get_messages(role, limit, reverse, pretty)
        result = []
        for msg in gen:
            result.append(msg.as_dict())
        return result

    def add_messages_as_dict(self, messages: list[dict]) -> None:
        for msg in messages:
            try:
                self.add_message(
                    message.Message(
                        role=msg["role"], content=msg["content"], model=self.model
                    )
                )
            except KeyError:
                raise exceptions.BadMessageDictionaryError(
                    "Message dictionary must have 'role' and 'content' keys."
                )

    def reset(self) -> None:
        """Resets the chatlog, clearing all messages."""
        self.data = []
        self.uuid = str(uuid.uuid4())

    def get_pretty_messages(
        self, role: str = None, reverse: bool = False, limit: int = None
    ) -> str:
        """Prints messages from the chatlog, optionally filtered by role and limited by limit. Starts from the end of the chatlog. Uses the pretty attribute of the Message object.
        See get_messages for more information on the parameters.
        """
        return "\n".join(self.get_messages(role, limit, pretty=True, reverse=reverse))

    def __str__(self):
        """Returns a string representation of the chatlog."""
        return self.get_pretty_messages()

    def __len__(self) -> int:
        return len(self.data)

    def export(self, format: str = "markdown", **kwargs):
        """Uses the exporter module to export the chatlog to a given format. Available formats: md, markdown, txt, text Any additional kwargs are passed to the exporter module. See exporter.export_data for more information. and included in header section(with any underscores replaced with spaces) See exporter.export_data for more information."""
        if format in ("md", "markdown"):
            return exporter.export_data(
                self.data,
                self.model,
                system_prompt=None,
                exporter_type="markdown",
                **kwargs,
            )
        elif format in ("txt", "text"):
            return exporter.export_data(
                self.data,
                self.model,
                system_prompt=None,
                exporter_type="text",
                **kwargs,
            )
        else:
            raise exceptions.BadFormatError(
                f"Invalid format: {format}, available formats: md, markdown, txt, text"
            )
