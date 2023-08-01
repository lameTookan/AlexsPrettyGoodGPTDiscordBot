import tiktoken
from collections import namedtuple, UserDict, UserList
import exceptions
from log_config import BaseLogger, DEFAULT_LOGGING_LEVEL
#tests can be found in tests/test_message.py
from enum import Enum
class Roles(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(UserDict):
    """This class represents a message in a conversation, with a role, content, and model. It has functionality for counting tokens and returning a pretty string representation of the message.
    Relies On:
        Custom:
            exceptions.BadRoleError
            Roles Enum
            BaseLogger, DEFAULT_LOGGING_LEVEL
        Python:
            UserDict, namedtuple from collections
            Enum from enum
            tiktoken
    Raises:
        exceptions.BadRoleError: If the role is not one of the allowed roles.
    Required By:
        TrimChatLog 
        Chatlog
        Everything else in the project
    Args:   
        role (str): The role of the message. Must be one of "user", "assistant", or "system".
        content (str): The content of the message.
        model (str): The model, used to count tokens
        
            
    Attributes:
        role (str): The role of the message. Must be one of "user", "assistant", or "system".
        content (str): The content of the message.
        model (str): The model, used to count tokens 
        tokens (int): The number of tokens in the message.
        data (dict): The data of the message, with keys "role" and "content".
        pretty (str): A pretty string representation of the message, styled with the get_pretty_message method.
    Methods:
        _verify_roles: Verifies that the role is allowed.
        _count_tokens: Counts the number of tokens in the message, using tiktoken.
        get_pretty_message: Returns a pretty string representation of the message.
        as_dict: Returns the data of the message as a dictionary.
        __str__: Returns the pretty string representation of the message.
        __repr__: Returns a string representation of the message, with the constructor and info, including the number of tokens and characters.
    
    """
    def __init__(self, role: str, content: str, model: str):
        self.logger = BaseLogger(__file__, identifier="Message", filename="message.log", level=DEFAULT_LOGGING_LEVEL)

        self._verify_roles(role)
        

        self.data = {"role": role, "content": content}
        self.role = role
        self.content = content
        self.model = model
        self.tokens = self._count_tokens(content, model)
        self.pretty = self.get_pretty_message()
    roles = Roles
    allowed_roles = (roles.USER.value, roles.ASSISTANT.value, roles.SYSTEM.value)
    def _verify_roles(self, role: str):
        """Verifies that the role is allowed."""
        if role not in self.allowed_roles:
            self.logger.error(f"Bad Role: {role}")
            raise exceptions.BadRoleError(role, self.allowed_roles)
    def _count_tokens(self, string: str, model: str) -> int:
        """Returns the number of tokens in a string."""
        encoding = None 
        try:
            encoding = tiktoken.encoding_for_model(model)
            
        except KeyError:
            self.logger.error(f"Tiktoken does not have an encoding for {model}, using cl100k_base")
            encoding = tiktoken.get_encoding("cl100k_base")
        return (len(encoding.encode(string)))
    def get_pretty_message(self):
        """Returns a pretty string representation of the message."""
        if self.data['role'] == 'user':
            return f"> {self.data['content']}"
        elif self.data['role'] == 'assistant':
            return f"\u001b[36m >> {self.data['content']} \u001b[0m"
        elif self.data['role'] == 'system':
            return f"\u001b[33m >>> {self.data['content']} \u001b[0m"
        else:
            return f"Unknown role: {self.data['role']}: {self.data['content']}"
    def __str__(self):
        return self.pretty
    def as_dict(self):
        return self.data
    def __repr__(self):
        constructor =  f"Message({self.data['role']}, {self.data['content']}, {self.model})"
        info = f"Message Object with {self.tokens} tokens, and {len(self.data['content'])} characters."
        
        return f"{constructor}\n{info}"
    
class MessageFactory:
    """Creates a message with a given role and model."""
    def __init__(self, model: str, role: str = None):
        self.model = model
        self.role = role
    def __call__(self, content: str, role: str = None):
        if role is None:
            role = self.role
        if role is None:
            raise exceptions.NoRoleProvidedError("Must provide a role either during initialization or during call.")
        return Message(role, content, self.model)
    def set_model(self, model: str):
        self.model = model
            
    def __repr__(self):
        return f"MessageFactory({self.model}, {self.role})"
    
if __name__ == '__main__':
    message = Message('user', 'Hello, world!', 'gpt2')
    print(message)
    print(message.as_dict())
    print(message.tokens)
    print(message)
    print(repr(message))
    print(message.pretty)
    print(message.data)
    print(message['role'])
    print(message['content'])
    print(message.model)
    print(message.model)
    print(message.role)
    print(message.tokens)
    print(message.pretty)
    print(message.data)