from chat_wrapper.rotate_save import RotatingSave
import unittest 
from handler.save_handler import DummySaveHandler
import exceptions 
from itertools import cycle
def make_saves_copy(save_name: str, num_saves: int) -> list:
    """Makes a list of save names"""
    # exact copy of the function in rotating_save.py
    return [f"{save_name}_{i}" for i in range(num_saves)]

class TestRotatingSave(unittest.TestCase):
    def setUp(self):
        """
        Um what the heck is a dummy save handler?
        
        Dummy save handler is a mock save handler that doesn't actually save anything
        it is valid: its a child of the AbstractCWSaveHandler class, but it just stores the save dict in memory(as a property called save_dict). So its very useful for testing so we don't have to deal with the file system(or a database) but we can still easily check if saves are being added correctly and retrieve them during runtime
        See APGCM/handler/save_handler.py for more info(its the last class in the file)
         
         """
        self.dummy_save_handler = DummySaveHandler()
        self.rotating_save = RotatingSave(self.dummy_save_handler)
        self.dummy_save_dict = {
            "This": "Is not a real save dict",
            "And this doesn't need to use the complex": "Schema that the real one does",
            "but ": "It shall do the job just fine",
            "1": 2,
            "a_list": [1, 2, 3, 4, 5],
            "nested_dict": {
                "a": "b",
                "c": "d",
            },
            "null": None,
            
        }
    def test_add_save_handler(self):
        """Tests that the save handler is added correctly"""
        self.rotating_save.add_save_handler(None)
        self.assertEqual(self.rotating_save.save_handler, None)
        self.rotating_save.add_save_handler(self.dummy_save_handler)
        self.assertEqual(self.rotating_save.save_handler, self.dummy_save_handler)
    def tests_bad_save_handler(self):
        """Tests that the incorrect object type error is raised correctly"""
        #making a class that is not a save handler
        class Example:
            def __str__(self):
                return "This is a dummy test class"
            pass
        example = Example()
        for i in [1, "Hello", True, 22.2, example, {"a": "b"}, [1, 2, 3, 4, 5], 4000, -500, "", ]:
            with self.subTest(str(i)):
                with self.assertRaises(exceptions.IncorrectObjectTypeError):
                    self.rotating_save.add_save_handler(i)
        with self.assertRaises(exceptions.IncorrectObjectTypeError):
            self.rotating_save.add_save_handler("Hello")
    def test_check_save_handler(self):
        """Tests that the save handler is checked correctly"""
        self.rotating_save.add_save_handler(None)
        # we can unset the save handler by setting it to None
        
        with self.assertRaises(exceptions.ObjectNotSetupError):
            # should raise an error because the save handler is not set
            self.rotating_save._check_save_handler()
        self.rotating_save.add_save_handler(self.dummy_save_handler)
        try:
            # we should not get an error here
            self.rotating_save._check_save_handler()
        except Exception as e:
            self.fail(f"Unexpected exception: {e}")
    def test_save_cycler(self):
        
        """Tests that the save cycler works as expected"""
        save_name = self.rotating_save.save_name 
        num_saves = self.rotating_save.num_saves
        # this is how the save naming scheme works
        save_names = [f"{save_name}_{i}" for i in range(num_saves)]
        cycle_iterator = self.rotating_save._make_cycle_iterator()
        for i in range(num_saves):
            with self.subTest(str(i)):
                # making sure that the cycle iterator returns the correct save names, just by iterating through it by the length of the save names (cycle_iterator is an infinite iterator so we can't just iterate through it)
                self.assertEqual(next(cycle_iterator), save_names[i])
    def test_save(self):
        """Tests that the save function works as expected"""
        self.rotating_save.save(self.dummy_save_dict)
        name = self.rotating_save.most_recent_entry_name 
        # making sure the save was added to the save handler
        self.assertEqual(self.dummy_save_handler.read_entry(name), self.dummy_save_dict)
    def test_find_most_recent_save(self):
        """Tests that the most recent save is found correctly"""
        # save dicts include a unix timestamp, here we are mocking that with some floats
        saves= dict(
        save1 = {"timecode": 1.02 }, save2 = {"timecode": 1.2 },save3 = {"timecode": 1.3})
        for name, value in saves.items():
            #save all of the saves
            self.rotating_save.save(value)
        most_recent_save_name = self.rotating_save.find_most_recent_save()
        # the most recent save should be save3
        actual_save = self.dummy_save_handler.read_entry(most_recent_save_name)   
        self.assertEqual(actual_save, saves["save3"]) 
    def test_set_save_info(self):
        """Tests that we can set the save name and number of saves correctly during runtime"""
        save_name = self.rotating_save.save_name
        self.rotating_save.set_save_info(save_name="new", num_saves=10)
        expected_saves = make_saves_copy(save_name="new", num_saves=10)
        # this property holds a list of all of the save names
        new_saves = self.rotating_save.saves 
        self.assertEqual(new_saves, expected_saves)
        # making sure the save name and number of saves were set correctly
        self.assertEqual(self.rotating_save.save_name, "new")
        
        self.assertEqual(self.rotating_save.num_saves, 10)
        #new saves should be the same length as the expected saves
        self.assertEqual(len(new_saves), 10)
    def test_bad_save_info_types(self):
        """Tests that a bad type error is raised when we try to set the save info to bad values"""
        # values are (save_name, num_saves). Save name should be a string, num_saves should be an int
        # an object that is def not a string or int
        class Example():
            def __str__(self):
                return "This is a dummy test class"
        example = Example()
        test_bad_info =[
            (10000, 10),
            (True, 10),
            (False, 10),
            ("Hello", "World"),
            ("Hello", 10.2),
            (10.2, 10),
            (10, 10.2),
            (example, 10),
            (10, example),
            (example, example),
            (None, 1.1),
            ({}, [])
        ]
        for i in test_bad_info:
            with self.subTest(str(i)):
                with self.assertRaises(exceptions.BadTypeError):
                    self.rotating_save.set_save_info(*i)
        

    def tearDown(self):
        #un comment for debuggings(Will save to test{int}.json in the saves directory) so we can see what the save dict looks like
        #self.dummy_save_handler.save_to_file(name="test")
        #if you want to inspect the save dict you can also do this:
        #self.dummy_save_handler.log_save_dict()
        # or if you wanna see it on the console:
        #self.dummy_save_handler.log_save_dict(print_save=True)
        del self.dummy_save_handler
        del self.rotating_save
        del self.dummy_save_dict
        
        
    
        
if __name__ == '__main__':
    unittest.main(verbosity=2)