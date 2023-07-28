import exceptions 
from chat.message import Message, MessageFactory
import func
import tiktoken
from typing import List, Dict, Union
import datetime 
from collections import namedtuple
import uuid 
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
    version = '0.0.1'
    
    def __init__(self, model: str, system_prompt_content: str = None) -> None:
        self.model = model
        self.uuid = str(uuid.uuid4())
        self._system_prompt = system_prompt_content
        self.system_prompt = system_prompt_content 
        self._system_prompt_tokens =  None 
        
     # for wildcard system (values replaced with wildcards in system prompt)
    
    wildcard_info = namedtuple('wildcard_info', "wildcard_name, wildcard_value, wildcard_description")
    system_prompt_wildcards = {
        'model': wildcard_info('model', '__model__', 'The name of the model.'),
        'cut_off': wildcard_info('cut_off', 'September 21, 2021', 'The cut off for the chat log.'),
        'date': wildcard_info('date', '__date__', 'the current date.'),
        "time": wildcard_info('time', '__time__', 'the current time.'),
        
    }
   
    def _add_wildcards_to_string(self, string: str ) -> str:
        """Adds wildcards to the system prompt. Wildcards start with || and end with ||."""
        def add_chars(string: str ):
            """Adds || to the beginning and || to the end of the string."""
            return f'||{string}||'
        wild_card_dict = {add_chars(name): value.wildcard_value for name, value in self.system_prompt_wildcards.items()}
        
        for name in wild_card_dict:
            if wild_card_dict[name] == '__model__':
                wild_card_dict[name] = self.model
            elif wild_card_dict[name] == '__date__':
                wild_card_dict[name] = datetime.date.today().strftime("%B %d, %Y")
            elif wild_card_dict[name] == '__time__':
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
    def system_prompt_raw(self)-> str:
        """Returns the system prompt without wildcards."""
        return self._system_prompt
    @property
    def system_prompt_tokens(self) -> int:
        """Gets the number of tokens in the system prompt. If the system prompt is None, returns None. If for some reason the system prompt tokens are not set, it will set them."""
        if self.system_prompt == None:
            return 0
        elif self._system_prompt_tokens == None:
            self._system_prompt_tokens = self._count_tokens_in_str(self.system_prompt_raw) + 20
        return self._system_prompt_tokens if self._system_prompt_tokens != None else 0 + 20
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
        return Message(role='system', content=self.system_prompt, model=self.model)
    def __str__(self) -> str:
        """Returns the system prompt as a string, using the Message object's pretty property."""
        return self._system_prompt 
    def __repr__(self) -> str:
        """Returns a representation of the SystemPrompt object, including the model, the number of tokens in the system prompt, the length of the system prompt, and the uuid."""
        constructor = f"SystemPrompt(model={self.model}, system_prompt_content={self._system_prompt_content})"
        info = f"SystemPrompt Object with model with {self.system_prompt_tokens} tokens, and a length of {len(self.system_prompt)} characters, and an id of {self.uuid}."
        return f"{constructor}\n{info}"
    
        
    