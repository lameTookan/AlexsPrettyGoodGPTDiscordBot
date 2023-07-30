import logging
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch
import time

import exceptions
import func
from chat import ChatLog, Message, MessageFactory, TrimChatLog
from chat_completion_wrapper import ChatCompletionWrapper
from chat_wrapper import ChatWrapper
from freezegun import freeze_time
from handler.save_handler import AbstractCWSaveHandler, JsonSaveHandler, DummySaveHandler
from handler.stream_handler import (AbstractStreamOutputHandler,
                                    StdoutStreamHandler)
from settings import OPENAI_API_KEY
from templates.template_selector import TemplateSelector, template_select

print(sys.executable)
class TestChatWrapper(unittest.TestCase):
    def setUp(self):
        self.chat_wrapper = ChatWrapper(API_KEY=OPENAI_API_KEY, model = "gpt-4")
        self.chat_wrapper.auto_setup()
        self.save_handler = DummySaveHandler()
        self.stream_handler = StdoutStreamHandler()
        
    def test_auto_setup(self):
        """Tests that the auto setup method works as expected"""
        self.assertTrue(self.chat_wrapper)
        self.assertTrue(self.chat_wrapper.trim_object)
        self.assertTrue
        self.assertTrue(self.chat_wrapper.message_factory)
        self.assertTrue(self.chat_wrapper.completion_wrapper)
    def test_user_message_setter(self):
        """Tests that the user message is set correctly"""
        self.chat_wrapper.user_message = "Hello, my name is Bob."
        self.assertIsNotNone(self.chat_wrapper.user_message)
        self.assertEqual(self.chat_wrapper.user_message, "Hello, my name is Bob.")
    def test_assistant_message_setter(self):
        """Tests that the assistant message is set correctly"""
        self.chat_wrapper.assistant_message = "Hello, my name is Bob."
        self.assertIsNotNone(self.chat_wrapper.assistant_message)
        self.assertEqual(self.chat_wrapper.assistant_message, "Hello, my name is Bob.")
    def test_return_type(self):
        """Tests that the return type is set correctly"""
        self.chat_wrapper.return_type = "str"
        self.assertEqual(self.chat_wrapper.return_type, "str")
        self.chat_wrapper.return_type = "Message"
        self.assertIsInstance(self.chat_wrapper._format_return("Hello, my name is Bob."), Message)
    def test_set_model(self):
        """Tests that the model is set correctly"""
        self.chat_wrapper.model = "gpt-4"
        self.assertEqual(self.chat_wrapper.model, "gpt-4")
        self.assertEqual(self.chat_wrapper.completion_wrapper.model, "gpt-4")
    def test_set_trim_object(self):
        """Tests that the trim object is set correctly"""
        trim = TrimChatLog(model = "gpt3", system_prompt="This is a test prompt ||model||, ||date||, ||time||, ||cut_off||")
        self.chat_wrapper.set_trim_object(trim)
        self.assertEqual(self.chat_wrapper.trim_object, trim)
    def test_set_system_prompt(self):
        """Tests that the system prompt is set correctly"""
        self.chat_wrapper.system_prompt= "This is a test prompt"
        self.assertEqual(self.chat_wrapper.system_prompt, "This is a test prompt")
    @freeze_time("2021-01-01 12:00:00")
    def test_save_system(self):
        """Tests that save dictionarioary is created correctly"""
        self.maxDiff = None
        self.chat_wrapper.user_message = "Hello, my name is Bob."
        self.chat_wrapper.assistant_message = "Hello, my name is Bob."
        save_dict = self.chat_wrapper.make_save_dict()
        # time stamp will be different so we need to remove it
        
        test_chat_wrapper = ChatWrapper(API_KEY=OPENAI_API_KEY)
        test_chat_wrapper.load_from_save_dict(save_dict=save_dict)
        new_save  = test_chat_wrapper.make_save_dict()
       
        self.assertEqual(save_dict, new_save)
    @patch.object(ChatCompletionWrapper, "chat", return_value="Hello, my name is Bob.")
    def test_chat(self, mock_chat):
        """Test that the chat method works as expected, and the data is stored correctly"""
        self.maxDiff = None
        self.chat_wrapper.return_type = "str"
       
        result = self.chat_wrapper.chat("Hello")
       
        self.assertEqual(result, "Hello, my name is Bob.")
        self.assertEqual(mock_chat.call_count, 1)
        mock_chat.assert_called_with([{ "role": "user", "content": "Hello"}])
        self.assertEqual(self.chat_wrapper.user_message, "Hello")
        self.assertEqual(self.chat_wrapper.assistant_message, "Hello, my name is Bob.")
    def test_template(self): 
        """Tests that the template is set correctly"""
        template = template_select.get_template("gpt-4_default")
        wrap = ChatWrapper(API_KEY=OPENAI_API_KEY, model = "gpt-4", template=template)
        self.assertEqual(wrap.template, template)
        wrap.auto_setup_from_template()
        self.assertIsInstance(wrap.trim_object, TrimChatLog)
        wrap.trim_object.set_token_info(1600, 1000, 1000, 100 )
        wrap.auto_setup_from_template()
        self.assertEqual(wrap.trim_object.token_padding, 500)
    def test_get_recent_as_Message(self):
        """Tests that the get_recent_as_Message method works as expected"""
        message = Message(role="user", content="Hello", model="gpt-4")
        self.chat_wrapper.trim_object.add_message(message)
        self.assertEqual(self.chat_wrapper.get_most_recent_Message(), message)
        self.assertEqual(self.chat_wrapper.get_most_recent_Message(role="user"), message)
    def test_make_trim_object(self):
        """Tests that the trim object is created correctly"""
        chat_wrap = ChatWrapper(API_KEY=OPENAI_API_KEY, model = "gpt-4")
        self.assertIsNone(chat_wrap.trim_object)
        chat_wrap.make_trim_object(max_tokens = 6000, max_completion = 500, system_prompt= "test", token_padding=100, max_messages = 100)
        self.assertIsNotNone(chat_wrap.trim_object)
        self.assertEqual(chat_wrap.trim_object.max_tokens, 6000)
        self.assertEqual(chat_wrap.trim_object.max_completion_tokens, 500)
        self.assertEqual(chat_wrap.trim_object.system_prompt.content, "test")
        self.assertEqual(chat_wrap.trim_object.token_padding, 100)
        self.assertEqual(chat_wrap.trim_object.max_messages, 100)
    def test_make_complet_wrapper(self):
        """Runs a test to ensure that the completion wrapper is created correctly"""
        self.chat_wrapper.make_chat_completion_wrapper(temperature=0.9, max_tokens=100, top_p=1, frequency_penalty=0, presence_penalty=0, )
        self.assertEqual(self.chat_wrapper.completion_wrapper.parameters.temperature, 0.9)
        self.assertEqual(self.chat_wrapper.completion_wrapper.parameters.max_tokens, 100)
        self.assertEqual(self.chat_wrapper.completion_wrapper.parameters.top_p, 1)
        self.assertEqual(self.chat_wrapper.completion_wrapper.parameters.frequency_penalty, 0)
        self.assertEqual(self.chat_wrapper.completion_wrapper.parameters.presence_penalty, 0)
    
    def test_add_save_handler(self):
        """Test that the save handler is added correctly"""
        save_handler = DummySaveHandler()
        self.chat_wrapper.add_save_handler(save_handler)
        self.assertTrue(self.chat_wrapper._check_save_handler())
        self.assertEqual(self.chat_wrapper.save_handler, save_handler)
    def test_check_file(self):
        """Test that the check file method works as expected"""
        save_handler = DummySaveHandler()
        self.chat_wrapper.add_save_handler(save_handler)
        save_handler.write_entry("test", {"test": "test"}, True)
        self.assertTrue(self.chat_wrapper.check_entry_name("test"))
        self.assertFalse(self.chat_wrapper.check_entry_name("test2"))
        self.chat_wrapper.delete_entry("test")
    def test_not_setup_error(self):
        
        """Checks that object not setup error is raised when the object is not setup and a """
        with self.assertRaises(exceptions.ObjectNotSetupError):
            self.chat_wrapper.save("test")
    @freeze_time("2021-01-01 12:00:00")
    def test_save(self):
        """Test that the save method works as expected Freeze time is used so we can check the time stamp"""
        self.chat_wrapper.add_save_handler(self.save_handler)
        self.chat_wrapper.save("Test", True)
        self.assertTrue(self.save_handler.check_entry("Test")) 
        test_dict = self.save_handler.read_entry("Test")
        self.assertEqual(test_dict, self.chat_wrapper.make_save_dict())
        try:
            self.chat_wrapper.load("Test")
        except:
            self.fail("Load failed")
        self.chat_wrapper.delete_entry("Test")
    def test_all_entry_names(self):
        self.chat_wrapper.add_save_handler(self.save_handler)
        self.chat_wrapper.save("Test", True)
        ls = self.chat_wrapper.all_entry_names 
        self.assertIsInstance(ls, list)
        self.assertIn("Test", ls)
        self.chat_wrapper.delete_entry("Test")
    def test_add_stream_handler(self):
        """Test that the stream handler is added correctly"""
        self.chat_wrapper.add_stream_handler(self.stream_handler)
        self.assertIsInstance(self.chat_wrapper.stream_handler, StdoutStreamHandler)
        self.assertIsInstance(self.chat_wrapper.stream_handler, AbstractStreamOutputHandler)
        self.assertIsInstance(self.chat_wrapper.completion_wrapper.stream_handler, AbstractStreamOutputHandler)
        self.assertTrue(self.chat_wrapper._has_stream_handler())
    def test_not_a_stream_handler(self):
        """Test that the correct error is raised when the object is not a stream handler"""
        class Example:
            pass
        with self.assertRaises(exceptions.IncorrectObjectTypeError):
            self.chat_wrapper.add_stream_handler(Example())
        with self.assertRaises(exceptions.IncorrectObjectTypeError):
            self.chat_wrapper.add_stream_handler("test")
    # =====(TESTS FOR THE NEW AUTO-SAVE FEATURE)=====
    def test_auto_save_is_setup(self):
        self.assertFalse(self.chat_wrapper._check_autosaving())
        self.assertFalse(self.chat_wrapper._is_autosaving)
        self.chat_wrapper.add_save_handler(self.save_handler)
        self.chat_wrapper.set_is_saving(True)
        self.assertTrue(self.chat_wrapper._check_autosaving())
        self.assertTrue(self.chat_wrapper._is_autosaving)
    def test_auto_save(self):
        """Tests that the auto save feature works as expected"""
        # to use the auto saving feature we need a save handler and for the attribute to be enabled
        self.chat_wrapper.add_save_handler(self.save_handler)
        self.chat_wrapper.auto_setup_autosaving() # this will automatically take care of all of that 
        self.assertTrue(self.chat_wrapper._is_autosaving)
        self.assertTrue(self.chat_wrapper._check_autosaving())
        self.chat_wrapper.set_auto_save_info(auto_save_entry_name="test", auto_save_frequency=1, auto_save_max_saves=3)
        for i in range(5):
            self.chat_wrapper.user_message = f"Test {i}"
            self.chat_wrapper.assistant_message = f"Test {i}"
        save_names = self.save_handler.entry_names
        
        self.assertEqual(len(save_names), 3) # we should have 3 saves
    def test_load_most_recent_save(self):
        self.maxDiff = None
        self.chat_wrapper.add_save_handler(self.save_handler)
        self.chat_wrapper.auto_setup_autosaving() # this will automatically take care of all of that
        self.chat_wrapper.set_auto_save_info(auto_save_entry_name="test", auto_save_frequency=1, auto_save_max_saves=3)
        for i in range(4):
            self.chat_wrapper.user_message = f"Test {i}"
            #time.sleep(2)
        # save dict will by its nature be the most recent save
        most_recent = self.chat_wrapper.rotating_save_handler.most_recent_entry_name 
        self.assertEqual(self.chat_wrapper.rotating_save_handler.find_most_recent_save(), most_recent)
       
        try:
             self.chat_wrapper.load_auto_save()
        except Exception as e:
            self.fail(f"Unexpected exception: {e}")
    def test_auto_save_on_init(self):
        """Tests that the auto save feature works as expected when it is enabled on init (with the save handler and after auto_setup_from_template)"""
        temp = template_select.get_template("gpt-4_default")
        new_cw = ChatWrapper(API_KEY=OPENAI_API_KEY, model = "gpt-4", save_handler=self.save_handler, template=temp,is_auto_saving=True) 
        new_cw.auto_setup_from_template()
        self.assertTrue(new_cw._is_autosaving)
        self.assertTrue(new_cw._check_autosaving())
    
    
        
     
    def tearDown(self):
        # so we can see the dummy save dict before it is deleted
        #print(self.save_handler.save_dict)
        del self.chat_wrapper
        del self.save_handler
        


if __name__ == "__main__":
    unittest.main(verbosity=2)
        

