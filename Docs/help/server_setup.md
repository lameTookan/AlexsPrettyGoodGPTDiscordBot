# Server Setup 
# Server Setup Guide for Alex's Pretty Good GPT Discord Bot

This guide explains how to set up the bot on a Linux server. We'll also introduce `screen`, which allows you to run your bot in the background.

## Prerequisites

1. A Linux server - this can be a virtual private server (VPS) or any Linux machine to which you have SSH access.
2. Python 3.6 or higher installed on your server. You can verify this by running `python3 --version`.
3. Git installed on your server. Verify this with `git --version`.

## Steps

1. **Connect to your server**

    Use SSH to connect to your server. The command generally looks like this:

    ```bash
    ssh yourusername@yourserverip
    ```

2. **Clone the Repository**

    Once connected, clone the repository into a directory of your choice:

    ```bash
    git clone https://github.com/lameTookan/AlexsPrettyGoodGPTDiscordBot/
    ```

    Then navigate to the cloned directory:

    ```bash
    cd AlexsPrettyGoodGPTDIscordBot
    ```

3. **Follow the Bot Setup Guide**

    Follow the standard bot setup guide provided in the readme file. This involves installing requirements, setting up your .env and config.ini files, and verifying the setup with `quick_test.py`.

4. **Install `screen`**

    `screen` is a terminal multiplexer that allows you to run processes in the background. Install it with:

    ```bash
    sudo apt-get install screen
    ```

5. **Start a `screen` Session**

    Start a new `screen` session named "discordbot":

    ```bash
    screen -S discordbot
    ```

    This will create a new terminal window within your existing terminal.

6. **Run the Bot**

    In your `screen` session, start the bot with:

    ```bash
    python main.py
    ```

    The bot should now be running!

7. **Detach from `screen`**

    Press `Ctrl + A`, then `D` to detach from the `screen` session. The bot will continue to run in the background.

    To resume the session, use:

    ```bash
    screen -r discordbot
    ```

Congratulations, you've now set up your Discord bot to run on a server!

