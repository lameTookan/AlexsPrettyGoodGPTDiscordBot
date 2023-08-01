
# HELP_ME.md - Beginners Guide to Setting Up This Project

Welcome! If you have never set up a Python project before, this guide will walk you through the process of setting up this project on your computer, in detail.

## Overview

1. Download and install Python and Pip
2. Clone the repository
3. _Optional_: Set up a virtual environment and activate it before installing requirements
4. Install the requirements
5. Configure the .env file
6. Run the `quick_test.py` script
7. Set up the Discord bot and obtain the token
8. Run the bot

## Step 1: Installing Python and Pip

Before we begin, it's important to ensure Python and Pip are both installed on your computer.

### Windows

1. Download Python from [https://www.python.org/downloads/](https://www.python.org/downloads/). Get the latest version.

2. Run the installer. During the installation process, make sure to check the box labeled "Add Python to PATH" before clicking "Install Now." This option ensures that Python and Pip (which is included with Python) are accessible from the command line in any directory.

**Note:** The latest versions of Python come with Pip pre-installed. If for some reason Pip is not installed, you can add it later by following these steps:

1. Download get-pip.py from [https://bootstrap.pypa.io/get-pip.py](https://bootstrap.pypa.io/get-pip.py).
2. Open a command prompt and navigate to the location where you downloaded get-pip.py.
3. Run the command `python get-pip.py`.

### Mac/Linux

Python usually comes preinstalled on most Mac/Linux systems. To check if it's installed, open a Terminal window and type `python --version`. If you see a version number in the response, Python is installed.

However, some older systems might not have Pip installed by default. Here's how to install it:

1. If Python 2.7 or later is not installed: Visit [https://www.python.org/downloads/](https://www.python.org/downloads/) and download the latest version. Follow the instructions on the Python website to install Python on your machine.

2. To check if Pip is installed, type `pip --version` or `pip3 --version` in Terminal. If you see a version number, Pip is installed.

3. If Pip is not installed, you can add it with the following command in Terminal: `sudo easy_install pip` for Python 2, or `sudo apt-get install python3-pip` for Python 3.

**Note:** You may need to enter your password for the sudo commands to run.

Double-check that Python is installed by running `python --version` in Terminal. If you get a version number, you're good to go.

## Step 2: Cloning the Repository

You have two options for downloading the project files:

1. Through GitHub

- On the project repository page, click the green "Code" button and select "Download ZIP." Extract the ZIP file to your desired location, and make a note of the path to the project folder.

2. Through Git

- Install git from [https://git-scm.com/downloads](https://git-scm.com/downloads).
- Open your terminal and navigate to the directory where you want to download the project files.
- Run `git clone https://github.com/lameTookan/Alexs-Pretty-Neat-GPT-CLI` to download the project files.
- Again, make a note of the path to the project folder.

Use `cd` to navigate to the project folder in your terminal.

## Step 3: Setting Up a Virtual Environment

A virtual environment (venv) keeps the dependencies required by different projects separate by creating isolated Python environments for them.
Install venv by running the following command in your terminal:

```bash
pip install virtualenv
```

### Windows/Mac/Linux

1. Open your terminal.
2. Navigate to your project directory (where you want your new project to be located).
3. Run `python -m venv env` to create a new virtual environment in a folder named `env`.

## Step 4: Activating the Virtual Environment

### Windows

Run `.\env\Scripts\activate`

### Mac/Linux

Run `source env/bin/activate`

You'll know it worked if `(env)` appears at the start of your terminal line.

## Step 5: Installing Requirements

Most Python projects will include a `requirements.txt` file which lists all of the package dependencies. Install these using pip.

Run `pip install -r requirements.txt`

## Step 6: Configuring the .env File

1. Open the `.env.example` file in a text editor.
2. In the following line replace `YOUR_API_KEY_HERE` with your OpenAI API key:

```bash
OPENAI_API_KEY= [YOUR_OPENAI_API_KEY_HERE] # This is mandatory
```

3. Choose a default model and template
   If you do not have access to GPT-4, uncomment the following lines:

```bash
## ___STEP 3:___
# FOR gpt-3-16K
#Choose this option if you do not have access to GPT-4
# uncomment this by removing the #
#DEFAULT_TEMPLATE_NAME = gpt-3-16K_default
#DEFAULT_MODEL_NAME = gpt-3-16K
```

If you do have access to GPT-4, uncomment the following lines:

```bash
# FOR gpt-4
#DEFAULT_TEMPLATE_NAME = gpt-4_default
#DEFAULT_MODEL_NAME = gpt-4
# See the template directory in the docs section for more information
```

**Note:** Do not uncomment both of these sections. Only uncomment the one you want to use. Also, these are only the default settings. You can change the model and template at any time in the program.

**Tip**: Uncommenting a line means removing the `#` at the start of the line.

4. Save the file as `.env` in the project directory.


## Step 7: Setting up the Discord Bot

1. Create a Discord bot and obtain its token. Follow the instructions in `Docs/help/setup_discord_bot.md` for a detailed guide on setting up the Discord bot and obtaining the token.

2. Once you have the token, open the `.env` file in a text editor and replace `[DISCORD BOT TOKEN HERE]` with the actual token in the `BOT_TOKEN` variable:

```bash
BOT_TOKEN = [DISCORD BOT TOKEN HERE] # This is mandatory if you want to use the Discord bot
```

3. Enable the developer mode in Discord, right-click the channel, and get the channel ID. Replace `[DISCORD HOME CHANNEL ID HERE]` with the actual channel ID in the `DISCORD_HOME_CHANNEL`

 variable:

```bash
DISCORD_HOME_CHANNEL = [DISCORD HOME CHANNEL ID HERE] # This is mandatory if you want to use the Discord bot (Can be changed with commands or in the config.ini file)
```
## Step 8: Running the Quick Test

Before running the bot, it's recommended to run the `quick_test.py` script to ensure everything is correctly set up.

In your terminal, run:

```bash
python quick_test.py
```

This will execute a quick test and help you identify any potential issues.


## Step 9: Running the Discord Bot

In your terminal, run:

```bash
python main.py
```

This will start the Discord bot, and you should see it online in your Discord server.

## Optional: Making Bash/Shell Scripts for Easy Start Up

### Windows

Create a new file with the `.bat` extension. Add the following lines to it:

```bat
@echo off
cd path_to_your_project
.\env\Scripts\activate
python main.py
```

Replace `path_to_your_project` with the full path to your project directory.

### Mac/Linux

Create a new file with the `.sh` extension. Add the following lines to it:

```bash
#!/bin/bash
cd path_to_your_project
source env/bin/activate
python main.py
```

Replace `path_to_your_project` with the full path to your project directory.

Make the script executable by running `chmod +x script_name.sh`.

---

Congratulations! You have successfully set up this project on your computer. If you have any questions, feel free to reach out to me on GitHub or open up an issue! Do not be afraid to ask questions; I am happy to help.
