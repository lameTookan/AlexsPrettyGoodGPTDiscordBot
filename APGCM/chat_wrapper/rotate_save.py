from itertools import cycle
from typing import Any, Dict, List, Optional, Union

import exceptions
from handler.save_handler import AbstractCWSaveHandler, JsonSaveHandler
from log_config import DEFAULT_LOGGING_LEVEL, BaseLogger


class RotatingSave:
    """Rotating save is a class that handles saving data to multiple saves. It will cycle through the saves and save the data to the next save in the cycle.
    Meant to be used by ChatWrapper to save data to automatically generated saves.
    Dependencies:
        Custom:
            exceptions
            AbstractCWSaveHandler(or children)
            BaseLogger and DEFAULT_LOGGING_LEVEL from log_config
        Python:
            itertools.cycle
            Typing for type hints
    Raises:
        exceptions.BadTypeError: Raised if a value is not the correct type
        exceptions.IncorrectObjectTypeError: Raised if an object is not the correct type
        exceptions.ObjectNotSetupError: Raised if save_handler is None and a method that requires save_handler is called
    Args:
        save_handler (AbstractCWSaveHandler): The save handler to use for saving the data
        save_name (str): The name of the save. The save name will be appended with a number to create the save names. Defaults to "auto_save"
        num_saves (int): The number of saves to use. Defaults to 3
    Attributes:
        logger (BaseLogger): The logger for the rotating save
        save_handler (AbstractCWSaveHandler): The save handler to use for saving the data
        save_name (str): The name of the save. The save name will be appended with a number to create the save names. Defaults to "auto_save"
        num_saves (int): The number of saves to use. Defaults to 3
        saves (List[str]): The names of the saves(automatically generated)
        cycle_iterator (cycle): The cycle iterator that cycles through the saves
        _save_handler (AbstractCWSaveHandler): The save handler to use for saving the data. This is the private version of save_handler. It is used to prevent infinite recursion when setting the save handler
    Methods:
        Private:
            _setup_names: Sets up the names for the saves, by appending a number to the save name, naming them save_name_0, save_name_1, etc. Checks that entries exist for the saves, and if they don't, creates them(Blank entries)
            _make_cycle_iterator: Makes the cycle iterator that cycles through the saves
            _check_save_handler: Checks that the save handler is not None. Raises an error if it is.
        Public:
            Setup/Names:
                set_save_info: Sets the save info. If the save info is None, then it is not set. Runs _setup_names to set up the names for the saves
            Save Handler Management:
                add_save_handler: Adds a save handler to the rotating save object. If the save handler is None, then the save handler is set to None.
                save_handler: The save handler to use for saving the data. Convenience methods for add_save_handler   
            Core:
                save: Saves the data using the save handler naming the save using the cycle iterator Will overwrite the save if it already exists
                find_most_recent_save() -> str : Finds the most recent save and returns the name of the save. Uses the unix time code stored in the save to determine which save is the most recent. Returns the entry name 
                
    Examples:
        Not really intended for public use, as ChatWrapper will create and use the rotating save object from it's save handler.
    
        How ChatWrapper uses RotatingSave:
        ((Note: This has not been implemented yet as of writting this class and is subject to change, however, this is the intended use))
            def auto_save_tick(self) -> None:
                self.logger.info("Auto save tick called!")
                if  not self._is_auto_saving():
                    return 
                self._auto_save_ticks += 1
                if self._auto_save_ticks >= self._auto_save_frequency:
                    self._auto_save_ticks = 0
                    self.logger.info("Auto save tick count reached, saving...")
                    self.rotating_save.save(self.get_save_dict())
                    self.logger.info("Save complete!")
        def load_auto_save(self) -> None:
            
            self.logger.info("Loading auto save...")
            self.rotating_save.set_save_info(num_saves=self._auto_save_entries, save_name=self._auto_save_entry_name)
            most_recent_save = self.rotating_save.find_most_recent_save()
            self.save_handler.load(most_recent_save)
            self.logger.info("Auto save loaded!")
            
        
    """
    def __init__(self, save_handler: AbstractCWSaveHandler = None , save_name: str = "auto_save", num_saves: int =3):
        self.logger = BaseLogger(module_name=__file__, filename="rotating_save.log",level=DEFAULT_LOGGING_LEVEL, identifier="rotating_save")
        self.logger.info("Initializing rotating save...")
        
        self.save_name = save_name
        self.num_saves = num_saves
        self.saves = None
        
        
        self.cycle_iterator = None
        self.most_recent_entry_name = ""
        self.add_save_handler(save_handler)
        self.logger.info("Rotating save initialized!")
    #======(SETUP/NAMING)======
    def _setup_names(self) -> None:
        """Sets up the names for the saves"""
        self.logger.info("Setting up names...")
        self.saves = [f"{self.save_name}_{i}" for i in range(self.num_saves)]
        self.cycle_iterator = self._make_cycle_iterator()
        # if self.save_handler is None:
        #     return
        # for save in self.saves:
        #     if not self.save_handler.check_entry(save):
        #         self.save_handler.write_entry(save, {})
        # I don't think this is necessary, as the save handler will create the entry if it doesn't exist. It could cause issues if the handler tries to load a blank entry that does exist, so removing it for now
        self.logger.info("Names set up!")
    def _make_cycle_iterator(self) -> cycle:
        self.logger.info("Making cycle iterator...")
        saves = self.saves
        cycle_iterator = cycle(saves)
        return cycle_iterator
    
    def set_save_info(self, num_saves: int = None, save_name: str = None) -> None:
        
        """Sets the save info. If the save info is None, then it is not set."""
        if num_saves is not None:
            if not isinstance(num_saves, int):
                raise exceptions.BadTypeError("num_saves must be an int")
            self.num_saves = num_saves
        if save_name is not None:
            if not isinstance(save_name, str):
                raise exceptions.BadTypeError("save_name must be a string")
            self.save_name = save_name
        self.logger.info(f"Save info set to num_saves: {self.num_saves}, save_name: {self.save_name}")
        self._setup_names()
    #======(SAVE HANDLER MANAGEMENT)======   
    def add_save_handler(self, save_handler: AbstractCWSaveHandler) -> None:
        """Adds a save handler to the rotating save object. If the save handler is None, then the save handler is set to None."""
        if not isinstance(save_handler, AbstractCWSaveHandler) and save_handler is not None:
            self.logger.error(f"Expected {AbstractCWSaveHandler}, got {type(save_handler)}")
            raise exceptions.IncorrectObjectTypeError(
                f"Expected {AbstractCWSaveHandler}, got {type(save_handler)}"
            )
        if save_handler is None:
            self.logger.info("Save handler set to None")
            self._save_handler = save_handler
            return 
        else:
            self.logger.info(f"Save handler set to {save_handler}")
            
            self._save_handler = save_handler
            self._setup_names()
        
    def _check_save_handler(self) -> None:
        "Raises an error if the save handler is None"
        if self._save_handler is None:
            self.logger.error("Save handler is None")
            raise exceptions.ObjectNotSetupError("Save handler is None and therefore cannot be used")
    @property
    def save_handler(self) -> AbstractCWSaveHandler:
        """Returns the save handler"""
        
        return self._save_handler
    @save_handler.setter
    def save_handler(self, value: AbstractCWSaveHandler) -> None:
        """Sets the save handler using the add_save_handler method"""
        # two methods to provide a convenient way and idiomatic way to set the save handler while maintaining the flexibility of the add_save_handler method(enables using it through reference and easy overriding)
        self.add_save_handler(value)
    #=======(CORE)======
    def save(self, data: dict) -> None:
        """Saves the data using the save handler"""
        self._check_save_handler()
        self.logger.info(f"Saving data: {data}")
        name = next(self.cycle_iterator)
        self.most_recent_entry_name = name
        self.save_handler.write_entry(name, data, overwrite=True)
        self.logger.info(f"Data saved to {name}")
    def reset(self) -> None:
        """Deletes all saves"""
        self._check_save_handler()
        self.logger.info("Resetting saves...")
        for save in self.saves:
            if self.save_handler.check_entry(save):
                self.save_handler.delete_entry(save)
            
                self.logger.warning(f"Save {save} deleted")
            else:
                self.logger.warning(f"Save {save} does not exist")
                
    def backup_saves(self):
        """Backs up all saves by renaming them to save_name_backup_i"""
        self._check_save_handler()
        self.logger.info("Backing up saves...")
        for i, save in enumerate(self.saves):
            if self.save_handler.check_entry(save):
                entry = self.save_handler.read_entry(save)
                # no rename method, so we have to read the entry, delete the old entry, and write the entry to the new name
                self.save_handler.write_entry(f"{self.save_name}_backup_{i}", entry, overwrite=True)
                self.logger.info(f"Save {save} backed up")
            else:
                self.logger.info(f"Save {save} does not exist")
    def find_most_recent_save(self) -> str:
        """Finds the most recent save and returns the name of the save. Uses the unix time code stored in the save to determine which save is the most recent.
        Will only work if the save names/number of saves have not been changed since the last time the most recent save was saved.
        """
        self._check_save_handler()
        self.logger.info("Finding most recent save...")
      
        if self.saves is None:
            # if the saves are not set up, then set them up
            self._setup_names()
        # set the first save as the most recent save so if they are all zero or empty, then the first save will be returned
        most_recent_timecode = 0
        most_recent_save = None
        
        for save in self.saves:
            if not self.save_handler.check_entry(save):
                self.logger.info(f"Save {save} does not exist")
                continue
            save_dict = self.save_handler.read_entry(save)
            timecode = float(save_dict.get("timecode", 0))
            if timecode > most_recent_timecode:
                most_recent_timecode = timecode
                most_recent_save = save
        self.logger.info(f"Most recent save is {most_recent_save}")
        return most_recent_save
        
    
        