import tiktoken
from collections import namedtuple
import random 
import unittest
from typing import NamedTuple, List, Tuple, Optional, Callable, Set, Dict, Deque
class BadMessageError(Exception):
    def __init__(self, message = None):
        if message is None:
            message = " "
        self.msg = message
    def __str__(self):
        temp = [
            "Incorrect message format",
            "Message must be a dict with keys 'role' and 'content'",
        ]
        temp.append(self.msg)
        return ' '.join(temp)

EncodedMessage = namedtuple('EncodedMessage', ['message', 'token_count'])
class EncodeMessage:


    """
    This is a class that encodes and decode messages into a named tuple with the message and token count
    Some important terms:
    message dict: A dict with keys 'role' and 'content', where role is a string and content is a string. This is the format that the API expects messages to be in.
    EncodedMessage: A named tuple with the message dict and the token count. Easier to work with than a message dict and tokens can be counted once and stored, rather than counting them every time they are needed.

    Relies on TikToken library for token counting, but can be used with any token counting function
    Also uses BadMessageError, a custom exception for improperly formatted messages
    As well as the EncodedMessage named tuple

    Attributes:
        model(str): The model to use for token counting, defaults to gpt-4. if using default token counter function, it is used with the tiktoken library
        styler_func(callable): A function that takes a message and returns a string, defaults to _default_styler_func. Formats message for display. Will be used if no styler function is passed to encode_message
        token_counter_func(callable): A function that takes a message and returns an int, defaults to _default_token_counter_func. Counts tokens in message. Will be used if no token counter function is passed to encode_message.
            must take two arguments, model and string, and return an int
    Methods:
        _check_token_counter_func: Checks that a token counter function is valid, raises ValueError if not
        _check_styler_func: Checks that a styler function is valid, raises ValueError if not
        _default_styler_func: Default styler function, returns message content
        _default_token_counter_func: Default token counter function, uses tiktoken library
        _token_counter: Wrapper for the token counter function, it will pass the self.model attribute if no model is provided
        _styler: Wrapper for the styler function. Will check if the message is a dict or an EncodedMessage, and will decode the EncodedMessage if needed

        _check_message_dict: Checks that a message is a valid message dict, raises BadMessageError if not
        _format_message(role: str, content: str) -> dict: Formats a message into a dict with keys 'role' and 'content'
        encode_message_dict(message:dict): Encodes a message dict into an EncodedMessage named tuple
        decode_message_dict(message: EncodedMessage): Decodes an EncodedMessage named tuple into a message dict to be sent to API
        encode(message: dict, role: str, content: str): can take either a message dict or a role and content and encode it into an EncodedMessage named tuple
            Must have either a message dict or a role and content
        decode(message: EncodedMessage): Decodes an EncodedMessage named tuple into a message dict to be sent to API
        encode_message_string(message: str, role: str): Encodes a message string into an EncodedMessage named tuple
        encode_message_list(message_list: List[dict]): Encodes a list of message dicts into a list of EncodedMessage named tuples
        decode_message_list(message_list: List[EncodedMessage]): Decodes a list of EncodedMessage named tuples into a list of message dicts to be sent to API
        count_tokens_in_list(message_list: List[EncodedMessage]): Counts the tokens in a list of EncodedMessage named tuples, returns a token count int
        style_messages(message: list[dict|EncodedMessage]): Styles a list of message dicts or EncodedMessage into string for display using the styler function



            """
    def __init__(self, model: str, styler_func: callable= None, token_counter_func: callable = None):
        self.model = model
        if token_counter_func is not None:
            self._check_token_counter_func(token_counter_func)
            self.token_counter_func = token_counter_func
        else:
            self.token_counter_func = EncodeMessage._default_token_counter_func
        if styler_func is not None:
            self._check_styler_func(styler_func)
            self.styler_func = styler_func
        else:
            self.styler_func = EncodeMessage._default_styler_func
        
        
      
      
    def _check_token_counter_func(self, token_counter_func: callable) -> None:
        """Checks that a token counter function is valid, raises ValueError if not"""
        if not callable(token_counter_func):
            raise ValueError('token_counter_func must be callable')
        if token_counter_func.__code__.co_argcount >= 2:
            raise ValueError('token_counter_func must take two arguments')
        if 'model' not in token_counter_func.__code__.co_varnames:
            raise ValueError('token_counter_func must have a model argument')
        if 'string' not in token_counter_func.__code__.co_varnames:
            raise ValueError('token_counter_func must have a string argument')
        if token_counter_func.__code__.co_varnames[0] != 'model':
            raise ValueError('token_counter_func must have model as first argument')
        test = token_counter_func('test', 'gpt-4')
        if not isinstance(test, int):
            raise ValueError('token_counter_func must return an int')
    
    def _check_styler_func(self, styler_func: callable) -> None:
        """Checks that a styler function is valid, raises ValueError if not"""
        if not callable(styler_func):
            raise ValueError('styler_func must be callable')
        if styler_func.__code__.co_argcount >= 1:
            raise ValueError('styler_func must take at least one argument')
        if 'message' not in styler_func.__code__.co_varnames:
            raise ValueError('styler_func must have a message argument')
        test = styler_func({'role': 'user', 'content': 'test'})
        if not isinstance(test, str):
            raise ValueError('styler_func must return a string')
        
        
    @staticmethod    
    def _default_styler_func( message: dict) -> str:
        """Syles a message dict into a string"""
        role = message['role']
        string = None
        if role == "user":
            string = f"> {message['content']}"
        elif role == "assistant":
            string = f"\u001b[32m >>{message['content']}\u001b[0m"
        elif role == "system":
            string = f"\u001b[33m >>>{message['content']}\u001b[0m"
        else:
            string = f"{message['content']}"
        return string

    
    @staticmethod
    def _default_token_counter_func( string, model = None) -> int:
        """Counts tokens in a string"""
      
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(string))
    
    def _styler(self, message: dict | EncodedMessage) -> str:
        """Wrapper for styler function"""
        if isinstance(message, EncodedMessage):
            message = self.decode_message_dict(message)
        
        self._check_message_dict(message)
        return self.styler_func(message)
    def _token_counter(self, string: str, model: str = None) -> int:
        """Wrapper for token counter function"""
        if model is None:
            model = self.model
        return self.token_counter_func(string, model)
    def _check_message_dict(self, message: dict)-> None:
        """Checks that a message is a valid message dict, raises BadMessageError if not"""
        expected_keys = {'role', 'content'}
        if not isinstance(message, dict):
            raise BadMessageError('message must be a dict')
        if set(message.keys()) != expected_keys:
            raise BadMessageError(f'message must have keys {expected_keys}')
        
        
    def _format_message(self, content: str, role: str) -> dict:
        """Formats a message into a message dict"""
        return {
            'role': role,
            'content': content,
        }
    def encode_message_dict(self, message: dict) -> EncodedMessage:
        """Encodes a message dict into an EncodedMessage"""
        self._check_message_dict(message)
        token_count = self._token_counter(message['content'])
        return EncodedMessage(message, token_count)
        
    def decode_message_dict(self, encoded_message: EncodedMessage) -> dict:
        
        """Decodes an EncodedMessage into a message dict"""
        return encoded_message.message
    def encode(self, message: dict = None, role: str = None, content: str = None) -> EncodedMessage:
        """Encodes a message dict into an EncodedMessage"""
        if message is None and (role is None or content is None):
            raise ValueError('either message or role and content must be provided')
        if message is None:
            if role is None or content is None:
                raise ValueError('both role and content must be provided')
            message = self._format_message(content, role)
        return self.encode_message_dict(message)
    def decode(self, encoded_message: EncodedMessage) -> dict:
        """Decodes an EncodedMessage into a message dict"""
        return self.decode_message_dict(encoded_message)
    def encode_message_string(self, message: str, role: str) -> EncodedMessage:
        """Encodes a message string into an EncodedMessage"""
        return self.encode_message_dict(self._format_message(message, role))
    def encode_message_list(self, message_list: list[dict]):
        """Encodes a list of message dicts into a list of EncodedMessages"""
        return [self.encode_message_dict(message) for message in message_list]
    def decode_message_list(self, encoded_message_list: list[EncodedMessage]):
        """Decodes a list of EncodedMessages into a list of message dicts"""
        return [self.decode_message_dict(message) for message in encoded_message_list]
    def count_tokens_message_list(self, message_list: list[EncodedMessage]) -> int:
        """Counts the tokens in a list of EncodedMessages"""
        token_count = 0
        for message in message_list:
            token_count += message.token_count
        return token_count
            
    def style_messages(self, messages: list[dict | EncodedMessage]) -> str:
        """Styles a message dict or EncodedMessage into a string"""
        return '\n'.join([self._styler(message) for message in messages])




# class TestChatLogGenerator:
#     default_short_sample_messages = [
#         {'role': 'user', 'content': 'Hello, how are you?'},
#         {'role': 'assistant', 'content': 'I am well, how are you?'},
#     ]
#     default_medium_sample_messages = [
#         {"role": "user", "content": "Hello I need a few test messages for something I am making. Maybe like a hundred per message. So I am typing this up and planning to add it to my test chat log function. 100 tokens is actually fairly long. I am currently at 44. Banana. Antidisestablishmentarianism. Reply to this message with some content of a similar length. Doesn't need to be anything special. I am almost done! 86 tokens so far. Um, I need a proper cup of coffee from a proper copper pot! "},
#         {"role": "assistant", 'content': "You need a test message of about a hundred tokens for your project. It's an interesting task! As we proceed, I'm at token number 21. How about discussing some random subjects, like the fascinating nature of quantum mechanics? Or perhaps the diverse cultures across our beautiful globe? Oh, and speaking of coffee from a copper pot, there's nothing like a warm, aromatic brew in the morning, right? Pneumonoultramicroscopicsilicovolcanoconiosis.  "}
#     ]
#     default_long_sample_messages = [
#         {'role': 'user', 'content': """
#         Absolutely! Here's your first long message. We're embarking on an incredible journey of words, where the primary aim is to achieve a count of around 400 tokens. Isn't language such a wonderful construct? How with just 26 letters, in the case of English, we can form a virtually limitless combination of words and sentences, and express such a vast array of thoughts, emotions, and ideas. From describing the magnificent view of a sunrise on a clear morning, to detailing the complex workings of a computer, or expressing our deepest emotions - all can be encapsulated within the framework of these letters.

# Exploring this train of thought further, language plays a fundamental role in our lives. It's our primary means of communication, our tool for expressing ideas, sharing knowledge, and forging connections with others. And the wonderful thing is, language is always evolving, changing, and growing with us. New words and phrases are created all the time, capturing the zeitgeist of the era.

# In addition, language can be beautiful and artistic, especially in the realm of literature and poetry. Think about the sonnets of Shakespeare or the verses of Robert Frost. The way they used words to paint vivid images, stir emotions, and provoke thought is nothing short of magical.

# Just as we sip our coffee from a copper pot, the warm, rich liquid awakening our senses, language too has the power to awaken our minds, stimulate our imaginations, and touch our hearts. As we reach our target token count, let's appreciate the marvel that is language and its incredible impact on our lives.

# Now, onto your second long message, approximately 400 tokens. The focus this time will be our magnificent Earth and its wonders. We live on a planet that's teeming with life, diversity, and beauty. From the icy poles to the scorching deserts, the lush rainforests to the vast oceans, our Earth is a treasure trove of breathtaking landscapes and incredible creatures."""},
#         {'role': 'assistant', 'content': """
#         But Earth is also a planet of contrasts. On one hand, we have the serene beauty of a rainforest, with its dense foliage and rich biodiversity. On the other hand, we have the stark, harsh landscape of a desert, where survival is a testament to the resilience of life.

# In the same vein, our planet experiences a variety of weather conditions - from the soothing rhythm of a gentle rain shower to the furious intensity of a hurricane, from the delightful coolness of a snowfall to the scorching heat of a summer day.


# Beyond the land and seas, our Earth is enveloped in a life-sustaining atmosphere, a delicate layer that not only provides us with the air we breathe but also shields us from the harsh radiation of the sun. It's a complex and dynamic system, with winds and currents, pressure systems and weather patterns, all intricately intertwined.

# Consider the diversity of ecosystems across our planet. Each one unique, teeming with organisms specially adapted to their environment, forming a delicate balance. From coral reefs often referred to as the "rainforests of the sea" due to their rich biodiversity, to the desolate beauty of tundra regions, where only the hardiest of species can survive, each ecosystem plays an essential part in the larger biosphere of Earth.

# Think about our celestial journey, too. As we spin on our axis and orbit the sun, we experience the rhythms of day and night, the cycles of seasons, the dance of constellations across the night sky. We're part of a larger cosmic order, our little blue planet twirling in the vast expanse of the cosmos.

# On a human level, Earth is a cradle of civilizations, cultures, and histories. Every corner of our globe tells a story - from ancient ruins whispering tales of bygone eras to bustling cities echoing with the pulse of modern life. And here is 10 more tokens! Animal crackers in my soup

#         """}
#      ]

#     def __init__(self, short_sample_messages = None, medium_sample_messages = None, long_sample_messages = None, model = None):
#         self._model = model or 'gpt-4'
#         self.short_sample_messages = short_sample_messages or self.default_short_sample_messages
#         self.medium_sample_messages = medium_sample_messages or self.default_medium_sample_messages
#         self.long_sample_messages = long_sample_messages or self.default_long_sample_messages
#         self.encode_sample_messages()

#         pass
#     def _encode_message(self, message: dict ):
#         token_count = self._count_tokens(message['content'])
#         return EncodedMessage(message, token_count)
#     def _decode_message(self, encoded_message: EncodedMessage):
#         return encoded_message.message
#     def _encode_messages(self, messages: list, ):
       
      
#             return [self._encode_message(message) for message in messages]
#     def _decode_messages(self, encoded_messages: list, ):
#         return [self._decode_message(encoded_message) for encoded_message in encoded_messages]
#     def _count_tokens(self, string: str, model = None):
#         model = model or self._model
#         encoding = tiktoken.encoding_for_model(model)
#         return len(encoding.encode(string))
#     def _add_encoded_messages_tokens(self, encoded_messages: list[EncodedMessage]):
#         token_count = 0
#         for encoded_message in encoded_messages:
#             token_count += encoded_message.token_count
#         return token_count
        
#     def generate_chat_log(self, target_tokens, mode):
#         if mode not in ['short', 'medium', 'long', 'random']:
#             raise ValueError("mode must be one of 'short', 'medium', 'long', or 'random'")
#         modes = {
#             'short': self._short_encoded_messages,
#             'medium': self._medium_encoded_messages,
#             'long': self._long_encoded_messages
#         }
#         if mode in modes:
#             return self.gen_test_chat_log_from_encoded_messages(target_tokens, modes[mode])
#         elif mode == 'random':
#             current_tokens = 0 
#             encoded_chat_log = []
#             while current_tokens < target_tokens:
#                 encoded_messages = random.choice([self._short_encoded_messages, self._medium_encoded_messages, self._long_encoded_messages])
#                 encoded_message = random.choice(encoded_messages)
#                 encoded_chat_log.append(encoded_message)
#                 current_tokens += encoded_message.token_count

#             while current_tokens > target_tokens:
#                 popped_msg = encoded_chat_log.pop()
#                 current_tokens -= popped_msg.token_count
#             return self._decode_messages(encoded_chat_log)

            
            
#     def gen_test_chat_log_from_encoded_messages(self,target_tokens, encoded_messages: list[EncodedMessage]):
#         chat_log = []
#         tokens = 0
#         tokens_in_pair = self._add_encoded_messages_tokens(encoded_messages)
#         num_messages = 0
#         if target_tokens % tokens_in_pair == 0:
#             num_messages = target_tokens // tokens
            
#         else:
#             num_messages = target_tokens // tokens -1
#         for i in range(num_messages):
#             for encoded_message in encoded_messages:
#                 chat_log.append(encoded_message.message)
#                 tokens += encoded_message.token_count
#                 if tokens >= target_tokens:
#                     break

#         return [self._decode_messages]

        
#     def encode_sample_messages(self):
#         self._short_encoded_messages = [self._encode_message(message) for message in self.short_sample_messages]
#         self._medium_encoded_messages = [self._encode_message(message) for message in self.medium_sample_messages]
#         self._long_encoded_messages = [self._encode_message(message) for message in self.long_sample_messages]


# generator = TestChatLogGenerator()

# print(generator.generate_chat_log(5000, 'random'))
