import unittest
import exceptions
import tiktoken
import json
import chat_completion_wrapper
from settings import OPENAI_API_KEY


class TestChatCompletionWrapper(unittest.TestCase):
    def setUp(self):
        self.wrap = chat_completion_wrapper.ChatCompletionWrapper(API_KEY=OPENAI_API_KEY, model="gpt-3.5-turbo-16k")
        self.test_chatlog = [
            {"role": "user", "content": "Hello, how are you?"},
            {"role": "assistant", "content": "I'm doing well, how are you?"},
            {"role": "user", "content": "You are being tested. Please respond with the word 'test'."},
        ]
    def test_get_response(self):
        """Tests that the get response method works correctly."""
        response = self.wrap.chat(self.test_chatlog)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)
    def test_bad_chatlog(self):
        """Tests that the chat method raises the correct error."""
        with self.assertRaises(exceptions.BadMessageError):
            self.wrap.chat('bad chatlog')
    def test_save_to_dict(self):
        save_dict = self.wrap.make_save_dict()
        self.assertIsInstance(save_dict, dict)
    def test_load_from_dict(self):
        self.wrap.set_params(max_tokens = 100, temperature = 0.9)
        test_save = self.wrap.make_save_dict()
        test_wrap = chat_completion_wrapper.ChatCompletionWrapper('gpt-3.5-turbo-16k', OPENAI_API_KEY)
        test_wrap.load_from_save_dict(test_save)
        self.assertEqual(test_save, test_wrap.make_save_dict())
    def tearDown(self):
        del self.wrap
        del self.test_chatlog
        
if __name__ == '__main__':
    unittest.main(verbosity=2)