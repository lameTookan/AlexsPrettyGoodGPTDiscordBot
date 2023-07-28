from file_handlers import GeneralFileHandler, JsonFileHandler,TextFileHandler
from pathlib import Path
import func 
import os
import unittest
import exceptions
def read_file(file_path):
    file_path = Path(file_path)
    return file_path.read_text()

class TestGeneralFileHandler(unittest.TestCase):
    def setUp(self):
        self.gen = GeneralFileHandler(save_folder = "./testing/file_handler", file_extension=".txt")
        self.file_path = Path("./testing/file_handler/")
    def test_write_to_file(self):
        self.gen.write_to_file("test.txt", "Hello World!")
        file_contents = read_file(self.file_path / "test.txt")
        self.assertEqual(file_contents, "Hello World!")
    def test_read_from_file(self):
        
        path = self.file_path / "test2.txt"
        path.write_text("Hello World!")
        
        file_contents = self.gen.get_file_contents("test2.txt")
        self.assertEqual(file_contents, "Hello World!")
    def test_delete_file(self):
        path = self.file_path / "test3.txt"
        path.write_text("Hello World!")
        self.gen.delete_file("test3.txt")
        self.assertFalse(path.exists())
    def test_get_file_list(self):
        self.gen.write_to_file("test4.txt", "Hello World!")
        self.gen.write_to_file("test5.txt", "Hello World!")
        self.gen.write_to_file("test6.txt", "Hello World!")
        self.assertEqual(set(self.gen.get_filenames()), {"test4.txt", "test5.txt", "test6.txt"})
    def test_file_not_found(self):
        with self.assertRaises(exceptions.FileNotFoundError):
            self.gen.get_file_contents("test7.txt")
    def test_file_exists_error(self):
        self.gen.write_to_file("test8.txt", "Hello World!")
        with self.assertRaises(exceptions.FileExistsError):
            self.gen.write_to_file("test8.txt", "Hello World!")
        self.gen.write_to_file("test8.txt", "Hello World!", overwrite=True)
        
    
        
        
    
    def tearDown(self):
        del self.gen
        for file in self.file_path.glob("*.txt"):
            os.remove(file)
        
        
if __name__ == "__main__":
    unittest.main(verbosity=2)