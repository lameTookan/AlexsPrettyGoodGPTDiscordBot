# Alex's Pretty Good GPT Discord Bot

![image](https://github.com/lameTookan/AlexsPrettyGoodGPTDiscordBot/assets/129829145/b2e54ebb-5b48-4c43-99aa-5368db3f89a0)

Powered by Alex's Pretty Good Chat Module! (APGCM)

## Important Note about this project

For right now, I am bringing this project to a close. I had a lot of fun making it, and learned a lot, but for right now, I am going to go back to focusing on learning more, at least for the rest of this month(August 4, 2023 as of writing this.).

I have only been coding for a few months, and I have a looot to learn. I will likely come back to this project next month however.

However, if anyone has any interest in this project, be sure to let me know on github, or my discord account (@LameTookan), and I start working on it again. I still have quite a few ideas for this project, and I'll start updating it again when I have time.

Check out the [About This Project](Docs/about_this_project.md) for more info, as well as future plans and general thoughts and reflections on this project.

## Introduction

This simple Discord bot is designed to provide access to the GPT API and can be easily customized for various applications. However, keep in mind, it's primarily designed for small servers and might not perform optimally on larger servers. I'm looking forward to feedback and will consider optimizing it based on your responses.

## Features

The bot includes:

- **Multiple Modes**: Choose from casual, assistant, and default modes to set the bot's conversational style. Plus, a helpful 'help' mode to answer your questions about the bot.
- **Customizability**: Adjust the 'temperature' of the conversation, set the 'home channel' the bot responds to, and even tweak the system prompt and 'System Reminder' value. All this can be done in real-time via Discord app commands.
- **Accumulator Command**: If the 2K character limit on Discord with a GPT bot bothers you, use the accumulator command. Switch it on to group your messages. They're sent to the AI when you use the command again.
- **Save & Load**: Save the ongoing conversation and load it whenever you want. The bot auto-saves every 10 messages and loads the previous conversation on startup.
- **Export Feature**: Export the conversation as a markdown file and download it directly from the Discord app.
- **History Management**: Reset and/or print history whenever you need with a Discord app command.
- **Powerful Template System**: Powered by APGCM, adjust every aspect of the bot's behavior using the template system. Take full advantage of the model's max tokens with up to 200 max messages in the chat history.

## Setup

For a detailed guide on setting the bot up, made especially for beginners check out the [HELP_ME_PLEASE.md](/Docs/help/HELP_ME_PLEASE.md)

1. Clone the repo
2. Install the requirements with pip:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a discord bot and get the token. See Docs/help/setup_discord_bot.md for a detailed guide on setting up the Discord bot.
4. Fill out the .env.example file and rename it to .env
    - Enable the developer mode in Discord, right-click the channel, and get the channel ID.
    - Get the bot token from the Discord developer portal.
    - Invite the bot to your server.
    - Get an API key from <https://platform.openai.com/>

    Follow the instructions under STEP 1, STEP 2, and STEP 3 comments in the .env.example file.

5. Add your home channel id to the config.ini.example and rename it to config.ini
6. I recommend running the `quick_test.py` script to ensure everything is correctly setup before running the bot.

    ```bash
    python quick_test.py
    ```

7. Finally, run the bot:

    ```bash
    python main.py
    ```

For a detailed Python setup guide and how to create a Discord bot, check out the HELP_ME_PLEASE.md file in the docs folder.

## What is APGCM?

APGCM is a highly customizable and extendable module developed for creating chatbots. It's interface and file system agnostic, meaning it can be used in any project that requires a chatbot. Here's a quick example of creating a CLI chatbot with APGCM in just a few lines of code:

```python
import APGCM
factory = APGCM.ChatFactory()
chat = factory.get_chat()
stream_handler = APGCM.StdoutStreamHandler()
chat.add_stream_handler(stream_handler)

while True:
    ans = input("You: ")
    if ans == 'q':
        break
    chat.chat(ans)
    # Stream will be visible in the console
```

If there's interest in APGCM, I plan to release it as a standalone module.
