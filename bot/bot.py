import sys

sys.path.append("./APGCM")
import asyncio

import APGCM
import discord
from APGCM import (
    DEFAULT_LOGGING_LEVEL,
    BaseLogger,
    ChatFactory,
    ChatWrapper,
    DisMessageSplitStreamHandler,
    JsonSaveHandler,
    exceptions
)
from APGCM.log_config import DEFAULT_LOGGING_LEVEL, BaseLogger
from APGCM.settings import SETTINGS_BAG
from bot.bot_helpers import (
    get_chat_history,
    make_chat_wrapper,
    process_save_command,
    split_response,
    str_to_bool,
)
from discord.ext import commands
from discord_settings import DISCORD_SETTINGS_BAG

"""
TODO LIST:
[] Add a param modification command
[x] Work out the typing issue(typing ends when the first await is called, so we need to find a way to keep it going until the last await is called)
[] Add a command to set the system prompt
[] Work out a command to change the bots home channel
[] Figure out how to add slash commands(if I have time)

[] Clean up this file, and make it more readable
    Suggestions?
    [] Move the help info to a separate file
    [] Move the discord bot class to a separate file
        (That way this file will only have the main function, and the imports)
    [] Slim down the imports
[x] Update the documentation and doc string for ChatWrapper to include all of the new features(autosave, reminder value, stream chat method etc)
[x] Clean up everything move commented out code to my old code file(Why not just delete it? Because I might need it later)
[] Make the main file in the project dir a little cuter, add some of my crappy ascii art to it(Why not lol thats always fun)


"""

HELP_INFO = "\n".join(
    [
        "Welcome to Alex's Maybe Kinda Decent Discord Bot!",
        "Here are the commands you can use:",
        "debug: Prints the chat wrapper's debug information to the channel.",
        "`reminder <reminder>`: Sets a reminder for the chat wrapper.(A special system prompt appended to the end of the chat log with the reminder text)",
        "`print_history`: Prints the chat wrapper's chat history to the channel.(May be long)",
        "`get_saves`: Prints the chat wrapper's saves to the channel.",
        "`load <save_name>`: Loads the save with the given name.",
        "`save <save_name> <overwrite>`: Saves the chat wrapper's current state to a save with the given name. If overwrite is True, it will overwrite the save if it already exists. If overwrite is False, it will not overwrite the save if it already exists.",
        "help: Prints this message to the channel.",
    ]
)


def split_response(response: str, max_len: int = 1990) -> list:
    """Take a string and split it into a list of strings, each of which is no longer than 2000 characters."""
    if len(response) >= max_len:
        return [response[i : i + max_len] for i in range(0, len(response), max_len)]
    else:
        return [response]


class DiscordBot(commands.Cog):
    """Main discord bot class. This class is responsible for handling all of the discord bot's commands and events."""

    def __init__(
        self,
        bot: commands.Bot,
        home_channel: int = DISCORD_SETTINGS_BAG.BOT_HOME_CHANNEL,
    ):
        self.logger = BaseLogger(
            module_name=__file__,
            level=DEFAULT_LOGGING_LEVEL,
            filename="discord_bot.log",
            identifier="discord_bot",
        )
        self.logger.info("Initializing discord bot...")
        self.bot: commands.Bot = bot
        self.cw = make_chat_wrapper()
        
        # return type deals with the way chatwrapper returns messages, we want it to return a string. In this bot we don't need the other return types.
        self.cw.return_type = "string"
        self.cw.system_prompt = DISCORD_SETTINGS_BAG.DEFAULT_DISCORD_SYSTEM_PROMPT
        self.cw.load_auto_save()  # will load the most recent auto save if one exists
        # we don't need a record of previous messages, unset the chatlog
        self.cw.trim_object.add_chatlog(None)
        self.cw.reminder = DISCORD_SETTINGS_BAG.DEFAULT_REMINDER
        self.home_channel = int(home_channel)
        self.typing = False
        self.logger.info("Discord bot initialized!")
    

    async def process_ai_message(self, message: discord.Message):
        """Processes an AI message and sends it to the channel."""
        channel = message.channel
        accumulated_message = ""
        self.logger.info(f"Message received: {message.content}")
        gen = self.cw.stream_chat(message.content)
        async with channel.typing():
            while True:
                try:
                    accumulated_message += next(gen)
                    self.logger.debug(
                        "Accumulated message: "
                        + accumulated_message
                        + "Message chunk length: "
                        + str(len(accumulated_message))
                    )
                    if (
                        len(accumulated_message)
                        >= DISCORD_SETTINGS_BAG.MESSAGE_CHUNK_LEN
                    ):
                        self.logger.info("Sending Message: " + accumulated_message)
                        await message.reply(accumulated_message)
                        accumulated_message = ""
                except StopIteration:
                    self.logger.info("Sending Message: " + accumulated_message)
                    if len(accumulated_message) > 0:
                        await message.reply(accumulated_message)
                    accumulated_message = ""

                    break

    @commands.command(name="debug")
    async def debug(self, ctx: commands.Context):
        """This command will print the chat wrapper's debug information to the channel."""
        self.logger.info("Debug command called!")
        debug_info = split_response(self.cw.debug())
        for i in debug_info:
            await ctx.send(i)
    @commands.command(name="sys_prompt")
    async def sys_prompt(self, ctx: commands.Context, *args):
        """Sets the system prompt for the chat wrapper.
        Args: system_prompt. If no system prompt is provided, it will print an error message.
        """
        if len(args) == 0:
            await ctx.send("Please provide a system prompt!")
            return
        self.logger.info("System prompt command called!")
        sys_prompt = " ".join(args)
        self.cw.system_prompt = sys_prompt
        await ctx.send("System prompt set to: " + self.cw.system_prompt)
        await ctx.send("With wildcards replaced: " + self.cw.trim_object.system_prompt_object.system_prompt)
    @commands.command(name="set_temp")
    async def set_temp(self, ctx: commands.Context, *args):
        """Sets the temperature for the model.
        Args: (number between 0-2)temperature. If no temperature is provided, it will print an error message.
        To unset and use the default openai temperature, use the words none, unset, or remove.
        To set the temperature to 0, use the words zero or 0.
        
        """
        if len(args) == 0:
            ctx.send("Please provide a temperature!")
            return 
        temp_raw = args[0]
        if temp_raw.strip().lower() in ("none", "unset", "remove"):
            temp = None
        elif temp_raw.strip().lower() in ("zero", "0"):
            temp  = 0.0
        else:
            try:
                temp = float(temp_raw)
            except ValueError:
                await ctx.send("Please provide a valid temperature!")
                return
        try: 
            self.cw.completion_wrapper.parameters.temperature = temp
            await ctx.send("Temperature set to: " + str(self.cw.completion_wrapper.parameters.temperature))
        except exceptions.PrettyGoodError as e:
            await ctx.send("Error setting temperature: " + str(e))
            return 
        except Exception as e:
            await ctx.send("Unknown error setting temperature: " + str(e))
            return 
        
        

    @commands.command(name="reminder")
    async def reminder(self, ctx: commands.Context, *args):
        """Sets a reminder for the chat wrapper.
        Parameters: reminder. If no reminder is provided, it will print an error message.
        A reminder is a special system prompt appended to the end of the chat log with the reminder text.
        """
        if len(args) == 0:
            await ctx.send("Please provide a reminder!")
            return
        self.logger.info("Reminder command called!")
        reminder = " ".join(args)
        self.logger.info("Reminder: " + reminder)
        if reminder.strip().lower() in ("none", "unset", "remove"):
            self.logger.info("Reminder unset!")
            reminder = None
        self.cw.reminder = reminder
        await ctx.send("Reminder set to: " + str(self.cw.reminder))

    @commands.command(name="print_history")
    async def print_history(self, ctx: commands.Context):
        """Prints all of the chat wrapper's chat history to the channel.
        Useful if you are loading a save and can't remember what the chat history was.
        """
        await ctx.send("Printing history...(This might be long)")
        history = get_chat_history(self.cw)
        for i in history:
            if len(i) > 0:
                if len(i) > 1990:
                   split = split_response(i)
                   for msg in split:
                       await ctx.send(str(msg))
                       
                else:
                    await ctx.send(i)
            else:
                continue 
        await ctx.send("History printed!")

    @commands.command()
    async def get_saves(self, ctx: commands.Context):
        """Shows a list of all save names the bot has."""
        await ctx.send("Getting saves...")
        saves = split_response(", ".join(self.cw.all_entry_names))
        self.logger.warning("Saves: " + str(saves))
        if len(saves) == 1:
            await ctx.send(saves[0])
            return
        else:
            for i in saves:
                await ctx.send(i)

    @commands.command(name="load")
    async def load(self, ctx: commands.Context, *args):
        """Loads the save with the given name.
        Parameters: save_name. If a save with the given name does not exist, it will print an error message.
        """
        if len(args) == 0:
            await ctx.send("Please provide a save name!")
            return
        if not self.cw.check_entry_name(args[0]):
            await ctx.send("Save not found!")
            return
        else:
            self.cw.load(args[0])
            await ctx.send("Save loaded!")

    @commands.command(name="save")
    async def save(self, ctx: commands.Context, *args):
        """
        Parameters: save_name, overwrite
        Overwrite can be yes or no, or true or false, or 1 or 0.

        Saves the bot's chat history to a save with the given name. If overwrite is True, it will overwrite the save if it already exists. If overwrite is False, it will not overwrite the save if it already exists.
        """
        success, message = process_save_command(self.cw, *args)
        if success:
            await ctx.send(message)
        else:
            await ctx.send(message)

    @commands.command(name="help_me")
    async def help_me(self, ctx: commands.Context):
        """I didn't know that the help command is automatically added to the bot, so I made my own help command."""

        await ctx.send(HELP_INFO)

    @commands.command(name="reset")
    async def reset(self, ctx: commands.Context):
        """This command will reset the chat wrapper."""
        self.logger.info("Reset command called!")
        self.cw.trim_object.reset()
        await ctx.send("Chat wrapper reset!")
    @commands.command(name="hard_reset")
    async def hard_reset(self, ctx: commands.Context):
        """Completely resets the chat wrapper, including the chat log, and deletes autosaves."""
        self.logger.info("Hard reset command called!")
        self.cw.reset()
        await ctx.send("Chat wrapper hard reset!")

    @commands.Cog.listener()
    async def on_ready(self):
        """Sends a message to the home channel when the bot is ready."""
        channel = self.bot.get_channel(self.home_channel)
        if channel is None:
            self.logger.error("Could not find home channel! Exiting...")
            return
        self.logger.info("Bot is ready!")
        await channel.send("Bot is ready!")
        await self.bot.change_presence(activity=discord.Game(name="Running!"))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        channel = message.channel
        if message.author == self.bot.user:
            return
        if message.channel.id != self.home_channel:
            return
        if message.content.startswith(DISCORD_SETTINGS_BAG.BOT_PREFIX):
            return
        else:
            await self.process_ai_message(message)
            return


def make_bot() -> commands.Bot:
    """Creates a bot object using the discord_settings.py file."""
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix=DISCORD_SETTINGS_BAG.BOT_PREFIX, intents=intents)
    return bot


async def setup(bot: commands.Bot, cog: commands.Cog):
    """This apparently need to be done in a coroutine, so I made it a coroutine."""
    await bot.add_cog(cog)


def main():
    bot = make_bot()
    bot_cog = DiscordBot(bot)

    asyncio.run(setup(bot, bot_cog))

    bot.run(DISCORD_SETTINGS_BAG.BOT_TOKEN)


if __name__ == "__main__":
    main()
