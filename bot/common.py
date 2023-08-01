from config import ChangeConfig, CONFIG_BAG
from discord_settings import DISCORD_SETTINGS_BAG


def get_is_auto_saving() -> bool:
    """Returns whether or not auto saving is enabled."""
    if CONFIG_BAG.auto_saving_enabled:
        return True
    else:
        return False
    
def get_auto_save_frequency() -> int:
    """Returns the auto save frequency."""
    return CONFIG_BAG.auto_save_frequency

def get_home_channel() -> int:
    if CONFIG_BAG.home_channel != 0:
        return CONFIG_BAG.home_channel
    else: 
        return DISCORD_SETTINGS_BAG.BOT_HOME_CHANNEL
    
