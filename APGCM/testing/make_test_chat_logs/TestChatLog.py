from EncodeMessage import EncodeMessage, EncodedMessage, BadMessageError
import random 
import json
import os
class BadModeError(Exception):
    def __init__(self, message: str = None, bad_mode: str  = None, allowed_modes: list  = None):
        def default_if_not_None(val, default):
            return val if val is not None else default
        msg_list = []
        msg_list.append(default_if_not_None(message, "Selected mode is not valid"))
        if bad_mode is not None:
            msg_list.append(f"Selected mode: {bad_mode}")
        msg_list.append(default_if_not_None(allowed_modes, "Allowed modes: short, medium, long, random"))
        self.message = "\n".join(msg_list)
    def __str__(self):
        return self.message
class GenerateTestChatLog:
    """
    This class generates a chat log of a given length, with messages of a given length.
    Includes sample messages to use in testing 
    Short messages are about 10 tokens long
    Medium messages are about 100 tokens long
    Long messages are about 400 tokens long
    Attributes:
        sample_messages (dict): A dictionary of sample messages to use in testing
        encoder (EncodeMessage): An instance of the EncodeMessage class, used to encode messages as EncodedMessage objects(includes token count and message dict)
        _modes (list): A list of modes to use in generating the chat log (short, medium, long, random)
        _encoded_sample_messages (dict): A dictionary of sample messages encoded as EncodedMessage objects

    Methods:
        encode_sample_messages: Returns list of Encoded message objects from a given category of sample messages
        encode_all_sample_messages: Goes through each category of sample messages and encodes them as EncodedMessage objects, saved in _encoded_sample_messages
        generate_chat_log_from_encoded_messages: Takes a list of EncodedMessage objects and a target token count, and generates a chat log of that length(can be less but not more)
        generate_chat_log: Generates a chat log of a given token length and mode (short, medium, long, random)
           type (str|list): The type of chat log to generate (short, medium, long, random)
           If type is a list, all messages from that type will be included in the chat log. Random is not supported for lists of messages
        add_sample_messages: Adds sample messages to the chat log. 
            type (str): The type of message to be added (short, medium, long)
            message(dict): Message to be added, must be a dict with keys 'role' and 'content'
            role, content(str): can be used instead of message to specify role and content of message
        remove_sample_messages: Removes sample messages from the chat log.



    """
    sample_messages = {
        "short": [
            {'role': 'user', 'content': 'Hello, how are you?'},
            {'role': 'assistant', 'content': 'I am well, how are you?'},
        ],
        "medium": [
            {"role": "user", "content": "Hello I need a few test messages for something I am making. Maybe like a hundred per message. So I am typing this up and planning to add it to my test chat log function. 100 tokens is actually fairly long. I am currently at 44. Banana. Antidisestablishmentarianism. Reply to this message with some content of a similar length. Doesn't need to be anything special. I am almost done! 86 tokens so far. Um, I need a proper cup of coffee from a proper copper pot! "},
            {"role": "assistant", 'content': "You need a test message of about a hundred tokens for your project. It's an interesting task! As we proceed, I'm at token number 21. How about discussing some random subjects, like the fascinating nature of quantum mechanics? Or perhaps the diverse cultures across our beautiful globe? Oh, and speaking of coffee from a copper pot, there's nothing like a warm, aromatic brew in the morning, right? Pneumonoultramicroscopicsilicovolcanoconiosis.  "} ],
        "long": [
            {'role': 'assistant', 'content': """But Earth is also a planet of contrasts. On one hand, we have the serene beauty of a rainforest, with its dense foliage and rich biodiversity. On the other hand, we have the stark, harsh landscape of a desert, where survival is a testament to the resilience of life.
        In the same vein, our planet experiences a variety of weather conditions - from the soothing rhythm of a gentle rain shower to the furious intensity of a hurricane, from the delightful coolness of a snowfall to the scorching heat of a summer day.
        Beyond the land and seas, our Earth is enveloped in a life-sustaining atmosphere, a delicate layer that not only provides us with the air we breathe but also shields us from the harsh radiation of the sun. It's a complex and dynamic system, with winds and currents, pressure systems and weather patterns, all intricately intertwined.
        Consider the diversity of ecosystems across our planet. Each one unique, teeming with organisms specially adapted to their environment, forming a delicate balance. From coral reefs often referred to as the "rainforests of the sea" due to their rich biodiversity, to the desolate beauty of tundra regions, where only the hardiest of species can survive, each ecosystem plays an essential part in the larger biosphere of Earth.
        Think about our celestial journey, too. As we spin on our axis and orbit the sun, we experience the rhythms of day and night, the cycles of seasons, the dance of constellations across the night sky. We're part of a larger cosmic order, our little blue planet twirling in the vast expanse of the cosmos.
        On a human level, Earth is a cradle of civilizations, cultures, and histories. Every corner of our globe tells a story - from ancient ruins whispering tales of bygone eras to bustling cities echoing with the pulse of modern life. And here is 10 more tokens! Animal crackers in my soup
        """}, 
            {'role': 'user', 'content': """
        Absolutely! Here's your first long message. We're embarking on an incredible journey of words, where the primary aim is to achieve a count of around 400 tokens. Isn't language such a wonderful construct? How with just 26 letters, in the case of English, we can form a virtually limitless combination of words and sentences, and express such a vast array of thoughts, emotions, and ideas. From describing the magnificent view of a sunrise on a clear morning, to detailing the complex workings of a computer, or expressing our deepest emotions - all can be encapsulated within the framework of these letters.

Exploring this train of thought further, language plays a fundamental role in our lives. It's our primary means of communication, our tool for expressing ideas, sharing knowledge, and forging connections with others. And the wonderful thing is, language is always evolving, changing, and growing with us. New words and phrases are created all the time, capturing the zeitgeist of the era.

In addition, language can be beautiful and artistic, especially in the realm of literature and poetry. Think about the sonnets of Shakespeare or the verses of Robert Frost. The way they used words to paint vivid images, stir emotions, and provoke thought is nothing short of magical.

Just as we sip our coffee from a copper pot, the warm, rich liquid awakening our senses, language too has the power to awaken our minds, stimulate our imaginations, and touch our hearts. As we reach our target token count, let's appreciate the marvel that is language and its incredible impact on our lives.

Now, onto your second long message, approximately 400 tokens. The focus this time will be our magnificent Earth and its wonders. We live on a planet that's teeming with life, diversity, and beauty. From the icy poles to the scorching deserts, the lush rainforests to the vast oceans, our Earth is a treasure trove of breathtaking landscapes and incredible creatures."""},


        ]
    }
    def __init__(self, model: str = "gpt-4")-> None:
        self.encoder = EncodeMessage(model = model)
        self._encoded_sample_messages = {}
        self.encode_all_sample_messages()
        self._modes = ["short", "medium", "long", 'random']
        
    def encode_all_sample_messages(self) -> None:
        """Encode all sample messages as EncodedMessage namedtuples"""
        for type in self.sample_messages.keys():
            self._encoded_sample_messages[type] = self.encode_sample_messages(type)
    def encode_sample_messages(self, type: str) -> list[EncodedMessage]:
        """Encode sample messages as EncodedMessage namedtuple of a given type"""
        if type not in self.sample_messages.keys():
            raise ValueError(f"Invalid type: {type}")
        return [self.encoder.encode(message) for message in self.sample_messages[type]]
    def generate_chat_log_from_encoded_messages(self, encoded_messages: list[EncodedMessage], target_token_count: int) -> list[EncodedMessage]:
        """Generate a chat log from a list of EncodedMessage namedtuples"""
        chat_log = []
        token_count = 0
        while token_count < target_token_count:
            message = random.choice(encoded_messages)
            chat_log.append(message)
            token_count += message.token_count
        while token_count > target_token_count:
            msg = chat_log.pop()
            token_count -= msg.token_count
        # double check that the token count is correct
        return chat_log
    def _check_type(self, mode: str|list) -> None:
        def check_mode(mode: str) -> None:
            if mode not in self._modes:
                raise BadModeError(f"Invalid type: {mode}")
        if isinstance(mode, str):
            check_mode(mode)
        elif isinstance(mode, list):
            for one in mode:
                check_mode(one)
        elif isinstance(mode, tuple) or isinstance(mode, set):
            for one in mode:
                check_mode(mode)
        else:
            raise BadModeError(f"Invalid type: {type(mode)}")
    def generate_chat_log(self, type: str|list, target_token_count: int) -> list[dict]:
        """Generate a chat log of a given type and target token count
        Type can be either a string or a list of strings
        Available types are: short, medium, long, random
            short - from the short sample messages
            medium - from the medium sample messages
            long - from the long sample messages
            random - from all sample messages
        If list of strings is provided, the chat log will be generated from all the specified types

        """
        if isinstance(type, str):
            if type not in self._modes:
                raise BadModeError(f"Invalid type: {type}")
            encoded_messages = []
            if type == "random":
                
                for key in self._encoded_sample_messages.keys():
                    for msg in self._encoded_sample_messages[key]:
                        encoded_messages.append(msg)
            elif type == 'long':
                encoded_messages = self._encoded_sample_messages['long']
            elif type == "medium":
                encoded_messages = self._encoded_sample_messages['medium']
            elif type == "short":
                encoded_messages = self._encoded_sample_messages['short']
        elif isinstance(type, list):
            encoded_messages = []
            for category in type:
                if category not in self._modes:
                    raise BadModeError(f"Invalid type: {category}")
                for msg in self._encoded_sample_messages[category]:
                   encoded_messages.append(msg)

        return self.encoder.decode_message_list(self.generate_chat_log_from_encoded_messages(encoded_messages, target_token_count))
    
    def add_sample_message(self, type: str, message: dict = None, role: str= None, content: str= None) -> None:
        """
        Add new sample message to the sample messages
        Must include type: str enum('short', 'medium', 'long')
        Must include either message: dict or role: str and content: str
            either message: dict or role: str and content: str
            not both or neither

        """

        if not message and not(role and content):
            raise ValueError("Either message or role and content must be provided")
        if message and (role or content):
            raise ValueError("Either message or role and content must be provided, not both")
        if not message:
            message = {'role': role, 'content': content}
        
        if type not in self.sample_messages.keys():
            raise ValueError(f"Invalid type: {type}")
        self.sample_messages[type].append(message)
        self.encode_all_sample_messages()
    def remove_sample_message(self, type: str, message: str) -> None:
        """Removes a sample message from the sample messages"""
        if type not in self.sample_messages.keys():
            raise ValueError(f"Invalid type: {type}")
        self.sample_messages[type].remove(message)
        self.encode_all_sample_messages()
    def generate_n_messages(self, mode: str | list, n: int) -> list[dict]:
        self._check_type(mode)
        messages = []
        if isinstance(mode, str):
            
            if mode == "random":
                messages.extend(self.sample_messages['short'] + self.sample_messages['medium'] + self.sample_messages['long'])
            else:
                messages.extend( self.sample_messages[mode])
        elif isinstance(mode, list):
            for category in mode:
                try: 
                    messages.extend(self.sample_messages[category])
                except KeyError:
                    raise BadModeError(f"Invalid type: {category}")
                
        for _ in range(n):
            messages.append(random.choice(messages))
        return messages
        
        

    
            

def gen_and_write(type, target_token_count, file_name):
    generator = GenerateTestChatLog(model="gpt-4")
    chat_log = generator.generate_chat_log(type, target_token_count)
    path = os.path.join("test_chat_logs", file_name)
    with open(path, "w") as f:
        f.write(json.dumps(chat_log))
    print(f"Generated chat log of type {type} with target token count {target_token_count} and saved to {path}")

def gen_and_write_all_in_set(params: list ):
    for param in params:
        gen_and_write(**param)
        print("Generated and wrote chat log with params: ", param)

params = [
    {"type": "short", "target_token_count": 7000, "file_name": "short_7000.json"},
    {"type": "short", "target_token_count": 10000, "file_name": "short_10000.json"},
    {"type": ["short", "medium"], "target_token_count": 7000, "file_name": "short_medium_7000.json"},
    {"type": ['medium', 'long'], "target_token_count": 7000, "file_name": "medium_long_7000.json"},
    {"type": 'random', "target_token_count": 7000, "file_name": "random_7000.json"},
    {"type": 'random', "target_token_count": 10000, "file_name": "random_10000.json"},
]

def generate_random_chat_log(target_token_count: int):
    generator = GenerateTestChatLog(model="gpt-4")
    chat_log = generator.generate_chat_log('random', target_token_count)
    return chat_log

if __name__ == "__main__":
    generator = GenerateTestChatLog(model="gpt-4")
    with open('short_7K_tokens.json', "w") as f:
        chat_log = generator.generate_chat_log('short', 7000)
        f.write(json.dumps(chat_log))
            

