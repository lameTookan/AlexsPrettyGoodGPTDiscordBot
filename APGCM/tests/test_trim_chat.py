import exceptions 
import chat 
import func
import unittest
import os
import sys 

"""Not Done, still need to add a few more tests(see below)"""


class TestTrimChatLog(unittest.TestCase):
    def setUp(self):
        self.trim = chat.TrimChatLog()
        self.message_factory = self.trim.get_message_factory()
    def test_add_message(self):
        message = self.message_factory(role='user', content='hello')
        self.trim.add_message(message)
        self.assertEqual(self.trim.get_finished_chatlog(), [message])
    def test_system_prompt(self):
        self.trim.system_prompt = "hello"
        self.assertEqual(self.trim.system_prompt.content, "hello")
    def test_get_message_factory(self):
        factory = self.trim.get_message_factory()
        self.assertIsInstance(factory, chat.MessageFactory)
    def test_get_finished_chatlog(self):
        """Tests that the get_finished_chatlog method returns the chatlog as a list of dictionaries"""
        self.trim.system_prompt = "hello"
        
        self.trim.add_message(self.message_factory(role='user', content='hello'))
        test_log = [
            {"role": "system", "content": "hello"},
            {"role": "user", "content": "hello"}
        ]
        self.assertEqual(self.trim.get_finished_chatlog(), test_log)
    def test_make_save_and_load(self):
        """Tests that save and load works together by making a save dict, loading it in a new object, and then comparing the two chatlogs
        Removes the timestamp and is_loaded keys from the save dict as these are designed to be different
        """
        self.maxDiff = None
        self.trim.system_prompt = "hello"
        self.trim.add_message(self.message_factory(role='user', content='hello'))
        
        test_save = self.trim.make_save_dict()
        test_trim = chat.TrimChatLog()
        test_trim.load_from_save_dict(test_save)
        self.assertEqual(test_trim.get_finished_chatlog(), self.trim.get_finished_chatlog())
        # these will by design be different, therefore in order to test them we must set them to the same value
        # we are testing that the rest of the save dict is the same
        test_save['timestamp'] = 0.00
        test_save['is_loaded'] = True 
        new_save = test_trim.make_save_dict()
        new_save['timestamp'] = 0.00
        new_save['is_loaded'] = True
        self.assertEqual(new_save, test_save)
    def test_user_message_setter(self):
        """Test that the user message setter works"""
        self.trim.user_message = "hello"
        self.assertEqual(self.trim.user_message, "hello")
        
        self.trim.user_message_as_Message = self.message_factory(role='user', content='hello')
        self.assertEqual(self.trim.user_message_as_Message.content, "hello")
    def test_assistant_message_setter(self):  
        """Test that the assistant message setter works"""
        self.trim.assistant_message = "hello"
        self.assertEqual(self.trim.assistant_message, "hello")
        
        self.trim.assistant_message_as_Message = self.message_factory(role='assistant', content='hello')
        self.assertEqual(self.trim.assistant_message_as_Message.content, "hello")
        
    def test_not_a_message_error(self):
        """Test that a non-message object raises an error"""
        with self.assertRaises(exceptions.NotAMessageError):
            self.trim.add_message("hello")
    def test_bad_save_dict_error(self):
        """Test that a bad save dict raises an error"""
        with self.assertRaises(exceptions.BadSaveDictionaryError):
            self.trim.load_from_save_dict({"hello": "world", "is_loaded": True, "timestamp": 0.00, "bad": "save_dict"})
        
    
    def test_trim_chat_log(self):
        """Tests that the trim_chat_log method works"""
        test_chat_log = func.get_test_chat_log()
        self.trim.add_messages_from_dict(test_chat_log)
        tokens_in_chat_log = 0
        for message in self.trim.get_finished_chatlog():
            tokens_in_chat_log += func.count_tokens_in_str(message['content'], 'gpt-4')
        self.assertLessEqual(tokens_in_chat_log, self.trim.max_chatlog_tokens)

    def test_set_token_info(self):
        self.trim.set_token_info(max_tokens = 20000, max_completion_tokens=1000, token_padding=100, max_messages=100)
        
        self.assertEqual(self.trim.max_completion_tokens, 1000)
        self.assertEqual(self.trim.token_padding, 100)
        self.assertEqual(self.trim.max_messages, 100)
    def test_set_model(self):
        self.trim.model = "gpt-3"
        self.assertEqual(self.trim.model, "gpt-3")
    def test_not_bad_save_dict_error(self):
        with self.assertRaises(exceptions.BadSaveDictionaryError):
            self.trim.load_from_save_dict({"bad": "save_dict"})
    
    def tearDown(self):
        del self.trim

if __name__ == '__main__':
    
    unittest.main(verbosity=2, )