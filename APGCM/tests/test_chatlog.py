import chat
import exceptions
import func 
import tiktoken
import unittest

class TestChatlog(unittest.TestCase):
    def setUp(self):
        self.chatlog = chat.ChatLog('gpt-4')
        self.user_message_content = "Hello, world!"
        self.assistant_message_content = "Hi, there"
        self.token_counter = func.count_tokens_in_str
        self.message_factory = chat.MessageFactory('gpt-4')
    def test_add_message(self):
        """Tests that the add message method works correctly."""
        message = self.message_factory(role = 'user', content = 'Hello, world!')
        self.chatlog.add_message(message)
        self.assertIn(message, self.chatlog.data)
    def test_add_message_bad_message(self):
        """Tests that the add message method raises the correct error."""
        with self.assertRaises(exceptions.NotAMessageError):
            self.chatlog.add_message('bad message')
    def test_get_messages(self):
        """Tests that the get messages method works correctly."""
        message = self.message_factory(role = 'user', content = 'Hello, world!')
        self.chatlog.add_message(message)
        for message in self.chatlog.get_messages():
            self.assertIsInstance(message, chat.Message)
            self.assertEqual(message.as_dict(), {'role': 'user', 'content': 'Hello, world!'})
    def test_get_pretty_messages(self):
        """Tests that the get pretty messages method works correctly."""
        self.chatlog.add_message(self.message_factory(role = 'user', content = 'Hello, world!'))
        self.assertEqual(self.chatlog.get_pretty_messages(), '> Hello, world!')
    def test_save_to_dict(self):
        msg = self.message_factory(role = 'user', content = 'Hello, world!')
        self.chatlog.add_message(msg)
        save_dict = self.chatlog.make_save_dict()
        self.assertIsInstance(save_dict, dict)
        self.assertIn('messages', save_dict)
        self.assertEqual(save_dict['messages'][0], msg.as_dict())
    def test_uuid_load(self):
        uuid = self.chatlog.uuid
        self.assertIsInstance(uuid, str)
        save_dict = self.chatlog.make_save_dict()
        test_chat_log: chat.ChatLog = chat.ChatLog('gpt-4')
        test_chat_log.load_from_dict(save_dict)
        self.assertEqual(test_chat_log.uuid, uuid)
    def test_load_from_dict(self):
        save_dict = self.chatlog.make_save_dict()
        test_chat = chat.ChatLog('gpt-4')
        test_chat.load_from_dict(save_dict)
        self.assertEqual(save_dict, test_chat.make_save_dict())
        
    def tearDown(self):
        del self.chatlog
        del self.user_message_content
        del self.assistant_message_content
        del self.token_counter
        del self.message_factory


if __name__ == '__main__':
    unittest.main(verbosity=2)
  