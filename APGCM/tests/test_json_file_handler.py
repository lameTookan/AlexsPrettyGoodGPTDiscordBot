from file_handlers import gen_file
import func
import unittest
import logging 
import os
import json
import exceptions
class TestJSONFileHandler(unittest.TestCase):
    def setUp(self):
        self.json = gen_file.JsonFileHandler(save_folder = "./testing/file_handler/json/", )
        self.file_path = "./testing/file_handler/json/"
        self.test_dict = {
            "test": "Hello World!",
            "nested": {
                "test2": "Hello World!",
                "test3": "Hello World!"
                
            },
            "int": 1,
            "float": 1.0,
            "list": ["Hello", "World!"],
            "bool": True,
            "none": None,
            
        }
    def test_write_to_file(self):
        self.json.write_to_file("test.json", self.test_dict)
        with open(self.file_path + "test.json", "r") as f:
            file_contents = json.load(f)
        self.assertEqual(file_contents, self.test_dict)
    def test_read_from_file(self):
        with open(self.file_path + "test2.json", "w") as f:
            json.dump(self.test_dict, f)
        self.assertEqual(self.json.get_file_contents("test2.json"), self.test_dict)
    def test_delete_file(self):
        self.json.write_to_file("test3.json", self.test_dict)
        self.json.delete_file("test3.json")
        self.assertFalse(os.path.exists(self.file_path + "test3.json"))
    def test_get_file_list(self):
        for i in range(4):
            self.json.write_to_file(f"test{i}.json", self.test_dict)
        self.assertEqual(set(self.json.get_filenames()), {"test0.json", "test1.json", "test2.json", "test3.json"})
    def test_check_file_exists(self):
        """Test that check_if_file_exists returns True when a file exists and False when it does not"""
        self.assertFalse(self.json.check_if_file_exists("fake.json"))
        self.json.write_to_file("test4.json", self.test_dict)
        self.assertTrue(self.json.check_if_file_exists("test4.json"))
    def test_file_not_found(self):
        """Test that a file not found error is raised when a file does not exist"""
        with self.assertRaises(exceptions.FileNotFoundError):
            self.json.get_file_contents("test5.json")
    def test_file_exists_error(self):
        """test that a file exists error is raised when a file already exists and overwrite is False
        Also test that the file is written when overwrite is True
        """
        with self.assertRaises(exceptions.FileExistsError):
            self.json.write_to_file("test6.json", self.test_dict)
            self.json.write_to_file("test6.json", self.test_dict)
        self.json.write_to_file("test6.json", self.test_dict, overwrite=True)
    def test_not_a_dict(self):
        with self.assertRaises(exceptions.BadTypeError):
            self.json.write_to_file("test7.json", "Hello World!")
    def test_bad_json_file(self):
        """Test that a bad json file raises a BadJSONFileError"""
        with self.assertRaises(exceptions.BadJSONFileError):
            with open(self.file_path + "test8.json", "w") as f:
                f.write("Hello World!")
            self.json.get_file_contents("test8.json")
    def tearDown(self):
        del self.json
        for file in os.listdir(self.file_path):
            os.remove(self.file_path + file)
        
    

if __name__ == "__main__":
    unittest.main(verbosity=2)