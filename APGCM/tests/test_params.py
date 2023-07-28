import chat_completion_wrapper
import func 
import unittest
import exceptions
import random 
print(dir(chat_completion_wrapper))
class TestParameters(unittest.TestCase):
    def setUp(self):
        self.parameters = chat_completion_wrapper.ModelParameters()
        self.test_parameters = {'temperature': 0.9, 'max_tokens': 150, 'top_p': 1, 'frequency_penalty': 0.0, 'presence_penalty': 0.0, }
    def test_set_temperature(self):
        self.parameters.temperature = 0.9
        self.assertEqual(self.parameters.temperature, 0.9)
    def test_set_max_tokens(self):
        self.parameters.max_tokens = 150
        self.assertEqual(self.parameters.max_tokens, 150)
    def test_set_top_p(self):
        self.parameters.top_p = 1
        self.assertEqual(self.parameters.top_p, 1)
    def test_set_frequency_penalty(self):
        self.parameters.frequency_penalty = 1.0
        self.assertEqual(self.parameters.frequency_penalty, 1.0)
    def test_set_presence_penalty(self):
        self.parameters.presence_penalty = 1.0
        self.assertEqual(self.parameters.presence_penalty, 1.0)
    def test_set_temperature_bad_value(self):
        with self.assertRaises(exceptions.BadModelParamError):
            self.parameters.temperature = 100
    def test_set_max_tokens_bad_value(self):
        with self.assertRaises(exceptions.BadModelParamError):
            self.parameters.max_tokens = -10
    def test_set_top_p_bad_value(self):
        with self.assertRaises(exceptions.BadModelParamError):
            self.parameters.top_p = 100
            
    def test_set_frequency_penalty_bad_value(self):
        with self.assertRaises(exceptions.BadModelParamError):
            self.parameters.frequency_penalty = 100
    def test_set_presence_penalty_bad_value(self):
        with self.assertRaises(exceptions.BadModelParamError):
            self.parameters.presence_penalty = 100
    def test_set_temperature_special_value(self):
        self.parameters.temperature = "none"
        self.assertEqual(self.parameters.temperature, None)
    def test_set_max_tokens_special_value(self):
        self.parameters.max_tokens = "none"
        self.assertEqual(self.parameters.max_tokens, None)
    def test_set_top_p_special_value(self):
        self.parameters.top_p = "none"
        self.assertEqual(self.parameters.top_p, None)
    def test_set_frequency_penalty_special_value(self):
        self.parameters.frequency_penalty = "none"
        self.assertEqual(self.parameters.frequency_penalty, None)
    def test_set_presence_penalty_special_value(self):
        self.parameters.presence_penalty = "none"
        self.assertEqual(self.parameters.presence_penalty, None)
    def test_set_temperature_str_good_val(self):
        self.parameters.temperature = "0.9"
        self.assertEqual(self.parameters.temperature, 0.9)
    def test_kwargs_dict(self):
        self.parameters.set_params(**self.test_parameters)
        self.assertEqual(self.test_parameters, self.parameters.get_param_kwargs())
        self.parameters.temperature = "none"
        self.assertNotIn("temperature", self.parameters.get_param_kwargs())
    def test_bad_dict_key(self):
        with self.assertRaises(exceptions.InvalidParamNameError):
            self.parameters.set_params(**{"bad_key": 1})
    def test_make_save_dict(self):
        self.parameters.set_params(**self.test_parameters)
        save_dict = self.parameters.make_save_dict()
        self.assertIsInstance(save_dict, dict)
    def test_load_save_dict(self):
        self.parameters.set_params(**self.test_parameters)
        save_dict = self.parameters.make_save_dict()
        test_params = chat_completion_wrapper.ModelParameters()
        test_params.load_from_save_dict(save_dict)
        self.assertEqual(test_params.get_param_kwargs(), self.parameters.get_param_kwargs())
        self.assertEqual(test_params.make_save_dict(), self.parameters.make_save_dict())
    def test_bad_save_dict(self):
        bad_save_dict = {"bad_key": 1}
        with self.assertRaises(exceptions.BadSaveDictionaryError):
            self.parameters.load_from_save_dict(bad_save_dict)
        
        
    
        
    
    def tearDown(self):
        del self.parameters
        del self.test_parameters
        
        
if __name__ == "__main__":
    unittest.main(verbosity=2)