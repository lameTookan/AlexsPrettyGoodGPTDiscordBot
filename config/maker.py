import os 

def make_config():
    content = """

[DISCORD BOT SETTINGS]
home_channel = 0
; Add CHANNEL ID here
; This is the channel ID of the channel that the bot will reply to messages and commands in 
auto_save_enabled = true
auto_save_interval = 10 
; How often the bot will save the database in minutes
chunk_length = 500 
; How many characters the bot will send in one message. If the message is longer than this, it will be split into multiple messages. Don't set higher than 1990 as that is the max length of a discord message

; Other important settings such as the bot token and openai key are in the .env file, these are just settings that are possible to change during runtime with commands

[DEFAULT]
; do not alter these settings, used to reload the config file(in case you don't like the changes you made)
; or to reset the config file to default values
auto_save_enabled = true
chunk_length = 500
auto_save_interval = 10
    """
    filename="config.ini"
    if os.path.isfile(filename):
        print("Config file already exists, skipping creation")
        return
    with open('config.ini', 'w') as f:
        f.write(content)
        print("Config file created")
    
    
