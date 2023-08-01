import sys
import MyStuff.mystuff as ms 

sys.path.append("./APGCM")
import asyncio
from typing import Literal, Optional, Union, Any, Tuple
import discord
from config import ChangeConfig
from discord import app_commands
from APGCM import DEFAULT_LOGGING_LEVEL, BaseLogger, exceptions, chat_utilities
from APGCM.log_config import DEFAULT_LOGGING_LEVEL, BaseLogger
from bot.bot_helpers import (
    get_chat_history,
    make_chat_wrapper,
    process_save_command,
    split_response,
    HELP_INFO,
)
from discord.ext import commands
from discord_settings import DISCORD_SETTINGS_BAG
from enum import Enum


config = ChangeConfig()


class Modes(Enum):
    DEFAULT_MODE = 1
    CASUAL_MODE = 2
    ASSISTANT_MODE = 3


def split_response(response: str, max_len: int = 1990) -> list:
    """Take a string and split it into a list of strings, each of which is no longer than 2000 characters."""

    if len(response) >= max_len:
        return [response[i : i + max_len] for i in range(0, len(response), max_len)]
    else:
        return [response]


# I am not quite sure how to make sure that the chat wrapper is shared between multiple cogs, so I am just putting everything in one cog for now.
# would be better just to make the chat wrapper a global variable, but that feels like a bad idea.
# TODO rework this to be a little more modular
class DiscordBot(commands.Cog):

    """Main discord bot class. This class is responsible for handling all of the discord bot's commands and events."""

    """
    
    Main discord bot class. This class is responsible for handling all of the discord bot's commands and events.
    
    I realize this class is way too long, but its hard to break it up as chat wrapper needs to be passed around and used by all of the methods. 
    
    Will likely make it a global variable in the future, and configure it in the main file. But for now, this does work well, and hopefully the sections make it easier to read.
    Dependencies: 
        External:
            discord.py
            discord.ext 
            discord.app_commands
        Custom:
            APGCM
            APGCM.chat_utilities
            BaseLogger
            DISCORD_SETTINGS_BAG from discord_settings.py
            ChangeConfig from config.py
            Various functions from bot_helpers.py
        Python:
            asyncio
            Typing for type hints and value restrictions
            Enum for the Modes enum
    Raises:
        None but APGCM will raise various errors if something goes wrong.
        All of these exceptions are children of PrettyGoodError, see APGCM/exceptions.py for more info.
    
    MAIN SECTIONS:
        HELPERS AND LISTENERS: Contains helper methods and event listeners.
            HELPERS: Contains helper methods.
            LISTENERS: Contains event listeners.
        COMMANDS: Contains command methods.
            MODE COMMANDS: Contains mode commands.
            SAVING COMMANDS: Contains saving commands.
            AUTO-SAVING COMMANDS: Contains auto-saving commands.
            GENERAL COMMANDS: Contains general commands.
            

    Attributes:
        bot (commands.Bot): The discord.py Bot instance.
        cw (ChatWrapper): The ChatWrapper instance used to interface with the AI.
        home_channel (int): The channel ID that the bot treats as its "home" channel. Most activity is limited to this channel.
        config (ChangeConfig): The bot's configuration object.
        help_mode (bool): Whether help mode is enabled. Help mode provides demo prompts and disables autosaving.
        current_mode (str): The current conversation mode. Can be "default", "casual", or "assistant".
        
    Methods:
        on_ready(): Called when the bot has connected to Discord. Sends a ready message to the home channel.
        
        on_message(message): Called when a message is sent in the home channel. Checks for command prefix, otherwise passes to AI.

        process_mode_change(mode): Changes conversation mode by updating prompt, reminder, etc.

        toggle_help(): Toggles help mode on/off by settings props and loading/saving history.

        process_ai_message(message): Passes a message to the AI and sends the response.

        COMMAND_NAME(interaction): The various command methods like help(), reset(), etc.

        _sync_home_channel(): Syncs config home channel to bot home channel property.

        _sync_autosaving(): Syncs config autosave settings to ChatWrapper.

    The bot also contains command groups under attributes like app_commands, modes, saving, etc.
    These are registered with discord.py to create the slash command structure.

    Lifecycle:
        1. Initialize bot, cw, configs
        2. Register listeners for on_ready and on_message
        3. Register command methods and command groups
        4. Run bot and process events/commands
    """

    def __init__(
        self,
        bot: commands.Bot,
        home_channel: int = DISCORD_SETTINGS_BAG.BOT_HOME_CHANNEL,
        config: ChangeConfig = config,
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
        self.logger.info("Discord bot initialized!")
        self.help_mode = False
        self.config = config
        self._sync_autosaving()
        self._sync_home_channel()
        self.current_mode = "default"

    
    autosaving = app_commands.Group(
        name="autosaving", description="Autosaving commands"
    )
    saving = app_commands.Group(name="saving", description="Saving commands")
    modes = app_commands.Group(name="modes", description="Mode commands")

    # ================================================================================

    # ............................HELPERS AND LISTENERS..............................

    # ================================================================================

    # =====================(HELPERS)====================#
    def _sync_home_channel(self):
        if (
            self.home_channel != self.config.home_channel
            and self.config.home_channel != 0
        ):
            self.home_channel = self.config.home_channel

    def _sync_autosaving(self):
        self.cw.set_is_saving(config.auto_saving_enabled)
        self.cw.set_auto_save_info(auto_save_frequency=config.auto_save_frequency)

    @property
    def all_saves(self) -> str:
        """Returns a string containing all of the save names."""
        return ", ".join(self.cw.all_entry_names)

    def process_mode_change(self, mode: int) -> None:
        """Processes a mode change."""
        if mode == Modes.DEFAULT_MODE.value:
            self.cw.system_prompt = DISCORD_SETTINGS_BAG.DEFAULT_DISCORD_SYSTEM_PROMPT
            self.cw.reminder = DISCORD_SETTINGS_BAG.DEFAULT_REMINDER
            self.current_mode = "default"
            print("Mode set to default!")

        elif mode == Modes.CASUAL_MODE.value:
            self.cw.system_prompt = DISCORD_SETTINGS_BAG.CASUAL_MODE_SYSTEM_PROMPT
            self.cw.reminder = DISCORD_SETTINGS_BAG.CASUAL_MODE_REMINDER
            self.current_mode = "casual"
            print("Mode set to casual!")
        elif mode == Modes.ASSISTANT_MODE.value:
            self.cw.system_prompt = DISCORD_SETTINGS_BAG.ASSISTANT_MODE_SYSTEM_PROMPT
            self.cw.reminder = DISCORD_SETTINGS_BAG.ASSISTANT_MODE_REMINDER
            self.current_mode = "assistant"
            print("Mode set to assistant!")
        else:
            raise ValueError("Invalid mode!")

        self.cw.rotating_save_handler.reset()  # so the old values don't get automatically loaded

    def toggle_help(self) -> Tuple[bool, str]:
        """
        Toggles help mode. If help mode is enabled, it will disable it. If help mode is disabled, it will enable it.
        Returns a tuple containing a bool and a string. The bool indicates weather or not the operation was successful. The string is a message indicating the result of the operation.
        """
        if self.help_mode:
            self.help_mode = False
            self.current_mode = self.old_mode
            self.logger.info("Help mode disabled!")
            if self.cw.check_entry_name("temp_help_mode_save"):
                self.cw.load("temp_help_mode_save")
                self.cw.set_is_saving(True)
                self.cw.delete_entry("temp_help_mode_save")
                return True, "Help mode disabled"
            else:
                self.logger.warning("Help mode save does not exist!")
                return (
                    False,
                    "Help mode save does not exist! If you are seeing this message, something has gone horribly wrong. Please contact the developer.",
                )
        else:
            self.old_mode = self.current_mode
            self.current_mode = "help"
            self.help_mode = True
            self.logger.info("Help mode enabled!")

            self.cw.save("temp_help_mode_save", overwrite=True)
            self.cw.set_is_saving(
                False
            )  # turn off auto saving so we dont loose previous autosaves
            self.cw.trim_object.reset()  # reset the chat log
            self.cw.reminder = DISCORD_SETTINGS_BAG.HELP_MODE_REMINDER
            self.cw.system_prompt = DISCORD_SETTINGS_BAG.HELP_MODE_PROMPT
            return True, "Help mode enabled"

    async def process_ai_message(self, message: discord.Message) -> None:
        """Processes an AI message and sends it to the channel."""
        channel = message.channel
        accumulated_message = ""
        self.logger.info(f"Message received: {message.content}")
        gen = self.cw.stream_chat(message.content)
        async with channel.typing():
            while True:
                try:
                    token = next(gen)
                    sys.stdout.write(token)
                    sys.stdout.flush()
                    accumulated_message += token
                    self.logger.debug(
                        "Accumulated message: "
                        + accumulated_message
                        + "Message chunk length: "
                        + str(len(accumulated_message))
                    )
                    if len(accumulated_message) >= self.config.chunk_length:
                        self.logger.info("Sending Message: " + accumulated_message)
                        sys.stdout.write("\n")
                        sys.stdout.flush()
                        await message.reply(accumulated_message)
                        accumulated_message = ""
                except StopIteration:
                    self.logger.info("Sending Message: " + accumulated_message)
                    if len(accumulated_message) > 0:
                        await message.reply(accumulated_message)
                    accumulated_message = ""

                    break

    # ______________________(END HELPERS)______________________#

    # ==========================(EVENT LISTENERS)========================#
    @commands.Cog.listener()
    async def on_ready(self)-> None:
        """Sends a message to the home channel when the bot is ready."""
        await self.bot.tree.sync()
        channel = self.bot.get_channel(self.home_channel)

        if channel is None:
            self.logger.error("Could not find home channel! Exiting...")
            print("Could not find home channel!")

            return

        self.logger.info("Bot is ready!")
        print("Bot is ready and running!")
        await self.bot.change_presence(activity=discord.Game(name="GPT-4"))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message)-> None:
        channel = message.channel
        result, msg = ms.nmxy(message.content)
        if message.author == self.bot.user:
            return
        if message.channel.id != self.home_channel:
            print("Got message but was not in home channel, discarding...")
            return
        if message.content.startswith(DISCORD_SETTINGS_BAG.BOT_PREFIX):
            return
        
        if result:
            msgs = split_response(msg)
            await channel.send( delete_after=20)
            for msg in msgs:
               await  channel.send(msg, delete_after=30)
            
            
            
        else:
            print("AI message received and being processed...")
            await self.process_ai_message(message)
            return

    # __________________________(END EVENT LISTENERS)________________________#

    # ===============================================================================

    # ..................................COMMANDS.....................................

    # ===============================================================================

    # =============================(MODE COMMANDS)==================================#
    @modes.command(
        name="default_mode",
        description="Sets the system prompt to the default system prompt.",
    )
    async def default_mode(self, interaction: discord.Interaction)-> None:
        self.process_mode_change(Modes.DEFAULT_MODE.value)
        self.logger.info("Default mode command called!")
        await interaction.response.send_message("Mode set to default!", delete_after=20)

    @modes.command(name="help_mode", description="Toggles help mode.")
    async def help_mode(self, interaction: discord.Interaction)-> None:
        result, message = self.toggle_help()
        self.logger.info("Help mode command called!")
        if result:
            await interaction.response.send_message(
                message + f" Current mode: {self.current_mode.title()}", delete_after=20
            )
        else:
            self.logger.error("Help mode toggle failed!")
            await interaction.response.send_message(
                message + f" Current mode: {self.current_mode.title()}", delete_after=20
            )

    @modes.command(
        name="casual_mode",
        description="Sets the system prompt to the casual system prompt.",
    )
    async def casual_mode(self, interaction: discord.Interaction)-> None:
        self.process_mode_change(Modes.CASUAL_MODE.value)
        self.logger.info("Casual mode command called!")
        print("Mode set to casual!")
        await interaction.response.send_message("Mode set to casual!", delete_after=20)

    @modes.command(
        name="assistant_mode",
        description="Sets the system prompt to the assistant system prompt.",
    )
    async def assistant_mode(self, interaction: discord.Interaction) -> None:
        self.process_mode_change(Modes.ASSISTANT_MODE.value)
        self.logger.info("Assistant mode command called!")
        await interaction.response.send_message(
            "Mode set to assistant!", delete_after=20
        )

    @modes.command(name="which_mode", description="Shows the current mode.")
    async def which_mode(self, interaction: discord.Interaction)-> None:
        await interaction.response.send_message(
            f"Current mode: {self.current_mode.title()}", delete_after=20
        )

    # _______________(END MODE COMMANDS)____________________#

    # ==============================(AUTO-SAVING COMMANDS)==============================#

    @autosaving.command(
        name="delete_all_auto_saves", description="Deletes all auto saves and backups."
    )
    async def delete_all_auto_saves(self, interaction: discord.Interaction) -> None:
        self.cw.rotating_save_handler.delete_all_saves_and_backups()
        await interaction.response.send_message(
            "All auto saves and backups deleted!", delete_after=20
        )

    @autosaving.command(
        name="change_frequency", description="Changes the auto save frequency."
    )
    @app_commands.describe(frequency="The new auto save frequency.")
    async def change_frequency(
        self, interaction: discord.Interaction, *, frequency: int
    )-> None:
        self.config.auto_save_frequency = frequency
        self._sync_autosaving()
        self.logger.info(
            "Auto save frequency changed!",
        )
        await interaction.response.send_message(
            "Auto save frequency changed!", delete_after=20
        )

    @autosaving.command(
        name="auto_saving_enabled", description="Enables or disables auto saving."
    )
    @app_commands.describe(enabled="Whether or not auto saving is enabled.")
    async def auto_saving_enabled(
        self, interaction: discord.Interaction, *, enabled: bool
    ):
        """Toggles auto saving."""
        self.config.auto_saving_enabled = enabled
        self._sync_autosaving()
        self.logger.info("Auto saving set to: " + str(enabled))
        msg = "Auto saving enabled!" if enabled else "Auto saving disabled!"
        await interaction.response.send_message(msg, delete_after=20)

    @autosaving.command(
        name="manual_autosave",
        description="Manually saves the chat wrapper's current state to an autosave.",
    )
    async def manual_autosave(self, interaction: discord.Interaction):
        self.cw.manual_auto_save()
        self.logger.info("Manual autosave command called!")
        await interaction.response.send_message(
            "Manual autosave complete!", delete_after=20
        )

    # ==============================(GENERAL COMMANDS)==============================#
    @app_commands.command(name="set_temp")
    @app_commands.describe(
        value="Sets the  for the model. Can be any number with a decimal point between 0 and 2. However, values between 0 and 1 are recommended.",
        unset="Unsets the temperature for the model. Defaults to OpenAI's default temperature of 0.7.",
    )
    async def set_temp(
        self,
        interaction: discord.Interaction,
        *,
        value: app_commands.Range[float, 0.0, 2.0],
        unset: Optional[bool] = False,
    ) -> None:
        """Sets the temperature for the model.
        Args: (number between 0-2)temperature. If no temperature is provided, it will print an error message.
        You can also use the unset flag to unset the temperature.
        """
        if not unset:
            try:
                self.cw.completion_wrapper.parameters.temperature = value
            except exceptions.PrettyGoodError as e:
                await interaction.response.send_message(
                    f"An error was encountered while setting the value {str(e)}",
                    delete_after=20,
                )
                return

            await interaction.response.send_message(
                f"Temperature set to {value}", delete_after=20
            )
        else:
            self.cw.completion_wrapper.parameters.temperature = None
            await interaction.response.send_message(
                "Temperature unset!", delete_after=20
            )

    @app_commands.command(name="help", description="Shows a list of commands.")
    async def help(self, interaction: discord.Interaction):
        """Help command. Shows a list of commands."""
        interaction.response.send_message("Outputting help info...", delete_after=20)
        help_info = split_response(HELP_INFO)
        for msg in help_info:
            await interaction.channel.send(msg, delete_after=20)

    @app_commands.command(
        name="reminder", description="Sets a reminder for the chat bot. "
    )
    @app_commands.describe(
        content="Sets a reminder for the chat bot.  ",
        unset="Unsets the reminder for the chat bot.",
    )
    async def reminder(
        self,
        interaction: discord.Interaction,
        *,
        content: str,
        unset: Optional[bool] = False,
    ) -> None:
        """Sets a reminder for the chat wrapper.
        Parameters: reminder. If no reminder is provided, it will print an error message.
        A reminder is a special system prompt appended to the end of the chat log with the reminder text.
        """

        self.logger.info("Reminder command called!")
        channel = interaction.channel
        self.logger.info("Reminder: " + str(content), delete_after=20)
        if not unset:
            self.cw.reminder = content
            await interaction.response.send_message(
                "Reminder set to: " + str(self.cw.reminder), delete_after=20
            )
            await channel.send(
                "With wildcards: "
                + str(self.cw.trim_object._reminder_obj.prepared_reminder),
                delete_after=20,
            )
        else:
            self.cw.reminder = None
            await interaction.response.send_message("Reminder unset!", delete_after=20)

    @app_commands.command(
        name="export",
        description="Exports the chat wrapper's chat history to a markdown file.",
    )
    async def export(self, interaction: discord.Interaction):
        # automatically extracts data and creates an export context manager
        ecm = chat_utilities.auto_get_exporter(self.cw)
        # ECM is a context manager that creates a markdown file, returns it in enter, and then deletes it in exit
        with ecm as f:
            file = discord.File(f, filename="export.md")
            channel = interaction.channel
            await channel.send(file=file, delete_after=60)
        await interaction.response.send_message("Export complete!", delete_after=20)
        self.logger.info("File exported!")

    @app_commands.command(
        name="reset", description="Resets the chat wrapper's chat log."
    )
    @app_commands.describe(
        hard_reset="If hard_reset is True, it will completely reset the chat wrapper, including the chat log, and deletes autosaves."
    )
    async def reset(
        self, interaction: discord.Interaction, *, hard_reset: Optional[bool] = False
    ) -> None:
        """Command to reset the chat wrapper's chat log."""
        if hard_reset:
            self.cw.reset()
            await interaction.response.send_message(
                "A hard reset was performed on the chat bot!", delete_after=20
            )
        else:
            # this will only reset the chat history, not the chat wrapper
            self.cw.trim_object.reset()
            await interaction.response.send_message("Chat log reset!", delete_after=20)

    @app_commands.command(
        name="debug",
        description="Prints the chat wrapper's debug information to the channel.",
    )
    async def debug(self, interaction: discord.Interaction):
        """Command to print the chat wrapper's debug information to the channel."""
        data = self.cw.debug()
        await interaction.response.send_message(
            "Outputting debug info...", delete_after=20
        )
        if len(data) > 1990:
            msgs = split_response(data)

            for msg in msgs:
                await interaction.channel.send(msg, delete_after=20)
        else:
            await interaction.channel.send(data, delete_after=20)

    @app_commands.command(
        name="home_channel", description="Changes the bot's home channel."
    )
    @app_commands.describe(channel="The new home channel.")
    @commands.has_permissions(administrator=True)
    async def home_channel(self, interaction: discord.Interaction, *, channel: str):
        try: 
            channel = int(channel)
        except ValueError:
            await interaction.response.send_message("Invalid channel ID!", delete_after=20)
            return 
        if channel != self.home_channel:
            ch = self.bot.get_channel(channel)
            if ch is None:
                await interaction.response.send_message(
                    "Channel not found!", delete_after=20
                )
                return
            self.config.home_channel = channel
            self._sync_home_channel()
            await interaction.response.send_message(
                "Home channel changed!", delete_after=20
            )

    @app_commands.command(name="chunk_length", description="Changes the chunk length.")
    @app_commands.describe(length="The new chunk length.")
    async def chunk_length(
        self,
        interaction: discord.Interaction,
        *,
        length: app_commands.Range[int, 10, 1990],
    ) -> None:
        """Changes the chunk length.
        Parameters: length. If no length is provided, it will print an error message.
        """
        self.config.chunk_length = length
        await interaction.response.send_message(
            "Chunk length changed!", delete_after=20
        )

    @app_commands.command(
        name="sys_prompt", description="Sets the system prompt for the chat bot."
    )
    @app_commands.describe(
        content="Sets the system prompt for the chat bot.",
    )
    async def sys_prompt(
        self, interaction: discord.Interaction, *, content: str
    ) -> None:
        """Sets the system prompt for the chat wrapper.
        Args: system_prompt. If no system prompt is provided, it will print an error message.
        """

        self.logger.info("System prompt command called!")

        self.cw.system_prompt = content
        channel = interaction.channel
        await interaction.response.send_message(
            "System prompt set to: " + str(self.cw.system_prompt), delete_after=20
        )
        channel.send(
            "With wildcards: "
            + str(self.cw.trim_object.system_prompt_object.system_prompt),
            delete_after=20,
        )

    @app_commands.command(
        name="print_history", description="Shows chat history(might be long)"
    )
    async def print_history(self, interaction: discord.Interaction):
        """Prints all of the chat wrapper's chat history to the channel.
        Useful if you are loading a save and can't remember what the chat history was.
        """
        print("Print history command called!")
        data = self.cw.trim_object.get_pretty_ish_chat_history()
        self.logger.info("Print history command called!")
        if data is not None:
            channel = interaction.channel
            await interaction.response.send_message(
                "Outputting full chat history...(May be long)", delete_after=20
            )
            if len(data) > 1990:
                msgs = split_response(data)
                for msg in msgs:
                    if len(msg) > 0:
                        await channel.send(msg, delete_after=20)
            else:
                await channel.send(data, delete_after=20)
        else:
            await interaction.response.send_message(
                "No chat history to print!", delete_after=20
            )

    # _______________(END GENERAL COMMANDS)_______________#

    # ==============================(SAVING COMMANDS)==============================#
    @saving.command(
        name="delete_saves", description="Deletes any saves within the provided list"
    )
    @app_commands.describe(saves="A list of saves to delete, separated by commas.")
    async def delete_saves(self, interaction: discord.Interaction, *, saves: str):
        """Deletes any saves within the provided list."""
        print("Got delete saves command!")
        channel = interaction.channel
        if ", " in saves:
            saves = saves.split(", ")
            for save in saves:
                if self.cw.check_entry_name(save):
                    await channel.send(f"Deleting save {save}", delete_after=20)
                    self.cw.delete_entry(save)
                else:
                    await channel.send(f"Save {save} does not exist!", delete_after=20)
            await interaction.response.send_message("Done!", delete_after=20)
        else:
            if self.cw.check_entry_name(saves):
                await channel.send(f"Deleting save {saves}", delete_after=20)
                self.cw.delete_entry(saves)
            else:
                await channel.send(f"Save {saves} does not exist!", delete_after=20)
            await interaction.response.send_message("Done!", delete_after=20)

    @saving.command(
        name="save",
        description="Saves the chat wrapper's current state to a save with the given name.",
    )
    @app_commands.describe(
        save_name="Unique name for the save.",
        overwrite="Overwrite the save if it already exists.",
    )
    async def save(
        self,
        interaction: discord.Interaction,
        *,
        save_name: str,
        overwrite: Optional[bool] = False,
    ) -> None:
        if overwrite:
            self.cw.save(save_name, overwrite=True)
            await interaction.response.send_message("Save created!", delete_after=20)
        else:
            if self.cw.check_entry_name(save_name):
                await interaction.response.send_message(
                    "Save already exists! Please use the get_saves command to see a list of all saves."
                )
            else:
                self.cw.save(save_name)
                await interaction.response.send_message(
                    "Save created!", delete_after=20
                )
        print("Saved to " + save_name)

    @saving.command(name="load", description="Loads the save with the given name.")
    @app_commands.describe(save_name="The name of the save to load.")
    async def load(self, interaction: discord.Interaction, *, save_name: str) -> None:
        """Loads the save with the given name.
        Parameters: save_name. If a save with the given name does not exist, it will print an error message.
        """
        self.logger.info("Load command called!")
        if self.cw.check_entry_name(save_name):
            self.cw.load(save_name)
            await interaction.response.send_message("Save loaded!", delete_after=20)
        else:
            await interaction.response.send_message(
                "Save does not exist! Please use the get_saves command to see a list of all saves."
            )

    @saving.command(
        name="get_saves", description="Shows a list of all save names the bot has."
    )
    @app_commands.describe(include_auto_saves="Include auto saves in the list.")
    async def get_saves(
        self,
        interaction: discord.Interaction,
        *,
        include_auto_saves: Optional[bool] = False,
    ):
        """Shows a list of all save names the bot has."""
        if include_auto_saves:
            entry_names = self.cw.all_entry_names
        else:
            entry_names = self.cw.all_non_rotating_entry_names
        saves = ", ".join(entry_names)
        channel = interaction.channel

        if len(saves) > 1990:
            msgs = split_response(saves)
            interaction.response.send_message(
                "Outputting saves...(May be long)", delete_after=20
            )
            for msg in msgs:
                await channel.send(msg, delete_after=40)
        else:
            await interaction.response.send_message(
                f"Current Saves: {saves}", delete_after=40
            )


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
