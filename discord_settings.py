from dotenv import load_dotenv
import os

load_dotenv()

# =============(BOT INFO)=============#

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_PREFIX = os.getenv("BOT_PREFIX")
BOT_HOME_CHANNEL = int(os.getenv("BOT_HOME_CHANNEL"))
MESSAGE_CHUNK_LEN = int(os.getenv("MESSAGE_CHUNK_LEN", 1000))
#================(SYSTEM PROMPTS)================#

#==================(DEFAULT MODES)=================#
#=====(CASUAL MODE )=====#
casual_mode_system  = "Hey there, Discord fam! 🎉  I am now running on discord!  I am  ready for some chill chats, fascinating trivia, and to answer any questions you have in mind. Just so you know, I'm running on the ||model|| model, and it's ||date|| today, with the current time being ||time||. The last time I updated my vast pool of knowledge was on ||cut_off||. All this is possible thanks to Alex's Pretty Good Discord Bot, powered by the incredible Alex's Pretty Good Chat Module! Let's dive into some exciting conversations! 😃 User: Hey whats up ai bot? \nAssistant: Oh nothing much, I am just waiting for messages to respond to! What about you?"
casual_mode_reminder = "You are currently on a discord server, be sure to maintain a friendly and casual tone. You are not here to provide assistance, but to have a casual conversation, so let the conversation flow naturally. Do not speak too formally, and do not remind users that you are a bot(This is specified in a prepend to all your messages). Behave as if you are a human. "



CASUAL_MODE_REMINDER  = os.getenv("CASUAL_MODE_REMINDER", casual_mode_reminder)
CASUAL_MODE_SYSTEM_PROMPT = os.getenv("CASUAL_MODE_SYSTEM_PROMPT", casual_mode_system)

#+=====(ASSISTANT MODE)=====#
assistant_mode_prompt = "You are a helpful AI assistant. Your model is ||model||, and it's ||date|| today, with the current time being ||time||. The last time I updated my vast pool of knowledge was on ||cut_off||. \n  User: Hey whats up ai bot? \nAssistant: As an AI assistant I do not have a life, I am always ready to help! What can I do for you today?"
assistant_mode_reminder = "You are currently being run on a discord server. You are powered by Alex's Pretty Good Chat Module. "




ASSISTANT_MODE_REMINDER = os.getenv("ASSISTANT_MODE_PROMPT", assistant_mode_prompt)
ASSISTANT_MODE_REMINDER = os.getenv("ASSISTANT_MODE_REMINDER", assistant_mode_reminder)


#=====(DEFAULT MODE)=====#


DEFAULT_REMINDER = os.getenv("DEFAULT_REMINDER", )
DEFAULT_DISCORD_SYSTEM_PROMPT = os.getenv("DEFAULT_DISCORD_SYSTEM_PROMPT", CASUAL_MODE_SYSTEM_PROMPT)



# =============(DISCORD SETTINGS BAG)=============#
class DiscordSettingsBag:
    BOT_PREFIX = BOT_PREFIX
    BOT_HOME_CHANNEL = BOT_HOME_CHANNEL
    BOT_TOKEN = BOT_TOKEN
    DEFAULT_DISCORD_SYSTEM_PROMPT = DEFAULT_DISCORD_SYSTEM_PROMPT
    MESSAGE_CHUNK_LEN = int(os.getenv("MESSAGE_CHUNK_LEN", 300))
    DEFAULT_REMINDER = DEFAULT_REMINDER
    DEFAULT_DISCORD_SYSTEM_PROMPT = DEFAULT_DISCORD_SYSTEM_PROMPT
    CASUAL_MODE_REMINDER = CASUAL_MODE_REMINDER
    CASUAL_MODE_SYSTEM_PROMPT = CASUAL_MODE_SYSTEM_PROMPT
    ASSISTANT_SYSTEM_PROMPT = ASSISTANT_SYSTEM_PROMPT
    ASSISTANT_REMINDER = ASSISTANT_REMINDER
    



DISCORD_SETTINGS_BAG = DiscordSettingsBag()




#================================================================================================
# =============(TESTING)=============#
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
    return "\n".join(
        [
            f"BOT_TOKEN: {token}",
            f"BOT_PREFIX: {DISCORD_SETTINGS_BAG.BOT_PREFIX}",
            f"BOT_HOME_CHANNEL: {DISCORD_SETTINGS_BAG.BOT_HOME_CHANNEL}",
            f"MESSAGE_CHUNK_LEN: {DISCORD_SETTINGS_BAG.MESSAGE_CHUNK_LEN}",
            f"DEFAULT_DISCORD_SYSTEM_PROMPT: {DISCORD_SETTINGS_BAG.DEFAULT_DISCORD_SYSTEM_PROMPT}",
            f"DEFAULT_REMINDER: {DISCORD_SETTINGS_BAG.DEFAULT_REMINDER}",
            
            f"CASUAL_MODE_REMINDER: {DISCORD_SETTINGS_BAG.CASUAL_MODE_REMINDER}",
            f"CASUAL_MODE_SYSTEM_PROMPT: {DISCORD_SETTINGS_BAG.CASUAL_MODE_SYSTEM_PROMPT}",
            f"ASSISTANT_SYSTEM_PROMPT: {DISCORD_SETTINGS_BAG.ASSISTANT_SYSTEM_PROMPT}",
            f"ASSISTANT_REMINDER: {DISCORD_SETTINGS_BAG.ASSISTANT_REMINDER}"
            
           
            
        ]
    )


def main():
    print(
        "\n".join(
            [
                "You are running discord_settings.py",
                "This file is charge of loading the settings for the discord bot from the .env file.",
                "It also includes a quick and dirty test of the discord_settings.py file, to ensure that the settings are loaded correctly.",
                "You will also have the option to hide the bot token for security purposes, so you can share the output of this file without worrying about your bot token being leaked.",
                "ie if your token is 10101010 it will display as 101****",
                "And if your token is not loaded, it will display as Not Present",
            ]
        )
    )
    ans = input("Would you like to show  the bot token? (y/n): ")
    hide_token = True 
    if ans.lower().strip() == "y":
        hide_token = False
    


    print(make_settings_string(hide_token=hide_token))
if __name__ == "__main__":
    # just to test to make sure everything was loaded correctly
    main()
