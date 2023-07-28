import datetime
import json
import logging
import os
import sys
import uuid
from typing import Any, Dict, List, Optional, Union

import exceptions
import func as f
import openai
import tiktoken
from chat.chatlog import ChatLog
from chat.message import Message, MessageFactory
from chat.system_prompt import SystemPrompt
from chat.trim_chat_log import TrimChatLog
from chat_completion_wrapper import (
    ChatCompletionWrapper,
    ModelParameters,
    ParamInfo,
    param_info,
)
from handler.save_handler import AbstractCWSaveHandler
from handler.stream_handler import AbstractStreamOutputHandler
from log_config import DEFAULT_LOGGING_LEVEL, BaseLogger
from templates.template_selector import TemplateSelector
from handler.stream_handler import AbstractStreamOutputHandler

"""This is the most complex class in this project. This is because it combines all the other classes in this project into one simple interface for chatbots. It also manages the return type system and the template system. I recommend reading the documentation for the TrimChatLog and ChatCompletionWrapper classes before reading this documentation.
Its confusing to follow, but each element provides an easy to use and helpful feature. 
It is also the most important class in this project, as it is the one that is used to actually chat with the model.
I promise it is not as complex as it looks, and it is actually quite simple to use.

TODO -> Organize the methods and properties into sections, and add a table of contents.
TODO -> Add documentation for the new SaveHandler System
TODO -> Add a method to add StreamOutputHandlers to the chat_completion_wrapper object( for streaming output!)
"""
"""
TODO FOR V3.0.0 ROADMAP:

1. Improvements:
    - [x ] 0.0.1 Add a method to add StreamOutputHandlers to the chat_completion_wrapper object (for streaming output!)
    - [x] 0.0.1 Ensure important values are consistent across both objects
    -[x] 0.0.2 Add SaveHandler System
    - [ ] 0.0.1 Add an emergency save method for openai errors
    - [ ] 0.0.1 Include some basic save handler and output handler info (potentially just if they are the default ones I have created)
        - [ ] 0.0.1 Maybe create a system for mapping names to file paths for save handlers, and a system for mapping names to classes for output handlers (For better customization and flexibility)
    - [ ] 0.0.1 Add handlers to object factory (this is not in this module, but in the factory module, yet highly related)
    - [x ] 0.0.1 Modify current __repr__ to a dedicated debug method, and add a __repr__ that returns the constructor args (Current __repr__ is too complex)
    - [ ] 0.0.1 Improve logging practices for this class
    - [ ] 0.0.1 Consider moving this class into a file in the project directory as it doesn't have any dependencies on related files
    - [ ] 0.0.1 Do a thorough check of everything, ensuring each method has a solid docstring and everything has type hints

2. Major class reorganization:
    Goals:
        - Improve the organization of methods into logical sections, grouping related sections together
        - Add a table of contents to the documentation
        - Create sections for handlers and new SaveHandler system
    Strategy:
        - [ ] 0.1.0 Create a checklist for each method and property
        - [ ] 0.1.0 Back up the file and rename this file
        - [ ] 0.1.0 Plan out which methods and properties should go in which section
        - [ ] 0.1.0 Create a new file with the current name
        - [ ] 0.1.0 Insert sections to the new file and add these to the docstring
        - [ ] 0.1.0 Move each method and property to the new file, updating the documentation as you go
        - [ ] 0.1.0 Add the table of contents to the docstring and the documentation
        - [ ] 0.1.0 Run unittests to ensure everything still works as expected
        - [ ] 0.1.0 Commit changes to git and push to GitHub
        - [ ] 0.1.0 Review the class to ensure everything is correctly organized
        - [ ] 0.1.0 Add any missing methods, properties and documentation to the correct section
        - [ ] 0.1.0 Update the version to 3.0.0 once all tasks are completed
"""


class ChatWrapper:
    version = "2.0.6"
    """
    A wrapper that combines the TrimChatLog and ChatCompletionWrapper classes to make a simple interface for chatbots .
    This class is likely the most complex in this project, as it combines everything together and manages the objects used. It also manages the return type system and the template system. I recommend reading the documentation for the TrimChatLog and ChatCompletionWrapper classes before reading this documentation.
    Dependencies:
        Custom:
            chat.TrimChatLog -> The object that manages the chat log and trimming it
                chat.ChatLog -> The object that manages the chat log
                chat.SystemPrompt -> The object that manages the system prompt
                chat.MessageFactory -> The object that manages the creation of Message objects
                chat.Message -> The object that represents a message
            chat.ChatCompletionWrapper -> Wrapper that abstracts away the making API calls to the OpenAI API
                chat_completion_wrapper.ModelParameters -> The object that manages the parameters for the model
                chat_completion_wrapper.ParamInfo -> The object that manages the information about the parameters
            templates.TemplateSelector -> The object that manages the templates
            ChatLogExporter -> The object that manages the exporting of the chat log
            
            exceptions -> Custom exceptions
            func -> General functions
            settings -> Settings for the program
            log_config -> Logging configuration
        Installed:
            openai -> The OpenAI API
            tiktoken -> Counts the number of tokens in a string
        Python:
            datetime -> For getting the current time
            logging -> For logging
            typing -> For type hinting
            uuid -> For generating uuids
    Raises:
        exceptions.IncorrectObjectTypeError: Raised if an incorrect object type is passed to a method
        exceptions.ObjectNotSetupError: Raised if an object is not set up and an operation is attempted that requires it to be set up
        exceptions.BadRoleError: Raised if an incorrect role is passed to a method
        exceptions.InvalidReturnTypeError: Raised if an invalid return type is passed to a method
        exceptions.MissingValueError: Raised if a required value is missing
    Args:
        API_KEY (str): The OpenAI API key to use
        return_type (str, optional): The return type to use. Defaults to "Message". Must be one of "Message", "str", "dict", "pretty".
        template (dict, optional): An optional template to simplify the setup process. Defaults to None. See templates.py for more info.
        model (str, optional): The model to use. Defaults to None. If None, must be set before chat is called.
    Properties:
        General:
            version (str): The version of the ChatWrapper object
            _model (str): (private) The model to use
            uuid (str): The uuid of the ChatWrapper object, used for logging and debugging
            template (dict): The template to use
            is_trimmed_setup (bool): Whether the TrimChatLog object has been set up
            is_completion_setup (bool): Whether the ChatCompletionWrapper object has been set up
            is_loaded (bool): Whether the ChatWrapper object has been loaded from a save dict
            constructor_args (dict): The arguments used to create the ChatWrapper object(used for __repr__)
        Objects:
            trim_object (TrimChatLog): The TrimChatLog object
            completion_wrapper (ChatCompletionWrapper): The ChatCompletionWrapper object
            message_factory (MessageFactory): The MessageFactory object
            logger (BaseLogger): The logger object for logging(pre-configured logging object )
   Methods:
        Core:
            chat(user_message: str | dict | Message) -> str | Message | dict: Sends the given message to the model and returns the response formatted to return type.
            auto_setup(trim_params: dict = None, completion_params: dict = None) -> None: Sets up the ChatWrapper object with the given parameters. See TrimChatLog and ChatCompletionWrapper for more info on the parameters.
            
            get_most_recent_Message(role: str = User, pretty: bool = False) -> Message: Returns the most recent message as a Message object of a given role. Raises an error if the role is not valid. If pretty is True, returns the message as a pretty string.
            Core Getters and Setters:
                user_message (str): The most recent user message as a string
                assistant_message (str): The most recent assistant message as a string
                system_prompt (str): The system prompt to use
                model (str): The model to use
                max_tokens(str) Set the maximum tokens allowed in a completion. This is nessesary as it must be the same as the max_completion_tokens used in the trim object. Otherwise, too many tokens can be included in the finished chat log, which can cause errors.
        Return Type System:
            return_type (str): (getter and setter) The return type to use
            _check_return_type(return_type: str) -> str: (private) Checks if the given return type is valid, returns the return type if it is, otherwise raises an error
            _format_return(response: str) -> str | Message | dict: (private) Formats the response to the given return type
        Template System:
            load_template(template: dict = None) -> None: Loads the given template.
            auto_setup_from_template(template: dict = None) -> None: Sets up the ChatWrapper object with the given template. See templates.py for more info on templates.
        Managing the Objects Used:
            make_trim_object(max_tokens: int = 8000, max_completion: int = 1000, system_prompt: str = None, token_padding: int = 500, max_messages: int = 400) -> None: Creates a TrimChatLog object with the given parameters
            make_chat_completion_wrapper(**kwargs) -> None: Creates a ChatCompletionWrapper object with the given parameters
            set_trim_object(trim_object: TrimChatLog) -> None: Sets the TrimChatLog object to the given object
            set_chat_completion_wrapper(completion_wrapper: ChatCompletionWrapper) -> None: Sets the ChatCompletionWrapper object to the given object
            set_trim_token_info(**kwargs) -> None: Sets the token info of the TrimChatLog object to the given parameters
            set_chat_completion_params(**kwargs) -> None: Sets the parameters of the ChatCompletionWrapper object to the given parameters
        
        
       
        Save/Load System:
            add_save_handler(save_handler: AbstractCWSaveHandler) -> None: Adds the given save handler to the ChatWrapper object
            make_save_dict() -> dict: Makes a save dict from the ChatWrapper object
            load_from_save_dict(save_dict: dict) -> None: Loads the ChatWrapper object from the given save dict
            _verify_save_dict(save_dict: dict) -> bool: (private) Verifies that the given save dict is valid. Raises a BadSaveDictError if it is not valid.
        Misc:
            __repr__() -> str: Returns the repr of the ChatWrapper object
            __str__() -> returns entire chat log pretty formatted as a string 
            _check_setup(setup_type: str = None) -> None: (private) Checks if the given setup type has been set up. Raises an error if it has not been set up. (Used for ensuring that required objects are setup before they are used, so a custom specific exception can be raised)
    Example Usage:
        chat_wrapper = ChatWrapper(API_KEY, model="gpt-4")
        chat_wrapper.auto_setup()
        chat_wrapper.system_prompt = "This is a test prompt"
        while True:
            user_message = input("You: ")
            print(chat_wrapper.chat(user_message))
            if user_message.lower() == "print":
                print(chat_wrapper)
            elif user_message.lower() == "save":
                save_file_handler = SaveFileHandler(chat_wrapper_obj=chat_wrapper)
                try:
                    save_file_handler.save("test_save.json") 
                except exceptions.FileExistsError:
                    print("File already exists")
            ...more logic/commands here...
                     
        


            
     TODO Make this table of contents more clear, incorporate it into the documentation
     Table of Contents:
     1. Setup/Template System
     2. Making/Managing Objects
     (Probably where StreamOutputHandler methods should go should go)
     3. Special Values that must be the same across both objects
     4. Core Method of Class
     5. Convenience Methods(mostly setters/getters) for Trim Chat Object       
     6.Return Type System
     7. Save Dictionaries 
     8. New Save Handler System (To be added to the documentation)
     9. Misc
     
            
        
    """

    def __init__(
        self,
        API_KEY: str,
        return_type: str = "Message",
        model: str = None,
        template: dict = None,
        save_handler: AbstractCWSaveHandler = None,
    ):
        self.constructor_args = {
            "model": model,
            "API_KEY": "exists",
            "return_type": return_type,
        }
        self.logger = BaseLogger(
            __file__, "chat_wrapper.log", "chat_wrapper", level=DEFAULT_LOGGING_LEVEL
        )
        self._model = model
        self.uuid = str(uuid.uuid4())
        self.API_KEY = API_KEY
        self.trim_object = None
        self.completion_wrapper = ChatCompletionWrapper(
            model=self.model, API_KEY=self.API_KEY
        )
        self.template = template
        self.return_type = self._check_return_type(return_type)
        self.message_factory = MessageFactory(model=self.model)
        self.is_trimmed_setup = False
        self.is_completion_setup = False
        self.stream_handler = None
        self.is_loaded = False
        self.save_handler = save_handler
        
        self.logger.info("Chat Wrapper Created")
        self.logger.debug("Chat Wrapper Created: " + repr(self))

    # ================(SETUP/TEMPLATE SYSTEM)================
    def load_template(self, template: dict = None) -> None:
        """Adds a new template to the chat wrapper"""
        self.template = template
        self.logger.info("Template Loaded")

    def auto_setup_from_template(self, template: dict = None) -> None:
        """Creates a new TrimChatLog and ChatCompletionWrapper object from the given template."""
        if self.template is None:
            self.load_template(template)
        if self.template is None:
            raise exceptions.MissingValueError(
                "Chat Wrapper has no template loaded and thus cannot auto setup from template."
            )
        self.model = self.template["model"]

        self.trim_object = TrimChatLog(**self.template["trim_object"])
        self.completion_wrapper = ChatCompletionWrapper(
            API_KEY=self.API_KEY, **self.template["chat_completion_wrapper"]
        )
        if self.stream_handler is not None:
            self.completion_wrapper.add_stream_output_handler(self.stream_handler)
        self.logger.info(
            f"Chat Wrapper Auto Setup Complete from Template {self.template['name']} Successfully Completed "
        )

    def reload_completion_from_template(self) -> None:
        """Reloads the completion wrapper from the template. Useful if you want to change the parameters of the completion wrapper, but want to keep the same template."""
        if self.template is None:
            raise exceptions.MissingValueError(
                "Chat Wrapper has no template loaded and thus cannot auto setup from template."
            )
        self.completion_wrapper = ChatCompletionWrapper(
            API_KEY=self.API_KEY, **self.template["chat_completion_wrapper"]
        )
        self.logger.info(
            f"Chat Wrapper Auto Setup Complete from Template {self.template['name']} Successfully Completed "
        )

    def auto_setup(
        self, trim_params: dict = None, completion_params: dict = None
    ) -> None:
        """Sets up the ChatWrapper object with the given parameters.
        Valid parameters:
        Trim Parameters:
            max_tokens: int The maximum number of tokens the model can work with. Typically the max for model, but can be lower to save money(costs are per token).
            max_completion: int The maximum number of tokens the model can use on completion. Used to work out how many tokens can be included in the finished chat log.
            system_prompt: str The system prompt to use for the TrimChatLog object.
            token_padding: int The number of tokens to subtract from the max_tokens to prevent errors in case tokens are counted incorrectly or other parameters take up more tokens than expected.
            max_messages: int The maximum number of messages allowed in the trimmed chat log. Generally this is not reached however if it is the oldest messages are removed. Used to save on resources(trimming off and managing too many messages can be slow). Set to None to disable.
        Completion Parameters:
            temperature: float The temperature to use for completion. Higher temperatures make the model more creative, but also more nonsensical. Must be between 0 and 2(but 0-1 is recommended).
            frequency_penalty: float The frequency penalty to use for
            presence_penalty: float The presence penalty. Sets how much the model should avoid repeating itself on
            completion. Higher values make the model less repetitive, but also more nonsensical. Must be between 0 and 2(but 0-1 is recommended).
            max_tokens: int The maximum number of tokens the model can use on completion.
            top_p: float The top p value to use for completion. Sets the probability of the model choosing the next token. Higher values make the model more creative, but also more nonsensical. Must be between 0 and 1.



        """
        if trim_params is None:
            trim_params = {}
        if completion_params is None:
            completion_params = {}
        self.make_trim_object(**trim_params)
        self.make_chat_completion_wrapper(**completion_params)
        if self.stream_handler is not None:
            self.completion_wrapper.add_stream_output_handler(self.stream_handler)
        self.is_trimmed_setup = True
        self.is_completion_setup = True
        self.logger.info("Chat Wrapper Auto Setup Complete")

    def _sync_models(self) -> None:
        """Ensures that the models of the trim object and the completion wrapper are the same."""
        trim_model = None
        completion_model = None

        if self.trim_object is not None:
            trim_model = self.trim_object.model
        if self.completion_wrapper is not None:
            completion_model = self.completion_wrapper.model
        if (
            trim_model is not None
            and completion_model is not None
            and trim_model != completion_model
        ):
            # we treat the trim model as the main model as an incorrect token type can cause errors
            self.logger.warning(
                "Models do not match, setting completion model to trim model"
            )
            self.completion_wrapper.model = trim_model
        if trim_model is not None and self.model != trim_model:
            self.logger.warning("Models do not match, setting model to trim model")
            self.model = trim_model
            self.message_factory = MessageFactory(model=self.model)
            self.logger.warning(
                "ChatWrapper model is different from trim model, setting model to trim model"
            )
            self.logger.info("ChatWrapper model set to " + str(self.model))

    # ================(MAKING/MANAGING OBJECTS)================
    def make_trim_object(
        self,
        max_tokens: int = 8000,
        max_completion: int = 1000,
        system_prompt: str = None,
        token_padding: int = 500,
        max_messages: int = 400,
    ) -> None:
        """Creates a TrimChatLog object with the given parameters."""
        self.trim_object = TrimChatLog(
            max_tokens=max_tokens,
            max_completion_tokens=max_completion,
            system_prompt=system_prompt,
            token_padding=token_padding,
            max_messages=max_messages,
        )
        self._sync_models()
        self.message_factory = self.trim_object.get_message_factory()
        self.logger.info("Trim Log object created: " + repr(self.trim_object))

    def make_chat_completion_wrapper(self, **kwargs) -> None:
        """Creates a ChatCompletionWrapper object with the given parameters."""
        self.completion_wrapper = ChatCompletionWrapper(
            model=self.model, API_KEY=self.API_KEY, **kwargs
        )
        self.is_completion_setup = True
        self._sync_models()
        self.logger.info(
            "Chat Completion Wrapper object created: " + repr(self.completion_wrapper)
        )

    def set_trim_object(self, trim_object: TrimChatLog) -> None:
        """Sets the TrimChatLog object to the given object."""
        if not isinstance(trim_object, TrimChatLog):
            raise exceptions.IncorrectObjectTypeError(
                "Object must be of type TrimChatLog, not " + str(type(trim_object))
            )
        self.trim_object = trim_object
        self._sync_models()
        self.message_factory = self.trim_object.get_message_factory()
        self.logger.debug("Trim Log object set: " + repr(self.trim_object))
        self.is_trimmed_setup = True

    def set_chat_completion_wrapper(
        self, completion_wrapper: ChatCompletionWrapper
    ) -> None:
        """Sets the ChatCompletionWrapper object to the given object."""
        if not isinstance(completion_wrapper, ChatCompletionWrapper):
            raise exceptions.IncorrectObjectTypeError(
                "Object must be of type ChatCompletionWrapper, not "
                + str(type(completion_wrapper))
            )
        self.completion_wrapper = completion_wrapper
        self._sync_models()
        self.is_completion_setup = True
        self.logger.info("Chat Completion Wrapper object set: ")

        self.logger.debug(
            "Chat Completion Wrapper Info: " + repr(self.completion_wrapper)
        )

    # change TrimChatLog parameters
    def set_trim_token_info(self, **kwargs) -> None:
        """Sets the token info of the TrimChatLog object to the given parameters.
        Valid parameters:
        max_tokens: int The maximum number of tokens the model can work with. Typically the max for model, but can be lower to save money(costs are per token).
        max_messages: int The maximum number of messages allowed in the trimmed chat log. Generally this is not reached however if it is the oldest messages are removed. Used to save on resources(trimming off and managing too many messages can be slow). Set to None to disable.
        max_completion_tokens: Maximum numbers the model can use on completion. Used to work out how many tokens can be included in the finished chat log
        token_padding: int Subtracted from the max_tokens to prevent errors in case tokens are counted incorrectly or other parameters take up more tokens than expected.

        """
        self.trim_object.set_token_info(**kwargs)

    # ==========================================================================
    # ========(SPECIAL VALUES THAT MUST BE THE SAME ACROSS BOTH OBJECTS)========

    @property
    def model(self) -> str:
        return self._model

    @model.setter
    def model(self, model: str) -> None:
        """Sets the model of the ChatWrapper object."""
        self._model = model
        self.message_factory = MessageFactory(model=self.model)
        if self.trim_object is not None:
            self.trim_object.model = model
        if self.completion_wrapper is not None:
            self.completion_wrapper.model = model
        self._sync_models()
        self.logger.info("Model set to " + str(model))

    @property
    def max_tokens(self) -> int:
        self._check_setup("trim")
        """The maximum number of completion tokens for the model. Must be the same across ChatCompletionWrapper and TrimChatLog."""
        if (
            not self.trim_object.max_completion_tokens
            == self.completion_wrapper.parameters.max_tokens
        ):
            self.logger.warning("Max tokens for trim and completion do not match")
            self.trim_object.set_token_info(
                max_completion_tokens=self.completion_wrapper.parameters.max_tokens
            )
        return self.trim_object.max_tokens

    @max_tokens.setter
    def max_tokens(self, max_tokens: int) -> None:
        if not isinstance(max_tokens, int):
            raise exceptions.BadTypeError(
                "Max tokens must be of type int, not " + str(type(max_tokens))
            )
        self._check_setup()
        self.trim_object.set_token_info(max_tokens=max_tokens)
        self.completion_wrapper.parameters.max_tokens = max_tokens
        self.logger.debug("Max tokens set to: " + str(max_tokens))

    # ==========================================================================
    # =============(CHANGE COMPLETION PARAMETERS)===============================
    def set_chat_completion_params(self, **kwargs) -> None:
        """Sets the parameters of the ChatCompletionWrapper object to the given parameters."""
        self._check_setup("completion")
        self.completion_wrapper.set_params(**kwargs)

    def _check_setup(self, setup_type: str = None) -> None:
        """Checks if the given setup type has been set up. Raises an error if it has not been set up."""
        if setup_type is None or setup_type.lower in (
            "trim",
            "chatlog",
            "trimmedchatlog",
        ):
            if not self.is_trimmed_setup:
                if self.trim_object is None:
                    raise exceptions.ObjectNotSetupError(
                        "TrimChatLog object has not been set up."
                    )
                else:
                    self.is_trimmed_setup = True
        if setup_type is None or setup_type.lower in (
            "completion",
            "completionwrapper",
            "chatcompletionwrapper",
        ):
            if not self.is_completion_setup:
                if self.completion_wrapper is None:
                    raise exceptions.ObjectNotSetupError(
                        "ChatCompletionWrapper object has not been set up."
                    )
                else:
                    self.is_completion_setup = True
    @property
    def stream(self) -> bool:
        if self.completion_wrapper is None:
            self.logger.warning("Chat Completion Wrapper is not set up")
            return False
        else:
            return self.completion_wrapper.stream
    # =============(CORE METHOD OF CLASS)================
    def chat(self, user_message: str | dict | Message):
        """Sends the given message to the model and returns the response formatted to return type."""
        self._check_setup()
        if isinstance(user_message, str):
            user_message = self.message_factory(role="user", content=user_message)
        elif isinstance(user_message, dict):
            user_message = self.message_factory(**user_message)
        elif not isinstance(user_message, Message):
            raise exceptions.IncorrectObjectTypeError(
                "Message must be of type str, dict, or Message, not "
                + str(type(user_message))
            )
        self.trim_object.user_message_as_Message = user_message
        response = self.completion_wrapper.chat(self.trim_object.get_finished_chatlog())
        self.trim_object.assistant_message = response

        return self._format_return(response)
   
            
    # =====(CONVENIENCE METHODS FOR TRIM CHAT OBJECT )=====
    
    @property
    def system_prompt(self) -> str:
        self._check_setup("trim")
        """The system prompt of the TrimChatLog object."""
        if self.trim_object.system_prompt is None:
            return None
        return self.trim_object.system_prompt.content

    @system_prompt.setter
    def system_prompt(self, system_prompt: str) -> None:
        self._check_setup("trim")
        if not isinstance(system_prompt, str):
            raise exceptions.IncorrectObjectTypeError(
                "System Prompt  must be of type str, not " + str(type(system_prompt))
            )
        self.trim_object.system_prompt = system_prompt
        self.logger.debug("System Prompt set to: " + system_prompt)

    @property
    def user_message(self) -> str:
        self._check_setup("trim")
        """The most recent user message as a string."""
        return self.trim_object.user_message

    @user_message.setter
    def user_message(self, user_message: str) -> None:
        self._check_setup("trim")
        if not isinstance(user_message, str):
            raise exceptions.IncorrectObjectTypeError(
                "User Message must be of type str, not " + str(type(user_message))
            )
        self.trim_object.user_message = user_message

    @property
    def assistant_message(self) -> str:
        self._check_setup("trim")
        """The most recent assistant message as a string."""
        return self.trim_object.assistant_message

    @assistant_message.setter
    def assistant_message(self, assistant_message: str) -> None:
        if not isinstance(assistant_message, str):
            raise exceptions.IncorrectObjectTypeError(
                "Assistant Message must be of type str, not "
                + str(type(assistant_message))
            )
        self.trim_object.assistant_message = assistant_message

    def get_most_recent_Message(
        self, role: str = "user", pretty: bool = False
    ) -> str | Message:
        """Returns either the most recent user or assistant message as a pretty string  or Message object.
        If Pretty is set to True, the message will be returned as a string stylized using Message's pretty property.
        """
        self._check_setup("trim")
        if role == "user":
            message = self.trim_object.user_message_as_Message
        elif role == "assistant":
            message = self.trim_object.assistant_message_as_Message
        else:
            raise exceptions.BadRoleError(
                "Role must be either 'user' or 'assistant', not " + str(role)
            )
        if pretty:
            return message.pretty
        else:
            return message

    # =================(RETURN TYPE SYSTEM)================
    possible_return_types = {"Message", "str", "dict", "pretty "}

    @property
    def return_type(self) -> str:
        """Gets the return type."""
        return self._return_type
    @return_type.setter
    def return_type(self, return_type: str) -> None:
        """Sets the return type to the given return type."""
        self.logger.info("Return type set to: " + return_type)
        self._return_type = self._check_return_type(return_type)

    def _check_return_type(self, return_type: str) -> str:
        """Checks if the given return type is valid. If not raises an InvalidReturnTypeError."""
        if return_type not in self.possible_return_types:
            raise exceptions.InvalidReturnTypeError(
                message=None,
                bad_type=return_type,
                possible_types=self.possible_return_types,
            )
        return return_type

    def _format_return(self, response: str) -> Union[Message, str, dict]:
        """Formats the given response to the return type."""
        if self.return_type == "Message":
            return self.message_factory(role="assistant", content=response)
        elif self.return_type == "str":
            return response
        elif self.return_type == "dict":
            return {"role": "assistant", "content": response}
        elif self.return_type == "pretty":
            msg = self.message_factory(role="assistant", content=response)
            return msg.pretty

    # ==================(SAVE DICTIONARIES )======================

    def make_save_dict(self):
        """Creates a save dictionary for the ChatWrapper object, that can be used to load the ChatWrapper object."""
        self._check_setup()
        save_dict = {}
        save_dict["trim_object"] = self.trim_object.make_save_dict()
        save_dict["completion_wrapper"] = self.completion_wrapper.make_save_dict()
        save_dict["return_type"] = self.return_type
        save_dict["is_trimmed_setup"] = self.is_trimmed_setup
        save_dict["is_completion_setup"] = self.is_completion_setup
        save_dict["model"] = self.model
        if self.template is not None:
            save_dict["template"] = self.template
        save_dict["meta"] = {
            "uuid": self.uuid,
            "time_stamp": str(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")),
            "version": self.version,
        }
        self.logger.info("Chat Wrapper Dictionary Created")
        return save_dict

    def _verify_save_dict(self, save_dict: dict) -> dict:
        """Verifies that the given save_dict is valid. If not raises an BadSaveDictionaryError."""
        required_keys = {
            "trim_object": dict,
            "completion_wrapper": dict,
            "return_type": str,
            "is_trimmed_setup": bool,
            "is_completion_setup": bool,
            "model": str,
            "meta": dict,
        }
        for key in required_keys:
            if key not in save_dict:
                raise exceptions.BadSaveDictionaryError(
                    message="Chat Wrapper save dictionary is missing the key "
                    + str(key)
                )
            if not isinstance(save_dict[key], required_keys[key]):
                raise exceptions.BadSaveDictionaryError(
                    "Chat Wrapper save dictionary key "
                    + str(key)
                    + " must be of type "
                    + str(required_keys[key])
                    + ", not "
                    + str(type(save_dict[key]))
                )
        for key in save_dict["meta"]:
            if not isinstance(save_dict["meta"][key], str):
                raise exceptions.BadSaveDictionaryError(
                    "Chat Wrapper save dictionary meta key "
                    + str(key)
                    + " must be of type str, not "
                    + str(type(save_dict["meta"][key]))
                )

        return save_dict

    def load_from_save_dict(self, save_dict: dict) -> None:
        """Loads the ChatWrapper object from the given save dictionary."""
        self.auto_setup()
        save_dict = self._verify_save_dict(save_dict)
        self.trim_object.load_from_save_dict(save_dict["trim_object"])
        self.completion_wrapper.load_from_save_dict(save_dict["completion_wrapper"])
        self.return_type = save_dict["return_type"]
        self.is_trimmed_setup = save_dict["is_trimmed_setup"]
        self.is_completion_setup = save_dict["is_completion_setup"]
        self.model = save_dict["model"]
        self.uuid = save_dict["meta"]["uuid"]
        self.version = save_dict["meta"]["version"]
        if "template" in save_dict:
            self.template = save_dict["template"]
        self.logger.info("Chat Wrapper Loaded from Save Dictionary")
        self.is_loaded = True

 
    # =====(NEW SAVE FILE HANDLER SYSTEM)=====
    def _check_save_handler(self) -> bool:
        """Returns True if a save handler has been set, otherwise returns False."""
        if self.save_handler is None:
            return False
        else:
            return True

    def add_save_handler(self, save_handler: AbstractCWSaveHandler):
        """Adds the given save handler to the ChatWrapper object."""
        if not isinstance(save_handler, AbstractCWSaveHandler) or save_handler is None:
            raise exceptions.IncorrectObjectTypeError(
                "Save Handler must be of type AbstractCWSaveHandler, not "
                + str(type(save_handler))
            )
        self.save_handler = save_handler
        self.logger.info("Save Handler Added")

    def save(self, entry_name: str, overwrite: bool = False) -> None:
        if not self._check_save_handler():
            raise exceptions.ObjectNotSetupError("Save Handler has not been set up")
        save_dict = self.make_save_dict()
        self.save_handler.write_entry(
            save_dict=save_dict, entry_name=entry_name, overwrite=overwrite
        )
        self.logger.info("Chat Wrapper Saved")

    def load(self, entry_name: str) -> None:
        if not self._check_save_handler():
            raise exceptions.ObjectNotSetupError("Save Handler has not been set up")
        save_dict = self.save_handler.read_entry(entry_name)
        self.load_from_save_dict(save_dict)
        self.logger.info("Chat Wrapper Loaded")

    def check_entry_name(self, entry_name: str) -> bool:
        if not self._check_save_handler():
            raise exceptions.ObjectNotSetupError("Save Handler has not been set up")
        return self.save_handler.check_entry(entry_name)

    def delete_entry(self, entry_name):
        """Deletes the entry with the given entry name."""
        self.save_handler.delete_entry(entry_name)

    @property
    def all_entry_names(self) -> list[str]:
        if not self._check_save_handler():
            raise exceptions.ObjectNotSetupError("Save Handler has not been set up")
        return self.save_handler.entry_names

    # ============(STREAM OUTPUT HANDLER SYSTEM)================
    def _add_stream_to_completion_wrapper(self) -> None:
        """Adds the stream handler to the completion wrapper."""
        if self.stream_handler is not None:
            self.completion_wrapper.add_stream_output_handler(self.stream_handler)
            self.logger.info("Stream Handler Added to Completion Wrapper")
        else:
            self.logger.warning(
                "Stream Handler is None, cannot add to completion wrapper"
            )

    def add_stream_handler(self, stream_handler: AbstractStreamOutputHandler) -> None:
        """Adds the given stream handler to the ChatWrapper object. Must be either None(to unset) or of type AbstractStreamOutputHandler. (See stream_output_handlers.py for more info on stream handlers"""
        if (
            not isinstance(stream_handler, AbstractStreamOutputHandler)
            and stream_handler is not None
        ):
            raise exceptions.IncorrectObjectTypeError(
                "Stream Handler must be of type AbstractStreamOutputHandler, not "
                + str(type(stream_handler))
            )
        if stream_handler is None:
            self.logger.info("Stream Handler is being unset")
        self.stream_handler = stream_handler
        self.logger.info("Stream Handler Added")
        self._add_stream_to_completion_wrapper()

    def _has_stream_handler(self) -> bool:
        """Returns True if a stream handler has been set, otherwise returns False."""
        if self.stream_handler is None:
            return False
        return True

    # ===============(MISC)================
    def __repr__(self) -> str:
        """Returns the repr of the ChatWrapper object."""
        return (
            "ChatWrapper("
            + "model = "
            + str(self.model)
            + ","
            + "API_KEY = "
            + "exists"
            + ","
            + "return_type = "
            + str(self.return_type)
            + ")"
        )

    def debug(self) -> str:
        """Outputs debug information about the ChatWrapper object."""
        constructor = (
            "ChatWrapper(" + str(self.model) + "API_KEY = " + "exists"
            "," + "return_type = " + str(self.return_type) + ")"
        )
        info = (
            "Chat Wrapper Object with UUID: "
            + str(self.uuid)
            + " and version: "
            + str(self.version)
        )
        msg_list = [constructor, info]
        msg_list.append("Is Trimmed Setup: " + str(self.is_trimmed_setup))
        msg_list.append("Is Completion Setup: " + str(self.is_completion_setup))
        msg_list.append("Is Loaded: " + str(self.is_loaded))
        msg_list.append("Trim Object Info:")
        msg_list.append("-" * 20)
        msg_list.append(self.trim_object.__repr__())
        msg_list.append("-" * 20)
        msg_list.append("Completion Wrapper Info:")
        msg_list.append("-" * 20)
        msg_list.append(self.completion_wrapper.__repr__())
        msg_list.append("-" * 20)
        return "\n".join(msg_list)

    def __str__(self):
        return self.trim_object.__str__()
