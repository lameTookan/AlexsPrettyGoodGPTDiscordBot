import sys
import time 


sys.path.append("./APGCM")
"""A simple test script meant to ensure users have correctly setup the project, before running the full program.
4 steps:
1. Checking that you have installed at least some of the dependencies.
2. Printing out your current settings to ensure that's been setup correctly.
3. Getting a test response from the AI to ensure that you have correctly entered your API key and template name.
4. Trying to send a discord message to ensure that you have correctly setup the discord bot.
"""
divider1 = "===================================================================================================="
divider1_len = len(divider1)
divider2 = "---------------------"*3

def print_header() -> None:
    header = [
        divider1,
        "\n",
        "\u001b[35m <============== QUICK SETUP TEST SCRIPT ==============> \u001b[0m".center(
            divider1_len
        ),
        " ",
        "\n",
        divider1,
        "\n",
        "Welcome to the quick setup test script!",
        "This script is designed to test that you have correctly setup this project.",
        "Before running this script, ensure you have done the following:",
        "1. Installed the dependencies in requirements.txt",
        "2. Created a .env file and entered your API key and discord token.",
        "3. Entered a template name in the .env file.",
        "4. Entered a home channel in the .env file.",
        "\n",
        
        divider2,
        "\n",
        "Overview of what we will be doing:",
        "1. Checking that you have installed at least some of the dependencies.",
        "2. Printing out your current settings to ensure that's been setup correctly.",
        "3. Getting a test response from the AI to ensure that you have correctly entered your API key and template name.",
        "4. Trying to send a discord message to ensure that you have correctly setup the discord bot.",
    ]
    print("\n".join(header))
    print("\n")
    input("Press enter to begin....")
    print("\n")
    print(divider1)
    


def test_dependencies():
    """Test that the dependencies are installed."""
    print("STEP 1: Testing dependencies...")
    print("Attempting to import dependencies...")
    try:
        import discord
        print("Discord dependency imported...")
        import tiktoken
        print("Tiktoken dependency imported...")
        import openai
        print("Openai dependency imported...")
        from dotenv import load_dotenv

    except Exception as e:
        print(
            "You are missing some dependencies. Please install the dependencies in requirements.txt"
        )
        print(
            "Use the following command to install the dependencies: pip install -r requirements.txt"
        )
        print("Error message:", e)
        print("\u001b[31m Step 1 FAILED....\u001b[0m")
        input("Press enter to exit....")
        print("Exiting...")

        sys.exit()
    print("Required dependencies are installed.")
    print("\u001b[34m Step 1 passed. \u001b[0m")
    input("Press enter to continue.")

def make_config():
    from config_maker import make_config
    # code will cause errors unless this file is made, so we will do it here as well as in main.
    print("Making config file(Used to store settings that can be changed during runtime)...")
    make_config()
def obscure_keys(key: str) -> str:
    """Obscure the key."""
    if key is None:
        return "Not Present"
    beginning = key[0:4]
    return f"{beginning}{('*' * (len(key) - 4))} (Length:  { str(len(key))})"


def test_settings():
    """Print out the settings to ensure they are correct."""
    print("STEP 2: Printing out settings...")
    from APGCM.settings import SETTINGS_BAG
    from discord_settings import DISCORD_SETTINGS_BAG
    print("\u001b[1m Please note that your settings in config.ini(or settings changed during run time with commands) take priority to their respective .env variables. This is limited to settings related to autosaving(frequency, enabled, etc), message chunk length, and home channel(unless home channel in config is 0) \u001b[0m")
    time.sleep(1)
    
    print(
        "Would you like to view your API keys and discord tokens? If you choose no, they will be obscured. (y/n)"
    )  
    
    
    ans = input(">>> ")
    show_api_keys = False
    if ans.lower().strip() == "y":
        show_api_keys = True
    print("Printing out your settings...")
    print(divider1)
    OPENAI_KEY = (
        SETTINGS_BAG.OPENAI_API_KEY
        if show_api_keys
        else obscure_keys(SETTINGS_BAG.OPENAI_API_KEY)
    )
    DISCORD_TOKEN = (
        DISCORD_SETTINGS_BAG.BOT_TOKEN
        if show_api_keys
        else obscure_keys(DISCORD_SETTINGS_BAG.BOT_TOKEN)
    )
    settings_list = [
        f"OPENAI_API_KEY: {OPENAI_KEY}",
        f"DISCORD BOT TOKEN:  {DISCORD_TOKEN}",
        f"TEMPLATE NAME: {SETTINGS_BAG.DEFAULT_TEMPLATE_NAME}",
        f"DEFAULT MODEL: {SETTINGS_BAG.DEFAULT_MODEL}",
        f"HOME CHANNEL: {DISCORD_SETTINGS_BAG.BOT_HOME_CHANNEL}",
        f"IS AUTOSAVING ENABLED: {DISCORD_SETTINGS_BAG.AUTO_SAVING_ENABLED}",
        f"AUTO SAVE FREQUENCY: {DISCORD_SETTINGS_BAG.AUTO_SAVE_FREQUENCY}",
        f"MESSAGE CHUNK LENGTH: {DISCORD_SETTINGS_BAG.MESSAGE_CHUNK_LEN}",
    ]
    print("\n".join(settings_list))
    input("Do these settings look correct? Press enter to continue....")
    print("The above should be the settings you entered in the .env file.")
   
    print("\u001b[34m Step 2 passed. \u001b[0m  ")
   
    input("Press enter to continue.")


def get_test_ai_response():
    """Attempt to get a test response from the AI."""
    print("STEP 3: Getting a test response from the AI...")
    print("Note that this is an actual request to the API not a mock. You will be charged for this request (But for a message of this length we are sending, it should a fraction of a cent, even with the most expensive model)")
    print(
        "You should see a loading spinner and then a response from the AI thats something like 'All systems are go!'"
    )
    try:
        import APGCM
        import openai

        cw = APGCM.chat_utilities.quick_make_chat_wrapper()
        print("Getting test response...")
        APGCM.chat_utilities.print_test_ai_response(cw)

    except openai.OpenAIError as e:
        print(
            "You have either not entered your API key in correctly or you are trying to use a model that you do not have access to."
        )
        print("The error message is:", e)
        print("\u001b[31m Step 3 FAILED....\u001b[0m")
        input("Press enter to exit....")
        print("Exiting...")
        sys.exit()
    except APGCM.exceptions.PrettyGoodError as e:
        print("You have not entered a template name in the .env file.")
        print("The error message is:", e)
        print("\u001b[31m Step 3 FAILED....\u001b[0m")
        input("Press enter to exit....")
        print("Exiting...")
        sys.exit()
    except Exception as e:
        print("An unknown error has occurred.")
        print("Please report this error to the developer.")
        print("The error message is:", e)
        print("\u001b[31m Step 3 FAILED....\u001b[0m")
        input("Press enter to exit....")
        print("Exiting...")
        sys.exit()

    print("\u001b[34m Step 3 passed. \u001b[0m  ")
    input("Press enter to continue.")


def test_discord():
    """Explain to user what the test will entail, confirm, and then run the test bot."""
    print("STEP 4: Testing discord...")
    print(
        "This one is a little more complex as there is no easy way to test this without running a bot."
    )
  
    print(
        "You can either do this now, or just try running the main.py file and see if it works."
    )
    ans = input("Test discord now? (y/n)")
    if ans.lower().strip() == "y":
        print("Starting discord bot...")
        print(
            "\u001b[1m If you see a message in the home channel that says \u001b[35m 'All systems are go!', \u001b[0m \u001b[1m then you have correctly setup the discord bot, and this test has passed. \u001b[0m"
        )

        print(
            "After that, we can be sure that everything is setup correctly and you can start using the program."
        )
        test_bot()
    else:
        print("Skipping discord test.")
        print("\u001b[34m All tests passed. \u001b[0m")
        print("You should be good to go!")
        input("Press enter to exit.")
        sys.exit()


def test_bot():
    try:
        import discord

        from discord_settings import DISCORD_SETTINGS_BAG

        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            home_channel = client.get_channel(DISCORD_SETTINGS_BAG.BOT_HOME_CHANNEL)
            await home_channel.send("All systems are go!")
            print("Sent message to home channel.")
            print("\u001b[34m Step 4 passed. \u001b[0m")
            print("\n")

            print("\u001b[34m All tests passed! \u001b[0m")
            print("\n")
            print("Thank you for using APGCM!")
            print("\u001b[31m Warning: You will see an error message after pressing enter. This is normal. You will also see an error message if you wait on this screen for too long. This is also normal. \u001b[0m")
            print("The test is passed if you see the message 'All tests passed!'")
            input("Press enter to exit.")
            sys.exit()

        client.run(DISCORD_SETTINGS_BAG.BOT_TOKEN)

    except Exception as e:
        print("An error has occurred.")
        print("This likely means that you have not setup the discord bot correctly.")
        print("The error message is:", e)
        print("\u001b[31m Step 4 FAILED....\u001b[0m")
        input("Press enter to exit....")
        print("Exiting...")
        sys.exit()


def main():
    print_header()
    test_dependencies()
    make_config()
    test_settings()
    get_test_ai_response()
    test_discord()


if __name__ == "__main__":
    main()
