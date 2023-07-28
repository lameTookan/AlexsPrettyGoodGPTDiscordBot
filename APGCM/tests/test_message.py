import chat
import unittest
import exceptions
from func import count_tokens_in_str

class TestMessageAndFactory(unittest.TestCase):
    def setUp(self):
        self.user_message = chat.Message('user', 'Hello, world!', 'gpt-4')
        self.assistant_message = chat.Message('assistant', 'Hi There!', 'gpt-4')
        self.user_message_content = "Hello, world!"
        self.assistant_message_content = "Hi, there"
        self.factory = chat.MessageFactory('gpt-4')
    def test_message_factory(self):
        """Tests that the message factory is created correctly."""
        self.assertIsInstance(self.factory, chat.MessageFactory)
        self.assertEqual(self.factory.model, 'gpt-4')
        self.assertIsNone(self.factory.role)
    def test_message_factory_make_message(self):
        """Tests that the message factory makes messages correctly."""
        test_message = self.factory(role = 'user', content = 'Hello, world!')
        self.assertIsInstance(test_message, chat.Message)
        self.assertEqual(test_message.as_dict(), {'role': 'user', 'content': 'Hello, world!'})
        self.assertEqual(test_message.role, 'user')
    def test_message_tokens(self):
        """Tests that the message tokens are counted correctly."""
        tokens_user = count_tokens_in_str(self.user_message_content, 'gpt-4')
        tokens_assistant = count_tokens_in_str(self.assistant_message_content, 'gpt-4')
        self.assertEqual(self.user_message.tokens, tokens_user)
        self.assertEqual(self.assistant_message.tokens, tokens_assistant)
    def test_message_pretty(self):
        """Tests that the message pretty string is created correctly."""
        self.assertEqual(self.user_message.pretty, "> Hello, world!")
    def test_message_as_dict(self):
        """Tests that the message is converted to a dictionary correctly."""
        self.assertEqual(self.user_message.as_dict(), {'role': 'user', 'content': 'Hello, world!'})
    def test_bad_role_error(self):
        """Tests that the bad role error is raised correctly."""
        with self.assertRaises(exceptions.BadRoleError):
            chat.Message('bad_role', 'Hello, world!', 'gpt-4')
        
        

        
    def tearDown(self):
        del self.user_message
        del self.assistant_message
        del self.factory


if __name__ == '__main__':
    unittest.main(verbosity=2)