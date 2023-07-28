import chat 
import datetime 
import unittest
import exceptions
import func 


"""datetime.date.today().strftime("%B %d, %Y")"""

class TestSystemPrompt(unittest.TestCase):
    def setUp(self):
        self.system_prompt = chat.SystemPrompt('gpt-4')
        self.test_system_prompt = "You are a helpful AI assistant. Your model is ||model||, todays date is  ||date||, and the time is  ||time||. Your training data was last updated on ||cut_off||."
        self.test_wildcard_prompt = "||model|| ||date|| ||time|| ||cut_off||"
    def test_system_prompt(self):
        """Tests that a system prompt can be set and retrieved."""
        self.system_prompt.system_prompt = self.test_system_prompt
        self.assertEqual(self.system_prompt._system_prompt, self.test_system_prompt)
        self.assertIsInstance(self.system_prompt.system_prompt, str)
    def test_system_prompt_tokens(self):
        """Tests that the number of tokens in the system prompt is correct."""
        test_tokens = func.count_tokens_in_str(model = 'gpt-4', string = self.test_system_prompt) + 20
        self.system_prompt.system_prompt = self.test_system_prompt
        self.assertEqual(self.system_prompt.system_prompt_tokens, test_tokens)
    def test_wildcard_model(self):
        """Tests that the model wildcard is replaced with the model name."""
        test_prompt_model = "||model||"
        self.system_prompt.system_prompt = test_prompt_model
        self.assertEqual(self.system_prompt.system_prompt, "gpt-4")
    def test_wildcard_date(self):
        """Tests that the date wildcard is replaced with the date."""
        test_prompt_date = "||date||"
        self.system_prompt.system_prompt = test_prompt_date
        self.assertEqual(self.system_prompt.system_prompt, datetime.date.today().strftime("%B %d, %Y"))
    def test_system_prompt_message(self) -> None:
        """Tests that the system prompt message is created correctly."""
        test_message = chat.Message(role='system', content="test", model = 'gpt-4')
        self.system_prompt.system_prompt = "test"
        self.assertEqual(self.system_prompt.system_prompt_message, test_message)

            
        

    def tearDown(self) -> None:
        del self.system_prompt
        
if __name__ == '__main__':
    unittest.main(verbosity=2)