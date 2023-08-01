from configparser import ConfigParser
from typing import Any, Union, TypeVar
import os 

config = ConfigParser()
config_ini_content = """


[DISCORD BOT SETTINGS]
home_channel = 
; Add CHANNEL ID here
; This is the channel ID of the channel that the bot will reply to messages and commands in 
auto_save_enabled = true
auto_save_interval = 10 
; How often the bot will save the database in minutes
chunk_length = 500 
; How many characters the bot will send in one message. If the message is longer than this, it will be split into multiple messages. Don't set higher than 1990 as that is the max length of a discord message

; Other important settings such as the bot token and openai key are in the .env file, these are just settings that are possible to change during runtime with commands

[DEFAULT]
; do not alter these settings, used to reload the config file(in case you don't like the changes you made)
; or to reset the config file to default values
auto_save_enabled = true
chunk_length = 500
auto_save_interval = 10

"""
# setup config 
def make_config_if_none(name="./config/ini", content=config_ini_content) -> None:
    if  os.path.exists(name):
        return 
    with open(name, "w") as f:
        f.write(content)
make_config_if_none()
config.read("./config.ini")
#=============(DISCORD SETTINGS)=============================#
discord_settings = config['DISCORD BOT SETTINGS']

home_channel =config['DISCORD BOT SETTINGS'].getint('home_channel', 0)

auto_saving_enabled= config['DISCORD BOT SETTINGS'].getboolean('auto_saving_enabled', True)

auto_save_frequency = config['DISCORD BOT SETTINGS'].getint('auto_save_frequency', 10)

chunk_length = config['DISCORD BOT SETTINGS'].getint('chunk_length', 500)


#=====(CONFIG BAG)=====#
class ConfigBag:
    home_channel = home_channel
    auto_saving_enabled = auto_saving_enabled
    auto_save_frequency = auto_save_frequency
    chunk_length = chunk_length
CONFIG_BAG = ConfigBag()
    
#=====(CHANGE CONFIG)=====# 
class ChangeConfig:
    """An extremely simple class for changing the config.ini file, as well as retrieving values from it.
    Dependencies: configparser
    Args:
        filename (str, optional): The name of the config file. Defaults to "./config.ini".
    Attributes:
        filename (str): The name of the config file.
        config (ConfigParser): The config parser object.
        discord_settings (dict): The discord settings section of the config file.(ProxySection)
    Setters and Getters:
        home_channel (int): The home channel for the bot. Defaults to 0.
        auto_saving_enabled (bool): Whether or not auto saving is enabled. Defaults to True.
        auto_save_frequency (int): The frequency of auto saves. Defaults to 10.
    Private Methods:
        _check_datatype: Raises an error if the value is not the specified datatype.
        _write : Writes the config to the file.
        _refresh: Refreshes the config(Rereads the file and updates the discord_settings attribute)
        _write_and_refresh: Writes the config to the file and refreshes it.
    
    """
    def __init__(self, filename: str = "./config.ini"):
        self.filename = filename
        self.config = ConfigParser()
        self.config.read(self.filename)
        self.discord_settings = self.config['DISCORD BOT SETTINGS']
    @property
    def home_channel(self) -> int:
        """The home channel for the bot. Defaults to 0.(Will use the .env file if the value is not present in the config.ini file)"""
        return self.discord_settings.getint('home_channel', 0)
    @home_channel.setter
    def home_channel(self, value: int) -> None:
        """Sets the home channel for the bot."""
        if not isinstance(value, int):
            raise TypeError("home_channel must be an integer")
        self.config['DISCORD BOT SETTINGS']['home_channel'] = str(value)
        self._write_and_refresh()
    @property
    def auto_saving_enabled(self) -> bool:
        """Whether or not auto saving is enabled. Defaults to True."""
        return self.discord_settings.getboolean('auto_saving_enabled', True)
    @auto_saving_enabled.setter
    def auto_saving_enabled(self, value: bool) -> None:
        """Sets whether or not auto saving is enabled."""
        self._check_datatype(value, bool)
        self.config['DISCORD BOT SETTINGS']['auto_saving_enabled'] = str(value)
        self._write_and_refresh()
    @property
    def auto_save_frequency(self) -> int:
        """The frequency of auto saves. Defaults to 10.(How many messages between each auto save)"""
        return self.discord_settings.getint('auto_save_frequency', 10)
    @auto_save_frequency.setter
    def auto_save_frequency(self, value: int) -> None:
        """Sets the frequency of auto saves."""
        self._check_datatype(value, int)
        self.config['DISCORD BOT SETTINGS']['auto_save_frequency'] = str(value)
        self._write_and_refresh()
    @property
    def chunk_length(self) -> int:
        return self.discord_settings.getint('chunk_length', 500)
    @chunk_length.setter
    def chunk_length(self, value: int) -> None:
        self._check_datatype(value, int)
        self.config['DISCORD BOT SETTINGS']['chunk_length'] = str(value)
        self._write_and_refresh()
    
        

    @property
    def chunk_length(self) -> int:
        return self.discord_settings.getint('chunk_length', 500)
    @chunk_length.setter
    def chunk_length(self, value: int) -> None:
        self._check_datatype(value, int)
        self.config['DISCORD BOT SETTINGS']['chunk_length'] = str(value)
        self._write_and_refresh() 
    def _check_datatype(self, value: Any , datatype: Any ) -> None:
        """Raises an error if the value is not the specified datatype."""
        if not isinstance(value, datatype):
            raise TypeError(f"Value must be a {str(datatype)}, not a {type(value)}")
           
       
    def _write_and_refresh(self) -> None:
        """Writes the config to the file and refreshes it."""
        self._write()
        self._refresh()
    def _write(self) -> None:
        
        """Writes the config to the file."""
        with open(self.filename, "w") as configfile:
            self.config.write(configfile)
    def _refresh(self) -> None:
        """Refreshes the config."""
        self.config.read(self.filename)
        self.discord_settings = self.config['DISCORD BOT SETTINGS']

