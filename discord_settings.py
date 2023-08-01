import os

from dotenv import load_dotenv
from config import CONFIG_BAG, ChangeConfig, prompts_bag
load_dotenv()
# NOTE OPENAI SETTINGS are in APGCM/settings.py (eg API key, default model, etc)

# =============(BOT INFO)=============#

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_PREFIX = os.getenv("BOT_PREFIX")
BOT_HOME_CHANNEL = int(os.getenv("BOT_HOME_CHANNEL"))
MESSAGE_CHUNK_LEN = int(os.getenv("MESSAGE_CHUNK_LEN", 1000))
MESSAGE_CHUNK_LEN = int(os.getenv("MESSAGE_CHUNK_LEN", 300))
#=======(AUTO SAVING)=======#
AUTO_SAVING_ENABLED = os.getenv("AUTO_SAVING_ENABLED", "True")
if AUTO_SAVING_ENABLED.lower().strip() in ("true", "1", "yes", "on", 1, "y"):
    AUTO_SAVING_ENABLED = True
else:
    AUTO_SAVING_ENABLED = False
AUTO_SAVE_FREQUENCY = int(os.getenv("AUTO_SAVE_FREQUENCY", 10))



# ================(SYSTEM PROMPTS)================#

# ==================(DEFAULT MODES)=================#
# =====(CASUAL MODE )=====#

CASUAL_MODE_REMINDER = os.getenv("CASUAL_MODE_REMINDER", prompts_bag.casual_mode_reminder)
CASUAL_MODE_SYSTEM_PROMPT = os.getenv("CASUAL_MODE_SYSTEM_PROMPT", prompts_bag.casual_mode_system)

# +=====(ASSISTANT MODE)=====#



ASSISTANT_MODE_SYSTEM_PROMPT = os.getenv("ASSISTANT_MODE_PROMPT", prompts_bag.assistant_mode_prompt)
ASSISTANT_MODE_REMINDER = os.getenv("ASSISTANT_MODE_REMINDER", prompts_bag.assistant_mode_reminder)


# =====(DEFAULT MODE)=====#


DEFAULT_REMINDER = os.getenv(
    "DEFAULT_REMINDER", prompts_bag.default_mode_reminder
)
DEFAULT_DISCORD_SYSTEM_PROMPT = os.getenv(
    "DEFAULT_DISCORD_SYSTEM_PROMPT", prompts_bag.default_mode_system_prompt
)
#=====(HELP MODE)=====#
HELP_MODE_REMINDER = prompts_bag.help_mode_reminder
HELP_MODE_PROMPT = prompts_bag.help_mode_prompt

# =============(DISCORD SETTINGS BAG)=============#
class DiscordSettingsBag:
    def __init__(self):
        self.BOT_PREFIX = BOT_PREFIX
        self.BOT_HOME_CHANNEL = BOT_HOME_CHANNEL
        self.BOT_TOKEN = BOT_TOKEN
        self.DEFAULT_DISCORD_SYSTEM_PROMPT = DEFAULT_DISCORD_SYSTEM_PROMPT
        self.MESSAGE_CHUNK_LEN = MESSAGE_CHUNK_LEN
        self.AUTO_SAVING_ENABLED = AUTO_SAVING_ENABLED
        self.AUTO_SAVE_FREQUENCY = AUTO_SAVE_FREQUENCY
        # ==================(DEFAULT MODES)=================#
        self.DEFAULT_REMINDER = DEFAULT_REMINDER
        self.DEFAULT_DISCORD_SYSTEM_PROMPT = DEFAULT_DISCORD_SYSTEM_PROMPT
        # =====(CASUAL MODE )=====#
        self.CASUAL_MODE_REMINDER = CASUAL_MODE_REMINDER
        self.CASUAL_MODE_SYSTEM_PROMPT = CASUAL_MODE_SYSTEM_PROMPT
        #=====(ASSISTANT MODE)=====#
        self.ASSISTANT_MODE_REMINDER =  ASSISTANT_MODE_REMINDER
        self.ASSISTANT_MODE_SYSTEM_PROMPT = ASSISTANT_MODE_SYSTEM_PROMPT
        #=====(HELP MODE)=====#
        self.HELP_MODE_REMINDER = HELP_MODE_REMINDER
        self.HELP_MODE_PROMPT = HELP_MODE_PROMPT
        
        self._sync_config()
    def _sync_config(self):
        self.config = ChangeConfig()
        if self.config.home_channel == 0:
            self.config.home_channel = self.BOT_HOME_CHANNEL

        if self.config.home_channel != BOT_HOME_CHANNEL :
            self.BOT_HOME_CHANNEL = self.config.home_channel
            self.BOT_HOME_CHANNEL = BOT_HOME_CHANNEL

        if self.config.chunk_length != self.MESSAGE_CHUNK_LEN:
            self.MESSAGE_CHUNK_LEN = self.config.chunk_length
        if self.config.auto_saving_enabled != AUTO_SAVING_ENABLED:
           self.AUTO_SAVING_ENABLED = self.config.auto_saving_enabled  
        if self.config.auto_save_frequency != AUTO_SAVE_FREQUENCY:
            self.AUTO_SAVE_FREQUENCY = self.config.auto_save_frequency

DISCORD_SETTINGS_BAG = DiscordSettingsBag()

#=============(SYNC CONFIG.INI)=============#



# ================================================================================================
# =============(TESTING)=============#
YELLOW = "\033[33m"
RESET = "\033[0m"
MAGENTA = "\033[35m"
divider = "=========================================================" 
divider_len = len(divider)
def hide_key(key: str | None) -> str:
    """Returns a string of asterisks the same length as the key."""
    if key is None:
        return "Not Present"
    obscured = key[:2]
    return obscured + ("*" * (len(key) - 2))


def make_settings_string(hide_token: bool = True) -> str:
    if hide_token:
        token = hide_key(DISCORD_SETTINGS_BAG.BOT_TOKEN)
    else:
        token = DISCORD_SETTINGS_BAG.BOT_TOKEN
        

    
   
    settings_list = [
        divider, 
        f"{MAGENTA}====(DISCORD SETTINGS)===={RESET}".center(divider_len),
        divider,
        "\n\n",
        "====================(BOT INFO)====================",
        
        f"{YELLOW}BOT_TOKEN:{RESET} {token}",
        f"{YELLOW}BOT_PREFIX:{RESET} {DISCORD_SETTINGS_BAG.BOT_PREFIX}",
        f"{YELLOW}BOT_HOME_CHANNEL:{RESET} {DISCORD_SETTINGS_BAG.BOT_HOME_CHANNEL}",
        f"{YELLOW}MESSAGE_CHUNK_LEN:{RESET} {DISCORD_SETTINGS_BAG.MESSAGE_CHUNK_LEN}",
        "\n",
        "====================(SYSTEM PROMPTS)====================",
        "\n",
        f"====(DEFAULT MODE)====",
        "\n",
        f"{YELLOW}DEFAULT_DISCORD_SYSTEM_PROMPT:{RESET} {DISCORD_SETTINGS_BAG.DEFAULT_DISCORD_SYSTEM_PROMPT}",
        f"{YELLOW}DEFAULT_REMINDER:{RESET} {DISCORD_SETTINGS_BAG.DEFAULT_REMINDER}",
        "\n",
        f"====(CASUAL MODE)====",
        f"{YELLOW}CASUAL_MODE_REMINDER:{RESET} {DISCORD_SETTINGS_BAG.CASUAL_MODE_REMINDER}",
        f"{YELLOW}CASUAL_MODE_SYSTEM_PROMPT:{RESET} {DISCORD_SETTINGS_BAG.CASUAL_MODE_SYSTEM_PROMPT}",
        "\n",
        f"====(ASSISTANT MODE)====",
        f"{YELLOW}ASSISTANT_MODE_REMINDER:{RESET} {DISCORD_SETTINGS_BAG.ASSISTANT_MODE_REMINDER}",
        f"{YELLOW}ASSISTANT_MODE_SYSTEM_PROMPT:{RESET} {DISCORD_SETTINGS_BAG.ASSISTANT_MODE_SYSTEM_PROMPT}",
    ]

    return "\n".join(settings_list)


def main():
    print(divider*2)
    print()
    print(f"{MAGENTA}<<<===========(TEST SETTINGS DEBUG SCRIPT)===========>>>{RESET}".center(divider_len*2))
    print()
    print(divider*2)
    print()
    print(
        "\n".join(
            [
                "You are running discord_settings.py",
                f"{MAGENTA} Please Note: These are only the discord related settings, not the settings for the chat module(eg template, API key, etc)",
                "To view the chat module settings, use the following command in the root directory of the project:",
                f"{YELLOW}python3 -m APGCM.settings{RESET}",
                "\n",
                "====================(ABOUT)====================",
                "This file is charge of loading the settings for the discord bot from the .env file.",
                "It also includes a quick and dirty test of the discord_settings.py file, to ensure that the settings are loaded correctly.",
                "You will also have the option to hide the bot token for security purposes, so you can share the output of this file without worrying about your bot token being leaked.",
                "ie if your token is 10101010 it will display as 101****",
                "And if your token is not loaded, it will display as Not Present",
            ]
        )
    )
    ans = input("Would you like to show  the bot token? (Y/N): ")
    hide_token = True
    if ans.lower().strip() == "Y":
        hide_token = False

    print(make_settings_string(hide_token=hide_token))


if __name__ == "__main__":
    # just to test to make sure everything was loaded correctly
    main()
