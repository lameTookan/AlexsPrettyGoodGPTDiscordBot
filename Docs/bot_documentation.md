# Bot Documentation

## Overview

The DiscordBot class manages a Discord bot through discord.py. It interfaces with an AI through the ChatWrapper class.

Key capabilities:

- Respond to messages in the designated home channel
- Change conversation modes
- Load/save chat history
- Export chat logs
- Reset history
- Help mode
- Commands for managing the bot

## Commands

### Modes

- `/default_mode` - Sets mode to default prompts
- `/casual_mode` - Sets mode to casual prompts
- `/assistant_mode` - Sets mode to assistant prompts  
- `/which_mode` - Reports current conversation mode
- `/help_mode` - Toggles help mode on/off

### Saving

- `/get_saves` - Lists available saved chat logs
- `/save <name>` - Saves current chat log to specified name
- `/load <name>` - Loads the specified saved chat log
- `/delete_saves <names>` - Deletes specified saves

### Autosaving

- `/manual_autosave` - Manually triggers an autosave
- `/auto_saving_enabled <true/false>` - Turn autosaving on/off
- `/change_frequency <number>` - Change autosave frequency
- `/delete_all_auto_saves` - Delete all autosaves

### Other

- `/reset` - Reset current chat log history
- `/export` - Export chat log to a file
- `/debug` - Print debug information
- `/print_history` - Print full chat log history
- `/help` - List all bot commands

### Configuration

- `/home_channel <id>` - Set a new home channel
- `/chunk_len <number>` - Set message chunk length
- `/set_temp <value>` - Set temperature for model
- `/sys_prompt <prompt>` - Set system prompt
- `/reminder <reminder>` - Set reminder phrase
  
## Command Groups

The commands are organized into groups:

- `app_commands` - General commands
- `modes` - Mode changing commands
- `saving` - Save/load commands
- `autosaving` - Autosaving commands

## Events

The main events handled:

- `on_ready()` - When bot has connected
- `on_message()` - When a message is received

## Conversation Logic

1. Bot initializes ChatWrapper, configs etc.
2. `on_message` takes each message and passes it to ChatWrapper
3. ChatWrapper streams back a response
4. Bot sends response in chunks to Discord

This allows a natural conversation flow to the bot.

## Help Mode

Help mode sets special prompts and disables autosaving.
It can be toggled on/off with the `/help_mode` command.
